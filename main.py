import streamlit as st
from dotenv import dotenv_values
import utils as utl

env = dotenv_values(".env")

st.logo(
    #env["SL_LOGO_URL_LARGE"],
    "https://www.snaplogic.com/media-kit/Logocombo_SnapLogic_RGB.png",
    link="https://www.snaplogic.com/products/genai-builder",
    icon_image="https://www.snaplogic.com/media-kit/Logocombo_SnapLogic_RGB-rev.png" #env["SL_LOGO_URL_SMALL"]
)

st.set_page_config(
	page_icon="https://raw.githubusercontent.com/mpentzek/SL-Chatbot-UI/refs/heads/main/images/favicon.ico", 
	layout="centered",
	page_title='SnapBot by SnapLogic',
	initial_sidebar_state="expanded"
)



pages = {
    "Chatbot": [
        st.Page("pages/chatbot.py", title="Chatbot",icon=":material/forum:")
    ],
    "Settings": [
        st.Page("pages/managedata.py", title="Manage Data Domains",icon=":material/database:")
    ],
    "Help": [
        st.Page("pages/documentation.py", title="Documentation",icon=":material/description:"),
        st.Page("pages/contact.py", title="Contact",icon=":material/alternate_email:")
    ]    
}

 # Loading CSS (applied to alle pages)
utl.local_css("style.css")

pg = st.navigation(pages)
pg.run()