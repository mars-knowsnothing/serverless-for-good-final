import os
import json
import logging
import os
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime, timezone, timedelta
from resources.decimal_encoder import DecimalEncoder
from utilities.aws_utils import AWSUtils

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Resource(object):

    def __init__(self, resourceId=None , *args, **kwargs):
        self.name = kwargs.pop("name","resource").replace(".","_")
        self.logger = logger
        self.stage = os.getenv("stage","dev")
        self.utils = AWSUtils(aws_access_key_id=os.getenv("ak"),aws_secret_access_key=os.getenv("sk"),region_name=os.getenv("region","ap-southeast-1"))
        self.dynamodb = self._ddb()
        try:
            self.table = self.dynamodb.Table('cmdb_{stage}_{name}'.format(stage=self.stage,name=self.name))
        except Exception as e:
            self.logger.info(e)
            raise e
        self.resourceId = resourceId
        self.pk = [k["AttributeName"] for k in self.table.key_schema if k["KeyType"]=="HASH"].pop()
        self.TIME_ZONE = timezone(timedelta(hours=8))
        self._handlers = {}
        self._props = {}
        self._options = kwargs.pop("options",{})
        for key,value in kwargs.items():
            setattr(self,key,value)
            self._props[key]=value
        self.API_GATEWAY_RESPONSE_SCHEMA = {
            "cookies" : [type("cookie1"),type("cookie2")],
            "isBase64Encoded": type(True),
            # "statusCode": type(200),
            "headers": type({"headername":"headervalue"}),
            # "body": type(json.dumps({"key":"value"}))
        }


    def to_dict(self):
        return self._props

    def to_json(self):
        return json.dumps(self._props)

    def _ddb(self):
        if not getattr(self,"dynamodb",None):
            return self.utils.session.resource('dynamodb')
        else:
            return self.dynamodb

    def register_apis(self,APIs):
        for api in APIs:
            self.Register(api["resource"],api["httpMethod"],getattr(self,api["func"]))

    def API(self,event,options=None):
        resource = event["resource"]
        httpMethod = event["httpMethod"]
        handler = self._handlers.get(resource).get(httpMethod)
        api_gateway_event = dict()

        pathParameters=event.get("pathParameters")
        if not pathParameters:
            pathParameters=dict()
        api_gateway_event["resources"]=pathParameters

        queryStringParameters=event.get("queryStringParameters")
        if not queryStringParameters:
            queryStringParameters=dict()
        api_gateway_event["filters"]=queryStringParameters

        payload = event.get("body")
        if not payload:
            payload=json.dumps(dict())
        payload=json.loads(payload)
        api_gateway_event["payload"]=payload
        try:
            resp = handler(event=api_gateway_event)
        except ClientError as ce:
            resp =  dict(
                code=ce.response["ResponseMetadata"]["HTTPStatusCode"],
                data=ce.response['Error'],
                messages=[ce.response["Error"]["Message"]]
            )
        # add cors headers
        resp.update({"headers":{
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,DELETE,PUT'
        }})
        return self.Response(resp)

    def DynamoDBUpdateExpression(self,payload,disabled=[]):
        UpdateExpressionList = []
        ExpressionAttributeValues = dict()
        for key,value in payload.items():
            if key not in disabled:
                UpdateExpressionList.append("{fieldName} = :val_{fieldName}".format(fieldName=key))
                ExpressionAttributeValues.update({
                    ":val_{fieldName}".format(fieldName=key):value
                })
        UpdateExpression = "SET "+", ".join(UpdateExpressionList)
        return UpdateExpression,ExpressionAttributeValues

    def DynamoDBFilters(self,queryStringParameters):
        FilterExpression = None
        for f,v in queryStringParameters.items():
            if not FilterExpression:
                if f.endswith(".contains"):
                    FilterExpression=Attr(f.split('.contains')[0]).contains(v)
                elif f.endswith(".notcontains"):
                    FilterExpression = ~Attr(f.split('.notcontains')[0]).contains(v.split(',')[0])
                    for item in v.split(',')[1:]:
                        FilterExpression=FilterExpression & ~Attr(f.split('.notcontains')[0]).contains(item)
                else:
                    FilterExpression=Attr(f).eq(v)
            else:
                if f.endswith(".contains"):
                    FilterExpression=FilterExpression & Attr(f.split('.contains')[0]).contains(v)
                elif f.endswith(".notcontains"):
                    for item in v.split(','):
                        FilterExpression=FilterExpression & ~Attr(f.split('.notcontains')[0]).contains(item)
                else:
                    FilterExpression=FilterExpression & Attr(f).eq(v)
        return FilterExpression

    def Response(self,handlerResponse):
        _resp = dict()
        _resp["statusCode"] = handlerResponse.get("code",200)
        _resp_body_json = dict(
            data=handlerResponse.get("data",[]),
            messages=handlerResponse.get("messages",[])
        )
        _resp["body"] = json.dumps(_resp_body_json)
        for key in self.API_GATEWAY_RESPONSE_SCHEMA.keys():
            if key in handlerResponse:
                _resp[key]=handlerResponse[key]
        return _resp
    
    def Register(self,resource,httpMethod,func):
        if not self._handlers.get(resource):
            self._handlers[resource] = {
                httpMethod:func
            }
        else:
            self._handlers[resource].update({
                httpMethod:func
            })

    def api_create(self,event:dict,**kwargs) -> dict:
        resp_api_create = self.create(obj=event["payload"])
        return resp_api_create

    def create(self, obj, **kwargs):
        try:
            now = datetime.utcnow().astimezone(self.TIME_ZONE)
            created_at = updated_at = now.strftime("%Y-%m-%d %H:%M:%S")
            assert self.pk in obj, "Primary key is missing, please check"
            _ = obj.copy()
            _["updatedAt"] = updated_at
            _["createdAt"] = created_at
            for key,value in _.items():
                setattr(self,key,value)
                self._props[key]=value
            response = self.table.put_item(
                Item=_,
                ConditionExpression = "attribute_not_exists({pk})".format(pk=self.pk)
            )
            return dict(
                code=response["ResponseMetadata"]["HTTPStatusCode"],
                data=_,
                messages = []
            )
        except ClientError as ce:
            return dict(
                code=ce.response["ResponseMetadata"]["HTTPStatusCode"],
                data=ce.response['Error'],
                messages=[ce.response["Error"]["Message"]]
            )

    def update(self, resourceId, obj):
        try:
            now = datetime.utcnow().astimezone(self.TIME_ZONE)
            updated_at = now.strftime("%Y-%m-%d %H:%M:%S")
            _ = obj.copy()
            _["updatedAt"] = updated_at
            UpdateExpression,ExpressionAttributeValues = self.DynamoDBUpdateExpression(payload=_,disabled=["envName","appName","projectCode","scaffoldName","platform","appId"])
            response = self.table.update_item(
                Key={
                    self.pk:resourceId
                },
                UpdateExpression=UpdateExpression,
                ExpressionAttributeValues=ExpressionAttributeValues
            )
            return dict(
                code=response["ResponseMetadata"]["HTTPStatusCode"],
                data=_,
                messages = []
            )
        except ClientError as ce:
            if ce.response["Error"]["Message"]=="The conditional request failed":
                return dict(
                    code=ce.response["ResponseMetadata"]["HTTPStatusCode"],
                    data=ce.response['Error']["Code"],
                    messages=["The conditional request failed","Resource with id {resourceId} does not exist".format(resourceId=resourceId)]
                )
            else:
                return dict(
                    code=ce.response["ResponseMetadata"]["HTTPStatusCode"],
                    data=ce.response['Error'],
                    messages=[ce.response["Error"]["Message"]]
                )

    def get(self,resourceId):
        try:
            response = self.table.get_item(
                Key={
                    self.pk:resourceId
                }
            )
            if not response.get("Item"):
                return dict(
                    code=404,
                    data=None,
                    messages=[]
                )
            else:
                return dict(
                    code=response["ResponseMetadata"]["HTTPStatusCode"],
                    data=response["Item"],
                    messages=[]
                )
        except ClientError as ce:
            if ce.response['Error']["Code"]=="ValidationException" and ce.response['Error']["Message"]=="The provided key element does not match the schema":
                return dict(
                    code=ce.response["ResponseMetadata"]["HTTPStatusCode"],
                    data=ce.response['Error'],
                    messages=[ce.response["Error"]["Message"],"check the type of resource id, should match the schema"]
                )
            else:
                return dict(
                    code=ce.response["ResponseMetadata"]["HTTPStatusCode"],
                    data=ce.response['Error'],
                    messages=[ce.response["Error"]["Message"]]
                )

    def list(self, event:dict, **kwargs)->dict:
        scan_params = dict()
        filters = event.get("filters")
        if filters:
            scan_params["FilterExpression"]=self.DynamoDBFilters(filters)
        data = list()
        response = self.table.scan(
            **scan_params
        )
        data.extend(response['Items'])
        while 'LastEvaluatedKey' in response:
            response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'],**scan_params)
            data.extend(response['Items'])
        return dict(
            code=response["ResponseMetadata"]["HTTPStatusCode"],
            data=data,
            messages=[]
        )

    def _from_ddb(self, resourceId, **kwargs):
        resp = self.get(resourceId=resourceId)
        if resp["code"] == 200:
            item = resp["data"]
        elif resp["code"] == 404:
            _ = self._props.copy()
            assert self.pk in _, "Primary key is missing, please check"
            resp_create = self.create(obj=_)
            item = resp_create["data"]
            # self.logger.info(item)
        for key, value in item.items():
            setattr(self, key, value)
            self._props[key]=value
        return item