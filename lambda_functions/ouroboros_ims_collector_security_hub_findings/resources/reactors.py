import json
from . import Resource


class Reactor(Resource):
    
    def __init__(self, resourceId,  *args, **kwargs):
        super().__init__(name="security.reactors",*args, **kwargs)
        self._from_ddb(resourceId=resourceId)
        self.logger.info(getattr(self,self.pk,"undefined"))


        self.register_apis(
            [
                {
                    "resource":"/resources/reactors",
                    "httpMethod":"GET",
                    "func":"list"
                }
            ]
        )
    
