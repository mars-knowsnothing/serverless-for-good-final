import json
import os
import tempfile
from utilities.aws_utils import AWSUtils

def invoke(client,func,payload):
    response = client.invoke(
        FunctionName=func,
        Payload=json.dumps(payload)
    )
    return response

def lambda_handler(event, context):
    # TODO implement
    output = event.copy()
    output["result"] = dict(
        messages=list()
    )
    if output["config"].get("configuredReactor"):
        output["result"]["messages"].append("execute lambda {func}".format(func=output["config"]["configuredReactor"]["resource"]["aws.lambda"]))
        utils = AWSUtils(aws_access_key_id=os.getenv("ak"),aws_secret_access_key=os.getenv("sk"),region_name=os.getenv("region","ap-southeast-1"))
        client = utils.client("lambda")
        resp = invoke(client,output["config"]["configuredReactor"]["resource"]["aws.lambda"],output["finding"])
        utils.logger.info(resp)
        output["result"]["messages"].append("{StatusCode} - {FunctionError} - {LogResult}".format(StatusCode=resp.get("StatusCode","na"),FunctionError=resp.get("FunctionError","na"),LogResult=resp.get("LogResult","na")))
    else:
        output["result"]["messages"].append("reactor not configured for control {controlId}".format(controlId=output["config"]["control"]["ControlId"]))
    return output

