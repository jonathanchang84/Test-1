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
                "Location": props.get("place", "Unknown Axis"),
                "Magnitude": props.get("mag", 0.0),
                "Time": pd.to_datetime(props.get("time", 0), unit='ms')
            })
        return pd.DataFrame(cleaned).sort_values(by="Time").reset_index(drop=True)
    except:
        return pd.DataFrame()

with st.spinner("Processing time-series vectors..."):
    ml_df = fetch_ml_data()

if not ml_df.empty:
    
    # --- UPPER ROW: SUMMARY METRICS & CHRONOLOGICAL CHART ---
    metric_col1, metric_col2, _ = st.columns([1, 1, 2])
    with metric_col1:
        st.metric("Training Sample Size (N)", len(ml_df))
    with metric_col2:
        st.metric("Mean Vector Magnitude", f"{ml_df['Magnitude'].mean():.2f} Mag")
        
    st.subheader("Linear Regression Model Trajectory Mapping", help="[Mechanism #5]: Fits trendlines straight over dynamic series arrays.")
    
    # Convert Timestamp arrays into numeric Unix float values for Scikit-Learn
    X_timestamps = np.array(ml_df['Time'].astype(np.int64) // 10**9).reshape(-1, 1)
    Y_magnitudes = ml_df['Magnitude'].values.reshape(-1, 1)
    
    # Train model and generate predictions
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

    st.markdown("---")

    # --- LOWER ROW: FULL-WIDTH ROW ENTRY MATRIX ---
    st.subheader("Model Input Matrix", help="[Mechanism #5]: This is the clean structural tabular vector dataset feeding directly into the Scikit-Learn training layer.")
    st.caption("📋 **[Mechanism #5]: Model Training Inputs (Chronological Order)**")
    st.dataframe(
        ml_df[["Time", "Location", "Magnitude"]],
        use_container_width=True,
        height=300
    )

# ==========================================
# EDUCATIONAL CORE & ENGINEERING DOCUMENTATION
# ==========================================
st.markdown("---")
edu_tabs = st.tabs(["📊 Linear Regression Mechanics Explained", "🛠️ System Engineering Blueprint"])

with edu_tabs[0]:
    st.subheader("Understanding the Trend Estimation Engine on this Page")
    st.markdown("""
    Because there are no deep neural networks or complex AI models visible on this workspace, the machine learning occurring here is purely mathematical, silent, and foundational. This node utilizes **Supervised Machine Learning**, specifically an optimization algorithm known as **Linear Regression**.

    #### 1. The Core Objective: Pattern Synthesis
    The system asks a fundamental predictive question: *Based on the chronological timeline of recent seismic events, is the overall data trajectory trending upward, trending downward, or remaining perfectly stable?*
    To answer this, the system cannot guess by simply inspecting the chart dots. It must mathematically establish a unified line of best fit.

    #### 2. The Step-by-Step Data Pipeline
    * **Feature Engineering:** Machine learning models cannot parse human date formats. The script transforms the **Time** column into raw Unix Epoch floats (total seconds elapsed since 1970). This yields our computational **Feature Matrix ($X$)**, while **Magnitude** serves as our **Target Vector ($Y$)**.
    * **Model Instantiation:** The application initializes a blank mathematical container using Python's `scikit-learn` ecosystem: `model = LinearRegression()`.
    * **Model Training (`.fit()`):** When executing `model.fit(X, Y)`, the algorithm parses every single row inside the data table below. It utilizes a routine called **Ordinary Least Squares (OLS)**, adjusting a linear trajectory until it minimizes the squared distances between the trendline and every historical scatter point.
    * **Statistical Prediction (`.predict()`):** The trained model outputs a mathematical formula in memory:
    """)
    
    st.latex(r"Y = \beta_0 + \beta_1X")
    
    st.markdown("""
    The script passes the time array back through this solved formula, calculating the precise coordinates needed to draw the dashed **red Trendline** overlaid on your canvas.

    #### Why is this "Learning"?
    The slope parameters ($\beta_1$) are never hardcoded. If you query data from a peaceful region, the AI dynamically "learns" a negative slope. If volatility spikes globally, the algorithm shifts its weights and computes a positive slope. The data table acts as the **Teacher**, the Scikit-Learn compiler is the **Student**, and the dashed **red trendline** is the **Solution**!
    """)

with edu_tabs[1]:
    st.markdown("""
    ### [Mechanism #5] Advanced Machine Learning Analytics & Predictive Trajectories
    * **The Feature:** A chronological data grid cross-referenced against a synchronized mathematical trend projection line.
    * **The Data Matrix:** Positioned directly beneath the mathematical canvas, the full-width `st.dataframe()` displays the clean, sorted input parameters ($X$ and $Y$ training variables). This stacked layout permits high-density, horizontal scannability of structural features like extended text-based locations and timestamps.
    * **The Mechanism:** Scikit-Learn structures cannot parse complex timestamp dates natively. The data pipeline transforms the calendar dates from our data table into raw numeric Unix epoch dimensions ($X$ float vector array). An ordinary least squares linear regression model is compiled ($Y = \\beta_0 + \\beta_1X + \\epsilon$) to construct continuous trend metrics, which are overlaid onto the data canvas as a dashed **red trajectory vector**.
    """)