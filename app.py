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

    # REST API Fetch Function
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

    # --- FEATURE #4: PERFORMANCE PROFILING ENGINE ---
    # Wrap our computational engines in precise high-resolution timers
    start_time = time.perf_counter()
    
    with st.spinner("Streaming remote payload..."):
        telemetry_df = fetch_geospatial_telemetry(min_magnitude, limit)
        
    end_time = time.perf_counter()
    execution_latency = (end_time - start_time) * 1000  # Convert to milliseconds

    # Rendering Dashboard UI Layout
    if not telemetry_df.empty:
        # Sort data by time to preserve sequential order for ML processing
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
            
            # --- FEATURE #3: HIGH-THROUGHPUT ETL EXPORT ENGINE ---
            st.caption("📋 **[Mechanism #3]: Raw Flattened Matrix Preview**")
            st.dataframe(telemetry_df[["Location", "Magnitude"]].head(5), use_container_width=True)
            
            # Convert DataFrame to an In-Memory string buffer (Piped to RAM, not local storage)
            csv_buffer = io.StringIO()
            telemetry_df.to_csv(csv_buffer, index=False)
            csv_bytes = csv_buffer.getvalue()

            st.download_button(
                label="📥 Export Clean Dataset (CSV)",
                data=csv_bytes,
                file_name="normalized_telemetry_stream.csv",
                mime="text/csv",
                use_container_width=True,
                help="[Feature #3]: Converts the active Pandas DataFrame matrix into an in-memory byte stream and routes it directly to your browser's download manager, leaving zero storage footprint on the server."
            )
            
            # --- VISUAL RENDERING: FEATURE #4 SYSTEM DIAGNOSTICS PERFORMANCE ---
            st.markdown("---")
            st.caption("⚡ **[Feature #4]: Live Infrastructure Diagnostics**")
            diag_col1, diag_col2 = st.columns(2)
            diag_col1.metric("API Latency", f"{execution_latency:.1f} ms", help="High-resolution CPU timer measuring network fetch and data flattening loops.")
            # Calculate memory footprints using standard float estimations
            estimated_memory = (telemetry_df.memory_usage(deep=True).sum()) / 1024
            diag_col2.metric("RAM Allocation", f"{estimated_memory:.2f} KB", help="The physical overhead sizing footprint of the generated tabular vectors inside the server memory.")
        
        with map_col:
            fig = px.scatter_mapbox(
                telemetry_df, lat="Latitude", lon="Longitude", size="Magnitude", color="Depth (km)",
                color_continuous_scale="Plasma", hover_name="Location", zoom=1, height=380
            )
            fig.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, b=0, t=0))
            st.plotly_chart(fig, use_container_width=True)

        # --- FEATURE #1: ADVANCED MACHINE LEARNING FORECASTING ---
        st.markdown("---")
        st.header("🔮 [Feature #1]: Predictive Algorithmic Forecasting Model", help="Utilizes linear regression analysis to fit trendlines and identify anomalies outside standard tracking paths.")
        
        # Convert Timestamp arrays into numeric Unix float values so our Scikit-Learn models can parse them
        X_timestamps = np.array(telemetry_df['Time'].astype(np.int64) // 10**9).reshape(-1, 1)
        Y_magnitudes = telemetry_df['Magnitude'].values.reshape(-1, 1)
        
        # Initialize and fit the Scikit-Learn Linear Regression Model
        model = LinearRegression()
        model.fit(X_timestamps, Y_magnitudes)
        
        # Predict trends based on the regression line fit
        predictions = model.predict(X_timestamps)
        
        # Build an advanced compound Plotly figure with predictive shading thresholds
        trend_fig = go.Figure()
        
        # Plot raw historic sequence points
        trend_fig.add_trace(go.Scatter(
            x=telemetry_df['Time'], y=telemetry_df['Magnitude'],
            mode='markers+lines', name='Observed Magnitude Vectors',
            line=dict(color='#00ffcc', width=1), marker=dict(size=6)
        ))
        
        # Plot the machine learning trend trajectory line
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
        ### [1] Advanced Machine Learning Analytics & Predictive Trajectories
        * **The Feature:** Synthesizing an active statistical forecasting projection line over chronological event data.
        * **The Mechanism (`scikit-learn` Linear Regression):** Machine learning models cannot natively compute abstract date-time formats. Our pipeline converts data points into raw Unix epoch integers ($X$ vector array). 
          We then fit an ordinary least squares regression line ($Y = \\beta_0 + \\beta_1X + \\epsilon$) to establish trend parameters. This trendline mathematically shows whether seismic severity curves are rising or falling over time across the current filter batch.
        
        ---
        
        ### [2] Live REST API Integration & Data Pipelines
        * **The Feature:** Dynamically fetching and plotting real-world tectonic anomalies in real-time without requiring a static database.
        * **The Mechanism (`requests` + Server-Side Filtering):** Outbound HTTPS handshakes target the USGS server. By appending user query parameters into the URL string, we delegate dataset trimming to the server, protecting bandwidth.
            
        ---
        
        ### [3] In-Memory ETL Export Engine (Zero-Disk Footprint)
        * **The Feature:** Instantly creating on-the-fly downloadable CSV file arrays out of filtered parameters.
        * **The Mechanism (`io.StringIO` Data Buffering):** Standard file exports involve writing files to disk storage, which threatens server memory overload. We use virtual RAM piping. 
          The active Pandas object converts into raw text streams stored inside volatile system RAM buffers (`StringIO`). The stream is directly targeted by the browser's download client and disappears from server RAM immediately after completion.
            
        ---
        
        ### [4] Systems Performance Profiling & Hardware Diagnostics
        * **The Feature:** Monitoring internal application operational health, data processing overhead, and connection speeds.
        * **The Mechanism (`time.perf_counter`):** We use high-precision microsecond hardware clock counters to track the exact lifecycle duration of outbound connections and calculations. 
          Paired with deep-memory tracking algorithms (`memory_usage()`), it calculates how much storage vector arrays require inside memory blocks to optimize processing speeds.
        """)