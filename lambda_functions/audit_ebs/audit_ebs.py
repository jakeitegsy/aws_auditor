import boto3
from botocore.exceptions import ClientError, NoCredentialsError

from datetime import datetime

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

def get_volumes():
    return (volume for volume in ec2.describe_volumes()['Volumes'])

def write_ebs_details_to_dynamodb():
    for volume in get_volumes():
        item=Ebs(volume).to_dict()
        try:
            print("[INFO] Writing item ", item, "to DynamoDB")
            dynamodb.Table("cdm_audit_ebs").put_item(Item=item)
        except ClientError as error:
            print("[ERROR ]Failed to write ", item , "to DynamoDB because", error)

def delete_error_message(id, error):
    print(f"Could not delete {id} because {errror}")

def delete_snapshot(id):
    try:
        return ec2.delete_snapshot(SnapshotId=id)
    except ClientError as error:
        delete_error_message(id, error)

def delete_volume(id):
    try:
        return ec2.delete_volume(VolumeId=id)
    except ClientError as error:
        delete_error_message(id, error)

def delete_unattached_volumes():
    for details in get_volumes():
        volume = Ebs(details)
        if volume.instance_id() is None:
            delete_volume(volume.volume_id())
            delete_snapshot(volume.snapshot_id())

def handler(event, context):
    delete_unattached_volumes()
    write_ebs_details_to_dynamodb()


class Ebs:

    def __init__(self, dictionary):
        self.dictionary = dictionary

    def getter(self, dictionary, key):
        try:
            return dictionary[key]
        except (KeyError, TypeError):
            return

    def get(self, key):
        return self.getter(self.dictionary, key)

    def get_attachments(self, key):
        try:
            return self.getter(self.get('Attachments')[0], key)
        except IndexError:
            return

    def volume_id(self):
        return self.get("VolumeId")

    def iops(self):
        return self.get("Iops")

    def availability_zone(self):
        return self.get("AvailabilityZone")

    def date_created(self):
        return self.get("CreateTime").strftime("%Y-%m-%dT%H:%M:%SZ")

    def encrypted(self):
        return self.get("Encrypted")

    def instance_id(self):
        return self.get_attachments('InstanceId')

    def kms_key_id(self):
        return self.get('KmsKeyId')

    def size_in_gib(self):
        return self.get('Size')

    def snapshot_id(self):
        return self.get('SnapshotId')

    def state(self):
        return self.get('State')

    def attached(self):
        return self.get_attachments('State')

    def volume_type(self):
        return self.get('VolumeType')

    def tags(self):
        return self.get('Tags')

    def get_instance_tags(self):
        try:
            return ec2.describe_instances(InstanceIds=[self.instance_id()])['Reservations'][0]['Instances'][0]['Tags']
        except Exception as error:
            print("Could not get Instance Information because", error)

    def get_tag_value(self, function):
        try:
            for tag in function():
                if tag['Key'] == 'Name':
                    return tag['Value']
        except(TypeError, NoCredentialsError) as error:
            return 'NoName'

    def get_instance_name(self):
        return self.get_tag_value(self.get_instance_tags)

    def get_volume_name(self):
        return self.get_tag_value(self.tags)

    def to_dict(self):
        return dict(
            Name=self.get_volume_name(),
            VolumeId=self.volume_id(),
            VolumeType=self.volume_type(),
            Iops=self.iops(),
            SnapshotId=self.snapshot_id(),
            State=self.state(),
            Attached=self.attached(),
            Encrypted=self.encrypted(),
            DateCreated=self.date_created(),
            InstanceName=self.get_instance_name(),
            InstanceId=self.instance_id(),
            AvailabilityZone=self.availability_zone(),
            KmsKeyId=self.kms_key_id(),
            SizeInGib=self.size_in_gib(),
        )

session = boto3.session.Session(region_name=region())
ec2 = create_client("ec2")
dynamodb = create_resource("dynamodb")