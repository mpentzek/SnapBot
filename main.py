import hmac
import streamlit as st
import logging
from dotenv import dotenv_values
import utils as utl

logging.basicConfig(level=logging.DEBUG)

logging.info("--------------")
logging.info("Start of main.py")
logging.debug(st.session_state)
logging.info("--------------")

# Load the env variables from .env file
env = dotenv_values(".env")

# define Logo settings
st.logo(
    env["SL_LOGO_BLUE"],
    link=env["SL_LOGO_LINK"],
    icon_image=env["SL_LOGO_WHITE"]
)

#define page config
st.set_page_config(
	page_icon=env["SL_APP_ICON"], 
	layout="centered",
	page_title=env["SL_APP_TILE"],
	initial_sidebar_state="expanded"
)


# define the sections & pages of the app
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

#load the pages 
pg = st.navigation(pages)

#run this app/page
pg.run()

logging.info("--------------")
logging.info("End of main.py")
logging.debug(st.session_state)
logging.info("--------------")