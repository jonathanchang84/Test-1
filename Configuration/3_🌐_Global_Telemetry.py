import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Global Telemetry", layout="wide")

# Session lock verification
if not st.session_state.get("authenticated", False):
    st.error("🔒 Access Denied. Please initialize the session on the Home page.")
    st.stop()

st.title("🌐 Live Global Telemetry Node")
st.subheader("REST API Integration & Geospatial Normalization")

# Sidebar Configuration for API Queries
st.sidebar.header("API Filter Matrix")
min_magnitude = st.sidebar.slider("Minimum Magnitude Threshold", 1.0, 7.0, 4.5, step=0.5)
limit = st.sidebar.slider("Max Record Ingestion Limit", 10, 200, 50, step=10)

# Complex Idea: API Fetching function with robust error handling and structural cleaning
def fetch_geospatial_telemetry(min_mag, max_rows):
    # Public REST API Endpoint (No Key Required)
    url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minmagnitude={min_mag}&limit={max_rows}"
    
    try:
        response = requests.get(url, timeout=10)
        # Check if the server returned an error code (e.g., 404, 500)
        response.raise_for_status() 
        raw_json = response.json()
        
        # Complex Idea: JSON Flattening/Normalization
        # Extracting nested lists from GeoJSON structure into a tabular format
        features = raw_json.get("features", [])
        
        cleaned_records = []
        for item in features:
            props = item.get("properties", {})
            geom = item.get("geometry", {})
            coords = geom.get("coordinates", [0, 0, 0]) # [longitude, latitude, depth]
            
            cleaned_records.append({
                "Location": props.get("place", "Unknown Axis"),
                "Magnitude": props.get("mag", 0.0),
                "Time": pd.to_datetime(props.get("time", 0), unit='ms'),
                "Longitude": coords[0],
                "Latitude": coords[1],
                "Depth (km)": coords[2]
            })
            
        return pd.DataFrame(cleaned_records)
        
    except requests.exceptions.RequestException as e:
        # Graceful failure state handling
        st.error(f"🔴 Telemetry Fetch Fault: Unable to resolve external API stream. Error: {e}")
        return pd.DataFrame()

# Execute Network Fetch
with st.spinner("Connecting to global telemetry stream..."):
    telemetry_df = fetch_geospatial_telemetry(min_magnitude, limit)

# Main UI View Logic based on data existence
if not telemetry_df.empty:
    
    # Structural Layout Splitting
    metrics_col, map_col = st.columns([1, 2])
    
    with metrics_col:
        st.markdown("### 📊 Ingested Vector Metrics")
        st.metric("Active Anomalies Detected", len(telemetry_df))
        st.metric("Peak Severity (Mag)", f"{telemetry_df['Magnitude'].max():.1f}")
        st.metric("Mean Crustal Depth", f"{telemetry_df['Depth (km)'].mean():.2f} km")
        
        st.markdown("---")
        st.markdown("##### Raw Normalized Payload Preview")
        st.dataframe(telemetry_df[["Location", "Magnitude", "Time"]].head(8), use_container_width=True)

    with map_col:
        st.markdown("### 🗺️ Live Geospatial Topology")
        
        # Build interactive geospatial scatter plot using Plotly
        fig = px.scatter_mapbox(
            telemetry_df, 
            lat="Latitude", 
            lon="Longitude", 
            size="Magnitude", 
            color="Depth (km)",
            color_continuous_scale="Viridis",
            hover_name="Location",
            zoom=1, 
            height=500,
            title="Real-Time Global Tectonic Activity Mapping"
        )
        # Using a clean open-source map style
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=40))
        
        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("⚠️ No active anomalies found matching current filter matrix criteria.")

# --- COMPREHENSIVE ARCHITECTURAL BLUEPRINT ---
st.markdown("---")
with st.expander("🛠️ Architectural Blueprint: External API Pipelines & Data Normalization"):
    st.markdown("""
    ### How External Data Streams Work
    When a web application consumes modern REST APIs, it acts as a client sending commands across HTTP/HTTPS networks to process remote instructions.
    """)
    
    # Visualizing how data moves from server to dataframe
    st.markdown("""
    ```text
    [ USGS Remote Server ] 
         │ (Sends Raw Nested GeoJSON Payload)
         ▼
    [ Python 'requests' Engine ] 
         │ (Parses payload, extracts 'properties' and 'geometry')
         ▼
    [ Pandas DataFrame Object ] 
         │ (Normalizes dictionary entries into tabular row/column vector matrix)
         ▼
    [ Plotly Mapbox Canvas ] -> Renders visual clusters in your browser DOM
    ```
    """)
    
    st.markdown("""
    ### Deep Dive into the Complex Engineering Mechanics
    1. **The Network Request Lifecycle:** Using `requests.get()`, our app hits a live endpoint. We pass query parameters (`minmagnitude` and `limit`) directly into the URL string. This is called *Server-Side Filtering*, which reduces internet bandwidth consumption by making the remote server trim down the dataset before sending it back.
    2. **Fault Tolerance & Defending the Main Thread:** Public APIs can suffer outages, latency spikes, or network drops. If our code didn't wrap this call in a `try/except` block with a defined `timeout=10`, a slow API could hang indefinitely, completely crashing our web server's browser thread.
    3. **GeoJSON Matrix Normalization:** Standard public APIs pass data in a **GeoJSON** format, which looks like highly nested structures:
       ```json
       "geometry": { "coordinates": [-118.4, 34.05, 12.4] }
       ```
       Browsers and mapping software cannot naturally read this flatly. The loop inside our custom function acts as a **Data Transformer**, programmatically extracting individual coordinates and structuring them straight into a clean, queryable column grid inside a memory-optimized Pandas DataFrame.
    """)