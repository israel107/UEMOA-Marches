import pandas as pd
import streamlit as st
import numpy as np
import ollama


with open("style2.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html= True)

#st.set_page_config(page_title="Market Chat", page_icon="", layout="wide")  

# st.text_input("_Ecrivez votre question_", key="styledinput")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.subheader("📌 Chat Non fonctionnel")
if prompt := st.chat_input("Que voudriez-vous savoir sur le marché de l'UEMOA ??"):
    #user
    st.session_state.messages.append({"role":"user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)
    
    #model
    with st.chat_message("assistant"):
        response = ollama.chat(model='llama3', messages=[
            {'role': m['role'], "content": m["content"]}
            for m in st.session_state.messages
        ], stream=True)

        response_content = " "
        def catch_response(response):
            global response_content 
            for chunk in response:
                response_content +=chunk['message']['content']
                yield chunk['message']['content']

        m_stream = catch_response(response)
        st.write_stream(m_stream)

        st.session_state.messages.append({"role": "assistant", "content": response_content})

# with st.expander("⏱ Filter Tabulation"):
#  #plot tabulation
#  tab=pd.crosstab([df_selection["gender"],df_selection["comment"]],df_selection["stream"],margins=True)
#  st.dataframe(tab,use_container_width=True)
#  #downloading link
#  csv1=convert_df(tab)
#  st.download_button("Press to Download",csv1,"yourfile.csv",key='download-csv')
