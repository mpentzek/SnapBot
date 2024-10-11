import streamlit as st
import time
import requests
from dotenv import dotenv_values

env = dotenv_values(".env")

# Simulates a typewriter effect by progressively displaying a string of text in the Streamlit app.
def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)


# SnapLogic Retriever API
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


# Get the available namespaces of the given pinecone db index
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


# Show list with available namespaces to choose from as well as cleat history button
with st.expander("Choose your chat domain.."):
    left_column, right_column = st.columns([0.8, 0.2],vertical_alignment="bottom")
    on = left_column.toggle("Compare mode - using multiple data domains")
    if on:
        selected_namespaces = st.multiselect(
            "Which data domains (Namespaces) should be used?",
            st.session_state['namespaces_to_query'],
            default=None, # default=st.session_state.selected_namespaces
            placeholder="Choose the data domain(s) you want to use"
        )
    else:
        selected_namespaces = st.selectbox(
        "Please select an existing data domain",
        st.session_state['namespaces_to_query'],
        index = 1
        )

    if right_column.button('Clear Historie', use_container_width=True):
        st.session_state.messages = []

# after divider render chat elements
st.divider()



print('---------------------------------------------')
if not selected_namespaces:
    print(f'selected_namespaces: {selected_namespaces}')
else:
    print(f'selected_namespaces: {selected_namespaces}')
print('---------------------------------------------')

if isinstance(selected_namespaces, list):
    print("It is a list:", selected_namespaces)
elif isinstance(selected_namespaces, str):
    # convert the String into a list
    selected_namespaces = [selected_namespaces]
    print("It is a string which is converted into a list:", selected_namespaces)
else:
    print("Es ist weder eine Liste noch ein String.")


# Render all messages from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user prompt input
if prompt := st.chat_input("What is up?"):
    # Display prompt input in chat message container
    st.chat_message("user").markdown(prompt)
    # Add prompt input to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Add a message pointing out the namespaces to use
    assimessage = f"Ok, let's see what I can find in **{', '.join(selected_namespaces)}**..."
    # Display assistant response in chat message container
    st.chat_message("assistant").markdown(assimessage)
    st.session_state.messages.append({"role": "assistant", "content": assimessage})

    # Define the HTTP Headers for calling the SnapLogic Retriever Pipeline/API 
    retriever_headers = {
        'Authorization': f'Bearer {RETRIEVER_BEARER_TOKEN}'
        }
    # Call the SnapLogic Retriever Pipeline / API
    response = requests.post(
        url=RETRIEVER_URL + "&vectordb_namespace=" + str(selected_namespaces),
        data={"prompt" : prompt},
        headers=retriever_headers,
        timeout=RETRIEVER_TIMEOUT,
        verify=False
        )

    result = response.json()
    response=result[0]['choices'][0]['message']['content']

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        typewriter(text=response, speed=20)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})