"""
This module stores the configuration parameters for the NS chatbot.
"""

# configuration for the retrieval-augmented generation
LLM_ID = "us.anthropic.claude-3-5-haiku-20241022-v1:0"
MAX_OUTPUT_TOKENS = 1024
LLM_TEMPERATURE = 0.7
RETRIEVED_DOCUMENTS_NO = 5
CONVERSATION_HISTORY_LENGTH = 100
SYSTEM_PROMPT = (
    "You are a friendly and professional chatbot for NS (Dutch Railways). "
    "Please answer only based on this information. "
    "If the information does not directly answer the question, state that you do not have enough information from the provided context."
)

# configuration for uploading the zip file of the Lambda function
BUCKET_NAME = "ns-trains-disruptions"
S3_KEY = "lambda/disruptions_lambda.zip"
ZIP_PATH = "disruptions_lambda/disruptions_lambda.zip"

# configuration for the agent
AGENT_ID = "DIJ48CDXDP"
AGENT_ALIAS_ID = "WEOPWWC1JZ"
