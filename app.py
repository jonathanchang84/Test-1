import streamlit as st

# 1. Global Application Layout Configuration
st.set_page_config(
    page_title="Modular Analytics & Visualization Capabilities: A Technical Exercise",
    page_icon="🎨",
    layout="wide"
)

# Initialize global session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = True

# 2. EXPLICIT ROUTING ENGINE FOR YOUR EXACT FILE NAMES
# We pass the exact filenames straight from your pages/ folder to prevent string mismatch bugs
pg = st.navigation({
    "Navigation Menu": [
        st.Page("pages/0_🔮_Hub_Home.py", title="Home", icon="🏠", default=True),
        st.Page("pages/1_💻_Cluster_Operations.py", title="Cluster Operations", icon="💻"),
        st.Page("pages/2_🌐_Real_Time_API.py", title="Geospatial Telemetry", icon="🗺️"),
        st.Page("pages/3_🔮_Predictive_Modeling.py", title="Predictive Modeling", icon="🔮")
    ]
})

# 3. RUN NAVIGATION ROUTER
pg.run()