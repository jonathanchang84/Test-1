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

# 2. FILE POSITION INDEX ENGINE WITH HARD LIMIT
pages_dir = Path(__file__).parent / "pages"
clean_nav_pages = []

if pages_dir.exists():
    # Grab all python files sitting in the pages folder and sort them 0, 1, 2...
    discovered_files = sorted(list(pages_dir.glob("*.py")))
    
    # CRITICAL FIX: Slice the list [:3] to strictly allow ONLY the first 3 files.
    # Any extra ghost files or duplicates on the server will be completely ignored.
    for idx, file_path in enumerate(discovered_files[:3]):
        filename = file_path.name
        relative_path = f"pages/{filename}"
        
        if idx == 0:
            clean_nav_pages.append(st.Page(relative_path, title="Home", icon="🏠", default=True))
        elif idx == 1:
            clean_nav_pages.append(st.Page(relative_path, title="Geospatial Telemetry", icon="🗺️"))
        elif idx == 2:
            clean_nav_pages.append(st.Page(relative_path, title="Predictive Modeling", icon="🔮"))

# 3. RUN ROUTER
if clean_nav_pages:
    pg = st.navigation(clean_nav_pages)
else:
    pg = st.navigation([])

pg.run()