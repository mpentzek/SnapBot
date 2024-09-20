import streamlit as st
import requests
from dotenv import dotenv_values

env = dotenv_values(".env")

# SnapLogic Indexer pipeline
#INDEXER_URL = env["SL_INDEXER_URL"] + "?vectordb_index=" + env["SL_VECTORDB_INDEX"] + "&vectordb_namespace=" + env["SL_VECTORDB_NAMESPACE"]
INDEXER_URL = env["SL_INDEXER_URL"] + "?vectordb_index=" + env["SL_VECTORDB_INDEX"] 
INDEXER_BEARER_TOKEN = env["SL_INDEXER_TOKEN"]
INDEXER_TIMEOUT = int(env["SL_INDEXER_TIMEOUT"])


# SnapLogic Pinecone Namespace API
NAMESPACES_API_URL = env["SL_NAMESPACES_API_URL"]
NAMESPACES_API_TOKEN = env["SL_NAMESPACES_API_TOKEN"]
NAMESPACES_API_TIMEOUT = int(env["SL_NAMESPACES_TIMEOUT"])

# Disbale the Upload and Delete Buttons by default
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
    #print(result)
    st.session_state.pineconens = [item["namespace"] for item in result]

if 'pineconens' not in st.session_state:
    write_namespaces_to_session_state()
    print('---------------------------------------------')
    print(f'Just added pineconens to session: {st.session_state}')
    print('---------------------------------------------')

if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None



st.header("Manage your RAG data domains")
st.divider()
st.subheader("Upload data into a namespace (index data)")


on = st.toggle("Use existing namespace",value=False)
if on:
    namespacetofeed = st.selectbox(
        "Please select an existing namespace",
        st.session_state['pineconens'],
        index = 1
        )
    st.session_state.namespacetofeed = namespacetofeed
else:
    namespacetofeed = st.text_input("Please type a name for your new namespace")


if namespacetofeed:
    upload_disabled = (namespacetofeed == "")

uploaded_file = st.file_uploader("Upload your data",type='pdf',disabled=upload_disabled )
if uploaded_file is not None and uploaded_file != st.session_state.uploaded_file:
    with st.spinner("Processing your file..."):
        # Define the HTTP Headers for calling the SnapLogic Indexer Pipeline /API
        indexer_headers = {
            'Authorization': f'Bearer {INDEXER_BEARER_TOKEN}',
            'Content-Type': 'application/octet-stream'
        }
        #Call the SnapLogic Indexer Pipeline /API
        response = requests.post(
            url=INDEXER_URL + "&filename=" + uploaded_file.name + "&vectordb_namespace=" + namespacetofeed,
            data=uploaded_file.getvalue(),
            headers=indexer_headers,
            timeout=INDEXER_TIMEOUT,
            verify=False
        )
        if response.status_code == 200:
            #add file to session state
            st.session_state.uploaded_file = uploaded_file
            print('---------------------------------------------')
            print(f'Session State after upload: {st.session_state}')
            print('---------------------------------------------')
            del st.session_state.pineconens
            print('---------------------------------------------')
            print(f'Session State after removal of pineconens: {st.session_state}')
            print('---------------------------------------------')
            st.toast(f'The file {uploaded_file.name} has been succesfully processed', icon=":material/upload_file:")
            st.rerun()


st.divider()
st.subheader("Delete an existing namespace")

if 'pineconens' not in st.session_state:
    write_namespaces_to_session_state()

left_column, right_column = st.columns([0.8, 0.2],vertical_alignment="bottom")

namespace_to_delete = left_column.selectbox(
    "Please select a namespace",
    st.session_state['pineconens'],
    index = None
    )



@st.dialog("Confirm Deletion")
def deleteNamespace (pineconens):
    st.write(f'Please type: **{pineconens}**')
    userinput = st.text_input("Namespace to delete:")
    disableSubmit = (userinput != pineconens)
    if st.button("Submit",disabled=disableSubmit):
        if userinput == pineconens:
            with st.spinner("Deleting namespace..."):
                # Define the HTTP Headers for calling the SnapLogic Retriever Pipeline 
                namespacesAPI_headers = {
                    'Authorization': f'Bearer {NAMESPACES_API_TOKEN}'
                    }
                # Call the SnapLogic Pinecone Namespace API
                response = requests.delete(
                    url=NAMESPACES_API_URL + "?namespace=" + namespace_to_delete,
                    headers=namespacesAPI_headers,
                    timeout=NAMESPACES_API_TIMEOUT,
                    verify=False
                    )
                result = response.status_code
                print(f'result after API call to delete namespace: {result}')
                if result==200:
                    print('---------------------------------------------')
                    print(f'Session State after delte: {st.session_state}')
                    print('---------------------------------------------')
                    del st.session_state['pineconens']
                    print('---------------------------------------------')
                    print(f'Session State after removing pineconens: {st.session_state}')
                    print('---------------------------------------------')
                    st.toast(f'Namespace {namespace_to_delete} has been succesfully deleted', icon=":material/delete:")
                    st.rerun()


if namespace_to_delete:
    delete_disabled = (namespace_to_delete == "")

if right_column.button('delete',disabled=delete_disabled, use_container_width=True):
    deleteNamespace(namespace_to_delete)
    





