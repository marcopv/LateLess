import time 
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import base64

st.set_page_config(
    page_title="USA airlines delays App",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# read and apply css
style = ""
with open("style/style.txt", "r") as style:
  style = style.read()
st.markdown(style, unsafe_allow_html=True)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('style/dddepth-308.jpg')    
# open readme file for info
markdown = ""
with open("infopage.md", "r") as mrk:
  markdown = mrk.read()

col1,col2,col3 = st.columns([0.5,2,0.5])

with col2:
    st.markdown(markdown, unsafe_allow_html=True)

    predict_button = st.button("Go To Prediction!")

    if predict_button:
        switch_page("prediction page")

