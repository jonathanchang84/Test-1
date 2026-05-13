import streamlit as st

# ==========================================
# SIDEBAR NAVIGATION & EXPLICIT ROUTING ENGINE
# ==========================================
# Define the sidebar navigation labels, file paths, and icons explicitly
home_page = st.Page(
    "Hello.py", 
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

# Render the sidebar navigation using our custom-labeled page objects
pg = st.navigation([home_page, map_page, model_page])

# Global Page Layout Configuration
st.set_page_config(
    page_title="Modular Analytics & Visualization Capabilities: A Technical Exercise",
    page_icon="🎨",
    layout="wide"
)

# Initialize global authentication state for subpages to verify
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = True

# Execute the page routing engine to draw the contents below
pg.run()


# ==========================================
# MAIN INTERFACE CAPABILITIES PORTFOLIO
# ==========================================

# Main Entry Title Block
st.title("🎨 Modular Analytics & Visualization Capabilities: A Technical Exercise")
st.markdown("##### *An Interactive Technical Portfolio Demonstrating Rapid Deployment Features for Data-Driven Applications*")
st.markdown("---")

# --- HIGH-LEVEL FRAMEWORK PURPOSE ---
st.subheader("💡 Purpose of this Framework")
st.markdown("""
This application serves as an interactive **Feature & Component Showcase**. It is engineered to demonstrate various modular functionalities, UI layouts, and data integration patterns that can be built and scaled within custom internal dashboards or client-facing data products. 

Instead of a single static report, this environment exhibits how real-time feeds, computational math engines, and interactive visual graphics can be combined to solve technical interface requirements.
""")

st.markdown("---")

# --- FEATURE CAPABILITIES MATRIX ---
st.subheader("⚙️ Scalable Features Showcase Index")
st.markdown("Below is an architectural breakdown of the core functionalities implemented across the active sub-nodes in this application:")

feat_col1, feat_col2, feat_col3 = st.columns(3)

with feat_col1:
    st.markdown("### 🎛️ 1. Core UI & Real-Time Ingestion")
    st.markdown("""
    Demonstrates foundational application structure, secure session state handling, and external API integrations.
    * **State Management:** Verifies active environment sessions across decoupled page scripts.
    * **Resilient Live Ingestion:** Features asynchronous multi-point REST API calls with robust intercept handling protocols for data timeouts and bad gateways.
    * **High-Density Metrics:** Utilizes native dashboard metric ribbons to distill raw volume counts into instant visual KPIs.
    """)

with feat_col2:
    st.markdown("### 🗺️ 2. High-Density Spatial Mapping")
    st.markdown("""
    Showcases complex coordinates and multi-dimensional spatial plots optimized for geographic visualization.
    * **Dynamic Layer Plotting:** Renders latitudinal and longitudinal coordinate matrices onto live maps.
    * **Contextual Data Tooltips:** Features high-density hover states that allow deep granular metadata inspection directly inside the spatial layer.
    * **Auto-Scaling Boundaries:** Adapts view frames automatically based on incoming vector dimensions.
    """)

with feat_col3:
    st.markdown("### 🔮 3. Statistical Engines & Forecasting")
    st.markdown("""
    Exhibits how to embed mathematical computation and analytical modeling seamlessly into consumer-facing charts.
    * **Descriptive Auditing:** Computes real-time array weights, central tendencies ($Mean$, $Median$), and distribution dispersion statistics ($\sigma$, $\sigma^2$).
    * **Predictive Extrapolation:** Integrates Scikit-Learn pipelines to dynamically compute OLS Linear Regression slopes.
    * **Trend Visualizers:** Uses an ordinal index sequencing model to plot trendlines directly over time-series data without UI or layout distortion.
    """)

st.markdown("---")

# --- CALL TO ACTION / NAV INSTRUCTIONS ---
st.subheader("🚀 Interactive Component Verification")
st.markdown("""
To explore how these individual modular components look, behave, and handle user interactions under real load, use the **Sidebar Navigation Menu** to traverse through the specialized execution nodes.
""")

st.info("💡 **Developer Note:** All components are fully responsive, utilize a unified global design theme, and pull live operational records dynamically from production data stores.")

st.markdown("---")
st.caption("⚙️ **Capabilities Framework Engine:** Active | **UI Framework:** Streamlit Dark Production | **API Layer:** Connected")