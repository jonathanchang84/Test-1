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

# 2. DYNAMIC FILENAME DISCOVERY ENGINE
# This scans your actual disk folder to find your files, ignoring string typos completely.
pages_dir = Path(__file__).parent / "pages"
found_pages = []

if pages_dir.exists():
    # Grab all .py files inside the pages/ folder and sort them alphabetically
    py_files = sorted(list(pages_dir.glob("*.py")))
    
    for file_path in py_files:
        filename = file_path.name
        
        # Assign custom titles based on what the file actually is
        if "Hub_Home" in filename or "0_" in filename:
            found_pages.append(st.Page(f"pages/{filename}", title="Home", icon="🏠", default=True))
        elif "Telemetry" in filename or "1_" in filename:
            found_pages.append(st.Page(f"pages/{filename}", title="Geospatial Telemetry", icon="🗺️"))
        elif "Predictive" in filename or "2_" in filename:
            found_pages.append(st.Page(f"pages/{filename}", title="Predictive Modeling", icon="🔮"))
        else:
            # Fallback title extraction if names are completely arbitrary
            clean_title = filename.split("_", 1)[-1].replace(".py", "").replace("_", " ")
            found_pages.append(st.Page(f"pages/{filename}", title=clean_title))

# 3. RUN NAVIGATION ROUTER
# If something went wrong with directory scanning, use Streamlit's native auto-discover array
if found_pages:
    pg = st.navigation(found_pages)
else:
    # This is the correct native structure for default automatic page mapping
    pg = st.navigation([])

pg.run()