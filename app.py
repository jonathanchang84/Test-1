import streamlit as st
from pathlib import Path

# 1. Global Application Layout Configuration
st.set_page_config(
    page_title="Modular Analytics & Visualization Capabilities: A Technical Exercise",
    page_icon="🎨",
    layout="wide"
)

# Initialize global session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = True

# 2. MATCH-SPECIFIC PAGE ROUTING ENGINE
pages_dir = Path(__file__).parent / "pages"
clean_nav_pages = []

if pages_dir.exists():
    # Grab all python files sitting in the pages folder and sort them
    discovered_files = sorted(list(pages_dir.glob("*.py")))
    
    for file_path in discovered_files:
        filename = file_path.name
        relative_path = f"pages/{filename}"
        
        # Explicitly assign pages based on unique keywords in their filenames
        if "Hub_Home" in filename or "0_" in filename:
            clean_nav_pages.append(st.Page(relative_path, title="Home", icon="🏠", default=True))
        elif "Telemetry" in filename or "1_" in filename:
            clean_nav_pages.append(st.Page(relative_path, title="Geospatial Telemetry", icon="🗺️"))
        elif "Predictive" in filename or "2_" in filename:
            clean_nav_pages.append(st.Page(relative_path, title="Predictive Modeling", icon="🔮"))
        elif "Cluster" in filename or "3_" in filename:
            clean_nav_pages.append(st.Page(relative_path, title="Cluster Operations", icon="⚙️"))
        # Any other backup or duplicate files are completely ignored by skipping the append

# 3. RUN ROUTER WITH FILTERED LIST
if clean_nav_pages:
    pg = st.navigation(clean_nav_pages)
else:
    pg = st.navigation([])

pg.run()