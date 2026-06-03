import streamlit as st
import json
import logging
from pathlib import Path
from config.settings import DATA_DIR, GEMINI_API_KEY
from services.db import get_user_projects
from agents.profile_agent import standardize_form_profile, extract_profile
from agents.retrieval_agent import run_retrieval
from agents.blueprint_agent import generate_project_recommendations
from tools.blueprint_compiler import compile_project_blueprint
from ui.components import render_header, render_glass_card, render_comparison_table, render_custom_loader

logger = logging.getLogger(__name__)

def load_sample_profiles():
    """Loads sample templates from JSON file."""
    path = DATA_DIR / "sample_profiles.json"
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading sample profiles: {e}")
    return []

def show_dashboard():
    """Renders the main student dashboard."""
    
    # Sidebar
    

    
    # Theme Toggle
    theme_label = "☀️ Light Theme" if st.session_state.theme == "dark" else "🌙 Dark Theme"
    if st.sidebar.button(theme_label, use_container_width=True):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()
        
    # Navigation
    st.sidebar.markdown("---")
    if st.sidebar.button("🏠 Recommendations Panel", use_container_width=True):
        st.session_state.sub_page = "recommend"
        st.rerun()
    if st.sidebar.button("📚 Saved Projects History", use_container_width=True):
        st.session_state.sub_page = "history"
        st.rerun()
        
    # Gemini Key Configuration (only shows if not set in config/settings.py)
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_ACTUAL_API_KEY_HERE":
        st.sidebar.markdown("---")
        st.sidebar.markdown("🔑 **Configure Gemini API Key**", unsafe_allow_html=True)
        user_api_key = st.sidebar.text_input(
            "Enter Gemini API Key", 
            value=st.session_state.get("gemini_key", ""),
            type="password",
            help="Required to connect to Gemini 2.5 Flash for reasoning and code generation."
        )
        if user_api_key != st.session_state.get("gemini_key", ""):
            st.session_state.gemini_key = user_api_key
            st.sidebar.success("Gemini API Key updated!")
    else:
        # Key is set in settings.py, bind it to session state automatically
        st.session_state.gemini_key = GEMINI_API_KEY
        
    # Log out
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout 🚪", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    # Main dashboard router based on sub_page state
    sub_page = st.session_state.get("sub_page", "recommend")
    
    if sub_page == "recommend":
        show_recommendation_panel()
    elif sub_page == "history":
        show_history_panel()

def show_recommendation_panel():
    """Renders the recommendation request panel."""
    render_header("Launchpad AI", "Research-Augmented Project Generation Engine")
    
    
    st.markdown("<h3 style='margin-top:0; font-family:Outfit, sans-serif;'>1. Build Student Profile</h3>", unsafe_allow_html=True)
    
    samples = load_sample_profiles()
    
    # Template Selection
    if samples:
        sample_names = ["Select Template (Optional)"] + [s["name"] for s in samples]
        selected_sample_name = st.selectbox("Quick-fill Profile Template", sample_names)
        
        # Populate values if selected
        if selected_sample_name != "Select Template (Optional)":
            sample_data = next(s for s in samples if s["name"] == selected_sample_name)
            st.session_state.form_name = sample_data["name"]
            st.session_state.form_major = sample_data["major"]
            st.session_state.form_skills = ", ".join(sample_data["skills"])
            st.session_state.form_interests = ", ".join(sample_data["interests"])
            st.session_state.form_goal = sample_data["career_goal"]
            
    # Form details
    form_name = st.text_input("Student Name", value=st.session_state.get("form_name", ""))
    form_major = st.text_input("Academic Major / Field", value=st.session_state.get("form_major", ""))
    form_skills = st.text_input("Technical Skills (comma-separated)", value=st.session_state.get("form_skills", ""))
    form_interests = st.text_input("Areas of Interest / Domains (comma-separated)", value=st.session_state.get("form_interests", ""))
    form_goal = st.text_input("Target Career Goal", value=st.session_state.get("form_goal", ""))
    
    st.markdown("---")
    st.markdown("💡 **Alternative: Paste Raw CV / Profile Text**", unsafe_allow_html=True)
    raw_cv_text = st.text_area("Paste resume details, university course modules, or biography here (AI will extract profile parameters):")
    
    # Search settings
    st.markdown("---")
    enable_rag = st.checkbox("Enable Research-Augmented Generation (DuckDuckGo Search)", value=True, help="Queries DuckDuckGo search to extract current industry project trends before blueprints are recommended.")
    
    generate_btn = st.button("Generate Tailored Project Recommendations 🚀", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if generate_btn:
        api_key = st.session_state.get("gemini_key", GEMINI_API_KEY)
        if not api_key:
            st.error("❌ Gemini API Key is missing. Please paste it in the sidebar to run the generation.")
            return
            
        # Create an empty placeholder container for custom loading animations
        loader_placeholder = st.empty()
        
        try:
            # 1. Processing Profile
            with loader_placeholder.container():
                render_custom_loader("Analyzing student profile details...")
                
            # Determine profile input type
            if raw_cv_text.strip():
                profile_obj = extract_profile(raw_cv_text, api_key)
            else:
                if not form_name or not form_skills or not form_goal:
                    st.error("Please fill in Name, Skills, and Career Goal (or paste a resume).")
                    loader_placeholder.empty()
                    return
                
                skills_list = [s.strip() for s in form_skills.split(",") if s.strip()]
                interests_list = [i.strip() for i in form_interests.split(",") if i.strip()]
                
                form_dict = {
                    "name": form_name,
                    "major": form_major,
                    "skills": skills_list,
                    "interests": interests_list,
                    "career_goal": form_goal
                }
                profile_obj = standardize_form_profile(form_dict, api_key)
            
            # Save extracted profile to state
            profile_dict = profile_obj.model_dump()
            st.session_state.extracted_profile = profile_dict
            
            # 2. Retrieving Context
            with loader_placeholder.container():
                render_custom_loader("Retrieving project domain research context (DuckDuckGo & Local)...")
                
            if enable_rag:
                retrieved_snippets = run_retrieval(st.session_state.extracted_profile)
            else:
                retrieved_snippets = []
            st.session_state.retrieved_snippets = retrieved_snippets
            
            # 3. Generating Recommendations
            with loader_placeholder.container():
                render_custom_loader("Generating tailored blueprints using Gemini 2.5 Flash...")
                
            raw_recommendations = generate_project_recommendations(
                st.session_state.extracted_profile,
                st.session_state.retrieved_snippets,
                api_key
            )
            
            # Run deterministic validation compiler for each recommendation
            compiled_recommendations = []
            for raw_rec in raw_recommendations:
                # Convert Pydantic object to dict
                raw_dict = raw_rec.model_dump()
                compiled_dict = compile_project_blueprint(raw_dict)
                compiled_recommendations.append(compiled_dict)
                
            st.session_state.recommendations = compiled_recommendations
            
            # Clear loader placeholder completely
            loader_placeholder.empty()
            st.success("Recommendations successfully compiled!")
            
        except Exception as e:
            loader_placeholder.empty()
            st.error(f"Failed to generate recommendations: {e}")
            return
                
    # Display Recommendations if present in Session State
    if st.session_state.get("recommendations"):
        display_recommendations()

def display_recommendations():
    """Displays generated project suggestions and comparison view."""
    recs = st.session_state.recommendations
    
    st.markdown("### Suggested Project Matches")
    
    # 3-Column Display of recommendations
    cols = st.columns(3, vertical_alignment="top")
    for idx, rec in enumerate(recs):
        with cols[idx]:
            render_glass_card(
                title=rec["project_title"],
                category=rec["project_type"],
                project_score=rec["project_score"],
                difficulty=rec["difficulty"],
                description=rec["problem_statement"],
                key_features=rec["key_features"],
                card_id=f"rec_{idx}",
                is_purple=(idx == 1)
            )
            
            # Action buttons
            # We use distinct keys to prevent streamlit rendering conflicts
            if st.button("Generate Full Report ⚡", key=f"btn_rep_{idx}", use_container_width=True):
                st.session_state.selected_project = rec
                st.session_state.page = "report"
                st.rerun()
                
    # Comparison View selector
    st.markdown("---")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; font-family:Outfit, sans-serif;'>📊 Compare Recommendations</h3>", unsafe_allow_html=True)
    
    options = [rec["project_title"] for rec in recs]
    selected_compares = st.multiselect(
        "Select up to 3 projects to compare side-by-side:",
        options,
        default=options[:3] if len(options) >= 3 else options
    )
    
    if selected_compares:
        selected_objs = [rec for rec in recs if rec["project_title"] in selected_compares]
        render_comparison_table(selected_objs)
    st.markdown('</div>', unsafe_allow_html=True)

def show_history_panel():
    """Renders the user's SQLite saved projects history."""
    render_header("Saved Blueprints History", "View previously generated and validated reports.")
    
    user_id = st.session_state.user["id"]
    projects = get_user_projects(user_id)
    
    if not projects:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.info("You have not generated any blueprints yet. Head to the Recommendations Panel to begin!")
        st.markdown('</div>', unsafe_allow_html=True)
        return
        
    for p in projects:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col_info, col_action = st.columns([4, 1])
        
        with col_info:
            difficulty_badge = "badge-blue"
            if p["complexity"] == "Intermediate":
                difficulty_badge = "badge-purple"
            elif p["complexity"] == "Advanced":
                difficulty_badge = "badge-red"
                
            st.markdown(
                f"""
                <span class='badge {difficulty_badge}'>{p['complexity']}</span>
                <span class='badge badge-green'>Score: {p['score']}/10</span>
                <span class='badge badge-blue'>{p['project_type']}</span>
                <h3 style='margin-top:10px; margin-bottom:5px; font-family:Outfit, sans-serif;'>{p['project_title']}</h3>
                <small style='color:gray;'>Generated on: {p['created_at']}</small>
                """,
                unsafe_allow_html=True
            )
            
        with col_action:
            st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
            if st.button("Open Full Report", key=f"hist_open_{p['id']}", use_container_width=True):
                # Put user profile and stored report dictionary into session state
                st.session_state.selected_project = p["report"]
                st.session_state.page = "report"
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)
