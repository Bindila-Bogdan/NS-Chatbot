"""
This module provides utility functions such as loading AWS-related environment variables.
"""

import os
import boto3
from dotenv import load_dotenv

from config import BUCKET_NAME, S3_KEY, ZIP_PATH


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

    return env_variables


def load_lambda_zip():
    """
    Loads the zip file with the Lambda function to S3.
    """

    # get the s3 client
    env_variables = load_env_variables()
    session = boto3.Session(
        profile_name=env_variables["profile_name"],
        region_name=env_variables["region_name"],
    )
    s3 = session.client("s3")

    s3.upload_file(ZIP_PATH, BUCKET_NAME, S3_KEY)
    print("The zip of the Lambda function is now uploaded to S3.")


if __name__ == "__main__":
    load_lambda_zip()
