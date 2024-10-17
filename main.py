import hmac
import streamlit as st
from dotenv import dotenv_values
import utils as utl

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




def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


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

#check if user is authorized
if not check_password():
    st.stop()

#run this app/page
pg.run()