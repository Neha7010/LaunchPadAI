import streamlit as st

# Set Streamlit Page Configuration as the very first command
st.set_page_config(
    page_title="Launchpad AI — Project Architect",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

from ui.styles import get_css
from ui.login_page import show_login_page
from ui.dashboard_page import show_dashboard
from ui.report_page import show_report_page
from config.settings import GEMINI_API_KEY

def initialize_session():
    """Initializes standard session state keys if they don't exist."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "page" not in st.session_state:
        st.session_state.page = "login"
    if "sub_page" not in st.session_state:
        st.session_state.sub_page = "recommend"
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"
    if "recommendations" not in st.session_state:
        st.session_state.recommendations = None
    if "extracted_profile" not in st.session_state:
        st.session_state.extracted_profile = None
    if "retrieved_snippets" not in st.session_state:
        st.session_state.retrieved_snippets = None
    if "selected_project" not in st.session_state:
        st.session_state.selected_project = None
    if "report_text" not in st.session_state:
        st.session_state.report_text = None
    if "gemini_key" not in st.session_state:
        st.session_state.gemini_key = GEMINI_API_KEY

def main():
    # Initialize states
    initialize_session()
    
    # Inject Custom Glassmorphism Styles based on the active theme mode
    css = get_css(st.session_state.theme)
    st.markdown(css, unsafe_allow_html=True)
    
    # Page Router
    page = st.session_state.page
    
    if not st.session_state.logged_in:
        st.session_state.page = "login"
        show_login_page()
    else:
        if page == "login":
            st.session_state.page = "dashboard"
            show_dashboard()
        elif page == "dashboard":
            show_dashboard()
        elif page == "report":
            show_report_page()

if __name__ == "__main__":
    main()
