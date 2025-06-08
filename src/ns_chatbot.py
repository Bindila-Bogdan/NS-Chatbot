"""
This module represents the base chatbot class that is inherited by the RAG and agent versions.
"""

from boto3.session import Session


from utils import load_env_variables


class NSChatbot:
    """
    The base class of the NS chatbot that is inherited by the classes of RAG and Agent chatbots.
    """

    def __init__(self):
        # get the environment variables from the .env file and start a session
        self.env_variables = load_env_variables()
        self.session = Session(
            profile_name=self.env_variables["profile_name"],
            region_name=self.env_variables["region_name"],
        )
        # initialize the Bedrock Agent Runtime client needed for retrieval
        self.agent_runtime_client = self.session.client("bedrock-agent-runtime")
