import streamlit as st
import time
import requests
from dotenv import dotenv_values

def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)

env = dotenv_values(".env")

st.title = env["SL_PAGE_TITLE"]

# SnapLogic Indexer pipeline
INDEXER_URL = env["SL_INDEXER_URL"] + "?vectordb_index=" + env["SL_VECTORDB_INDEX"] + "&vectordb_namespace=" + env["SL_VECTORDB_NAMESPACE"]
INDEXER_BEARER_TOKEN = env["SL_INDEXER_TOKEN"]
INDEXER_TIMEOUT = int(env["SL_INDEXER_TIMEOUT"])

# SnapLogic Retriever pipeline
RETRIEVER_URL = env["SL_RETRIEVER_URL"] + "?vectordb_index=" + env["SL_VECTORDB_INDEX"] + "&vectordb_namespace=" + env["SL_VECTORDB_NAMESPACE"]
RETRIEVER_BEARER_TOKEN = env["SL_RETRIEVER_TOKEN"]
RETRIEVER_TIMEOUT = int(env["SL_RETRIEVER_TIMEOUT"])



if "uploader_visible" not in st.session_state:
    st.session_state["uploader_visible"] = False
def show_upload(state:bool):
    st.session_state["uploader_visible"] = state
    
with st.chat_message("system"):
    cols= st.columns((3,1,1))
    cols[0].write("Do you want to upload a file?")
    cols[1].button("yes", use_container_width=True, on_click=show_upload, args=[True])
    cols[2].button("no", use_container_width=True, on_click=show_upload, args=[False])

#Sample comment
if st.session_state["uploader_visible"]:
    with st.chat_message("system"):
        file = st.file_uploader("Upload your data")
        if file:
            with st.spinner("Processing your file"):
                # Define the HTTP Headers for calling the SnapLogic Indexer Pipeline /API
                indexer_headers = {
                    'Authorization': f'Bearer {INDEXER_BEARER_TOKEN}',
                    'Content-Type': 'application/octet-stream'
                }
                #Call the SnapLogic Indexer Pipeline /API
                response = requests.post(
                    url=INDEXER_URL + "&filename=" + file.name,
                    data=file.getvalue(),
                    headers=indexer_headers,
                    timeout=INDEXER_TIMEOUT,
                    verify=False
                )
                print(response)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Define the HTTP Headers for calling the SnapLogic Retriever Pipeline 
    retriever_headers = {
        'Authorization': f'Bearer {RETRIEVER_BEARER_TOKEN}'
        }
    # Call the SnapLogic Retriever Pipeline / API
    response = requests.post(
        url=RETRIEVER_URL,
        data={"prompt" : prompt},
        headers=retriever_headers,
        timeout=RETRIEVER_TIMEOUT,
        verify=False
        )

    result = response.json()
    response=result[0]['choices'][0]['message']['content']

    print(response)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        #st.markdown(response)
        typewriter(text=response, speed=20)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
