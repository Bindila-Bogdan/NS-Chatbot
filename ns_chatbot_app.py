"""
This is the main Python modules which defines the interactions with the chatbot through
an UI designed with Streamlit.
"""

import sys
import streamlit as st

sys.path.append("./src/")

from src.ns_chatbot_rag import NSChatbotRAG
from src.ns_chatbot_agent import NSChatbotAgent


print("Its running!!")


def generate_response(query):
    """Generates a response from the chatbot based on the given query. It dynamically handles
    the interaction with the RAG-based chatbot or with the agent-based chatbot.

    Parameters
    ----------
    query : str
        The user's input query to the chatbot.

    Returns
    -------
    str
        The complete response from the chatbot, potentially including
        retrieved document metadata or citations, formatted for display.
    """

    if hasattr(st.session_state.chatbot, "retrieve_top_k_documents"):
        retrieved_docs, docs_metadata = st.session_state.chatbot.retrieve_top_k_documents(query)
        response = st.session_state.chatbot.ask_chatbot(query, retrieved_docs)
        complete_response = f"{response.strip()}\n\n---\n\n{docs_metadata.strip()}"
    else:
        response, citations = st.session_state.chatbot.ask_chatbot(query)

        if len(citations) != 0:
            complete_response = f"{response.strip()}\n\n---\n\n{citations.strip()}"
        else:
            complete_response = response.strip()

    return complete_response


# define general aspects of the page
st.set_page_config(page_title="NS Chatbot")
st.markdown(
    "<h1 style='text-align: left; color: #113084;'>NS Chatbot 🚆</h1>", unsafe_allow_html=True
)
st.write(
    """Welcome to the NS Chatbot! Your assistant for train travel with NS. Switch modes in the sidebar:


* **RAG-based chatbot:** Answers general questions about NS.
* **Agent-based chatbot:** Provides general answers and live train disruption information."""
)

# sidebar control for choosing the chatbot type
with st.sidebar:
    st.header("Chatbot Mode")
    chatbot_mode = st.selectbox("Choose chatbot mode", ["RAG-based chatbot", "Agent-based chatbot"])

    # switch chatbot when mode changes and clear the chat history
    if "current_mode" not in st.session_state or st.session_state.current_mode != chatbot_mode:
        if chatbot_mode == "RAG-based chatbot":
            st.session_state.chatbot = NSChatbotRAG()
        else:
            st.session_state.chatbot = NSChatbotAgent()

        st.session_state.messages = []
        st.session_state.current_mode = chatbot_mode
        st.success(f"Switched to {chatbot_mode} and cleared chat history.")


if "chatbot" not in st.session_state:
    st.session_state.chatbot = NSChatbotRAG()
    st.session_state.current_mode = "RAG-based chatbot"
    st.session_state.messages = []

# display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# get use input
if prompt := st.chat_input("Please enter your message here..."):
    # add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # get response from the chatbot
    chatbot_response = generate_response(prompt)

    # display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(chatbot_response)

    # add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": chatbot_response})
