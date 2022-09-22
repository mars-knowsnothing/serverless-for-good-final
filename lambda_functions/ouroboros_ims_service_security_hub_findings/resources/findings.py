import json
from botocore.exceptions import ClientError
from . import Resource


class Finding(Resource):
    
    def __init__(self,  *args, **kwargs):
        super().__init__(name="security.findings",*args, **kwargs)
        # self._from_ddb(resourceId=resourceId)
        self.logger.info(getattr(self,self.pk,"undefined"))


        self.register_apis(
            [
                {
                    "resource":"/resources/findings",
                    "httpMethod":"GET",
                    "func":"list"
                }
            ]
        )
    
    def get_findings(self, *args, **kwargs):
        findings = list()
        query_string_params = kwargs.get("filters",{})
        
        params = dict(
            MaxResults=query_string_params.get("MaxResults",50)
        )
        if query_string_params.get("Filters"):
            params["Filters"] = query_string_params["Filters"]
        client = self.utils.client("securityhub")
        response = client.get_findings(**params)
        findings.extend(response["Findings"])
        while "NextToken" in response:
            response = client.get_findings(
                NextToken = response["NextToken"],
                **params
            )
            findings.extend(response["Findings"])

        return dict(
            code=response["ResponseMetadata"]["HTTPStatusCode"],
            data=findings,
        )
    
    