import json
from . import Resource


class Reactor(Resource):
    
    def __init__(self,  *args, **kwargs):
        super().__init__(name="security.reactors",*args, **kwargs)
        if self.resourceId:
            self._from_ddb(resourceId=resourceId)
            
        self.logger.info(getattr(self,self.pk,"undefined"))


        self.register_apis(
            [
                {
                    "resource":"/hub/reactors",
                    "httpMethod":"GET",
                    "func":"list"
                },
                {
                    "resource":"/hub/reactors",
                    "httpMethod":"POST",
                    "func":"api_create"
                }
            ]
        )
    
