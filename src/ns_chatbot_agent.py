import re
import uuid

from ns_chatbot import NSChatbot
from config import AGENT_ID, AGENT_ALIAS_ID


class NSChatbotAgent(NSChatbot):
    """
    An agent chatbot that answers questions about NS (Dutch Railways) and leverages a mocked API
    which provides information about train disruptions at train stations in the Netherlands.
    """

    def __init__(self, enable_trace=False):
        """
        Initialize the NSChatbotAgent instance. Each instance of this class represents a new
        converation session with the chatbot.

        Parameters
        ----------
        enable_trace : bool, optional
            Whether to collect trace events from the agent response (default is False).
        """

        super().__init__()
        self.session_id = str(uuid.uuid4())
        self.enable_trace = enable_trace

    def ask_chatbot(self, query):
        """
        Send a query to the chatbot agent and receive the response with optional citations.

        Parameters
        ----------
        query : str
            The user input query to be sent to the agent.

        Returns
        -------
        response_text : str
            The textual response from the agent.
        citations_text : str
            A string of source document names and page numbers, if any citations are used.

        Raises
        ------
        Exception
            Catches and prints any exception that occurs during the Bedrock retrieve API call.
        """

        response_text = ""
        citations_text = ""

        try:
            # call the agent
            response = self.agent_runtime_client.invoke_agent(
                agentId=AGENT_ID,
                agentAliasId=AGENT_ALIAS_ID,
                sessionId=self.session_id,
                inputText=query,
                enableTrace=self.enable_trace,
            )

            citations = set()
            trace = []

            # the response is a streaming response, so there's a need to iterate through chunks
            for event in response["completion"]:
                # get the agent trace
                if self.enable_trace:
                    trace.append(event["trace"])

                # get the response of the agent
                if "chunk" in event:
                    response_text += event["chunk"]["bytes"].decode("utf-8")

                """
                In case the knowledge base is used, get the unique document name and page number
                from where the information was taken.
                """
                try:
                    for citation in event["chunk"]["attribution"]["citations"]:
                        for reference in citation["retrievedReferences"]:
                            metadata = reference["metadata"]
                            citations.add(
                                (
                                    metadata["x-amz-bedrock-kb-source-uri"].split("/")[-1][:-4],
                                    int(metadata["x-amz-bedrock-kb-document-page-number"]),
                                )
                            )
                except KeyError:
                    pass

            # print the agent trace
            if self.enable_trace:
                print("\n--- Agent Trace ---\n{trace}\n-------------------\n")

            # format response and citations
            if len(response_text) == 0:
                response_text = "There was an error and the model could not answer."
            else:
                response_text = re.sub(r"\n{3,}", "\n\n", response_text)

            if len(citations) != 0:
                citations_text += "Citations:\n"

                for citation in citations:
                    citations_text += f"Document {citation[0]} at page {citation[1]}\n"

        except Exception as e:
            print(f"An error occurred: {e}")

        return response_text, citations_text


if __name__ == "__main__":
    ns_chatbot_agent = NSChatbotAgent()

    FIRST_QUERY = "What is NS?"
    response_text, citations_text = ns_chatbot_agent.ask_chatbot(FIRST_QUERY)
    print(response_text, citations_text)

    SECOND_QUERY = "Is there any disruption in Enschede at the moment?"
    response_text, citations_text = ns_chatbot_agent.ask_chatbot(SECOND_QUERY)
    print(response_text, citations_text)

    THIRD_QUERY = "Please let me know if there is any disruption in Amsterdam at the moment and how I can get a refund?"
    response_text, citations_text = ns_chatbot_agent.ask_chatbot(THIRD_QUERY)
    print(response_text, citations_text)
