import streamlit as st

#######################################
# PAGE SETUP
#######################################
st.set_page_config(page_title="Market Dashboard", page_icon=":bar_chart:", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html= True)

#######################################
# PAGE LOADING
#######################################
home_page = st.Page(
    "Pages/m_Home.py",
    title="Home",
    icon=":material/bar_chart:",
)

project_1_page = st.Page(
    "Pages/MarketChat.py",
    title="Market Chat",
    icon=":material/smart_toy:",
)


pg = st.navigation(
        {
            "Onglets": [home_page, project_1_page],
        }
    )
pg.run()
 
