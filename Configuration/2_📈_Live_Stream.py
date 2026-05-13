import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="Live Stream", layout="wide")

if not st.session_state.get("authenticated", False):
    st.error("🔒 Access Denied. Please initialize the session on the Home page.")
    st.stop()

st.title("📈 Real-Time Algorithmic Feed")
st.subheader("Asynchronous Metric Streaming Simulation")

# Layout placeholders for streaming data
metric_spot = st.empty()
chart_spot = st.empty()

# Complex Idea: Streamlit Dynamic Placeholders inside a loop
# This simulates listening to a live WebSocket or Kafka broker
stream_data = pd.DataFrame(columns=["Timestamp", "Volatility Metric"])

if st.button("Start Live Ingestion Feed"):
    stop_feed = st.button("Halt Ingestion Feed")
    
    for i in range(100):
        if stop_feed:
            st.warning("Feed halted by user.")
            break
            
        # Generate complex random walk data
        new_row = pd.DataFrame({
            "Timestamp": [pd.Timestamp.now()],
            "Volatility Metric": [np.random.normal(0, 1) + (i * 0.05)]
        })
        
        stream_data = pd.concat([stream_data, new_row], ignore_index=True)
        
        # Update metric snapshot dynamically
        with metric_spot.container():
            col1, col2 = st.columns(2)
            col1.metric("Current Delta", f"{new_row['Volatility Metric'][0]:.4f}")
            col2.metric("Cumulative Variance", f"{stream_data['Volatility Metric'].std():.4f}")
            
        # Update live chart smoothly
        with chart_spot.container():
            st.line_chart(stream_data.set_index("Timestamp"))
            
        time.sleep(0.3) # Simulating network latency