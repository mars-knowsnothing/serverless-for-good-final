import os

from utilities.aws_utils import AWSUtils
from resources.controls import Control
from resources.reactors import Reactor

def parse_config(finding):
    parsed_config = dict()
    _control = Control()
    if finding["ProductFields"].get("ControlId"):
        cid = finding["ProductFields"]["ControlId"]
    elif finding["ProductFields"].get("StandardsGuideArn")=="arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0":
        cid = ".".join(["CIS",finding["ProductFields"]["RuleId"]])

    _c = _control.get(resourceId=cid)
    _control_info = _c["data"]
    parsed_config["control"]=_control_info

    _reactor = Reactor()
    if _control_info.get("ReactorId"):
        _configured_reactor = _reactor.get(resourceId=_control_info.get("ReactorId"))
        parsed_config["configuredReactor"]=_configured_reactor["data"]
    else:
        _available_reactors = _reactor.list(event={"filters":{"controlId":cid}})
        parsed_config["availableReactors"]=_available_reactors["data"]
    return parsed_config

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
    findings = event["findings"]
    output = list()
    for finding in findings:
        output.append(
            {
                "finding":finding,
                "config":parse_config(finding)
            }
        )
    return output
