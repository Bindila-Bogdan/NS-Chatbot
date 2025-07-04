"""
This module implements the NS chatbot with RAG and conversational memory. It leverages
AWS Bedrock services such as the knowledge base, which leveraes an embedding model for
indexing and search, and a foundational LLM for answering questions.
"""

import sys
import json

sys.path.append(".")

from ns_chatbot import NSChatbot
from config import (
    LLM_ID,
    MAX_OUTPUT_TOKENS,
    LLM_TEMPERATURE,
    RETRIEVED_DOCUMENTS_NO,
    SYSTEM_PROMPT,
    CONVERSATION_HISTORY_LENGTH,
    KNOWLEDGE_BASE_ID,
)


class NSChatbotRAG(NSChatbot):
    """
    A RAG (Retrieval Augmented Generation) chatbot with built-in memory for NS (Dutch Railways)
    which answers questions based on k retrieved documents from the knowledge base.
    """

    def __init__(self):
        """
        Initialize the NSChatbotRAG instance.
        """

        super().__init__()
        # initialize the Bedrock Runtime client needed to call the LLM
        self.runtime_client = self.session.client("bedrock-runtime")
        # initialize conversation history
        self.conversation_history = []

    def retrieve_top_k_documents(self, query, verbose=False):
        """
        Retrieves the top-k most similar documents from the AWS knowledge base configured with
        vector store. The similarity search is performed using Embed English V3 embeddings.

        Parameters
        ----------
        query : str
            The user's query string used to search the knowledge base.
        verbose : bool, optional
            If True, prints the retrieved documents to the console. Defaults to False.

        Returns
        -------
        list
            A list of dictionaries, where each dictionary represents a retrieved document
            and contains 'document_name', 'page_number', and 'content'.
            Returns an empty list if an error occurs during retrieval.
        str
            A string which contains the name and page of the retrieved document, needed to be
            displayed to the user.

        Raises
        ------
        Exception
            Catches and prints any exception that occurs during the Bedrock retrieve API call.
        """

        # call the retrieve API
        try:
            response = self.agent_runtime_client.retrieve(
                knowledgeBaseId=KNOWLEDGE_BASE_ID,
                retrievalQuery={"text": query},
                retrievalConfiguration={
                    "vectorSearchConfiguration": {"numberOfResults": RETRIEVED_DOCUMENTS_NO}
                },
            )
        except Exception as e:
            print(f"Error during document retrieval: {e}")
            return []

        retrieved_documents = []

        # process and print the retrieved documents
        if verbose:
            print(f"\nTop {RETRIEVED_DOCUMENTS_NO} most similar documents:\n")
        for document in response["retrievalResults"]:
            content = document["content"]["text"]
            page_number = int(document["metadata"]["x-amz-bedrock-kb-document-page-number"])
            document_name = document["metadata"]["x-amz-bedrock-kb-source-uri"].split("/")[-1][:-4]

            retrieved_documents.append(
                {
                    "document_name": document_name,
                    "page_number": page_number,
                    "content": content,
                }
            )

            if verbose:
                print(f"{content}\nFrom: {document_name} at page {page_number}\n")

        retrieved_documents_metadata = "**Retrieved documents:**\n"
        included_documents = set()

        # include only unique document name - page number pairs
        for retrieved_document in retrieved_documents:
            if (
                retrieved_document["document_name"],
                retrieved_document["page_number"],
            ) in included_documents:
                continue

            retrieved_documents_metadata += f"- {retrieved_document['document_name']}"
            retrieved_documents_metadata += f", page {retrieved_document['page_number']}\n"
            included_documents.add(
                (retrieved_document["document_name"], retrieved_document["page_number"])
            )

        return retrieved_documents, retrieved_documents_metadata

    def ask_chatbot(self, query, retrieved_documents=None):
        """
        Invokes the LLM (by default Claude 3.5 Haiku) with a given query, incorporating retrieved
        documents as context and maintaining conversation history. The conversation history is
        truncated based on `CONVERSATION_HISTORY_LENGTH` to avoid exceeding the LLM's context size.

        Parameters
        ----------
        query : str
            The current user's query or message.
        retrieved_documents : list, optional
            A list of dictionaries, where each dictionary is a retrieved document. If provided,
            these documents are added to the prompt as context for the LLM. Defaults to None.

        Returns
        -------
        str
            The text response generated by the LLM. Returns a fallback message if an error occurs
            during LLM invocation.

        Raises
        ------
        Exception
            Catches and prints any exception that occurs during the Bedrock invoke_model API call.
        """

        context = ""

        if retrieved_documents is not None and len(retrieved_documents) != 0:
            # build the context string from retrieved documents
            context = "\n\n**Here is some relevant information:**\n"
            for document_index, document in enumerate(retrieved_documents):
                context += (
                    f'<document id="{document_index+1}">\n'
                    f"<source>{document["document_name"]} page {document["page_number"]}</source>\n"
                    f"<content>\n{document["content"]}\n</content>\n"
                    f"</document>\n"
                )
            context += "\n"

        # construct the full prompt including context
        full_user_prompt = f"{context}{query}"

        """Keep only the last 100 messages (50 from user and 50 from chatbot) to avoid exceeding
        the maximum context length of 200k tokens. Computed considering that a conversation turn
        has about 3.6k tokens (5 * 100 for documents, 100 for question and 1,000 for answer)."""
        self.conversation_history = self.conversation_history[-CONVERSATION_HISTORY_LENGTH:]

        self.conversation_history.append(
            {"role": "user", "content": [{"type": "text", "text": full_user_prompt}]}
        )

        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "system": SYSTEM_PROMPT,
                "messages": self.conversation_history,
                "max_tokens": MAX_OUTPUT_TOKENS,
                "temperature": LLM_TEMPERATURE,
            }
        )

        try:
            response = self.runtime_client.invoke_model(
                body=body, modelId=LLM_ID, accept="application/json", contentType="application/json"
            )

            response_text = json.loads(response.get("body").read())["content"][0]["text"]

            # append the LLM's response to the conversation history
            self.conversation_history.append(
                {"role": "assistant", "content": [{"type": "text", "text": response_text}]}
            )
            return response_text

        except Exception as e:
            print(f"Error during LLM invocation: {e}")
            fallback_message = (
                "I apologize, but I'm having trouble processing your request right now."
                "Please try again later."
            )
            self.conversation_history.append(
                {"role": "assistant", "content": [{"type": "text", "text": fallback_message}]}
            )

            return fallback_message

    def reset_conversation(self):
        """Clears the conversation history to start a new chat session."""

        self.conversation_history = []


if __name__ == "__main__":
    ns_chatbot_rag = NSChatbotRAG()

    FIRST_QUERY = "What is NS?"
    retrieved_docs, _ = ns_chatbot_rag.retrieve_top_k_documents(FIRST_QUERY, True)
    print(ns_chatbot_rag.ask_chatbot(FIRST_QUERY, retrieved_docs))

    # test what happens when a question is asked without retrieved documents
    SECOND_QUERY = "And what is their main goal?"
    print(ns_chatbot_rag.ask_chatbot(SECOND_QUERY))

    # test the memory of the chatbot
    THIRD_QUERY = "Can you tell me more about that?"
    print(ns_chatbot_rag.ask_chatbot(THIRD_QUERY))

    # test if clearning the conversation history works
    ns_chatbot_rag.reset_conversation()
    print(ns_chatbot_rag.ask_chatbot(THIRD_QUERY))
