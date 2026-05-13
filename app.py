import streamlit as st

# Define the paths relative to the root directory where app.py lives
home_page = st.Page(
    "pages/0_🔮_Hub_Home.py",  # Point directly to your home script location
    title="Home", 
    icon="🏠", 
    default=True
)
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

# Render the sidebar navigation routing framework
pg = st.navigation([home_page, map_page, model_page])

# Set global page configurations
st.set_page_config(
    page_title="Modular Analytics & Visualization Capabilities: A Technical Exercise",
    page_icon="🎨",
    layout="wide"
)

# Initialize session state globally
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = True

# Execute the active page routing engine
pg.run()