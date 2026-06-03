def get_css(theme: str = "dark") -> str:
    """Returns CSS strings for glassmorphism styling in Streamlit."""
    
    if theme == "dark":
        bg_gradient = "linear-gradient(135deg, #120004 0%, #2f010b 100%)"
        text_color = "#F5F5DA"
        glass_bg = "rgba(47, 1, 11, 0.65)"
        glass_border = "rgba(245, 245, 218, 0.15)"
        glass_shadow = "0 8px 32px 0 rgba(0, 0, 0, 0.5)"
        glow_color = "#7B021D"
        glow_secondary = "#E4D0A3"
        input_bg = "rgba(35, 1, 7, 0.6)"
        input_border = "rgba(245, 245, 218, 0.2)"
        input_text = "#F5F5DA"
        card_text_secondary = "#d6cca9"
        bar_bg = "rgba(255, 255, 255, 0.08)"
        glow_shadow_color = "rgba(123, 2, 29, 0.3)"
        glow_secondary_shadow = "rgba(228, 208, 163, 0.25)"
        sidebar_bg = "linear-gradient(180deg, #1E0915 0%, #100003 100%)"
        sidebar_border = "rgba(245, 245, 218, 0.06)"
    else: # light theme
        bg_gradient = "linear-gradient(135deg, #fdfdf5 0%, #F5F5DA 100%)"
        text_color = "#300008"
        glass_bg = "rgba(255, 255, 255, 0.75)"
        glass_border = "rgba(123, 2, 29, 0.2)"
        glass_shadow = "0 8px 32px 0 rgba(123, 2, 29, 0.05)"
        glow_color = "#7B021D"
        glow_secondary = "#9e0325"
        input_bg = "rgba(255, 255, 255, 0.95)"
        input_border = "rgba(123, 2, 29, 0.25)"
        input_text = "#300008"
        card_text_secondary = "#6b565a"
        bar_bg = "rgba(0, 0, 0, 0.05)"
        glow_shadow_color = "rgba(123, 2, 29, 0.2)"
        glow_secondary_shadow = "rgba(158, 3, 37, 0.18)"
        sidebar_bg = "linear-gradient(180deg, #fdfdf5 0%, #F5F5DA 100%)"
        sidebar_border = "rgba(123, 2, 29, 0.08)"

    css = f"""
    <style>
    /* Global Styles */
    .stApp {{
        background: {bg_gradient} !important;
        color: {text_color} !important;
        font-family: 'Inter', 'Outfit', sans-serif !important;
    }}
    
    /* Sidebar Styling Overrides */
    section[data-testid="stSidebar"] {{
        background: {sidebar_bg} !important;
        border-right: 1px solid {sidebar_border} !important;
    }}
    
    /* Global Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;600;700&family=Fira+Code:wght@400;500&display=swap');
    
    /* Glassmorphism Containers */
    .glass-card {{
        background: {glass_bg};
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid {glass_border};
        border-radius: 16px;
        padding: 24px;
        margin: 0px 0px 20px 0px !important;
        box-shadow: {glass_shadow};
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.65s cubic-bezier(0.165, 0.84, 0.44, 1) both;
    }}
    
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    /* Hover Shimmer Light sweep effect */
    .glass-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -150%;
        width: 50%;
        height: 100%;
        background: linear-gradient(
            to right,
            rgba(255, 255, 255, 0) 0%,
            rgba(255, 255, 255, 0.06) 50%,
            rgba(255, 255, 255, 0) 100%
        );
        transform: skewX(-25deg);
        transition: 0.75s cubic-bezier(0.165, 0.84, 0.44, 1);
        z-index: 1;
        pointer-events: none;
    }}
    
    .glass-card:hover::before {{
        left: 150%;
    }}
    
    /* Premium Hover Scale and Glow Animations */
    .glass-card:hover {{
        border-color: {glow_color} !important;
        box-shadow: 0 12px 40px {glow_shadow_color}, 0 0 20px {glow_color}33;
        transform: translateY(-5px) scale(1.015);
    }}
    
    .glow-purple:hover {{
        border-color: {glow_secondary} !important;
        box-shadow: 0 12px 40px {glow_secondary_shadow}, 0 0 20px {glow_secondary}33;
        transform: translateY(-5px) scale(1.015);
    }}
    
    /* Slide effect on list items inside cards */
    .glass-card li {{
        transition: transform 0.25s ease, color 0.25s ease;
    }}
    
    .glass-card li:hover {{
        transform: translateX(4px);
        color: {text_color} !important;
    }}
    
    /* Custom Headers */
    .brand-title {{
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 3rem;
        background: linear-gradient(to right, {glow_color}, {glow_secondary});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        text-align: center;
        transition: transform 0.3s ease;
    }}
    
    .brand-title:hover {{
        transform: scale(1.02);
    }}
    
    /* Typewriter effect for header */
    .typewriter-container {{
        overflow: hidden; 
        border-right: .15em solid {glow_color}; 
        white-space: nowrap; 
        margin: 0 auto; 
        letter-spacing: .05em; 
        animation: 
          typing 3.5s steps(40, end),
          blink-caret .75s step-end infinite;
        font-family: 'Fira Code', monospace;
        font-size: 1.1rem;
        color: {glow_color};
        margin-bottom: 25px;
        width: fit-content;
    }}
    
    @keyframes typing {{
      from {{ width: 0 }}
      to {{ width: 100% }}
    }}
    
    @keyframes blink-caret {{
      from, to {{ border-color: transparent }}
      50% {{ border-color: {glow_color}; }}
    }}
    
    /* Custom Badges */
    .badge {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-right: 6px;
        margin-bottom: 6px;
        transition: transform 0.2s ease;
    }}
    
    .badge:hover {{
        transform: scale(1.05);
    }}
    
    .badge-blue {{
        background: rgba(228, 208, 163, 0.15);
        color: #E4D0A3;
        border: 1px solid rgba(228, 208, 163, 0.3);
    }}
    
    .badge-purple {{
        background: rgba(123, 2, 29, 0.15);
        color: #ffa4b2;
        border: 1px solid rgba(123, 2, 29, 0.3);
    }}
    
    .badge-green {{
        background: rgba(74, 222, 128, 0.15);
        color: #4ade80;
        border: 1px solid rgba(74, 222, 128, 0.3);
    }}
    
    .badge-red {{
        background: rgba(123, 2, 29, 0.3);
        color: #ffcbd1;
        border: 1px solid rgba(123, 2, 29, 0.5);
    }}
    
    /* Forms, Inputs, Text Areas */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
        background-color: {input_bg} !important;
        border: 1px solid {input_border} !important;
        color: {input_text} !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {{
        border-color: {glow_color} !important;
        box-shadow: 0 0 10px {glow_color}44 !important;
    }}
    
    /* Buttons Customization with Gradient Animations */
    .stButton>button {{
        background: linear-gradient(135deg, {glow_color} 0%, {glow_secondary} 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 8px 24px !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 14px rgba(123, 2, 29, 0.4) !important;
        background-size: 200% auto !important;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }}
    
    .stButton>button:hover {{
        background-position: right center !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(123, 2, 29, 0.6) !important;
    }}
    
    /* Secondary Action Buttons */
    .secondary-btn>button, div[data-testid="stFormSubmitButton"]>button {{
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid {glass_border} !important;
        color: {text_color} !important;
        box-shadow: none !important;
    }}
    
    .secondary-btn>button:hover {{
        border-color: {glow_color} !important;
        background: rgba(123, 2, 29, 0.1) !important;
    }}
    
    /* Comparison Table Styling */
    .comparison-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 0.95rem;
        border-radius: 8px;
        overflow: hidden;
    }}
    
    .comparison-table th {{
        background-color: rgba(123, 2, 29, 0.25);
        color: {text_color};
        padding: 14px 16px;
        text-align: left;
        border-bottom: 2px solid {glass_border};
        font-weight: 600;
    }}
    
    .comparison-table td {{
        padding: 14px 16px;
        border-bottom: 1px solid {glass_border};
        color: {text_color};
        transition: background-color 0.2s ease;
    }}
    
    .comparison-table tr:hover td {{
        background-color: rgba(245, 245, 218, 0.04);
    }}
    
    /* Custom list elements */
    .icon-list {{
        list-style-type: none;
        padding-left: 0;
    }}
    
    .icon-list li {{
        position: relative;
        padding-left: 25px;
        margin-bottom: 8px;
    }}
    
    .icon-list li::before {{
        content: "✓";
        position: absolute;
        left: 0;
        top: 0;
        color: #4ade80;
        font-weight: bold;
        transition: transform 0.2s ease;
    }}
    
    .icon-list li:hover::before {{
        transform: scale(1.3);
    }}
    
    .icon-list-missing li::before {{
        content: "✗";
        color: #f87171;
    }}
    
    /* Category Text style inside cards */
    .card-category {{
        font-size: 0.85rem;
        color: {card_text_secondary};
        margin-bottom: 10px;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }}
    
    /* RAG Insight Snippets Styling */
    .insight-snippet {{
        font-size: 0.88rem;
        margin-bottom: 8px;
        color: {card_text_secondary};
        border-left: 3px solid {glow_color};
        padding-left: 10px;
        transition: padding-left 0.3s ease;
    }}
    
    .insight-snippet:hover {{
        padding-left: 15px;
        color: {text_color};
    }}
    
    /* Why Recommended Bullet Styling */
    .recommended-bullet {{
        font-size: 0.95rem;
        margin-bottom: 8px;
        color: {text_color};
        font-weight: 600;
        background: rgba(123, 2, 29, 0.08);
        padding: 8px 12px;
        border-radius: 8px;
        border-left: 4px solid {glow_color};
        transition: all 0.3s ease;
    }}
    
    .recommended-bullet:hover {{
        transform: translateX(4px);
        background: rgba(123, 2, 29, 0.15);
    }}

    /* Progress Bar for Score Dials */
    .score-container {{
        margin: 18px 0;
    }}
    .score-label {{
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
        color: {text_color};
    }}
    .score-bar-bg {{
        background: {bar_bg};
        border: 1px solid {glass_border};
        border-radius: 999px;
        height: 8px;
        width: 100%;
        overflow: hidden;
    }}
    .score-bar-fill {{
        background: linear-gradient(90deg, {glow_color} 0%, {glow_secondary} 100%);
        height: 100%;
        border-radius: 999px;
        box-shadow: 0 0 8px {glow_color}66;
        transition: width 1.2s cubic-bezier(0.19, 1, 0.22, 1);
        animation: pulseGlow 3s ease-in-out infinite;
    }}
    
    @keyframes pulseGlow {{
        0%, 100% {{ box-shadow: 0 0 8px {glow_color}66; }}
        50% {{ box-shadow: 0 0 15px {glow_color}bb, 0 0 5px {glow_color}; }}
    }}

    /* Split-Pane Login Screen Layout using :has selector */
    div[data-testid="stHorizontalBlock"]:has(.illustration-wrapper) {{
        max-width: 950px;
        margin: 4% auto;
        border-radius: 24px;
        overflow: hidden;
        border: 1px solid rgba(245, 245, 218, 0.1) !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.55);
        background: linear-gradient(to right, #2D101D 0%, #2D101D 53.5%, #5F212C 53.5%, #5F212C 100%) !important;
        gap: 0px !important;
    }}
    
    /* Left column */
    div[data-testid="stHorizontalBlock"]:has(.illustration-wrapper) > div[data-testid="column"]:first-child {{
        background: linear-gradient(135deg, #1E0915 0%, #2D101D 50%, #3A1224 100%) !important;
        padding: 40px !important;
        border-right: 1px solid rgba(245, 245, 218, 0.08) !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        flex: 1.15 1 0% !important;
        width: 53.5% !important;
        min-width: 53.5% !important;
    }}
    
    /* Right column */
    div[data-testid="stHorizontalBlock"]:has(.illustration-wrapper) > div[data-testid="column"]:last-child {{
        background: linear-gradient(135deg, #712531 0%, #5F212C 50%, #4E1C27 100%) !important;
        padding: 40px !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        flex: 1 1 0% !important;
        width: 46.5% !important;
        min-width: 46.5% !important;
    }}

    @media (max-width: 768px) {{
        div[data-testid="stHorizontalBlock"]:has(.illustration-wrapper) {{
            flex-direction: column !important;
            background: linear-gradient(to bottom, #2D101D 0%, #2D101D 450px, #5F212C 450px, #5F212C 100%) !important;
        }}
        div[data-testid="stHorizontalBlock"]:has(.illustration-wrapper) > div[data-testid="column"]:first-child {{
            border-right: none !important;
            border-bottom: 1px solid rgba(245, 245, 218, 0.06) !important;
            padding: 30px !important;
            width: 100% !important;
            min-width: 100% !important;
        }}
        div[data-testid="stHorizontalBlock"]:has(.illustration-wrapper) > div[data-testid="column"]:last-child {{
            padding: 30px !important;
            width: 100% !important;
            min-width: 100% !important;
        }}
    }}

    /* Browser Mockup & Orbit Illustration */
    .illustration-wrapper {{
        width: 280px;
        height: 250px;
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }}
    
    .orbit-ring {{
        position: absolute;
        border: 1px dashed rgba(245, 245, 218, 0.07);
        border-radius: 50%;
        animation: spin 35s linear infinite;
    }}
    
    .orbit-outer {{
        width: 250px;
        height: 250px;
    }}
    
    .orbit-inner {{
        width: 190px;
        height: 190px;
        animation-direction: reverse;
        animation-duration: 25s;
    }}
    
    @keyframes spin {{
        100% {{ transform: rotate(360deg); }}
    }}
    
    .floating-badge {{
        position: absolute;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #1f0107;
        border: 1px solid rgba(245, 245, 218, 0.12);
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 0.85rem;
        box-shadow: 0 0 10px rgba(123, 2, 29, 0.4);
        color: #F5F5DA;
        animation: float-badge 6s ease-in-out infinite;
        font-weight: bold;
    }}
    
    @keyframes float-badge {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-5px); }}
    }}
    
    .badge-pos1 {{ top: 15px; left: 35px; animation-delay: 0s; }}
    .badge-pos2 {{ top: 105px; right: 10px; animation-delay: 1.5s; }}
    .badge-pos3 {{ bottom: 15px; left: 95px; animation-delay: 3s; }}
    .badge-pos4 {{ top: 175px; left: 10px; animation-delay: 4.5s; }}

    .browser-card {{
        width: 160px;
        height: 125px;
        background: rgba(30, 2, 7, 0.75);
        border: 1px solid rgba(245, 245, 218, 0.1);
        border-radius: 12px;
        position: relative;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        overflow: hidden;
        display: flex;
        flex-direction: column;
        padding: 10px;
        z-index: 2;
    }}
    
    .browser-header-dots {{
        display: flex;
        gap: 4px;
        margin-bottom: 10px;
    }}
    
    .browser-dot {{
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: rgba(245, 245, 218, 0.25);
    }}
    
    .browser-body-content {{
        display: flex;
        flex-direction: column;
        gap: 6px;
    }}
    
    .browser-line {{
        height: 4px;
        background: rgba(245, 245, 218, 0.08);
        border-radius: 3px;
    }}
    
    .line-short {{ width: 50%; }}
    .line-medium {{ width: 75%; }}
    .line-long {{ width: 90%; }}
    
    .browser-stars {{
        color: #7B021D;
        font-size: 0.65rem;
        margin-bottom: 2px;
        letter-spacing: 1px;
    }}
    
    .browser-icon-box {{
        width: 24px;
        height: 16px;
        background: rgba(123, 2, 29, 0.2);
        border: 1px solid rgba(123, 2, 29, 0.4);
        border-radius: 4px;
        color: #ffa4b2;
        font-size: 0.55rem;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
        margin-bottom: 4px;
    }}
    
    .magnifying-glass-svg {{
        position: absolute;
        width: 70px;
        height: 70px;
        right: 35px;
        bottom: 45px;
        z-index: 3;
        filter: drop-shadow(0 4px 12px rgba(123, 2, 29, 0.5));
        animation: pulse-magnifier 4s ease-in-out infinite;
    }}
    
    @keyframes pulse-magnifier {{
        0%, 100% {{ transform: scale(1) translate(0, 0); }}
        50% {{ transform: scale(1.06) translate(2px, -2px); }}
    }}

    /* Tabs Styling Overrides to Match Mockup */
    div[data-testid="stTabBar"] {{
        background: transparent !important;
        border-bottom: 1px solid rgba(245, 245, 218, 0.08) !important;
        margin-bottom: 25px !important;
        display: flex !important;
        justify-content: flex-start !important;
        gap: 15px !important;
    }}
    
    button[data-baseweb="tab"] {{
        background: transparent !important;
        color: {card_text_secondary} !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        border: none !important;
        padding: 8px 16px !important;
        transition: all 0.3s ease !important;
        border-radius: 0px !important;
    }}
    
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {text_color} !important;
        border-bottom: 2px solid {glow_color} !important;
    }}

    /* Form Overrides */
    form[data-testid="stForm"] {{
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }}

    div[data-testid="stFormSubmitButton"] {{
        text-align: center !important;
        margin-top: 15px;
    }}

    div[data-testid="stFormSubmitButton"]>button {{
        width: 100% !important;
        padding: 12px 24px !important;
        font-size: 0.95rem !important;
    }}

    /* Form Footer */
    .form-footer {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        margin-top: 25px;
        font-size: 0.8rem;
        color: {card_text_secondary};
    }}
    
    .footer-line {{
        flex: 1;
        height: 1px;
        background: rgba(245, 245, 218, 0.08);
    }}
    
    .footer-link {{
        color: {card_text_secondary} !important;
        text-decoration: none !important;
        transition: color 0.2s ease !important;
    }}
    
    .footer-link:hover {{
        color: {text_color} !important;
    }}

    /* Custom Loading Rocket Animations */
    .loading-card {{
        max-width: 520px;
        margin: 40px auto !important;
        text-align: center;
        box-shadow: 0 15px 40px rgba(123, 2, 29, 0.3) !important;
        border-color: {glow_color} !important;
    }}

    @keyframes rocketLaunch {{
        0%, 100% {{ transform: translateY(0) rotate(0deg); }}
        50% {{ transform: translateY(-12px) rotate(6deg) scale(1.08); filter: drop-shadow(0 0 15px {glow_color}); }}
    }}
    
    .loader-rocket {{
        display: inline-block;
        animation: rocketLaunch 0.9s ease-in-out infinite;
    }}

    /* Ensure no margin issues on purple glowing card */
    .glow-purple {{
        margin: 0px 0px 20px 0px !important;
    }}

    /* Force dashboard columns to align at the top */
    div[data-testid="stHorizontalBlock"]:not(:has(.illustration-wrapper)) > div[data-testid="column"] {{
        align-self: flex-start !important;
    }}
    </style>
    """
    return css
