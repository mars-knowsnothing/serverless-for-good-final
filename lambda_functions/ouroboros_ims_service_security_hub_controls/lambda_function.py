import os

from utilities.aws_utils import AWSUtils
from resources.controls import Control

def lambda_handler(event, context):
    """
    This is a description of this Lambda function, getting EC2 instances of given account.
    :param event: event json from Example
        event = {
            "resource": "/accounts/{accountid}/services/ec2/instances",
            "httpMethod": "get"
        }
    :param context:
        context
    :return: None
    """
    ret = dict()
    _control = Control()
    ret = _control.to_dict()
    response = _control.API(event=event)
    return response
