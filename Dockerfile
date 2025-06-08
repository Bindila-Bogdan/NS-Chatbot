# use an official Python runtime as a parent image
FROM python:3.12-slim-bookworm

# set the working directory in the container
WORKDIR /app

# copy the requirements file and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the application code into the container
COPY . .

# expose the port that Streamlit runs on
EXPOSE 8501

# command to run the Streamlit application
CMD ["streamlit", "run", "ns_chatbot_app.py", "--server.port", "8501"]
