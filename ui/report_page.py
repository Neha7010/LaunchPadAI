import streamlit as st
from fpdf import FPDF
from services.db import save_project
from agents.report_agent import generate_long_form_report
from config.settings import GEMINI_API_KEY
from ui.components import render_header

def clean_pdf_text(text: str) -> str:
    """Cleans Unicode characters to avoid FPDF latin-1 encoding errors."""
    replacements = {
        "\u201c": '"', "\u201d": '"', "\u2018": "'", "\u2019": "'",
        "\u2013": "-", "\u2014": "-", "\u2022": "*", "\u2713": "[Yes]",
        "\u2717": "[No]", "\u2192": "->", "\u25bc": "v", "\u25b2": "^"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode('latin-1', 'replace').decode('latin-1')

def generate_pdf_bytes(title: str, text: str) -> bytes:
    """Generates PDF binary data from a text string."""
    pdf = FPDF()
    pdf.add_page()
    
    # Title Page/Header
    pdf.set_font("helvetica", style="B", size=16)
    pdf.multi_cell(0, 10, clean_pdf_text(title))
    pdf.ln(8)
    
    # Body Text
    pdf.set_font("helvetica", size=10)
    pdf.multi_cell(0, 6, clean_pdf_text(text))
    
    # Return as bytes
    return bytes(pdf.output())

def show_report_page():
    """Renders the detailed project report page."""
    
    if not st.session_state.get("selected_project"):
        st.error("No project selected.")
        if st.button("↩ Back to Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
        return
        
    rec = st.session_state.selected_project
    title = rec["project_title"]
    
    # Back button and page layout
    col_back, col_save = st.columns([4, 1])
    with col_back:
        if st.button("↩ Back to Dashboard"):
            # Clear selected project details and redirect
            st.session_state.selected_project = None
            st.session_state.report_text = None
            st.session_state.page = "dashboard"
            st.rerun()
            
    with col_save:
        # Save blueprint report button
        if st.button("💾 Save to History", use_container_width=True):
            user_id = st.session_state.user["id"]
            success = save_project(
                user_id=user_id,
                project_title=title,
                project_type=rec["project_type"],
                score=rec["project_score"],
                complexity=rec["difficulty"],
                report_data=rec
            )
            if success:
                st.success("Blueprint saved!")
            else:
                st.error("Failed to save blueprint.")

    render_header(title, f"{rec['project_type']} — {rec['difficulty']} Level")

    # 1. Dashboard Metrics Summary
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; font-family:Outfit, sans-serif;'>📊 Symbolic Parameters & Scores</h3>", unsafe_allow_html=True)
    
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.metric("Launchpad Score", f"{rec['project_score']}/10")
    with m_col2:
        st.metric("Novelty Rating", f"{rec['novelty_score']}/10")
    with m_col3:
        st.metric("Difficulty Level", rec["difficulty"])
    with m_col4:
        st.metric("Estimated Cost", f"${rec['costs']['initial_budget']}")
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. "Why Recommended" Explanation Panel (Mandatory Section)
    st.markdown('<div class="glass-card glow-purple">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; font-family:Outfit, sans-serif;'>🔍 Why Launchpad AI Recommended This</h3>", unsafe_allow_html=True)
    for bullet in rec.get("why_recommended", []):
        st.markdown(f"<div class='recommended-bullet'>✓ {bullet}</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. Project Blueprint Details
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; font-family:Outfit, sans-serif;'>💡 Project Blueprint Definition</h3>", unsafe_allow_html=True)
    
    st.markdown(f"**Problem Statement:**\n{rec['problem_statement']}")
    st.markdown("**Core Features:**")
    for feat in rec["key_features"]:
        st.markdown(f"- {feat}")
        
    st.markdown("**Suggested Technologies:**")
    st.write(", ".join(rec["suggested_technologies"]))
    
    if rec.get("estimated_hardware"):
        st.markdown("**Estimated Hardware Components:**")
        st.write(", ".join(rec["estimated_hardware"]))
        
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. Systems Architecture Layout
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; font-family:Outfit, sans-serif;'>⚙️ System Architecture Flow</h3>", unsafe_allow_html=True)
    st.write(rec["architecture_description"])
    st.markdown("**ASCII Topology:**")
    st.code(rec["text_architecture_diagram"], language="text")
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. Local Symbolic Validation Warnings & Resume Analysis
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; font-family:Outfit, sans-serif;'>🛡️ Technology Stack Validation</h3>", unsafe_allow_html=True)
    
    val = rec["validation"]
    if val["warnings"]:
        st.warning("⚠️ **Architecture Validation Warnings:**")
        for warn in val["warnings"]:
            st.markdown(f"- {warn}")
    else:
        st.success("✓ Technology compatibility validation passed! No warnings detected.")
        
    # Resume Skills Checklist
    st.markdown("---")
    st.markdown("💼 **Resume Skill Alignment Analysis**")
    
    col_d, col_m = st.columns(2)
    with col_d:
        st.markdown("🟢 **Skills Demonstrated:**")
        if val["demonstrated_categories"]:
            for cat, techs in val["demonstrated_categories"].items():
                st.markdown(f"- **{cat}**: {', '.join(techs)}")
        else:
            st.write("None detected based on stack.")
            
    with col_m:
        st.markdown("🔴 **Missing CV Domains:**")
        if val["missing_categories"]:
            for cat in val["missing_categories"]:
                st.markdown(f"- ✗ {cat}")
        else:
            st.write("✓ None! Great, well-rounded tech stack.")
    st.markdown('</div>', unsafe_allow_html=True)

    # 6. Detailed Project Cost Estimation Breakdown
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; font-family:Outfit, sans-serif;'>💰 Project Budget Cost Estimations</h3>", unsafe_allow_html=True)
    
    costs = rec["costs"]
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        st.markdown("**Recurring Monthly Costs:**")
        st.markdown(f"- **Hosting**: ${costs['monthly_hosting']} ({costs['hosting_description']})")
        st.markdown(f"- **Database**: ${costs['monthly_database']} ({costs['database_description']})")
        st.markdown(f"- **APIs**: ${costs['monthly_api']} ({costs['api_description']})")
        st.markdown(f"**Total Monthly recurring:** ${costs['total_monthly']}/mo")
        
    with c_col2:
        st.markdown("**One-Time Hardware Costs:**")
        st.markdown(f"- **Total Hardware budget**: ${costs['one_time_hardware']}")
        if costs["hardware_items"]:
            for item in costs["hardware_items"]:
                st.markdown(f"  - {item}")
        else:
            st.caption("No hardware component required.")
            
    st.markdown(f"📈 **Initial Launch Budget (Total Setup + Month 1)**: **${costs['initial_budget']}**")
    st.markdown('</div>', unsafe_allow_html=True)

    # 7. 4-Week Timeline Roadmap
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; font-family:Outfit, sans-serif;'>📅 4-Week Roadmap Timeline</h3>", unsafe_allow_html=True)
    for phase in rec["implementation_phases"]:
        with st.expander(f"⚙️ {phase['phase_name']} ({phase['duration']})"):
            for task in phase["tasks"]:
                st.markdown(f"- [ ] {task}")
    st.markdown('</div>', unsafe_allow_html=True)

    # 8. Download Starter Repository (GitHub starter pack zip bytes)
    st.markdown('<div class="glass-card glow-purple">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; font-family:Outfit, sans-serif;'>📦 Download GitHub Starter Repository</h3>", unsafe_allow_html=True)
    st.write("Extracting this starter kit yields your standard folder layout, a sample `README.md`, dynamic `requirements.txt` listing packages, and a checklist `milestones.md` containing weekly milestones.")
    
    st.download_button(
        label="Download Starter Repository Package (.ZIP) 📥",
        data=rec["zip_bytes"],
        file_name=f"{title.replace(' ', '_').lower()}_starter_kit.zip",
        mime="application/zip",
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # 9. Detailed Long-form Academic Report Generation (Gemini reasoning engine)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; font-family:Outfit, sans-serif;'>📝 Detailed Academic Report Generation</h3>", unsafe_allow_html=True)
    
    api_key = st.session_state.get("gemini_key", GEMINI_API_KEY)
    
    if st.button("Generate Detailed Academic Report", use_container_width=True):
        if not api_key:
            st.error("Please configure your Gemini API Key in the dashboard sidebar to use this feature.")
        else:
            with st.spinner("Expanding blueprint into standard Academic Report formats (this might take up to 20 seconds)..."):
                try:
                    report_markdown = generate_long_form_report(
                        st.session_state.extracted_profile,
                        rec,
                        api_key
                    )
                    st.session_state.report_text = report_markdown
                except Exception as e:
                    st.error(f"Failed to generate report text: {e}")
                    
    # Render generated report and export options if generated
    if st.session_state.get("report_text"):
        report_text = st.session_state.report_text
        
        st.markdown("---")
        st.markdown("#### Generated Report Preview")
        st.markdown(report_text)
        
        # Export Buttons
        st.markdown("---")
        st.markdown("#### Export Report Formats")
        
        ex_col1, ex_col2, ex_col3 = st.columns(3)
        
        with ex_col1:
            st.download_button(
                label="Export as Markdown (.md)",
                data=report_text,
                file_name=f"{title.replace(' ', '_').lower()}_report.md",
                mime="text/markdown",
                use_container_width=True
            )
            
        with ex_col2:
            st.download_button(
                label="Export as TXT (.txt)",
                data=report_text,
                file_name=f"{title.replace(' ', '_').lower()}_report.txt",
                mime="text/plain",
                use_container_width=True
            )
            
        with ex_col3:
            # Generate PDF in memory on download press
            with st.spinner("Compiling PDF bytes..."):
                try:
                    pdf_bytes = generate_pdf_bytes(title, report_text)
                    st.download_button(
                        label="Export as PDF (.pdf)",
                        data=pdf_bytes,
                        file_name=f"{title.replace(' ', '_').lower()}_report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Error compiling PDF: {e}")
                    
    st.markdown('</div>', unsafe_allow_html=True)
