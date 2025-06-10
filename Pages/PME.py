import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np

st.set_page_config(page_title="PME Chart", page_icon=":bar_chart:", layout="wide")

st.markdown("<h2 style='text-align: left; font-size: 40px;  font-weight: bold;'>Tableau de bord des PME</h2>", unsafe_allow_html=True)
st.image("C:/Users/ckoupoh/Documents/Dash_Market/pays_uemoa_png.png", caption="", use_container_width=False)

#graphs will use css
theme_plotly = None

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html= True)
