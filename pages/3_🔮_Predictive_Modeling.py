import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Predictive Modeling", layout="wide")

if not st.session_state.get("authenticated", False):
    st.error("🔒 Access Denied. Please initialize the session on the Hub landing page.")
    st.stop()

st.title("🔮 Predictive Algorithmic Forecasting Model")
st.markdown("---")

# Pull baseline reference data from the API
def fetch_ml_data():
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minmagnitude=3.0&limit=80"
    try:
        response = requests.get(url, timeout=10)
        raw_json = response.json()
        features = raw_json.get("features", [])
        cleaned = []
        for item in features:
            props = item.get("properties", {})
            cleaned.append({
                "Magnitude": props.get("mag", 0.0),
                "Time": pd.to_datetime(props.get("time", 0), unit='ms')
            })
        return pd.DataFrame(cleaned).sort_values(by="Time").reset_index(drop=True)
    except:
        return pd.DataFrame()

with st.spinner("Processing time-series vectors..."):
    ml_df = fetch_ml_data()

if not ml_df.empty:
    st.header("Linear Regression Model Trajectory Mapping", help="[Mechanism #5]: Fits trendlines straight over dynamic series.")
    
    X_timestamps = np.array(ml_df['Time'].astype(np.int64) // 10**9).reshape(-1, 1)
    Y_magnitudes = ml_df['Magnitude'].values.reshape(-1, 1)
    
    model = LinearRegression()
    model.fit(X_timestamps, Y_magnitudes)
    predictions = model.predict(X_timestamps)
    
    trend_fig = go.Figure()
    trend_fig.add_trace(go.Scatter(
        x=ml_df['Time'], y=ml_df['Magnitude'],
        mode='markers+lines', name='Observed Magnitude Vectors',
        line=dict(color='#00ffcc', width=1), marker=dict(size=6)
    ))
    trend_fig.add_trace(go.Scatter(
        x=ml_df['Time'], y=predictions.flatten(),
        mode='lines', name='Linear Regression Model Trendline',
        line=dict(color='#ff0055', width=2, dash='dash')
    ))
    trend_fig.update_layout(
        template="plotly_dark", height=400, margin=dict(l=40, r=40, b=20, t=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(trend_fig, use_container_width=True)

# Engineering Notes Section
st.markdown("---")
with st.expander("🛠️ System Engineering Blueprint: Feature Matrix & Core Mechanisms", expanded=True):
    st.markdown("""
    ### [Mechanism #5] Advanced Machine Learning Analytics & Predictive Trajectories
    * **The Feature:** Mathematical trend projection generated across chronologically sorted event datasets.
    * **The Mechanism:** Scikit-Learn structures cannot parse complex timestamp dates natively. The data pipeline transforms dates into numeric Unix epoch dimensions ($X$ float vector array). An ordinary least squares linear regression model is compiled ($Y = \\beta_0 + \\beta_1X + \\epsilon$) to construct continuous trend metrics.
    """)