import streamlit as st
import sys
import os

# Ensure Python can find your src folder
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import the function instead of the hidden variable
from src.agents.modernization_crew import run_crew

# Configure the web page
st.set_page_config(page_title="Code Modernization Engine", page_icon="⚡", layout="wide")

# Header Section
st.title("⚡ AI Code Modernization Engine")
st.markdown("**Created by Pradeep Kumar Sharma**")
st.markdown("This engine connects to a live Neo4j graph database, analyzes monolithic code structures, and autonomously generates a modernized, modular architecture.")

st.divider()

# Layout: Left control panel, Right output screen
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Control Panel")
    st.info("Ensure your Neo4j database is running before executing the pipeline.")
    
    # The big red launch button
    start_button = st.button("🚀 Execute Pipeline", use_container_width=True, type="primary")

with col2:
    st.header("Engine Output")
    
    if start_button:
        with st.spinner("Waking up the Architect and Coder on the Groq Network..."):
            try:
                # Trigger the AI agents using the function
                result = run_crew()
                
                st.success("Mission Complete! Modular Python files have been physically written to your hard drive.")
                
                # Display the Architect's reasoning
                st.subheader("Architect's Blueprint")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"Engine Failure: {e}")
    else:
        st.write("Awaiting execution command...")