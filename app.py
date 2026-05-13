import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Quantum Analytics Hub",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Page Header
st.title("🔮 Quantum Analytics Hub")
st.markdown("---")

# 3. Sidebar Filters for the API
st.sidebar.header("Global API Filter Matrix")
min_magnitude = st.sidebar.slider("Minimum Magnitude", 1.0, 7.0, 4.5, step=0.5)
limit = st.sidebar.slider("Max Record Limit", 10, 200, 50, step=10)

# 4. API Ingestion Engine
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

# Execute Fetch on Homepage
with st.spinner("Connecting to global telemetry stream..."):
    telemetry_df = fetch_geospatial_telemetry(min_magnitude, limit)

# 5. Render Layout on Homepage
if not telemetry_df.empty:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("System Metrics")
        st.metric("Active Anomalies", len(telemetry_df))
        st.metric("Peak Severity (Mag)", f"{telemetry_df['Magnitude'].max():.1f}")
        st.metric("Mean Crustal Depth", f"{telemetry_df['Depth (km)'].mean():.2f} km")
        st.dataframe(telemetry_df[["Location", "Magnitude"]].head(5), use_container_width=True)
    
    with col2:
        st.header("Live Geospatial Topology")
        fig = px.scatter_mapbox(
            telemetry_df, lat="Latitude", lon="Longitude", size="Magnitude", color="Depth (km)",
            color_continuous_scale="Viridis", hover_name="Location", zoom=1, height=400
        )
        fig.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, b=0, t=0))
        st.plotly_chart(fig, use_container_width=True)

# 6. Architectural Commentary at the bottom
st.markdown("---")
with st.expander("🛠️ Home Node Blueprint: Real-Time Data Ingestion"):
    st.markdown("""
    ### What is happening here?
    This main landing page (`app.py`) is now initiating a live HTTP REST API handshake directly with the USGS seismic databases upon every browser refresh. 
    It streams raw JSON packets over the internet, flattens the nested structures into tables using Pandas, and renders a live geographic map layout directly onto your home screen.
    """)