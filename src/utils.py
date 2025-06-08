"""
This module provides utility functions such as loading AWS-related environment variables.
"""

import os
from dotenv import load_dotenv


def load_env_variables():
    """
    Loads environment variables from a .env file and returns them as a dictionary.

    Returns
    -------
    dict of str
        A dictionary containing the following environment variables: AWS profile name,
        AWS region name and the Bedrock Knowledge Base ID.
    """

    # load env variables from the .evn file
    load_dotenv()

    env_variables = {}

    env_variables["profile_name"] = os.getenv("AWS_PROFILE_NAME", None)
    env_variables["region_name"] = os.getenv("AWS_REGION_NAME", None)
    env_variables["knowledge_base_id"] = os.getenv("KNOWLEDGE_BASE_ID", None)

    return env_variables
