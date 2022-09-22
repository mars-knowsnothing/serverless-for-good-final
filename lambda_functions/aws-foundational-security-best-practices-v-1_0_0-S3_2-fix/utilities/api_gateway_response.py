import json


class APIGatewayResponse(object):
    def __init__(self, cookies=None, isBase64Encoded=False, statusCode=200, headers=None) -> None:
        self.cookies = cookies
        self.isBase64Encoded = isBase64Encoded
        self.statusCode = statusCode
        self.headers = headers

    def json(self):
        _json_output = dict(
            statusCode=self.statusCode
        )
        _body = dict()
        for key in ["data", "message"]:
            _prop = getattr(self, key, None)
            if _prop:
                _body[key] = _prop
        _json_output["body"] = json.dumps(_body)
        return _json_output
