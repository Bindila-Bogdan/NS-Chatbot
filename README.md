# NS Chatbot

NS chatbot is a helpful assistant that helps travelers with information regarding travelling by train with NS and train disruptions in the Netherlands. It answers questions based on a [guide](https://www.ns.nl/binaries/_ht_1575971177922/content/assets/ns-en/terms/travelling-with-ns.pdf) released by NS (divided in 16 PDFs based on chapters) and the information from the NS Wikipedia [page](https://en.wikipedia.org/wiki/Nederlandse_Spoorwegen) stored as a PDF.

### Overview

The project was developed utilizing exclusively AWS services and has two main modes, which are presented below.

##### RAG-based chatbot

It answers questions and provides the name and page of the retrieved documents used to craft the answer. However, it cannot answer questions about train disruptions. The RAG is implemented in Python by first extracting the most relevant documents and then providing them to the LLM. Additionally, chat memory is implemented manually. This version of the chatbot was implemented to provide more control over the hyperparameters of the retrieval and LLM.

![RAG-based chabot](images/rag_based_chatbot.png)

##### Agent-based chatbot

It answers questions and provides the name and page of the documents used to generate the answer, and can answer questions about disruptions by leveraging a mock tool containing disruption data for the vast majority of train stations in the Netherlands. The agent is set up in AWS Bedrock and called from Python. It has built-in memory of the conversation. The tool which provides details about train disruptions at train stations in the Netherlands leverages a Lambda function implemented in Python.

![Agent-based chabot](images/agent_based_chatbot.png)

### Technical Details

The entire project was set up using the AWS web portal to accelerate development. Below are described the settings of the project components.

**Foundational LLM**
Both versions of the chatbot leverage Claude 3.5 Haiku.

**Data Storage**
The PDF documents are stored in a S3 bucket.

**Knowledge base**
It was set up to take get the documents from the S3 bucket and is represented by Amazon OpenSearch Serverless.
The documents were divided into chunks of 500 words with an overlap of 20%.

**Embedding model**
It is represented by the Cohere Embed English V3 with an embedding size of 1024.

**Agent**
Uses the default orchestration and has 2 tools:
1. knowledge base from where retrieves 5 chunks at a time
2. group function represented by a Lambda function inside an action group

**Lambda function**
It is packaged as a ZIP including a helper script and a CSV file represented by 2024 [train disruptions data](https://www.rijdendetreinen.nl/en/open-data/disruptions) in the Netherlands and uploaded to S3 using Python. For a given station, if it exists in the dataset, it returns one disruption with the destination, duration in minutes, and cause. 

**User Interface**
The UI is developed with Streamlit and substitutes the CLI for a better experience.

### Testing

The prompts were engineered based on a list of [questions](data/questions.md) that cover the large majority of scenarios. The testing was done manually, and the performance was maximized across 3 criteria:
- factual accuracy (to avoid hallucinations)
- completeness
- coherence

Based on the tests, the chatbot provides correct and useful answers while politely refusing to answer questions about other topics.

### Project Structure

The project structure is described below:

```
├───.streamlit - contains the style configuration for the Streamlit UI
├───data - contains the used documents for RAG and questions for testing the chatbot
├───images - stores images that are displayed in this README file
├───src
│   ├───config.py - stores LLM hyperparameters, prompts, and identifiers for agents, knowledge base, etc.
│   ├───ns_chatbot_agent.py - code for the agent chatbot which utilizes the disruptions tool
│   ├───ns_chatbot_rag.py - code for the chatbot with RAG implemented manually
│   ├───ns_chatbot.py - store the class extended by RAG-based and agent-based chatbot classes
│   ├───utils.py - script for loading env variables and the zip of the Lambda function to S3
│   └───disruptions_lambda - the code for the Lambda function and the disruptions data (includes their zip)
├───Dockerfile
├───ns_chatbot_app.py - the main script which defines the UI and interaction with the chatbot
└───requirements.txt
```

### Quick Start Guide

The project was developed on a Windows machine with the AWS credentials stored at `C:\Users\Bogdan\.aws`. It was packaged with Docker for portability. 

To run this project, you would need the same credentials to access the configured AWS services. To run it locally, please follow the steps:

0. Set the AWS credentials, where `ACCESS_KEY_ID`, `SECRET_ACCESS_KEY`, and `PROFILE_NAME` have to be replaced by the actual values.

```sh
aws configure set aws_access_key_id ACCESS_KEY_ID --profile PROFILE_NAME
aws configure set aws_secret_access_key SECRET_ACCESS_KEY --profile PROFILE_NAME
```

1. Clone the project.

```sh
git clone https://github.com/Bindila-Bogdan/NS-Chatbot.git
```

2. Add a `.env` file to the project directory with the following format, where `PROFILE_NAME` and `REGION_NAME` should be replaced by the actual values.

```
AWS_PROFILE_NAME=PROFILE_NAME
AWS_REGION_NAME=REGION_NAME
```

2. Build the Docker image.

```sh
docker build -t ns_chatbot .
```

3. Run the Docker container.

```sh
docker run -p 8501:8501 -v /c/Users/Bogdan/.aws:/root/.aws:ro ns_chatbot
```

4. Access the chatbot at `http://localhost:8501`.

5. Have fun!

### Future Enhancements

- [ ] Include presentation slides
- [ ] Add unit tests
- [ ] Add a CI/CD pipeline 
- [ ] Implement an automated way to test the chatbot
- [ ] Deploy the chatbot on an EC2 instance
