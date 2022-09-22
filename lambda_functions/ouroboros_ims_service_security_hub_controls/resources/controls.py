import json
from . import Resource


class Control(Resource):
    
    def __init__(self, resourceId=None,  *args, **kwargs):
        super().__init__(name="security.controls",*args, **kwargs)
        if resourceId:
            self._from_ddb(resourceId=resourceId)
        self.logger.info(getattr(self,self.pk,"undefined"))


        self.register_apis(
            [
                {
                    "resource":"/resources/controls",
                    "httpMethod":"GET",
                    "func":"list"
                },
                {
                    "resource":"/resources/controls/{ControlId}",
                    "httpMethod":"PUT",
                    "func":"api_update"
                }
            ]
        )