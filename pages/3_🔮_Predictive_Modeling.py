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
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minmagnitude=3.0&limit=80&orderby=time-asc"
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
        return pd.DataFrame(cleaned)
    except:
        return pd.DataFrame()

with st.spinner("Processing time-series vectors..."):
    ml_df = fetch_ml_data()

if not ml_df.empty:
    
    # 1. Clean data and force strict sequence indexing
    ml_df = ml_df.sort_values(by="Time").reset_index(drop=True)
    
    # Create a human-friendly "Event Number" column starting at 1 instead of 0
    ml_df["Event Number"] = ml_df.index + 1
    
    # --- UPPER ROW: SUMMARY METRICS & CHRONOLOGICAL CHART ---
    metric_col1, metric_col2, _ = st.columns([1, 1, 2])
    with metric_col1:
        st.metric("Training Sample Size (N)", len(ml_df))
    with metric_col2:
        st.metric("Mean Vector Magnitude", f"{ml_df['Magnitude'].mean():.2f} Mag")
        
    st.subheader("Linear Regression Model Trajectory Mapping", help="[Mechanism #5]: Fits trendlines straight over dynamic series arrays.")
    
    # 2. MACHINE LEARNING ENGINE MATRICES
    X_train = ml_df["Event Number"].values.reshape(-1, 1)
    Y_train = ml_df['Magnitude'].values.reshape(-1, 1)
    
    # Train the model
    model = LinearRegression()
    model.fit(X_train, Y_train)
    
    # 3. GENERATE THE FUTURE STEPS
    # Graph out all historical events and project cleanly out to 20 imaginary future events
    historical_count = len(ml_df)
    forecast_extension = 20
    total_horizon_steps = historical_count + forecast_extension
    
    # Create an array representing [1, 2, 3 ... 80, 81 ... 100]
    forecast_axis = np.arange(1, total_horizon_steps + 1).reshape(-1, 1)
    
    # Predict values for the entire line
    predictions = model.predict(forecast_axis)
    
    # 4. PLOT VISUALIZATION CANVAS
    trend_fig = go.Figure()
    
    # Historical Observed Points (X-axis is now the clean integer sequence)
    trend_fig.add_trace(go.Scatter(
        x=ml_df["Event Number"], 
        y=ml_df['Magnitude'],
        mode='markers+lines', 
        name='Observed Magnitude Vectors',
        hovertext=ml_df['Location'] + "<br>" + ml_df['Time'].dt.strftime('%Y-%m-%d %H:%M'),
        line=dict(color='#00ffcc', width=1), 
        marker=dict(size=6)
    ))
    
    # Extended Red Predictive Trendline (Cuts right through history and pushes into the future horizon)
    trend_fig.add_trace(go.Scatter(
        x=forecast_axis.flatten(), 
        y=predictions.flatten(),
        mode='lines', 
        name='Predictive Forecasting Trendline',
        line=dict(color='#ff0055', width=2, dash='dash')
    ))
    
    trend_fig.update_layout(
        template="plotly_dark", 
        height=400, 
        margin=dict(l=40, r=40, b=20, t=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(
            title="Chronological Event Sequence (Historical Tracking ➡️ Future Forecast Window)",
            dtick=10  # Put a marker every 10 events to keep it scannable
        ),
        yaxis=dict(title="Magnitude")
    )
    st.plotly_chart(trend_fig, use_container_width=True)

    st.markdown("---")

    # --- LOWER ROW: FULL-WIDTH ROW ENTRY MATRIX ---
    st.subheader("Model Input Matrix", help="[Mechanism #5]: This is the clean structural tabular vector dataset feeding directly into the Scikit-Learn training layer.")
    st.caption("📋 **[Mechanism #5]: Model Training Inputs (Chronological Order)**")
    st.dataframe(
        ml_df[["Event Number", "Time", "Location", "Magnitude"]],
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

    #### 1. The Core Objective: Trend Extrapolation
    The system asks a fundamental predictive question: *Based on the chronological timeline of recent seismic events, what is the mathematical trajectory of upcoming events?*
    To completely eliminate layout distortions and date-parsing crashes, the canvas maps data against sequential **Event Numbers ($1, 2, 3...$)** rather than volatile datetime intervals. 

    #### 2. The Step-by-Step Data Pipeline
    * **Feature Engineering:** The script maps time strictly to an ordered ordinal sequence integer **Feature Matrix ($X$)**, while **Magnitude** serves as our **Target Vector ($Y$)**. 
    * **Model Instantiation:** The application initializes a blank mathematical container using Python's `scikit-learn` ecosystem: `model = LinearRegression()`.
    * **Model Training (`.fit()`):** When executing `model.fit(X, Y)`, the algorithm parses every single row inside the data table below, adjusting a linear trajectory until it minimizes the squared distances between the trendline and every historical scatter point.
    * **Statistical Forecasting Horizon (`.predict()`):** The trained model leverages its mathematical formula in memory ($Y = \\beta_0 + \\beta_1X$). The code generates an expanded array matrix stretching past your historical metrics (e.g., out to Event 100), calculates predictions for those future spaces, and plots them as the dashed **red Trendline** breaking out past your last data point.
    """)

with edu_tabs[1]:
    st.markdown("""
    ### [Mechanism #5] Advanced Machine Learning Analytics & Predictive Trajectories
    * **The Feature:** A chronological data grid cross-referenced against an extrapolated mathematical forecasting serialization line.
    * **The Extrapolation:** Positioned inside the mathematical canvas, the dashed **red trajectory vector** leverages calculated historical slopes to compute future estimations, plotting data projections safely past the newest index row entry.
    * **The Mechanism:** Scikit-Learn structures cannot parse complex timestamp dates natively. The data pipeline indexes the tabular entries into clean sequence integers ($X$ vector array). An ordinary least squares linear regression model is compiled ($Y = \\beta_0 + \\beta_1X + \\epsilon$) to construct continuous trend metrics, which are evaluated over an expanded future sequence array and rendered on-screen.
    """)