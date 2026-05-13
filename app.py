import streamlit as st

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="Quantum Analytics Hub",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Complex Idea: Global Session State Management
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Simple mock authentication gate
def login_user():
    st.session_state.authenticated = True

def logout_user():
    st.session_state.authenticated = False

# 3. UI Layout
st.title("🔮 Quantum Analytics Hub")
st.markdown("---")

if not st.session_state.authenticated:
    st.subheader("Secure Gateway")
    st.info("Please initialize the session to unlock advanced analytics pages.")
    if st.button("Initialize Session", type="primary"):
        login_user()
        st.rerun()
else:
    st.sidebar.success("Session Active")
    if st.sidebar.button("Terminate Session"):
        logout_user()
        st.rerun()
        
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Welcome to the Edge of Data Science")
        st.write("""
            This application demonstrates complex architectural patterns in Streamlit:
            * **State Preservation:** Keeps track of your auth state across page navigation.
            * **Multi-Page Routing:** Dynamically handles disparate data workloads.
            * **Reactive Computations:** Updates elements only when inputs strictly change.
        """)
    
    with col2:
        st.center = st.status("System Status", expanded=True)
        st.center.write("🔄 Caching Engines: Operational")
        st.center.write("📡 Async Data Pipelines: Ready")
        st.center.write("🔐 Session Token: Verified")