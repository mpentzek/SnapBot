import streamlit as st
import requests
from dotenv import dotenv_values
import utils as utl
import pandas as pd

env = dotenv_values(".env")

# Read the environment variables
INDEX = env["SL_VECTORDB_INDEX"]

# SnapLogic Indexer pipeline
INDEXER_URL = env["SL_INDEXER_URL"] + "?vectordb_index=" + env["SL_VECTORDB_INDEX"] 
INDEXER_BEARER_TOKEN = env["SL_INDEXER_TOKEN"]
INDEXER_TIMEOUT = int(env["SL_INDEXER_TIMEOUT"])

# SnapLogic Pinecone Namespace API
NAMESPACES_API_URL = env["SL_NAMESPACES_API_URL"]
NAMESPACES_API_TOKEN = env["SL_NAMESPACES_API_TOKEN"]
NAMESPACES_API_TIMEOUT = int(env["SL_NAMESPACES_TIMEOUT"])

# Disable the Upload and Delete Buttons by default
upload_disabled = True
delete_disabled = True

print('---------------------------------------------')
print(f'Code Start Session State: {st.session_state}')
print('---------------------------------------------')


def write_namespaces_to_session_state():
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
    st.session_state.pineconens = [item["namespace"] for item in result]
    st.session_state.pineconestats = result


if 'pineconens' not in st.session_state:
    write_namespaces_to_session_state()
    print('---------------------------------------------')
    print(f'Just added pineconens to session: {st.session_state}')
    print('---------------------------------------------')

if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

# Create a centered layout using columns
col1, col2, col3 = st.columns([1, 2, 1])  # The middle column (col2) is wider to center the content

#with col2:
st.header("Manage your RAG data domains")
#st.header("Manage your RAG data domains",divider=True)
#st.title("Manage your RAG data domains")


if 'pineconestats' not in st.session_state:
    write_namespaces_to_session_state()

st.subheader(f"Overview of namespaces in index {INDEX}")

if st.session_state.pineconestats:
    df = pd.DataFrame(st.session_state.pineconestats, columns=['namespace', 'vectorCount'])
    st.dataframe(df, use_container_width=True) 

st.divider()
st.subheader("Upload data into a namespace (index data)")

on = st.toggle("Use existing namespace", value=False)

if on:
    namespacetofeed = st.selectbox(
        "Please select an existing namespace",
        st.session_state['pineconens'],
        index=1
    )
    st.session_state.namespacetofeed = namespacetofeed
else:
    namespacetofeed = st.text_input("Please type a name for your new namespace")

if namespacetofeed:
    upload_disabled = (namespacetofeed == "")

uploaded_file = st.file_uploader("Upload your data", type='pdf', disabled=upload_disabled)

if uploaded_file is not None and uploaded_file != st.session_state.uploaded_file:
    with st.spinner("Processing your file..."):
        indexer_headers = {
            'Authorization': f'Bearer {INDEXER_BEARER_TOKEN}',
            'Content-Type': 'application/octet-stream'
        }
        response = requests.post(
            url=INDEXER_URL + "&filename=" + uploaded_file.name + "&vectordb_namespace=" + namespacetofeed,
            data=uploaded_file.getvalue(),
            headers=indexer_headers,
            timeout=INDEXER_TIMEOUT,
            verify=False
        )
        if response.status_code == 200:
            st.session_state.uploaded_file = uploaded_file
            del st.session_state.pineconens
            st.toast(f'The file {uploaded_file.name} has been successfully processed', icon=":material/upload_file:")
            st.rerun()

st.divider()
st.subheader("Delete an existing namespace")

if 'pineconens' not in st.session_state:
    write_namespaces_to_session_state()

left_column, right_column = st.columns([0.8, 0.2],vertical_alignment="bottom")

namespace_to_delete = left_column.selectbox(
    "Please select a namespace",
    st.session_state['pineconens'],
    index=None
)

@st.dialog("Confirm Deletion")
def deleteNamespace(pineconens):
    st.write(f'Please type: **{pineconens}**')
    userinput = st.text_input("Namespace to delete:")
    disableSubmit = (userinput != pineconens)
    if st.button("Submit", disabled=disableSubmit):
        if userinput == pineconens:
            with st.spinner("Deleting namespace..."):
                namespacesAPI_headers = {
                    'Authorization': f'Bearer {NAMESPACES_API_TOKEN}'
                }
                response = requests.delete(
                    url=NAMESPACES_API_URL + "?namespace=" + namespace_to_delete,
                    headers=namespacesAPI_headers,
                    timeout=NAMESPACES_API_TIMEOUT,
                    verify=False
                )
                result = response.status_code
                if result == 200:
                    del st.session_state['pineconens']
                    st.toast(f'Namespace {namespace_to_delete} has been successfully deleted', icon=":material/delete:")
                    st.rerun()

delete_disabled = (namespace_to_delete == "")

if right_column.button('Delete', disabled=delete_disabled,use_container_width=True):
    deleteNamespace(namespace_to_delete)

