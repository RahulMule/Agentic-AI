import streamlit as st
import asyncio
from main import run_agent_workflow

st.set_page_config(page_title="Agentic API Generator", layout="wide")
st.title("🧠 API Genius: Agentic API Builder")

if st.button("Run Agent Workflow"):
    with st.spinner("Agents are working... ⏳"):
        output = asyncio.run(run_agent_workflow())
        st.success("🎉 Done! See output below:")
        st.code(output, language="text")