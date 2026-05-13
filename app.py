import streamlit as st

st.set_page_config(
    page_title="Quantum Analytics Hub",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

st.title("🔮 Quantum Analytics Hub")
st.markdown("---")

if not st.session_state.authenticated:
    st.subheader("Secure Gateway")
    st.info("💡 **System Note:** The application is currently state-locked. Click below to trigger a global session state change.")
    if st.button("Initialize Session", type="primary"):
        st.session_state.authenticated = True
        st.rerun()
else:
    st.sidebar.success("Session Active")
    if st.sidebar.button("Terminate Session"):
        st.session_state.authenticated = False
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

    # --- NEW COMMENTARY SECTION ---
    st.markdown("---")
    with st.expander("🛠️ Architectural Blueprint: How this page works", expanded=True):
        st.markdown("""
        ### Core Concept: Global Session State Management
        Standard web applications require heavy backend frameworks (like Flask or Django) paired with cookies to remember who you are. 
        Streamlit handles this natively via `st.session_state`, acting as an in-memory key-value store tied to this specific browser tab session.
        
        * **The Logic:** When you clicked *Initialize Session*, we set `st.session_state.authenticated = True` and forced a `st.rerun()`.
        * **The Impact:** Every sub-page inside the `pages/` directory constantly checks this boolean. If a user tries to bookmark or bypass straight to the Analytics page without authenticating here, the system intercepts them and calls `st.stop()`, killing the execution thread instantly.
        """)