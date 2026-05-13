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
    
    # Force chronological alignment and reset indices to sequential integers (0, 1, 2...)
    ml_df = ml_df.sort_values(by="Time").reset_index(drop=True)
    
    # --- UPPER ROW: SUMMARY METRICS & CHRONOLOGICAL CHART ---
    metric_col1, metric_col2, _ = st.columns([1, 1, 2])
    with metric_col1:
        st.metric("Training Sample Size (N)", len(ml_df))
    with metric_col2:
        st.metric("Mean Vector Magnitude", f"{ml_df['Magnitude'].mean():.2f} Mag")
        
    st.subheader("Linear Regression Model Trajectory Mapping", help="[Mechanism #5]: Fits trendlines straight over dynamic series arrays.")
    
    # 1. FEATURES AND TARGETS: Use sequential index integers instead of raw timestamp numbers
    # This guarantees no weird scaling loops or hidden millisecond cluster bugs.
    X_indices = ml_df.index.values.reshape(-1, 1)
    Y_magnitudes = ml_df['Magnitude'].values.reshape(-1, 1)
    
    # 2. Train the model on row sequence
    model = LinearRegression()
    model.fit(X_indices, Y_magnitudes)
    
    # 3. GENERATE FORECAST WINDOW PAST THE FINAL ROW ENTRY
    # We create a trajectory line that traces all historical rows and projects forward out to an imaginary 20 extra rows
    historical_count = len(ml_df)
    forecast_extension = 20
    
    total_steps = historical_count + forecast_extension
    forecast_indices = np.arange(total_steps).reshape(-1, 1)
    
    # Generate predictive output values across the expanded index line
    extended_predictions = model.predict(forecast_indices)
    
    # To prevent Plotly from breaking the horizontal layout, we generate placeholder dates for the future entries
    # by adding artificial time steps onto the latest known date
    last_known_date = ml_df['Time'].max()
    time_delta = ml_df['Time'].diff().mean()  # average spacing between current events
    if pd.isna(time_delta):
        time_delta = pd.Timedelta(hours=1) # fallback if delta is zero
        
    future_dates = [last_known_date + (i * time_delta) for i in range(1, forecast_extension + 1)]
    extended_timeline_dates = list(ml_df['Time']) + future_dates

    # 4. PLOT VISUALIZATION CANVAS
    trend_fig = go.Figure()
    
    # Historical Observed Points (Guaranteed to fill the screen since dates are naturally aligned)
    trend_fig.add_trace(go.Scatter(
        x=ml_df['Time'], y=ml_df['Magnitude'],
        mode='markers+lines', name='Observed Magnitude Vectors',
        line=dict(color='#00ffcc', width=1), marker=dict(size=6)
    ))
    
    # Extended Red Predictive Trendline (Stretches smoothly through history and past the edge)
    trend_fig.add_trace(go.Scatter(
        x=extended_timeline_dates, y=extended_predictions.flatten(),
        mode='lines', name='Predictive Forecasting Trendline',
        line=dict(color='#ff0055', width=2, dash='dash')
    ))
    
    trend_fig.update_layout(
        template="plotly_dark", height=400, margin=dict(l=40, r=40, b=20, t=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(title="Timeline Sequence (Historical Feed into Forecast Margin)"),
        yaxis=dict(title="Magnitude")
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

    #### 1. The Core Objective: Trend Extrapolation
    The system asks a fundamental predictive question: *Based on the chronological timeline of recent seismic events, what is the mathematical trajectory of upcoming events?*
    To answer this, the system trains on your historical table data, maps the calculated slope, and then extends that slope line forward beyond your latest data parameters into empty future time coordinates without compromising chart aspect ratios.

    #### 2. The Step-by-Step Data Pipeline
    * **Feature Engineering:** Machine learning models cannot parse human date formats. The script transforms the chronological index positions into a continuous integer **Feature Matrix ($X$)**, while **Magnitude** serves as our **Target Vector ($Y$)**. This removes erratic scaling bugs entirely.
    * **Model Instantiation:** The application initializes a blank mathematical container using Python's `scikit-learn` ecosystem: `model = LinearRegression()`.
    * **Model Training (`.fit()`):** When executing `model.fit(X, Y)`, the algorithm parses every single row inside the data table below, adjusting a linear trajectory until it minimizes the squared distances between the trendline and every historical scatter point.
    * **Statistical Forecasting Horizon (`.predict()`):** The trained model leverages its mathematical formula in memory ($Y = \\beta_0 + \\beta_1X$). The code generates an expanded array index stretching past your historical metrics, calculates predictions for those future spaces, and plots them as the dashed **red Trendline** breaking out past your last data point.
    """)

with edu_tabs[1]:
    st.markdown("""
    ### [Mechanism #5] Advanced Machine Learning Analytics & Predictive Trajectories
    * **The Feature:** A chronological data grid cross-referenced against an extrapolated mathematical forecasting projection line.
    * **The Extrapolation:** Positioned inside the mathematical canvas, the dashed **red trajectory vector** leverages calculated historical slopes to compute future estimations, plotting data projections safely past the newest row entry.
    * **The Mechanism:** Scikit-Learn structures cannot parse complex timestamp dates natively. The data pipeline indexes the tabular entries into clean sequence numbers ($X$ integer array). An ordinary least squares linear regression model is compiled ($Y = \\beta_0 + \\beta_1X + \\epsilon$) to construct continuous trend metrics, which are evaluated over an expanded future sequence array and rendered on-screen.
    """)