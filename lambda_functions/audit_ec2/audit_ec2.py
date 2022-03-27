import boto3

def region():
    return "us-west-2"

def endpoint_url(service):
    return f"https://{service}.{region()}.amazonaws.com"

def create_resource(service):
    return session.resource(
        service, endpoint_url=endpoint_url(service)
    )

def create_client(service):
    return session.client(
        service, endpoint_url=endpoint_url(service)
    )

def get_instance_details(data):
    instance = Instance(data)
    details = instance.to_dict()
    details.update(instance.get_ebs_details())
    return details

def list_instances():
    return (
        instances
        for reservation in ec2_client.describe_instances()['Reservations']
        for instances in reservation['Instances']
    )

def log_instance_details_to_dynamodb():
    for instances in list_instances():
        item=get_instance_details(instances)
        try:
            print("[INFO] Writing item ", item, "to DynamoDB")
            dynamodb.Table("cdm_audit_ec2").put_item(Item=item)
        except ClientError as error:
            print("[ERROR ]Failed to write ", item , "to DynamoDB because", error)

def handler(event, context):
    log_instance_details_to_dynamodb()


class Instance:

    def __init__(self, dictionary):
        self.dictionary = dictionary

    def getter(self, dictionary, key):
        try:
            return dictionary[key]
        except (KeyError, TypeError):
            return

    def get(self, key):
        return self.getter(self.dictionary, key)

    def get_dictionary(self, value, key):
        return self.getter(self.get(value), key)

    def image_id(self):
        return self.get("ImageId")

    def instance_id(self):
        return self.get("InstanceId")

    def instance_type(self):
        return self.get("InstanceType")

    def key_name(self):
        return self.get("KeyName")

    def launch_time(self):
        return self.get("LaunchTime").strftime("%Y-%m-%dT%H:%M:%SZ")

    def availability_zone(self):
        return self.get_dictionary('Placement', 'AvailabilityZone')

    def os(self):
        return self.get("Platform")

    def state(self):
        return self.get_dictionary('State', 'Name')

    def subnet_id(self):
        return self.get("SubnetId")

    def vpc_id(self):
        return self.get("VpcId")

    def role_arn(self):
        return self.get_dictionary('IamInstanceProfile', 'Arn')

    def role_id(self):
        return self.get_dictionary('IamInstanceProfile', 'Id')

    def security_groups(self):
        return self.get('SecurityGroups')

    def tags(self):
        return self.get('Tags')

    def block_device_mappings(self):
        return self.get('BlockDeviceMappings')

    def security_group_ids(self):
        return str([security_group['GroupId'] for security_group in self.security_groups()])

    def security_group_names(self):
        return str([security_group['GroupName'] for security_group in self.security_groups()])
    def cores(self):
        return self.get_dictionary('CpuOptions', 'CoreCount')

    def name(self):
        for tag in self.tags():
            if tag["Key"] == "Name":
                return tag["Value"]

    def volume_ids(self):
        return (volume["Ebs"]["VolumeId"] for volume in self.block_device_mappings())

    def to_dict(self):
        return dict(
            Name=self.name(),
            InstanceId=self.instance_id(),
            SubnetId=self.subnet_id(),
            RoleArn=self.role_arn(),
            RoleId=self.role_id(),
            KeyName=self.key_name(),
            InstanceType=self.instance_type(),
            ImageId=self.image_id(),
            AZ=self.availability_zone(),
            State=self.state(),
            VpcId=self.vpc_id(),
            OS=self.os(),
            Cores=self.cores(),
            SecurityGroupIds=self.security_group_ids(),
            SecurityGroupNames=self.security_group_names()
        )

    def get_ebs_details(self):
        details = {}
        for index, volume_id in enumerate(self.volume_ids()):
            volume = ec2_resource.Volume(volume_id)
            prefix = f"EbsVol_{index}_"
            details[f"{prefix}Id"] = volume_id
            details[f"{prefix}Encrypted"] =  volume.encrypted
            details[f"{prefix}KMSKeyId"] = volume.kms_key_id
            details[f"{prefix}SnapshotId"] = volume.snapshot_id
            details[f"{prefix}State"] = volume.state
        return details

session = boto3.session.Session(region_name=region())
ec2_client = create_client("ec2")
ec2_resource = create_resource("ec2")
dynamodb = create_resource("dynamodb")
