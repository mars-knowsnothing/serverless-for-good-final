import os

from utilities.aws_utils import AWSUtils
from resources.findings import Finding

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
    _finding = Finding()
    ret = _finding.to_dict()
    response = _finding.API(event=event)
    return response
