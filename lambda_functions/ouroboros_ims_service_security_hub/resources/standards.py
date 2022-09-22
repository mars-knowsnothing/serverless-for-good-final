import json
from botocore.exceptions import ClientError
from . import Resource


class Standard(Resource):
    
    def __init__(self,  *args, **kwargs):
        super().__init__(name="security.standards",*args, **kwargs)
        # self._from_ddb(resourceId=resourceId)
        self.logger.info(getattr(self,self.pk,"undefined"))


        self.register_apis(
            [
                {
                    "resource":"/resources/standards",
                    "httpMethod":"GET",
                    "func":"list"
                },
                {
                    "resource":"/services/security-hub/enabled-standards",
                    "httpMethod":"GET",
                    "func":"get_enabled_standards"
                },
                {
                    "resource":"/services/security-hub/enabled-standards/controls",
                    "httpMethod":"GET",
                    "func":"describe_standards_controls"
                }
            ]
        )

    def describe_standards_controls(self, *args, **kwargs):
        controls = list()
        event = kwargs["event"]
        filters = event["filters"]

        client = self.utils.client("securityhub")

        params = dict(
            MaxResults=int(filters.get("MaxResults",50))
        )
        params["StandardsSubscriptionArn"]=filters["StandardsSubscriptionArn"]
        try:
            response = client.describe_standards_controls(
                **params
            )
            controls.extend(response["Controls"])
            while "NextToken" in response:
                params["NextToken"] = response["NextToken"]
                response = client.describe_standards_controls(
                    **params
                )
                controls.extend(response["Controls"])
            return dict(
                code=response["ResponseMetadata"]["HTTPStatusCode"],
                data=controls,
                messages=["mock response"]
            )
        except ClientError as ce:
            return dict(
                code=ce.response["ResponseMetadata"]["HTTPStatusCode"],
                data=ce.response['Error'],
                messages=[ce.response["Error"]["Message"]]
            )

    def get_enabled_standards(self, *args, **kwargs):
        standards_subscriptions = list()
        event = kwargs["event"]
        client = self.utils.client("securityhub")
        filters = event.get("filters",{})
        params = dict(
            MaxResults=int(filters.get("MaxResults",50))
        )
        if filters.get("StandardsSubscriptionArns"):
            params["StandardsSubscriptionArns"]=filters["StandardsSubscriptionArns"].split(",")
        if filters.get("NextToken"):
            params["NextToken"] = filters["NextToken"]
        try:
            response = client.get_enabled_standards(**params)
            standards_subscriptions.extend(response["StandardsSubscriptions"])
            while "NextToken" in response:
                params["NextToken"] = response["NextToken"]
                response = client.get_enabled_standards(**params)
                standards_subscriptions.extend(response["StandardsSubscriptions"])
            return dict(
                code=response["ResponseMetadata"]["HTTPStatusCode"],
                data=standards_subscriptions,
                messages = []
            )
        except ClientError as ce:
            return dict(
                code=ce.response["ResponseMetadata"]["HTTPStatusCode"],
                data=ce.response['Error'],
                messages=[ce.response["Error"]["Message"]]
            )
    
    
