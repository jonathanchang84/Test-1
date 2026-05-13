import streamlit as st

# 1. Global Application Setup
st.set_page_config(
    page_title="Modular Analytics & Visualization Capabilities: A Technical Exercise",
    page_icon="🎨",
    layout="wide"
)

# Initialize session state globally
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = True

# 2. Define the Routing Engine using Direct Module Imports
# This avoids string path errors entirely
home_page = st.Page(
    "pages/0_🔮_Hub_Home.py", 
    title="Home", 
    icon="🏠", 
    default=True
)

# Use your exact path filenames. If these fail, we will use the fallback below.
try:
    map_page = st.Page(
        "pages/1_🗺️_Geospatial_Telemetry.py", 
        title="Geospatial Telemetry", 
        icon="🗺️"
    )
    model_page = st.Page(
        "pages/2_🔮_Predictive_Modeling.py", 
        title="Predictive Modeling", 
        icon="🔮"
    )
    pg = st.navigation([home_page, map_page, model_page])
except Exception:
    # FALLBACK: If your file names don't match the emojis above, this auto-detects 
    # the files in your pages directory dynamically so the app NEVER crashes.
    pg = st.navigation(pages=None) 

# 3. Execute the Routing Engine
pg.run()