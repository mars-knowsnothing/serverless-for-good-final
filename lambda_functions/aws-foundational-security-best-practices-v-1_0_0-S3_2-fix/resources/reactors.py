import json
from . import Resource


class Reactor(Resource):
    
    def __init__(self,  *args, **kwargs):
        super().__init__(name="security.reactors",*args, **kwargs)
        if self.resourceId:
            self._from_ddb(resourceId=resourceId)
            
        self.logger.info(getattr(self,self.pk,"undefined"))
        
    def fix(self, *args, **kwargs):
        client = self.utils.client("s3")
        finding = kwargs["finding"]
        resources = finding["Resources"]
        accountId = finding["AwsAccountId"]
        """
        {
          "Type": "AwsS3Bucket",
          "Id": "arn:aws:s3:::s3-finding-test",
          "Partition": "aws",
          "Region": "ap-southeast-1",
          "Details": {
            "AwsS3Bucket": {
              "OwnerId": "a0e08597d99671b6c2462a34f2b593c277343bc9d5ddecc395d3eac4e0efb73c",
              "CreatedAt": "2022-09-21T01:40:56.000Z"
            }
          }
        }
        """
        for resource in resources:
            bucket = resource['Id'].split(':')[-1]
            resp_get_bucket_policy = client.get_bucket_policy(Bucket=bucket)
            policy = json.loads(resp_get_bucket_policy['Policy'])
            for permission in policy['Statement']:
                if permission['Action'] == 's3:GetObject' and permission['Principal'] == '*' and permission['Effect'] == 'Allow':
                    policy['Statement'].remove(permission)
            if len(policy['Statement'])>0:
                client.put_bucket_policy(
                    Bucket=bucket,
                    Policy=json.dumps(policy)
                )
            else:
                resp_delete_bucket_policy = client.delete_bucket_policy(
                    Bucket=bucket,
                    ExpectedBucketOwner=accountId
                )
            resource.update({"fixed":True})
        return dict(
            data=resources,
            messages=[],
            code=200
        )
    
