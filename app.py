import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# 1. Global Page Configuration
st.set_page_config(
    page_title="Quantum Analytics Hub",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Global Session State Management (From our first step!)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

st.title("🔮 Quantum Analytics Hub")
st.markdown("---")

# 3. Security Gateway Interface
if not st.session_state.authenticated:
    st.subheader("Secure Gateway Connection Required")
    st.info("💡 **System Note:** The multi-page cluster is currently state-locked. Initialize the session token below to unlock full telemetry.")
    if st.button("Initialize Master Session", type="primary"):
        st.session_state.authenticated = True
        st.rerun()
        
else:
    # Sidebar session control
    st.sidebar.success("🔑 Global Session Active")
    if st.sidebar.button("Terminate Session Matrix"):
        st.session_state.authenticated = False
        st.rerun()

    # --- RESTORING WORKOR_1: Original Welcome Dashboard ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Core Cluster Operations")
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

    # --- RESTORING WORK_2: Live API Telemetry Map ---
    st.header("🌐 Integrated Real-Time API Node")
    
    st.sidebar.markdown("---")
    st.sidebar.header("Global API Filters")
    min_magnitude = st.sidebar.slider("Minimum Magnitude", 1.0, 7.0, 4.5, step=0.5)
    limit = st.sidebar.slider("Max Record Limit", 10, 100, 40, step=10)

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

    if not telemetry_df.empty:
        metric_col, map_col = st.columns([1, 2])
        
        with metric_col:
            st.metric("Detected Vectors", len(telemetry_df))
            st.metric("Peak Severity", f"{telemetry_df['Magnitude'].max():.1f} Mag")
            st.dataframe(telemetry_df[["Location", "Magnitude"]].head(6), use_container_width=True)
        
        with map_col:
            fig = px.scatter_mapbox(
                telemetry_df, lat="Latitude", lon="Longitude", size="Magnitude", color="Depth (km)",
                color_continuous_scale="Plasma", hover_name="Location", zoom=1, height=350
            )
            fig.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, b=0, t=0))
            st.plotly_chart(fig, use_container_width=True)