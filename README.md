This is a streamlit build Chatbot UI which uses backend services created within SnapLogic, the first platform for generative integration.

##### Table of Contents
[Using the chatbot](#using-the-chatbot)  
&nbsp;&nbsp;&nbsp;&nbsp;[Chat with one data domain](#chat-with-one-data-domain)  
&nbsp;&nbsp;&nbsp;&nbsp;[Chat with multiple data domains](#chat-with-multiple-data-domains)  
[Managing Domain Data](#managing-domain-data)  
&nbsp;&nbsp;&nbsp;&nbsp;[Overview of available namespaces](#overview-of-available-namespace)  
&nbsp;&nbsp;&nbsp;&nbsp;[Upload data into a new namespace](#upload-data-into-a-new-namespace)  
&nbsp;&nbsp;&nbsp;&nbsp;[Add data to an existing namespace](#add-data-to-an-existing-namespace)  
&nbsp;&nbsp;&nbsp;&nbsp;[Delete a namespace](#delete-a-namespace)  



# Using the chatbot
## Chat with one data domain
Choose a data domain you want to ask your questions against.
Enter your query in the chat box. For example, if you're using a HR service chatbot, you might ask, "When do I got paid?".
![one data domain](https://raw.githubusercontent.com/mpentzek/SnapBot/refs/heads/main/images/chatbot_use_single_data_source.png)

## Chat with multiple data domains
You also can choose more than one data domain to chat with.
Switching on "use of multiple data domains" will let you pick multiple data domains.
![Multiple Data domains](https://raw.githubusercontent.com/mpentzek/SnapBot/refs/heads/main/images/chatbot_use_multiple_data_source.png)

When you select more than one data domain, you can ask questions that will highlight differences between them. For instance, if you choose the Lyft Annual Report and the Uber Annual Report as your data domains, you might ask, 'How do the service offerings in both reports compare?' or 'What is the difference in revenue between the two companies in 2022?'
![prompt for multiple data domains](https://raw.githubusercontent.com/mpentzek/SnapBot/refs/heads/main/images/chatbot_use_multiple_data_source_prompt.png)



# Managing Domain Data
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