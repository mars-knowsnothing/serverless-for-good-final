from multiprocessing import context
import os

from utilities.aws_utils import AWSUtils
from resources.reactors import Reactor

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
    _reactor = Reactor()
    response = _reactor.API(event=event)
    return response
