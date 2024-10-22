This is a streamlit build Chatbot UI which uses backend services created within SnapLogic, the first platform for generative integration.

# Manage Domain Data
As this is a Retrieval-Augmented Generation (RAG) chatbot the data is stored in Pinecone Vector Database.
With this chatbot you can manage the data and the corresponding namespaces. 
However, you need to authenticate first befor you can manage the domain data.
![Authenticate](https://raw.githubusercontent.com/mpentzek/SnapBot/refs/heads/main/images/manage_datadomain_authenticate.png)

## Overview of available namespace
In the Overview section all available namespaces are listed with the corresponding vector count.

![Namespace Overview](https://raw.githubusercontent.com/mpentzek/SnapBot/refs/heads/main/images/manage_datadomain_namespac_overview.png)

## Upload data into a new namespace
You can upload data into a new namespace by providing a  name (for the namespace) followed by the selection of PDF file.
![Namespace Overview](https://raw.githubusercontent.com/mpentzek/SnapBot/refs/heads/main/images/manage_datadomain_uploaddatainnewnamespace.png)

## Add data to an existing namespace
You also can add new data to an existing namespace by selecting the appropiate namespace follwed by the selection of PDF file.


## Delete a namespace
Existing namespaces can be deleted after confirmation.
This process removes all vectors irreversible.

![Namespace Deletion](https://raw.githubusercontent.com/mpentzek/SnapBot/refs/heads/main/images/manage_datadomain_delete_namespace.png)


# Use the chatbot
## Chat with one data domain
Choose a data domain you want to ask your questions against.
Enter your query in the chat box. For example, if you're using a HR service chatbot, you might ask, "When do I got paid?".

## Chat with multiple data domains
You also can choose more than one data domain to chat with.In that case you can ask question which will return differences in the data domains. I you you choose for example Lyft Annual Report and Uber Annual Report as data domains you can ask e.g. How does the service offerings in both reports differ?" or "What is the difference in revenue in 2022 for both companies?"
 

![Chatbot UI](https://github.com/mpentzek/SL-Chatbot-UI/blob/main/images/Chatbot.png?raw=true)

