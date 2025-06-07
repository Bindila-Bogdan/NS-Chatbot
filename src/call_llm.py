import json
from boto3.session import Session

from config import LLM_ID
from utils import load_env_variables


def call_bedrock_llm(session, prompt):
    client = session.client("bedrock-runtime")

    system_prompt = "You are a friendly and professional chatbot for NS (Dutch Railways)."

    messages = []
    messages.append({"role": "user", "content": [{"type": "text", "text": prompt}]})

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "system": system_prompt,
            "messages": messages,
            "max_tokens": 1024,
            "temperature": 0.7,
        }
    )

    response = client.invoke_model(
        body=body, modelId=LLM_ID, accept="application/json", contentType="application/json"
    )

    response_body = json.loads(response.get("body").read())
    response = response_body["content"][0]["text"]

    print(response)


if __name__ == "__main__":
    env_variables = load_env_variables()

    session = Session(
        profile_name=env_variables["profile_name"], region_name=env_variables["region_name"]
    )
    call_bedrock_llm(session, "What is NS?")
