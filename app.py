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

# 2. MATCH BY NUMBER TO BYPASS EMOJI CODES
pages_dir = Path(__file__).parent / "pages"
clean_nav_pages = []

if pages_dir.exists():
    # Gather and sort all python files inside the pages/ directory
    all_files = sorted(list(pages_dir.glob("*.py")))
    
    for file_path in all_files:
        filename = file_path.name
        relative_path = f"pages/{filename}"
        
        # Check how the filename starts to map it safely
        if filename.startswith("0_"):
            clean_nav_pages.append(st.Page(relative_path, title="Home", icon="🏠", default=True))
        elif filename.startswith("1_"):
            clean_nav_pages.append(st.Page(relative_path, title="Cluster Operations", icon="💻"))
        elif filename.startswith("2_"):
            clean_nav_pages.append(st.Page(relative_path, title="Geospatial Telemetry", icon="🗺️"))
        elif filename.startswith("3_"):
            clean_nav_pages.append(st.Page(relative_path, title="Predictive Modeling", icon="🔮"))

# 3. RUN THE SYSTEM NAVIGATION
if clean_nav_pages:
    pg = st.navigation(clean_nav_pages)
else:
    pg = st.navigation([])

pg.run()