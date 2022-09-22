import os
import json

from utilities.complex_encoder import ComplexEncoder
from utilities.aws_utils import AWSUtils
from resources.findings import Finding
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
    
    _finding = Finding()
    _resp_findings = _finding.get_findings()
    _finding.logger.info(_resp_findings)
    if  _resp_findings["code"]==200:
        pass
        for f in _resp_findings["data"]:
            if f["Compliance"]["Status"]=="FAILED":
                ControlId=f["ProductFields"]["ControlId"] if f["ProductFields"].get("ControlId") else ".".join(["CIS",f["ProductFields"]["RuleId"]])
                _resp_control = _control.get(resourceId=ControlId)
                _c = _resp_control["data"]
                _ = dict(
                    Id=f["Id"],
                    Title=f["Title"],
                    AwsAccountId=f["AwsAccountId"],
                    GeneratorId=f["GeneratorId"],
                    ControlId=ControlId,
                    Resources=f["Resources"],
                    Reactor=_c.get("ReactorId","not configured")
                )
                _finding.create(obj=json.loads(json.dumps(_,cls=ComplexEncoder)))
        _finding.logger.info(len(_resp_findings["data"]))
    else:
        _finding.logger.info(_resp_findings)
    """
    _enabled_standards = _standard.get_enabled_standards(event={})
    if _enabled_standards["code"]==200:
        ret["enabled-standards"] = _enabled_standards["data"]
    else:
        ret["enabled-standards"] = []
    for s in ret["enabled-standards"]:
        _obj = s.copy()
        _obj["standardId"]=_obj["StandardsArn"]
        _standard.create(obj=json.loads(json.dumps(_obj,cls=ComplexEncoder)))
        _controls = _standard.describe_standards_controls(event={"filters":{"StandardsSubscriptionArn":s["StandardsSubscriptionArn"]}})
        if _controls["code"]==200:
            for c in _controls["data"]:
                _o = json.loads(json.dumps(c,cls=ComplexEncoder))
                _o["StandardsArn"]=s["StandardsArn"]
                _control.create(obj=_o)
            s.update({
                "controls":_controls["data"]
            })
    """
    return json.loads(json.dumps(ret,cls=ComplexEncoder))
