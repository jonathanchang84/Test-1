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

# 2. DEFINE PAGES USING THE NATIVE DICTIONARY FORMAT
# This completely eliminates string checking bugs and prevents duplicate links
pg = st.navigation({
    "Navigation": [
        st.Page("pages/0_🔮_Hub_Home.py", title="Home", icon="🏠", default=True),
        st.Page("pages/1_🗺️_Geospatial_Telemetry.py", title="Geospatial Telemetry", icon="🗺️"),
        st.Page("pages/2_🔮_Predictive_Modeling.py", title="Predictive Modeling", icon="🔮")
    ]
})

# 3. RUN NAVIGATION ROUTER
pg.run()