import streamlit as st
import requests
import utils as utl



# GitHub URL to fetch the raw markdown file
url = 'https://raw.githubusercontent.com/mpentzek/SL-Chatbot-UI/main/README.md'

# Fetch the content
response = requests.get(url)
if response.status_code == 200:
    markdown_text = response.text
else:
    markdown_text = "Error fetching the markdown file."

# Create a centered layout using columns
#col1, col2, col3 = st.columns([1, 2, 1])  # The middle column (col2) is wider to center the content

#with col2:
st.header("Documentation")
# Render the markdown content in Streamlit
st.markdown(markdown_text)
