import json
from botocore.exceptions import ClientError
from . import Resource


class Control(Resource):
    
    def __init__(self,  *args, **kwargs):
        super().__init__(name="security.controls",*args, **kwargs)
        # self._from_ddb(resourceId=resourceId)
        self.logger.info(getattr(self,self.pk,"undefined"))