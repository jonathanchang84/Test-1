import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Advanced Analytics", layout="wide")

# Complex Idea: State-locking pages based on root app state
if not st.session_state.get("authenticated", False):
    st.error("🔒 Access Denied. Please initialize the session on the Home page.")
    st.stop()

st.title("📊 Multi-Dimensional Analytics Engine")

# Complex Idea: Advanced Caching (@st.cache_data)
# This prevents expensive math functions from re-running on every user click
@st.cache_data
def generate_complex_tensor_data(points):
    x = np.linspace(-5, 5, points)
    y = np.linspace(-5, 5, points)
    X, Y = np.meshgrid(x, y)
    # Creating a complex mathematical wave pattern (Sinusoidal Tensor)
    Z = np.sin(np.sqrt(X**2 + Y**2)) 
    
    df = pd.DataFrame({
        'X Axis': X.flatten(),
        'Y Axis': Y.flatten(),
        'Z Amplitude': Z.flatten()
    })
    return df

# UI Controls
points_slider = st.sidebar.slider("Resolution Matrix Size", 20, 100, 50)
color_theme = st.sidebar.selectbox("Color Palette", ["Viridis", "Plasma", "Cividis", "Turbo"])

st.subheader("Mathematical Surface Mapping")
st.caption("Rendering a simulated 3D scalar field utilizing vector meshgrids.")

# Generate data based on slider
data = generate_complex_tensor_data(points_slider)

# Build a sophisticated Plotly 3D Scatter plot
fig = px.scatter_3d(
    data, x='X Axis', y='Y Axis', z='Z Amplitude',
    color='Z Amplitude', color_continuous_scale=color_theme,
    opacity=0.7, title="3D Wave Tensor Topology"
)
fig.update_layout(margin=dict(l=0, r=0, b=0, t=40))

st.plotly_chart(fig, use_container_width=True)