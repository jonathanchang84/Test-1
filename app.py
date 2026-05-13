import streamlit as st

# Initialize Global Session Security Token
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Explicitly define our standalone workspace nodes
home_node = st.Page("pages/0_🔮_Hub_Home.py", title="Quantum Analytics Hub", icon="🔮", default=True)
cluster_node = st.Page("pages/1_🖥️_Cluster_Operations.py", title="Cluster Operations", icon="🖥️")
api_node = st.Page("pages/2_🌐_Real_Time_API.py", title="Real-Time API Node", icon="🌐")
ml_node = st.Page("pages/3_🔮_Predictive_Modeling.py", title="Predictive Modeling", icon="🔮")

# SECURITY BRIDGE ROUTER
# If unauthenticated, the sidebar ONLY displays the locked landing pad.
# Once clicked, the active session array expands dynamically.
if not st.session_state.authenticated:
    nav_matrix = st.navigation([home_node], position="sidebar")
else:
    nav_matrix = st.navigation([home_node, cluster_node, api_node, ml_node], position="sidebar")

# Run the active page target
nav_matrix.run()