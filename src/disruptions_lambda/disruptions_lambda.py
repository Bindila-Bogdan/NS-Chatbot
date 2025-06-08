import logging
from typing import Dict, Any
from http import HTTPStatus

from check_disruptions import CheckDisruptions

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for processing Bedrock agent requests.

    Args:
        event (Dict[str, Any]): The Lambda event containing action details
        context (Any): The Lambda context object

    Returns:
        Dict[str, Any]: Response containing the action execution results

    Raises:
        KeyError: If required fields are missing from the event
    """

    try:
        action_group = event["actionGroup"]
        function = event["function"]
        message_version = event.get("messageVersion", 1)
        parameters = event.get("parameters", [])

        # get the train station name parameter
        train_station_name = None

        for parameter in parameters:
            if parameter["name"].lower() == "train_station_name":
                train_station_name = parameter["value"]

        if function == "get_disruptions_train_station":
            # get disruptions status
            if train_station_name is not None:
                disruptions_status = CheckDisruptions.get_disruption_from_station(
                    train_station_name
                )
            # treat the case when the train station name has not been passed
            else:
                disruptions_status = "Please pass the 'train_station_name' parameter."
        # treat the case when the function name has not been passed correctly
        else:
            disruptions_status = "The available function name 'get_disruptions_train_station' has not been passed correctly."

        response_body = {"TEXT": {"body": disruptions_status}}

        action_response = {
            "actionGroup": action_group,
            "function": function,
            "functionResponse": {"responseBody": response_body},
        }
        response = {"response": action_response, "messageVersion": message_version}

        logger.info("Response: %s", response)
        return response

    except KeyError as e:
        logger.error("Missing required field: %s", str(e))
        return {"statusCode": HTTPStatus.BAD_REQUEST, "body": f"Error: {str(e)}"}
    except Exception as e:
        logger.error("Unexpected error: %s", str(e))
        return {"statusCode": HTTPStatus.INTERNAL_SERVER_ERROR, "body": "Internal server error"}
