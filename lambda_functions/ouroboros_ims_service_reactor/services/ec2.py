# pylama:ignore=E501
from services import Service
from utilities import interceptor


class Instance(Service):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_apis(
            [
                {
                    "resource": "/accounts/{accountid}/services/ec2/instances",
                    "httpMethod": "GET",
                    "func": "list_instances"
                }
            ]
        )

    def register_apis(self, APIs: list) -> None:
        for api in APIs:
            self.register(api["resource"], api["httpMethod"], getattr(self, api["func"]))

    @staticmethod
    def get_filters(filters: dict = {}) -> dict:
        _available_filters = ["vpc-id", "instance-id"]
        _filters = list()
        for k, v in filters.items():
            if k not in _available_filters and k.split(":")[0] not in _available_filters:
                continue
            _filters.append({
                'Name': k,
                'Values': v.split(',')
            })
        return _filters

    @interceptor
    def list_instances(self, event: dict, **kwargs) -> dict:
        instances = list()
        client = self.utils.client("ec2")
        _params_describe_instances = dict(
            Filters=self.get_filters(event.get("filters", {})),
            MaxResults=50
        )
        fields = event.get("fields", None)
        default_fields = ["InstanceId"]
        try:
            _instances_raw = client.describe_instances(**_params_describe_instances)
            for Reservation in _instances_raw["Reservations"]:
                if fields:
                    instances.extend([{key: d.get(key) for key in fields.split(',') + default_fields} for d in Reservation["Instances"]])
                else:
                    instances.extend(Reservation["Instances"])
            while "NextToken" in _instances_raw:
                _instances_raw = client.describe_instances(
                    NextToken=_instances_raw["NextToken"],
                    **_params_describe_instances)
                for Reservation in _instances_raw["Reservations"]:
                    if fields:
                        instances.extend([{key: d.get(key) for key in fields.split(',') + default_fields} for d in Reservation["Instances"]])
                    else:
                        instances.extend(Reservation["Instances"])
        except Exception as e:
            print(e)
            # print(_instances_raw.json())
            return dict(
                code=400,
                message=["failed to describe instances"]
            )
        return dict(
            code=200,
            data=instances
        )
