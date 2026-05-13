import streamlit as st

st.set_page_config(
    page_title="Modular Analytics & Visualization Capabilities: A Technical Exercise",
    page_icon="🎨",
    layout="wide"
)

# Initialize global authentication state for the subpages to check
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = True

# Updated main title
st.title("🎨 Modular Analytics & Visualization Capabilities: A Technical Exercise")
st.markdown("##### *An Interactive Technical Portfolio Demonstrating Rapid Deployment Features for Data-Driven Applications*")
st.markdown("---")

# ... rest of your homepage content remains exactly the same ...