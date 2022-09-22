import json

from utilities.aws_utils import AWSUtils


class Service(object):

    def __init__(self, utils: AWSUtils, *args, **kwargs) -> None:
        self.name = "service"
        self.utils = utils
        self._handlers = {}

    def api(self, event: dict, options=None) -> dict:
        """
        event = {
            "resource": "/accounts/{accountid}/services/ec2/instances",
            "httpMethod": "get"
        }
        :param event:
        :param options:
        :return:
        """
        resource = event["resource"]
        http_method = event["httpMethod"]
        handler = self._handlers.get(resource).get(http_method)
        api_gateway_event = dict()

        path_parameters = event.get("pathParameters")
        if not path_parameters:
            path_parameters = dict()
        api_gateway_event["resources"] = path_parameters

        query_string_parameters = event.get("queryStringParameters")
        if not query_string_parameters:
            query_string_parameters = dict()
        api_gateway_event["fields"] = query_string_parameters.pop("fields", None)
        api_gateway_event["filters"] = query_string_parameters

        payload = event.get("body")
        if not payload:
            payload = json.dumps(dict())
        payload = json.loads(payload)

        api_gateway_event["payload"] = payload
        resp = handler(event=api_gateway_event)
        return resp

    def register(self, resource: str, httpMethod: str, func: any) -> None:
        if not self._handlers.get(resource):
            self._handlers[resource] = {
                httpMethod: func
            }
        else:
            self._handlers[resource].update({
                httpMethod: func
            })
