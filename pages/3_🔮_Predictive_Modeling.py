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
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        raw_json = response.json()
        features = raw_json.get("features", [])
        
        if not features:
            st.warning("⚠️ API Connection successful, but the USGS database returned zero events.")
            return pd.DataFrame()
            
        cleaned = []
        for item in features:
            props = item.get("properties", {})
            cleaned.append({
                "Location": props.get("place", "Unknown Axis"),
                "Magnitude": props.get("mag", 0.0),
                "Time": pd.to_datetime(props.get("time", 0), unit='ms')
            })
        return pd.DataFrame(cleaned)
    except Exception as e:
        st.error(f"🔴 Critical Script Intercept: {e}")
        return pd.DataFrame()

with st.spinner("Processing time-series vectors..."):
    ml_df = fetch_ml_data()

if not ml_df.empty:
    ml_df = ml_df.sort_values(by="Time").reset_index(drop=True)
    ml_df["Event Number"] = ml_df.index + 1
    
    # --- CALCULATE STATISTICAL DESCRIPTORS ---
    sample_size = len(ml_df)
    mean_mag = ml_df['Magnitude'].mean()
    median_mag = ml_df['Magnitude'].median()
    std_mag = ml_df['Magnitude'].std()
    variance_mag = ml_df['Magnitude'].var()
    
    # --- METRIC RIBBON ---
    metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)
    with metric_col1: st.metric("Training Sample Size (N)", sample_size)
    with metric_col2: st.metric("Mean Magnitude (Average)", f"{mean_mag:.2f} Mag")
    with metric_col3: st.metric("Median Magnitude (Middle)", f"{median_mag:.2f} Mag")
    with metric_col4: st.metric("Standard Deviation (σ)", f"±{std_mag:.2f} Mag")
    with metric_col5: st.metric("Statistical Variance (σ²)", f"{variance_mag:.4f}")
        
    st.subheader("Linear Regression Model Trajectory Mapping", help="[Mechanism #5]: Fits trendlines straight over dynamic series arrays.")
    
    # --- MACHINE LEARNING ENGINE ---
    X_train = ml_df["Event Number"].values.reshape(-1, 1)
    Y_train = ml_df['Magnitude'].values.reshape(-1, 1)
    
    model = LinearRegression()
    model.fit(X_train, Y_train)
    
    # Extract Equation parameters
    m_slope = model.coef_[0][0]
    b_intercept = model.intercept_[0]
    equation_text = f"y = {m_slope:.4f}x + {b_intercept:.2f}"

    # Visual Equation Display immediately above chart
    st.latex(equation_text)
    
    # --- FORECAST GENERATION ---
    forecast_extension = 20
    forecast_axis = np.arange(1, len(ml_df) + forecast_extension + 1).reshape(-1, 1)
    predictions = model.predict(forecast_axis)
    
    # --- PLOT VISUALIZATION CANVAS ---
    trend_fig = go.Figure()
    
    trend_fig.add_trace(go.Scatter(
        x=ml_df["Event Number"], 
        y=ml_df['Magnitude'],
        mode='markers+lines', 
        name='Observed Magnitude Vectors',
        hovertext=ml_df['Location'] + "<br>" + ml_df['Time'].dt.strftime('%Y-%m-%d %H:%M'),
        line=dict(color='#00ffcc', width=1), 
        marker=dict(size=6)
    ))
    
    trend_fig.add_trace(go.Scatter(
        x=forecast_axis.flatten(), 
        y=predictions.flatten(),
        mode='lines', 
        name=f'Predictive Trendline ({equation_text})',
        line=dict(color='#ff0055', width=2, dash='dash')
    ))
    
    trend_fig.update_layout(
        template="plotly_dark", height=400, 
        margin=dict(l=40, r=40, b=20, t=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(title="Chronological Event Sequence (Historical Tracking ➡️ Future Forecast Window)", dtick=10),
        yaxis=dict(title="Magnitude")
    )
    st.plotly_chart(trend_fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Model Input Matrix", help="[Mechanism #5]: Raw vector dataset feeding into Scikit-Learn.")
    st.dataframe(ml_df[["Time", "Location", "Magnitude"]], use_container_width=True, hide_index=True, height=300)

# ==========================================
# FULL RESTORED EDUCATIONAL & ENGINEERING TABS
# ==========================================
st.markdown("---")
edu_tabs = st.tabs(["📊 Linear Regression Mechanics Explained", "🛠️ System Engineering Blueprint"])

with edu_tabs[0]:
    st.subheader("Understanding the Trend Estimation Engine on this Page")
    st.markdown(f"""
    Because there are no deep neural networks or complex AI models visible on this workspace, the machine learning occurring here is purely mathematical, silent, and foundational. This node utilizes **Supervised Machine Learning**, specifically an optimization algorithm known as **Linear Regression**.

    #### 1. The Core Objective: Trend Extrapolation
    The system asks a fundamental predictive question: *Based on the chronological timeline of recent seismic events, what is the mathematical trajectory of upcoming events?*
    To completely eliminate layout distortions and date-parsing crashes, the canvas maps data against sequential **Event Numbers ($1, 2, 3...$)** rather than volatile datetime intervals. 

    #### 2. The Current Mathematical Identity
    The Ordinary Least Squares (OLS) algorithm has resolved the following linear equation for this live dataset:
    
    **Equation:** ${equation_text}$

    * **The Slope ($m$):** Calculated at **{m_slope:.4f}**. This value represents the 'velocity' of the trend. A positive value indicates a rising magnitude trajectory across the sequence, while a negative value suggests a dampening effect.
    * **The Intercept ($b$):** Calculated at **{b_intercept:.2f}**. This is the theoretical value of $Y$ when the sequence index is at zero, providing the model's baseline anchor point.

    #### 3. The Step-by-Step Data Pipeline
    * **Feature Engineering:** The script maps time strictly to an ordered ordinal sequence integer **Feature Matrix ($X$)**, while **Magnitude** serves as our **Target Vector ($Y$)**. 
    * **Model Instantiation:** The application initializes a blank mathematical container using Python's `scikit-learn` ecosystem: `model = LinearRegression()`.
    * **Model Training (`.fit()`):** When executing `model.fit(X, Y)`, the algorithm parses every single row inside the data table below, adjusting a linear trajectory until it minimizes the squared distances between the trendline and every historical scatter point.
    * **Statistical Forecasting Horizon (`.predict()`):** The trained model leverages its mathematical formula in memory ($Y = \\beta_0 + \\beta_1X$). The code generates an expanded array matrix stretching past your historical metrics, calculates predictions for those future spaces, and plots them as the dashed **red Trendline** breaking out past your last data point.
    """)

with edu_tabs[1]:
    st.markdown("""
    ### [Mechanism #5] Advanced Machine Learning Analytics & Predictive Trajectories
    * **The Feature:** A chronological data grid cross-referenced against an extrapolated mathematical forecasting serialization line.
    * **The Extrapolation:** Positioned inside the mathematical canvas, the dashed **red trajectory vector** leverages calculated historical slopes to compute future estimations, plotting data projections safely past the newest index row entry.
    * **The Mechanism:** Scikit-Learn structures cannot parse complex timestamp dates natively. The data pipeline indexes the tabular entries into clean sequence integers ($X$ vector array). An ordinary least squares linear regression model is compiled ($Y = \\beta_0 + \\beta_1X + \\epsilon$) to construct continuous trend metrics, which are evaluated over an expanded future sequence array and rendered on-screen.
    """)