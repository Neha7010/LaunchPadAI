import streamlit as st
import textwrap
from services.db import register_user, login_user

def show_login_page():
    """Renders login/registration split-pane view."""
    
    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.15, 1])
    
    with col_left:
        # Render left-side illustration inside an iframe using st.components.v1.html
        left_panel_html = textwrap.dedent("""\
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Fira+Code:wght@400;500&display=swap');
                
                body {
                    margin: 0;
                    padding: 0;
                    background: transparent;
                    color: #F5F5DA;
                    font-family: 'Outfit', sans-serif;
                    overflow: hidden;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    text-align: center;
                }
                
                .illustration-wrapper {
                    width: 280px;
                    height: 250px;
                    position: relative;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin-bottom: 20px;
                    transform: scale(1.4);
                }
                
                .orbit-ring {
                    position: absolute;
                    border: 1px dashed rgba(245, 245, 218, 0.08);
                    border-radius: 50%;
                    animation: spin 35s linear infinite;
                }
                
                .orbit-outer {
                    width: 250px;
                    height: 250px;
                }
                
                .orbit-inner {
                    width: 190px;
                    height: 190px;
                    animation-direction: reverse;
                    animation-duration: 25s;
                }
                
                @keyframes spin {
                    100% { transform: rotate(360deg); }
                }
                
                .floating-badge {
                    position: absolute;
                    width: 36px;
                    height: 36px;
                    border-radius: 50%;
                    background: #1f0107;
                    border: 1px solid rgba(245, 245, 218, 0.15);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    font-size: 0.85rem;
                    box-shadow: 0 0 10px rgba(123, 2, 29, 0.4);
                    color: #F5F5DA;
                    animation: float-badge 6s ease-in-out infinite;
                    font-weight: bold;
                }
                
                @keyframes float-badge {
                    0%, 100% { transform: translateY(0); }
                    50% { transform: translateY(-5px); }
                }
                
                .badge-pos1 { top: 15px; left: 35px; animation-delay: 0s; }
                .badge-pos2 { top: 105px; right: 10px; animation-delay: 1.5s; }
                .badge-pos3 { bottom: 15px; left: 95px; animation-delay: 3s; }
                .badge-pos4 { top: 175px; left: 10px; animation-delay: 4.5s; }

                .browser-card {
                    width: 160px;
                    height: 125px;
                    background: rgba(30, 2, 7, 0.85);
                    border: 1px solid rgba(245, 245, 218, 0.12);
                    border-radius: 12px;
                    position: relative;
                    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
                    overflow: hidden;
                    display: flex;
                    flex-direction: column;
                    padding: 10px;
                    z-index: 2;
                }
                
                .browser-header-dots {
                    display: flex;
                    gap: 4px;
                    margin-bottom: 12px;
                }
                
                .browser-dot {
                    width: 5px;
                    height: 5px;
                    border-radius: 50%;
                    background: rgba(245, 245, 218, 0.3);
                }
                
                .browser-body-content {
                    display: flex;
                    flex-direction: column;
                    gap: 6px;
                }
                
                .browser-line {
                    height: 4px;
                    background: rgba(245, 245, 218, 0.1);
                    border-radius: 3px;
                }
                
                .line-short { width: 50%; }
                .line-medium { width: 75%; }
                .line-long { width: 90%; }
                
                .browser-stars {
                    color: #7B021D;
                    font-size: 0.65rem;
                    margin-bottom: 2px;
                    letter-spacing: 1px;
                }
                
                .browser-icon-box {
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
                }
                
                .magnifying-glass-svg {
                    position: absolute;
                    width: 70px;
                    height: 70px;
                    right: 35px;
                    bottom: 45px;
                    z-index: 3;
                    filter: drop-shadow(0 4px 12px rgba(123, 2, 29, 0.6));
                    animation: pulse-magnifier 4s ease-in-out infinite;
                }
                
                @keyframes pulse-magnifier {
                    0%, 100% { transform: scale(1) translate(0, 0); }
                    50% { transform: scale(1.06) translate(2px, -2px); }
                }

                .brand-title {
                    font-family: 'Outfit', sans-serif;
                    font-weight: 800;
                    font-size: 2rem;
                    color: #F5F5DA;
                    margin: 40px 0 8px 0;
                }

                .brand-subtitle {
                    font-size: 0.9rem;
                    color: #d6cca9;
                    max-width: 280px;
                    margin: 0 auto;
                    font-weight: 400;
                    line-height: 1.4;
                }

                .brand-divider {
                    width: 40px;
                    height: 2px;
                    background: #7B021D;
                    margin: 15px auto 0 auto;
                    border-radius: 99px;
                }
            </style>
        </head>
        <body>
            <div class="illustration-wrapper">
                <div class="orbit-ring orbit-outer"></div>
                <div class="orbit-ring orbit-inner"></div>
                <div class="floating-badge badge-pos1">&lt;/&gt;</div>
                <div class="floating-badge badge-pos2">🗄️</div>
                <div class="floating-badge badge-pos3">📊</div>
                <div class="floating-badge badge-pos4">⚙️</div>
                <div class="browser-card">
                    <div class="browser-header-dots">
                        <span class="browser-dot"></span>
                        <span class="browser-dot"></span>
                        <span class="browser-dot"></span>
                    </div>
                    <div class="browser-body-content">
                        <div class="browser-icon-box">&lt;/&gt;</div>
                        <div class="browser-stars">★★★★★</div>
                        <div class="browser-line line-short"></div>
                        <div class="browser-line line-medium"></div>
                        <div class="browser-line line-long"></div>
                    </div>
                </div>
                <svg class="magnifying-glass-svg" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="10" cy="10" r="7" stroke="#7B021D" stroke-width="2.5" fill="rgba(123, 2, 29, 0.15)"/>
                    <line x1="15" y1="15" x2="22" y2="22" stroke="#7B021D" stroke-width="3" stroke-linecap="round"/>
                </svg>
            </div>
            <div class="brand-title">Launchpad AI</div>
            <div class="brand-subtitle">Find the right software projects. Faster. Smarter. Together.</div>
            <div class="brand-divider"></div>
        </body>
        </html>
        """)
        
        st.components.v1.html(left_panel_html, height=500, scrolling=False)
        
    with col_right:
        tab_login, tab_signup = st.tabs(["🔒 Sign In", "👤 Create Account"])
        
        with tab_login:
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="👤 Enter your username", key="login_username")
                password = st.text_input("Password", type="password", placeholder="🔒 Enter your password", key="login_password")
                submit = st.form_submit_button("Log In")
                
                if submit:
                    user = login_user(username, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        st.session_state.page = "dashboard"
                        st.success(f"Welcome back, {user['username']}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
                        
            # Forgot Password footer decoration
            st.markdown("""
            <div class="form-footer">
                <span class="footer-line"></span>
                <a href="#" class="footer-link">Forgot Password?</a>
                <span class="footer-line"></span>
            </div>
            """, unsafe_allow_html=True)
                        
        with tab_signup:
            with st.form("signup_form"):
                reg_username = st.text_input("Choose Username", placeholder="👤 Enter a username", key="reg_username")
                reg_password = st.text_input("Choose Password", type="password", placeholder="🔒 Choose a secure password", key="reg_password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="🔒 Confirm your password", key="confirm_password")
                submit_reg = st.form_submit_button("Sign Up")
                
                if submit_reg:
                    if reg_password != confirm_password:
                        st.error("Passwords do not match.")
                    elif len(reg_password) < 4:
                        st.error("Password must be at least 4 characters.")
                    elif not reg_username.strip():
                        st.error("Username cannot be empty.")
                    else:
                        success = register_user(reg_username, reg_password)
                        if success:
                            st.success("Account created successfully! Please log in.")
                        else:
                            st.error("Username is already taken.")
