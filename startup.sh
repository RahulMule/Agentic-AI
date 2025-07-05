#!/bin/bash

# Ensure dependencies are installed
pip install -r requirements.txt

# Start your Streamlit app
streamlit run streamlit_app.py --server.port=8000 --server.enableCORS=false
