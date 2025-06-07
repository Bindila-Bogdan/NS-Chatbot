from boto3.session import Session

from utils import load_env_variables


def retrieve_top_k_documents(query, documents_no=5):
    # initialize the Bedrock Agent Runtime client
    client = session.client("bedrock-agent-runtime")

    # call the retrieve API
    response = client.retrieve(
        knowledgeBaseId=env_variables["knowledge_base_id"],
        retrievalQuery={"text": query},
        retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults": documents_no}},
    )

    # process and print the retrieved documents
    print(f"\nTop {documents_no} most similar documents:\n")
    for doc in response["retrievalResults"]:
        content = doc["content"]["text"]
        page_number = doc["metadata"]["x-amz-bedrock-kb-document-page-number"]
        document_name = doc["metadata"]["x-amz-bedrock-kb-source-uri"].split("/")[-1][:-4]

        print(f"{content}\nFrom: {document_name} at page {page_number}\n")


if __name__ == "__main__":
    env_variables = load_env_variables()

    session = Session(
        profile_name=env_variables["profile_name"], region_name=env_variables["region_name"]
    )
    retrieve_top_k_documents("What is NS?", 3)
