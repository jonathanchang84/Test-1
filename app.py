# ==========================================
# 1. GLOBAL PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Quantum Analytics Hub",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
    # FORCING THE NAVIGATION MATRIX BACK INTO VIEW:
    menu_items={
        'Get Help': 'https://docs.streamlit.io'
    }
)

# Force clear sidebar navigation visibility rules via a hidden markdown style patch
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {
            display: block !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)