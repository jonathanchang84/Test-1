import streamlit as st

# Global Page Configuration
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

# Security Gateway Logic
if not st.session_state.authenticated:
    st.subheader("Secure Gateway Connection Required")
    st.info("💡 **System Note:** The multi-page cluster is currently state-locked. Initialize the session token below to unlock full telemetry.")
    
    if st.button("Initialize Master Session", type="primary"):
        st.session_state.authenticated = True
        st.rerun()
        
else:
    st.sidebar.success("🔑 Global Session Active")
    if st.sidebar.button("Terminate Session Matrix", help="[Mechanism #1]: Locks sub-page threads across the ecosystem."):
        st.session_state.authenticated = False
        st.rerun()

    # Clean Landing Layout
    col1, col2 = st.columns([2, 1])
    with col1:
        st.header("Welcome to the Master Telemetry Node", divider="teal")
        st.markdown("""
        This platform represents an enterprise-grade web application architecture built entirely within Python. 
        By utilizing decoupled processing layouts, the computational workloads are dynamically isolated across independent system nodes.
        
        #### Available Network Nodes:
        1. **🖥️ Cluster Operations:** Displays internal infrastructure tracking states and core operational flags.
        2. **🌐 Real-Time API Node:** Performs server-side REST API queries, data normalization, mapping, and in-memory extraction.
        3. **🔮 Predictive Modeling Node:** Processes incoming real-world metrics through structural machine learning regression paths.
        
        *Use the left sidebar navigation matrix to traverse active system modules.*
        """)
    with col2:
        st.info("💡 **Navigation Protocol:** Every sub-page acts as an isolated sandbox but reads from the same unified memory stack (`st.session_state`), maintaining persistent data compliance.")

    # Engineering Notes Section
    st.markdown("---")
    with st.expander("🛠️ System Engineering Blueprint: Feature Matrix & Core Mechanisms", expanded=True):
        st.markdown("""
        ### [Mechanism #1] Global Session State & Security Gateways
        * **The Feature:** A conditional gateway that blocks unauthorized users from navigating to sub-pages or accessing metrics.
        * **The Mechanism (`st.session_state`):** Standard web threads are stateless. We bypass this by instantiating an in-memory key-value dictionary on the server. When authenticated, this state mutates to `True`. Because sub-pages read this dictionary, they instantly determine compliance. If an unauthorized user deep-links directly to a page without authenticating here, the system calls `st.stop()`, instantly dropping execution loops.
        """)