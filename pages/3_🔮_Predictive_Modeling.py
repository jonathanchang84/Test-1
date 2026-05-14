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
    
    # --- STATISTICAL DESCRIPTORS ---
    sample_size = len(ml_df)
    mean_mag = ml_df['Magnitude'].mean()
    median_mag = ml_df['Magnitude'].median()
    std_mag = ml_df['Magnitude'].std()
    variance_mag = ml_df['Magnitude'].var()
    
    metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)
    with metric_col1: st.metric("Sample Size (N)", sample_size)
    with metric_col2: st.metric("Mean Mag", f"{mean_mag:.2f}")
    with metric_col3: st.metric("Median Mag", f"{median_mag:.2f}")
    with metric_col4: st.metric("Std Dev (σ)", f"±{std_mag:.2f}")
    with metric_col5: st.metric("Variance (σ²)", f"{variance_mag:.4f}")
        
    st.subheader("Linear Regression Model Trajectory Mapping")
    
    # --- MACHINE LEARNING ENGINE ---
    X_train = ml_df["Event Number"].values.reshape(-1, 1)
    Y_train = ml_df['Magnitude'].values.reshape(-1, 1)
    
    model = LinearRegression()
    model.fit(X_train, Y_train)
    
    # EXTRACTION OF EQUATION PARAMETERS
    m_slope = model.coef_[0][0]
    b_intercept = model.intercept_[0]
    equation_text = f"y = {m_slope:.4f}x + {b_intercept:.2f}"

    # DISPLAY EQUATION ABOVE CHART
    st.latex(equation_text)
    
    # --- GENERATE FORECAST ---
    forecast_extension = 20
    forecast_axis = np.arange(1, len(ml_df) + forecast_extension + 1).reshape(-1, 1)
    predictions = model.predict(forecast_axis)
    
    # --- PLOT VISUALIZATION ---
    trend_fig = go.Figure()
    
    trend_fig.add_trace(go.Scatter(
        x=ml_df["Event Number"], 
        y=ml_df['Magnitude'],
        mode='markers+lines', 
        name='Observed Vectors',
        line=dict(color='#00ffcc', width=1), 
        marker=dict(size=6)
    ))
    
    trend_fig.add_trace(go.Scatter(
        x=forecast_axis.flatten(), 
        y=predictions.flatten(),
        mode='lines', 
        name=f'Trendline ({equation_text})', # Equation added to Legend
        line=dict(color='#ff0055', width=2, dash='dash')
    ))
    
    trend_fig.update_layout(
        template="plotly_dark", height=400, 
        margin=dict(l=40, r=40, b=20, t=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(trend_fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Model Input Matrix")
    st.dataframe(ml_df[["Time", "Location", "Magnitude"]], use_container_width=True, hide_index=True, height=300)

# ==========================================
# EDUCATIONAL CORE & ENGINEERING DOCUMENTATION
# ==========================================
st.markdown("---")
edu_tabs = st.tabs(["📊 Linear Regression Mechanics Explained", "🛠️ System Engineering Blueprint"])

with edu_tabs[0]:
    st.subheader("Understanding the Trend Estimation Engine")
    st.markdown(f"""
    This node utilizes **Linear Regression** to find the line of best fit. 
    The mathematical identity currently resolved for this dataset is:
    
    #### **Equation:** ${equation_text}$
    
    * **The Slope ($m$):** For every event that occurs, the magnitude is predicted to change by **{m_slope:.4f}**.
    * **The Intercept ($b$):** The theoretical starting magnitude at index 0 is **{b_intercept:.2f}**.
    """)

with edu_tabs[1]:
    st.markdown("""
    ### [Mechanism #5] Advanced Machine Learning Analytics
    * **The Feature:** A chronological data grid cross-referenced against an extrapolated mathematical forecasting serialization line.
    * **The Mechanism:** Compiled via Ordinary Least Squares ($Y = \\beta_0 + \\beta_1X + \\epsilon$) to construct continuous trend metrics.
    """)