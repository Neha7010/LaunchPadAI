import streamlit as st
import textwrap
from typing import List, Dict, Any

def render_header(title: str, subtitle: str):
    """Renders a premium typewriter header wrapped inside a glass card."""
    st.markdown(
        f"""
        <div class="glass-card" style="text-align: center; padding: 20px 24px; margin-bottom: 25px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <div class="brand-title" style="margin-bottom: 0;">{title}</div>
            <div class="typewriter-container" style="margin: 10px auto 0 auto;">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_glass_card(title: str, category: str, project_score: float, difficulty: str, description: str, key_features: List[str], card_id: str, is_purple: bool = False) -> str:
    """Renders a project card with custom glassmorphism style."""
    features_html = "".join([f"<li>{feat}</li>" for feat in key_features[:3]])
    card_class = "glass-card glow-purple" if is_purple else "glass-card"
    
    difficulty_badge = "badge-blue"
    if difficulty == "Intermediate":
        difficulty_badge = "badge-purple"
    elif difficulty == "Advanced":
        difficulty_badge = "badge-red"
        
    html = f"""<div class="{card_class}">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
<span class="badge {difficulty_badge}">{difficulty}</span>
</div>
<h3 style="margin-top:5px; margin-bottom:5px; font-family:'Outfit', sans-serif;">{title}</h3>
<p class="card-category">{category}</p>
<p style="font-size:0.9rem; margin-bottom:15px; min-height:60px;">{description}</p>
<div class="score-container">
<div class="score-label">Match Score: <strong>{project_score}/10</strong></div>
<div class="score-bar-bg">
<div class="score-bar-fill" style="width: {project_score * 10}%;"></div>
</div>
</div>
<div style="font-size:0.85rem; margin-bottom:15px;">
<strong>Core Features:</strong>
<ul style="margin-top:5px; padding-left:20px;">
{features_html}
</ul>
</div>
</div>"""
    st.markdown(html.replace("\n", " "), unsafe_allow_html=True)

def render_comparison_table(projects: List[Dict[str, Any]]):
    """Renders a side-by-side comparison table of up to 3 projects."""
    if not projects:
        st.info("No projects selected for comparison.")
        return
        
    headers = [f"<th>{p['project_title']}</th>" for p in projects]
    
    # 1. Difficulty
    diff_row = [f"<td><span class='badge badge-purple'>{p['difficulty']}</span></td>" for p in projects]
    # 2. Complexity Score
    comp_row = [f"<td><strong>{p['complexity_score']}/10</strong></td>" for p in projects]
    # 3. Novelty Score
    nov_row = [f"<td><strong>{p['novelty_score']}/10</strong></td>" for p in projects]
    # 4. Estimated Cost
    cost_row = [f"<td>One-time: ${p['costs']['total_one_time']}<br>Monthly: ${p['costs']['total_monthly']}/mo</td>" for p in projects]
    # 5. Resume Value
    res_row = [f"<td>{len(p['validation']['demonstrated_categories'])} Categories Demonstrated</td>" for p in projects]
    # 6. Industry Relevance
    rel_row = [f"<td>{p['project_type']}</td>" for p in projects]
    
    table_html = f"""
    <table class="comparison-table">
        <thead>
            <tr>
                <th style="width:200px;">Metric</th>
                {"".join(headers)}
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Difficulty Tier</strong></td>
                {"".join(diff_row)}
            </tr>
            <tr>
                <td><strong>Complexity Score</strong></td>
                {"".join(comp_row)}
            </tr>
            <tr>
                <td><strong>Novelty Score</strong></td>
                {"".join(nov_row)}
            </tr>
            <tr>
                <td><strong>Estimated Cost</strong></td>
                {"".join(cost_row)}
            </tr>
            <tr>
                <td><strong>Resume Value</strong></td>
                {"".join(res_row)}
            </tr>
            <tr>
                <td><strong>Project Category</strong></td>
                {"".join(rel_row)}
            </tr>
        </tbody>
    </table>
    """
    st.markdown(textwrap.dedent(table_html), unsafe_allow_html=True)

def render_custom_loader(status_text: str):
    """Renders an animated premium loading card representing rocket launch status."""
    html = f"""
    <div class="glass-card loading-card">
        <div class="loader-rocket" style="font-size: 3rem; margin-bottom: 15px;">🚀</div>
        <h3 style="margin-top:5px; margin-bottom:10px; font-family:'Outfit', sans-serif; font-size:1.4rem;">Launchpad Engine Active</h3>
        <p style="font-size:0.92rem; color:#d6cca9; margin-bottom:15px; font-weight:500;">{status_text}</p>
        <div class="score-bar-bg" style="max-width: 240px; margin: 0 auto; height: 6px;">
            <div class="score-bar-fill" style="width: 100%;"></div>
        </div>
    </div>
    """
    st.markdown(textwrap.dedent(html), unsafe_allow_html=True)
