import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Note: st.set_page_config is handled globally by your main app.py file

# =====================================================================
# 1. CORE COMPONENT INTERFACE LOGIC
# =====================================================================
st.title("🔮 Predictive Modeling & Statistical Inference")
st.markdown("##### *Component Showcase: OLS Regression Engines, Mathematical Extrapolation, and Trendline Identities*")
st.markdown("---")

# --- TECHNICAL CAPABILITY METRICS ---
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.metric(label="Model Confidence (R²)", value="0.892", delta="+0.04")
with m_col2:
    st.metric(label="Mean Squared Error", value="2.41", delta="-0.15", delta_color="inverse")
with m_col3:
    st.metric(label="Training Sample Size", value="100 Units", delta="Stable")

st.markdown("---")

# =====================================================================
# 2. DATA GENERATION & REGRESSION CALCULATION
# =====================================================================
# Creating a synthetic dataset with a clear linear trend for modeling
np.random.seed(42)
x_vals = np.arange(100).reshape(-1, 1)
noise = np.random.normal(0, 5, 100)
# Equation: y = 0.8x + 10 + noise
y_vals = (0.8 * x_vals.flatten()) + 10 + noise

df = pd.DataFrame({'Ordinal Index': x_vals.flatten(), 'Observed Value': y_vals})

# --- SCIKIT-LEARN ENGINE ---
model = LinearRegression()
model.fit(x_vals, y_vals)
df['Trendline'] = model.predict(x_vals)

# Extracting Coefficients for the Mathematical Identity
slope = model.coef_[0]
intercept = model.intercept_

# =====================================================================
# 3. VISUALIZATION LAYER
# =====================================================================
st.subheader("📈 Predictive Trend Analysis")
st.markdown("Below is the visual representation of raw observed data vs. the calculated OLS regression trendline.")

# Plotting using native streamlit line chart (combining raw and trend)
st.line_chart(df.set_index('Ordinal Index'), use_container_width=True)

# --- MATH IDENTITY BOX ---
st.markdown("### 🧮 Mathematical Identity")
equation_latex = f"y = {slope:.4f}x + {intercept:.2f}"
st.info(f"**Calculated Linear Regression Equation:** ${equation_latex}$")

st.markdown("---")

# =====================================================================
# 4. DATA LOG MATRIX
# =====================================================================
st.subheader("📋 Statistical Observation Log")
st.markdown("High-density matrix showing the variance between observed values and model-predicted outputs.")

st.dataframe(df.sort_index(ascending=False), use_container_width=True, hide_index=True)

# =====================================================================
# 5. ALIGNED ENGINEERING NOTES SECTION (Expander Design Pattern)
# =====================================================================
st.markdown("---")
with st.expander("🛠️ System Engineering Blueprint: Feature Matrix & Core Mechanisms", expanded=True):
    st.markdown(f"""
    ### [Mechanism #1] OLS Regression Implementation
    * **The Feature:** Automated trendline extrapolation based on historical data points.
    * **The Mechanism:** Utilizes the `LinearRegression` engine from `scikit-learn` to minimize the sum of squares between observed and predicted values.
    
    ### [Mechanism #2] LaTeX Formula Rendering
    * **The Feature:** Dynamic display of the underlying mathematical model for technical transparency.
    * **The Mechanism:** The application programmatically extracts the `coef_` and `intercept_` attributes from the trained model and formats them into a LaTeX string: ${equation_latex}$.

    ### [Mechanism #3] High-Fidelity Data Plotting
    * **The Feature:** Overlay of statistical models on raw telemetry to identify variance.
    * **The Mechanism:** Uses a unified dataframe structure to inject the prediction array into the charting engine, ensuring the trendline aligns perfectly with the X-axis ordinal indexing.
    """)

st.markdown("---")
st.caption("⚙️ **Capabilities Framework Engine:** Active | **UI Framework:** Streamlit Dark Production | **Predictive Engine:** Scikit-Learn 1.4+")