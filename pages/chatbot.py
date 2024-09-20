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


# SnapLogic Retriever pipeline
#RETRIEVER_URL = env["SL_RETRIEVER_URL"] + "?vectordb_index=" + env["SL_VECTORDB_INDEX"] + "&vectordb_namespace=" + env["SL_VECTORDB_NAMESPACE"]
RETRIEVER_URL = env["SL_RETRIEVER_URL"] + "?vectordb_index=" + env["SL_VECTORDB_INDEX"] 
RETRIEVER_BEARER_TOKEN = env["SL_RETRIEVER_TOKEN"]
RETRIEVER_TIMEOUT = int(env["SL_RETRIEVER_TIMEOUT"])


# SnapLogic Pinecone Namespace API
NAMESPACES_API_URL = env["SL_NAMESPACES_API_URL"]
NAMESPACES_API_TOKEN = env["SL_NAMESPACES_API_TOKEN"]
NAMESPACES_API_TIMEOUT = int(env["SL_NAMESPACES_TIMEOUT"])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


if 'namespaces_to_query' not in st.session_state:
    # Define the HTTP Headers for calling the SnapLogic Retriever Pipeline 
    namespacesAPI_headers = {
        'Authorization': f'Bearer {NAMESPACES_API_TOKEN}'
        }
    # Call the SnapLogic Pinecone Namespace API
    response = requests.get(
        url=NAMESPACES_API_URL,
        headers=namespacesAPI_headers,
        timeout=NAMESPACES_API_TIMEOUT,
        verify=False
        )
    result = response.json()
    print(result)
    st.session_state['namespaces_to_query'] = [item["namespace"] for item in result]

#namespaces = [item["namespace"] for item in result]
#print(namespaces)
# debug
#st.write(st.session_state)


#if "selected_namespaces" not in st.session_state:
#    st.session_state.selected_namespaces = st.session_state['namespaces_to_query'][:1]
    #st.session_state.selected_namespaces = namespaces[:1]
    #st.write("Adding selected_namespaces to state")


left_column, right_column = st.columns([0.8, 0.2],vertical_alignment="bottom")

on = left_column.toggle("Compare Documents - using multiple namespaces")
if on:
    #st.write("Feature activated!")
    selected_namespaces = st.multiselect(
        "Which data domains (Namespaces) should be used?",
        #namespaces,
        st.session_state['namespaces_to_query'],
        default=None, # default=st.session_state.selected_namespaces
        placeholder="Choose the data domain(s) you want to use"
    )
    #st.session_state.messages = []
else: 
    selected_namespaces = st.selectbox(
    "Please select an existing namespace",
    st.session_state['namespaces_to_query'],
    index = 1
    )
    #st.session_state.messages = []
    #st.session_state.namespacetofeed = namespacetofeed

if right_column.button('Clear Historie', use_container_width=True):
    st.session_state.messages = []

st.divider()

# Check if more than one option is selected
#if len(selected_namespaces) > 1:
#    st.error("Please select only one option.")
#else:
#    if selected_namespaces:
#        st.write(f"You selected: {selected_namespaces[0]}")


#print(selected_namespaces)
print('---------------------------------------------')
if not selected_namespaces:
    print(f'selected_namespaces: {selected_namespaces}')
else:
    print(f'selected_namespaces: {selected_namespaces}')
print('---------------------------------------------')

if isinstance(selected_namespaces, list):
    print("Es ist eine Liste:", selected_namespaces)
elif isinstance(selected_namespaces, str):
    # String in eine Liste umwandeln
    selected_namespaces = [selected_namespaces]
    print("Es war ein String und wurde in eine Liste umgewandelt:", selected_namespaces)
else:
    print("Es ist weder eine Liste noch ein String.")

#st.session_state.selected_namespaces = selected_namespaces

#st.write(f"Selected namespaces: {selected_namespaces}")




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
        url=RETRIEVER_URL + "&vectordb_namespace=" + str(selected_namespaces), #env["SL_VECTORDB_NAMESPACE"],
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
