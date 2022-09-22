SFN_EXECUTION_CONTEXT = {
  'Execution': {
    'Id': '2arn:aws-cn:states:cn-north-1:843403612003:execution:IMS-AWS-Create-Environment:473b5768-fa4d-4a22-958d-6ee910cdff65',
    'Input': {
      'input': {
        'accountId': '843064179036',
        'image': '',
        'envState': 'pending-approval',
        'updatedBy': {
          'code': 'LANLIU'
        },
        'isProduction': False,
        'size': 'small',
        'projectCode': 'oap2',
        'envName': 'hahhaha',
        'envId': '9f18b61bc3c35f00b45b42a1f193976c',
        'platform': 'AWS',
        'updatedAt': '2022-09-02 14:53:41'
      }
    },
    'Name': '473b5768-fa4d-4a22-958d-6ee910cdff65',
    'RoleArn': 'arn:aws-cn:iam::843403612003:role/service-role/StepFunctions-AWS-Resource-Deployment-role-991b04a1',
    'StartTime': '2022-09-02T06:53:43.934Z'
  },
  'StateMachine': {
    'Id': 'arn:aws-cn:states:cn-north-1:843403612003:stateMachine:IMS-AWS-Create-Environment',
    'Name': 'IMS-AWS-Create-Environment'
  },
  'State': {
    'Name': 'Parse Input',
    'EnteredTime': '2022-09-02T06:53:43.970Z',
    'RetryCount': 0
  }
}

AVAILABILITY_ZONE_LIST = [
    'cn-north-1a', 'cn-north-1b','cn-north-1d'
]

NETWORK_SIZE = {
    "small":24,
    "middle":23,
    "large":22
}

NETWORK_CONFIG = {
    "account": {
        "Id": "076513887860",
        "projectCode": "salessvc",
        "envName": "prod"
    },
    "params": {
        "cidrBlocks": [
            "10.200.184.0/23"
        ],
        "tgwAttachments": [
            {
                "transitGatewayId": "tgw-0592595280677252f"
            }
        ],
        "domainName": "cn133.aws.cn",
        "dnsServers": [
            "10.200.21.164",
            "10.200.21.148"
        ]
    }
}