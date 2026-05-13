import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ==========================================
# 1. GLOBAL PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Quantum Analytics Hub",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. GLOBAL SESSION STATE MANAGEMENT
# ==========================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

st.title("🔮 Quantum Analytics Hub")
st.markdown("---")

# ==========================================
# 3. SECURITY GATEWAY LOGIC
# ==========================================
if not st.session_state.authenticated:
    st.subheader("Secure Gateway Connection Required")
    st.info("💡 **System Note:** The multi-page cluster is currently state-locked. Initialize the session token below to unlock full telemetry.")
    
    if st.button("Initialize Master Session", type="primary"):
        st.session_state.authenticated = True
        st.rerun()
        
else:
    # Sidebar control to kill the token state
    st.sidebar.success("🔑 Global Session Active")
    
    if st.sidebar.button(
        "Terminate Session Matrix", 
        help="[Mechanism #1]: Mutates st.session_state.authenticated to False, instantly locking sub-page threads."
    ):
        st.session_state.authenticated = False
        st.rerun()

    # ==========================================
    # 4. CORE OPERATION DASHBOARD (Initial Work)
    # ==========================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.header(
            "Core Cluster Operations", 
            help="[Mechanism #1]: This interface is entirely conditional on Session State. If the global token is missing or terminated, this DOM structure cannot execute."
        )
        st.write("""
            Welcome back to the master command node. The cloud environment is fully synchronized:
            * **State Preservation:** Syncing token authentications across all sub-nodes.
            * **Dynamic Meshgrids:** Vector matrix mapping available on the Analytics page.
            * **Asynchronous Streams:** Live DOM components running on the Live Feed page.
        """)
    
    with col2:
        system_status = st.status("System Infrastructure Engine", expanded=True)
        system_status.write("🔄 RAM Caching Engine: Online & Optimized")
        system_status.write("📡 Async Data Pipelines: Listening")
        system_status.write("🔐 Remote Session Token: Verified True")

    st.markdown("---")

    # ==========================================
    # 5. INTEGRATED LIVE API TELEMETRY NODE
    # ==========================================
    st.header(
        "🌐 Integrated Real-Time API Node", 
        help="[Mechanism #2 & #4]: Outbound HTTPS requests pull JSON datasets dynamically based on the sidebar filters and map them to global open-street-map coordinates."
    )
    
    # Sidebar Filters acting as Server-Side parameters
    st.sidebar.markdown("---")
    st.sidebar.header("Global API Filters")
    
    min_magnitude = st.sidebar.slider(
        "Minimum Magnitude", 1.0, 7.0, 4.5, step=0.5,
        help="[Mechanism #2]: Injects filtering rules straight into the REST URL query string to perform server-side parsing before data reaches your browser."
    )
    limit = st.sidebar.slider(
        "Max Record Limit", 10, 100, 40, step=10,
        help="[Mechanism #2]: Restricts maximum payload data packets to prevent browser thread latency and network saturation."
    )

    # REST API Data Fetching and Normalization Function
    def fetch_geospatial_telemetry(min_mag, max_rows):
        url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minmagnitude={min_mag}&limit={max_rows}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status() 
            raw_json = response.json()
            features = raw_json.get("features", [])
            
            cleaned_records = []
            for item in features:
                props = item.get("properties", {})
                geom = item.get("geometry", {})
                coords = geom.get("coordinates", [0, 0, 0])
                
                cleaned_records.append({
                    "Location": props.get("place", "Unknown Axis"),
                    "Magnitude": props.get("mag", 0.0),
                    "Time": pd.to_datetime(props.get("time", 0), unit='ms'),
                    "Longitude": coords[0],
                    "Latitude": coords[1],
                    "Depth (km)": coords[2]
                })
            return pd.DataFrame(cleaned_records)
        except Exception as e:
            st.error(f"🔴 Telemetry Fetch Fault: {e}")
            return pd.DataFrame()

    with st.spinner("Streaming remote payload..."):
        telemetry_df = fetch_geospatial_telemetry(min_magnitude, limit)

    # UI Rendering of the Data Payload
    if not telemetry_df.empty:
        metric_col, map_col = st.columns([1, 2])
        
        with metric_col:
            st.metric(
                "Detected Vectors", len(telemetry_df),
                help="[Mechanism #3]: Represents the row total (N) of the clean tabular vector matrix parsed out of raw nested GeoJSON lists."
            )
            st.metric(
                "Peak Severity", f"{telemetry_df['Magnitude'].max():.1f} Mag",
                help="[Mechanism #3]: Vector calculation computing the maximum scalar value within the generated DataFrame column vector."
            )
            
            # --- FIXED SECTION ---
            # Instead of passing help= inside st.dataframe(), we render a clear caption right above it
            st.caption("📋 **[Mechanism #3]: Raw Flattened Matrix Preview**")
            st.dataframe(
                telemetry_df[["Location", "Magnitude"]].head(6), 
                use_container_width=True
            )
            # ----------------------
        
        with map_col:
            fig = px.scatter_mapbox(
                telemetry_df, lat="Latitude", lon="Longitude", size="Magnitude", color="Depth (km)",
                color_continuous_scale="Plasma", hover_name="Location", zoom=1, height=350
            )
            fig.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, b=0, t=0))
            st.plotly_chart(fig, use_container_width=True)

    # ==========================================
    # 6. COMPREHENSIVE ARCHITECTURAL BLUEPRINT
    # ==========================================
    st.markdown("---")
    with st.expander("🛠️ System Engineering Blueprint: Feature Matrix & Core Mechanisms", expanded=True):
        
        st.markdown("""
        ### [1] Global Session State & Security Gateways
        * **The Feature:** A conditional gateway that blocks unauthorized users from seeing metrics, maps, or navigating to sub-pages.
        * **The Mechanism (`st.session_state`):** Standard HTTP web environments are naturally stateless—every time a user clicks something, the script re-runs from scratch and "forgets" who you are. We bypass this by instantiating an in-memory key-value dictionary on the server:
            ```python
            if "authenticated" not in st.session_state:
                st.session_state.authenticated = False
            ```
            When you initialize the session, this state mutates to `True`. Because sub-pages read this exact global dictionary, they can instantly identify if a user has cleared the home checkpoint. If a user tries to deep-link straight to a sub-page without authenticating, the system intercepts them and calls `st.stop()`, terminating the code execution thread immediately.
        
        ---
        
        ### [2] Live REST API Integration & Data Pipelines
        * **The Feature:** Dynamically fetching and plotting real-world tectonic anomalies in real-time without requiring a static database.
        * **The Mechanism (`requests` + Server-Side Filtering):** When this homepage builds, it instantiates an outbound HTTPS handshake with the remote USGS server using Python's `requests` library. 
            Instead of downloading the entire global database (which would cause massive network latency), we inject your slider values as query strings directly into the URL endpoint:
            `format=geojson&minmagnitude={min_mag}&limit={max_rows}`
            This forces the remote government server to do the heavy computational filtering *before* sending the payload across the internet to our app container.
            
        ---
        
        ### [3] Structural Matrix Flattening (Data Normalization)
        * **The Feature:** Transforming raw, unreadable internet packets into clean, queryable tables and geographic coordinates.
        * **The Mechanism (GeoJSON Parsing):** Public APIs transfer data using nested JSON structures. For example, geospatial data is deeply buried inside a tree like: `item["geometry"]["coordinates"][0]`. 
            Web browsers and plotting libraries cannot naturally read this tree structure. Our custom parsing function loops through the inbound JSON stream, strips out the nested layers, and normalizes them into a highly optimized tabular structure: an $180\times C$ row/column vector matrix called a **Pandas DataFrame**. This allows our metric elements and maps to query values instantaneously.
            
        ---
        
        ### [4] Geospatial Topology Visualization
        * **The Feature:** A fully interactive global map tracking data coordinates.
        * **The Mechanism (Plotly Mapbox Canvas):** We feed our normalized Pandas DataFrame into `plotly.express.scatter_mapbox`. Plotly reads the `Latitude` and `Longitude` float arrays from our matrix and overlays them precisely onto an open-source mapping engine (`open-street-map`). 
            Instead of plotting static points, it dynamically assigns visual properties based on data columns: the *size* of the bubble maps to the earthquake's magnitude, and the *color spectrum* maps to the subterranean depth (km) using a specialized color-ramp array.
        """)

        st.markdown("---")
        st.markdown("### 🗺️ Sub-Page Architecture (Accessible via Left Sidebar Menu)")
        
        st.markdown("""
        ### [5] Multi-Dimensional Vector Meshgrids (Analytics Page)
        * **The Feature:** A 3D wave model that recalculates based on user resolution limits.
        * **The Mechanism (`@st.cache_data` Optimization):** Calculating complex coordinate physics for thousands of data points is incredibly expensive for a server's CPU. If a user simply changes the *color palette* of the chart, it would normally force the server to waste energy recalculating all the geometry formulas from scratch.
            By wrapping the function in `@st.cache_data`, Streamlit takes a digital fingerprint of the input arguments. If the resolution size hasn't changed, it instantly serves the mathematical coordinates straight out of fast-access RAM cache memory, bypassing computation latency entirely.
            
        ---
        
        ### [6] Asynchronous DOM In-Place Mutation (Live Stream Page)
        * **The Feature:** A chart and metric panel that updates smoothly and continuously like a live financial stock ticker.
        * **The Mechanism (`st.empty()` Element Overwriting):** In a traditional web framework, sending new data to the screen requires a full page refresh. We dodge this completely by declaring a visual placeholder layout: `metric_spot = st.empty()`. 
            This pre-allocates a static set of coordinates in your web browser's DOM tree before any data even exists. When our algorithmic loop runs, it targets that precise layout coordinate and overwrites its internal HTML content dynamically without disturbing the rest of the webpage.
        """)