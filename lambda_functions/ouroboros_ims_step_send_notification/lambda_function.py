import os
import json

from utilities.complex_encoder import ComplexEncoder
from utilities.aws_utils import AWSUtils

def send_message(client,message):
    response = client.publish(
        TopicArn='arn:aws:sns:ap-southeast-1:592336536196:ouroboros-sns-topic-notification',
        Message=message
    )
    return

def lambda_handler(event, context):
    utils = AWSUtils(aws_access_key_id=os.getenv("ak"),aws_secret_access_key=os.getenv("sk"),region_name=os.getenv("region","ap-southeast-1"))
    client = utils.client("sns")
    for message in event["messages"]:
        send_message(client,message)
    return event
