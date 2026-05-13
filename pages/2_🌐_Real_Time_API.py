import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import io
import time

st.set_page_config(page_title="Real-Time API", layout="wide")

if not st.session_state.get("authenticated", False):
    st.error("🔒 Access Denied. Please initialize the session on the Hub landing page.")
    st.stop()

st.title("🌐 Integrated Real-Time API Node")
st.markdown("---")

st.sidebar.header("Global API Filters")
min_magnitude = st.sidebar.slider("Minimum Magnitude", 1.0, 7.0, 4.0, step=0.5, help="[Mechanism #2]: Injects filter arguments into server-side queries.")
limit = st.sidebar.slider("Max Record Limit", 15, 150, 50, step=5, help="[Mechanism #2]: Restricts data packets to optimize network transport scales.")

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

start_time = time.perf_counter()
with st.spinner("Streaming remote payload..."):
    telemetry_df = fetch_geospatial_telemetry(min_magnitude, limit)
end_time = time.perf_counter()
execution_latency = (end_time - start_time) * 1000 

if not telemetry_df.empty:
    metric_col, map_col = st.columns([1, 2])
    with metric_col:
        st.metric("Detected Vectors", len(telemetry_df), help="[Mechanism #3]: Tabular row counts.")
        st.metric("Peak Severity", f"{telemetry_df['Magnitude'].max():.1f} Mag", help="[Mechanism #3]: Max scalar computation.")
        
        st.caption("📋 **[Mechanism #3]: Raw Flattened Matrix Preview**")
        st.dataframe(telemetry_df[["Location", "Magnitude"]].head(5), use_container_width=True)
        
        csv_buffer = io.StringIO()
        telemetry_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📥 Export Clean Dataset (CSV)", data=csv_buffer.getvalue(),
            file_name="normalized_telemetry_stream.csv", mime="text/csv", use_container_width=True,
            help="[Mechanism #3]: Stream coordinates routed to RAM buffer loops, optimizing server footprints."
        )
        
        st.markdown("---")
        st.caption("⚡ **[Mechanism #6]: Live Infrastructure Diagnostics**")
        diag_col1, diag_col2 = st.columns(2)
        diag_col1.metric("API Latency", f"{execution_latency:.1f} ms")
        diag_col2.metric("RAM Allocation", f"{(telemetry_df.memory_usage(deep=True).sum()) / 1024:.2f} KB")
        
    with map_col:
        fig = px.scatter_mapbox(
            telemetry_df, lat="Latitude", lon="Longitude", size="Magnitude", color="Depth (km)",
            color_continuous_scale="Plasma", hover_name="Location", zoom=1, height=380
        )
        fig.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, b=0, t=0))
        st.plotly_chart(fig, use_container_width=True)

# Engineering Notes Section
st.markdown("---")
with st.expander("🛠️ System Engineering Blueprint: Feature Matrix & Core Mechanisms", expanded=True):
    st.markdown("""
    ### [Mechanism #2] Live REST API Integration & Data Pipelines
    * **The Feature:** Dynamically fetching and plotting real-world tectonic anomalies via API handshakes.
    * **The Mechanism:** Outbound connections send explicit filter parameters to the USGS cluster, executing efficient *Server-Side Filtering* before downloading payloads.
    
    ### [Mechanism #3] Structural Matrix Flattening & In-Memory ETL Export Engine
    * **The Feature:** Converting tree-like JSON entries into tabular Pandas grids and serving download streams.
    * **The Mechanism:** Iterates through structural branches, reshaping nested coordinates into a flat layout matrix. Downloads use `io.StringIO` to pipe text chunks through high-speed server RAM rather than touching local solid-state storage arrays.
    
    ### [Mechanism #4] Geospatial Topology Visualization
    * **The Feature:** High-fidelity interactive open-source mapping charts.
    * **The Mechanism:** Plotly reads series arrays from the DataFrame matrix, drawing vector diameters proportional to event size metrics over an Open-Street-Map coordinate layer.
    """)