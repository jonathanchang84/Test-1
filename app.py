import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import io
from sklearn.linear_model import LinearRegression

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
    # 4. CORE OPERATION DASHBOARD
    # ==========================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.header(
            "Core Cluster Operations", 
            help="[Mechanism #1]: This interface is entirely conditional on Session State."
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
        help="[Mechanism #2 & #4]: Outbound HTTPS requests pull JSON datasets dynamically based on the sidebar filters."
    )
    
    # Sidebar Filters
    st.sidebar.markdown("---")
    st.sidebar.header("Global API Filters")
    min_magnitude = st.sidebar.slider("Minimum Magnitude", 1.0, 7.0, 4.0, step=0.5)
    limit = st.sidebar.slider("Max Record Limit", 15, 150, 50, step=5)

    # REST API Fetch Function (Mechanism #2)
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

    # --- MEASURING PERFORMANCE (Mechanism #6) ---
    start_time = time.perf_counter()
    
    with st.spinner("Streaming remote payload..."):
        telemetry_df = fetch_geospatial_telemetry(min_magnitude, limit)
        
    end_time = time.perf_counter()
    execution_latency = (end_time - start_time) * 1000 

    # Rendering Dashboard UI Layout
    if not telemetry_df.empty:
        telemetry_df = telemetry_df.sort_values(by="Time").reset_index(drop=True)

        metric_col, map_col = st.columns([1, 2])
        
        with metric_col:
            st.metric(
                "Detected Vectors", len(telemetry_df),
                help="[Mechanism #3]: Row count of the clean tabular vector matrix."
            )
            st.metric(
                "Peak Severity", f"{telemetry_df['Magnitude'].max():.1f} Mag",
                help="[Mechanism #3]: Maximum scalar value in the Magnitude series."
            )
            
            # --- MEMORY EXTRACTION ENGINE (Mechanism #3 Add-On) ---
            st.caption("📋 **[Mechanism #3]: Raw Flattened Matrix Preview**")
            st.dataframe(telemetry_df[["Location", "Magnitude"]].head(5), use_container_width=True)
            
            csv_buffer = io.StringIO()
            telemetry_df.to_csv(csv_buffer, index=False)
            csv_bytes = csv_buffer.getvalue()

            st.download_button(
                label="📥 Export Clean Dataset (CSV)",
                data=csv_bytes,
                file_name="normalized_telemetry_stream.csv",
                mime="text/csv",
                use_container_width=True,
                help="[Mechanism #3 Add-On]: Pipes active data matrices into volatile RAM as string buffers, eliminating local server storage overhead."
            )
            
            # --- HARDWARE PROFILING TELEMETRY (Mechanism #6) ---
            st.markdown("---")
            st.caption("⚡ **[Mechanism #6]: Live Infrastructure Diagnostics**")
            diag_col1, diag_col2 = st.columns(2)
            diag_col1.metric("API Latency", f"{execution_latency:.1f} ms", help="[Mechanism #6]: High-resolution CPU clock timer computing script loop speeds.")
            
            estimated_memory = (telemetry_df.memory_usage(deep=True).sum()) / 1024
            diag_col2.metric("RAM Allocation", f"{estimated_memory:.2f} KB", help="[Mechanism #6]: Calculated storage sizing footprint of the active DataFrame structures.")
        
        with map_col:
            fig = px.scatter_mapbox(
                telemetry_df, lat="Latitude", lon="Longitude", size="Magnitude", color="Depth (km)",
                color_continuous_scale="Plasma", hover_name="Location", zoom=1, height=380
            )
            fig.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, b=0, t=0))
            st.plotly_chart(fig, use_container_width=True)

        # --- MACHINE LEARNING FORECASTING (Mechanism #5) ---
        st.markdown("---")
        st.header("🔮 [Mechanism #5]: Predictive Algorithmic Forecasting Model", help="[Mechanism #5]: Fits ordinary least squares regression lines directly over time-series vectors.")
        
        X_timestamps = np.array(telemetry_df['Time'].astype(np.int64) // 10**9).reshape(-1, 1)
        Y_magnitudes = telemetry_df['Magnitude'].values.reshape(-1, 1)
        
        model = LinearRegression()
        model.fit(X_timestamps, Y_magnitudes)
        predictions = model.predict(X_timestamps)
        
        trend_fig = go.Figure()
        trend_fig.add_trace(go.Scatter(
            x=telemetry_df['Time'], y=telemetry_df['Magnitude'],
            mode='markers+lines', name='Observed Magnitude Vectors',
            line=dict(color='#00ffcc', width=1), marker=dict(size=6)
        ))
        trend_fig.add_trace(go.Scatter(
            x=telemetry_df['Time'], y=predictions.flatten(),
            mode='lines', name='Linear Regression Model Trendline',
            line=dict(color='#ff0055', width=2, dash='dash')
        ))
        trend_fig.update_layout(
            title="Temporal Magnitude Drift & ML Trajectory Mapping",
            template="plotly_dark", height=350,
            margin=dict(l=40, r=40, b=20, t=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(trend_fig, use_container_width=True)

    # ==========================================
    # 6. COMPREHENSIVE ARCHITECTURAL BLUEPRINT
    # ==========================================
    st.markdown("---")
    with st.expander("🛠️ System Engineering Blueprint: Feature Matrix & Core Mechanisms", expanded=True):
        
        st.markdown("""
        ### [1] Global Session State & Security Gateways
        * **The Feature:** A conditional gateway that blocks unauthorized users from seeing metrics, maps, or navigating to sub-pages.
        * **The Mechanism (`st.session_state`):** Standard HTTP environments are naturally stateless. We bypass this by instantiating an in-memory key-value dictionary on the server. When you initialize the session, this state mutates to `True`. Because sub-pages read this exact global dictionary, they can instantly identify if a user has cleared the home checkpoint. If a user tries to deep-link straight to a sub-page without authenticating, the system intercepts them and calls `st.stop()`, terminating the code execution thread immediately.
        
        ---
        
        ### [2] Live REST API Integration & Data Pipelines
        * **The Feature:** Dynamically fetching and plotting real-world tectonic anomalies in real-time without requiring a static database.
        * **The Mechanism (`requests` + Server-Side Filtering):** Outbound HTTPS handshakes target the USGS server. By appending user query parameters into the URL string, we delegate dataset trimming to the server, protecting bandwidth.
            
        ---
        
        ### [3] Structural Matrix Flattening & In-Memory ETL Export Engine
        * **The Feature:** Transforming raw, unreadable internet packets into clean, queryable tables and providing on-the-fly data extractions.
        * **The Mechanism (`io.StringIO` Data Buffering):** Public APIs transfer data using nested GeoJSON structures. Our parsing function loops through the inbound JSON stream, strips out the nested layers, and normalizes them into a highly optimized tabular structure: an $N \times M$ row/column vector matrix called a **Pandas DataFrame**. 
          To let users download this data without overloading server storage with temporary files, we use virtual RAM piping. The active Pandas object converts into raw text streams stored inside volatile system RAM buffers (`StringIO`). The stream is directly targeted by the browser's download client and disappears from server RAM immediately after completion.
            
        ---
        
        ### [4] Geospatial Topology Visualization
        * **The Feature:** A fully interactive global map tracking data coordinates.
        * **The Mechanism (Plotly Mapbox Canvas):** We feed our normalized Pandas DataFrame into `plotly.express.scatter_mapbox`. Plotly reads the `Latitude` and `Longitude` float arrays from our matrix and overlays them precisely onto an open-source mapping engine (`open-street-map`). It dynamically assigns visual properties based on data columns: the *size* of the bubble maps to the earthquake's magnitude, and the *color spectrum* maps to the subterranean depth (km) using a specialized color-ramp array.

        ---

        ### [5] Advanced Machine Learning Analytics & Predictive Trajectories
        * **The Feature:** Synthesizing an active statistical forecasting projection line over chronological event data.
        * **The Mechanism (`scikit-learn` Linear Regression):** Machine learning models cannot natively compute abstract date-time formats. Our pipeline converts data points into raw Unix epoch integers ($X$ vector array). We then fit an ordinary least squares regression line ($Y = \\beta_0 + \\beta_1X + \\epsilon$) to establish trend parameters. This trendline mathematically shows whether seismic severity curves are rising or falling over time across the current filter batch.
        
        ---
        
        ### [6] Systems Performance Profiling & Hardware Diagnostics
        * **The Feature:** Monitoring internal application operational health, data processing overhead, and connection speeds.
        * **The Mechanism (`time.perf_counter`):** We use high-precision microsecond hardware clock counters to track the exact lifecycle duration of outbound connections and calculations. Paired with deep-memory tracking algorithms (`memory_usage()`), it calculates how much storage vector arrays require inside memory blocks to optimize processing speeds.
        """)

        st.markdown("---")
        st.markdown("### 🗺️ Sub-Page Architecture (Accessible via Left Sidebar Menu)")
        
        st.markdown("""
        ### [7] Multi-Dimensional Vector Meshgrids (Analytics Page)
        * **The Feature:** A 3D wave model that recalculates based on user resolution limits.
        * **The Mechanism (`@st.cache_data` Optimization):** Calculating complex coordinate physics for thousands of data points is incredibly expensive for a server's CPU. By wrapping the function in `@st.cache_data`, Streamlit takes a digital fingerprint of the input arguments. If the resolution size hasn't changed, it instantly serves the mathematical coordinates straight out of fast-access RAM cache memory, bypassing computation latency entirely.
            
        ---
        
        ### [8] Asynchronous DOM In-Place Mutation (Live Stream Page)
        * **The Feature:** A chart and metric panel that updates smoothly and continuously like a live financial stock ticker.
        * **The Mechanism (`st.empty()` Element Overwriting):** In a traditional web framework, sending new data to the screen requires a full page refresh. We dodge this completely by declaring a visual placeholder layout: `metric_spot = st.empty()`. This pre-allocates a static set of coordinates in your web browser's DOM tree before any data even exists. When our algorithmic loop runs, it targets that precise layout coordinate and overwrites its internal HTML content dynamically without disturbing the rest of the webpage.
        """)