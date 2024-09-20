import streamlit as st
from dotenv import dotenv_values

env = dotenv_values(".env")

st.logo(
    env["SL_LOGO_URL_LARGE"],
    link="https://www.snaplogic.com/products/genai-builder",
    #icon_image=None
    icon_image=env["SL_LOGO_URL_SMALL"]
)

pages = {
    "Chatbot": [
        st.Page("pages/chatbot.py", title="Chatbot",icon=":material/forum:")
        #st.Page("manage_account.py", title="Manage your account"),
    ],
    "Settings": [
        st.Page("pages/managedata.py", title="Manage Data Domains",icon=":material/database:")
    ],
    "Help": [
        
        st.Page("pages/documentation.py", title="Documentation",icon=":material/description:"),
        st.Page("pages/contact.py", title="Contact",icon=":material/alternate_email:")
    ]    
}

pg = st.navigation(pages)
pg.run()