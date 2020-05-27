import json

import boto3


def get_instance(instance_id):
    ec2_resource = boto3.resource("ec2")
    return ec2_resource.Instance(instance_id)


def get_instance_ids(tag_key, tag_value):
    """
    When passed a tag key, tag value this will return a list of InstanceIds that were found.
    """
    ec2_client = boto3.client("ec2")
    response = ec2_client.describe_instances(
        Filters=[
            {
                "Name": "tag:" + tag_key,
                "Values": tag_value
            }
        ]
    )
    results = []
    for reservation in (response["Reservations"]):
        for instance in reservation["Instances"]:
            results.append(instance["InstanceId"])
    return results


def get_public_ip(name):
    result = {"name": name, "public_ip": None}
    instance_ids = get_instance_ids("Name", name)
    if instance_ids:
        result["public_ip"] = get_instance(instance_ids[0]).public_ip_address
    return json.dumps(result)


def find_elastic_ip(public_ip):
    """
    Describes one of your Elastic IP addresses. The address is for use in a VPC
    https://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.Client.describe_addresses
    """
    ec2_client = boto3.client("ec2")
    response = ec2_client.describe_addresses(
        Filters=[
            {
                "Name": "domain",
                "Values": ["vpc"]
            },
        ],
        PublicIps=[public_ip]
    )
    return response


def assign_elastic_ip(elastic_ip, instance_name):
    """
    [EC2-Classic, VPC in an EC2-VPC-only account] If the Elastic IP address is already associated with a different
    instance, it is disassociated from that instance and associated with the specified instance.
    If you associate an Elastic IP address with an instance that has an existing Elastic IP address,
    the existing address is disassociated from the instance, but remains allocated to your account.

    [VPC in an EC2-Classic account] The Elastic IP address is associated with the primary IP address.
    If the Elastic IP address is already associated with a different instance or a network
    interface, you get an error. You cannot associate an Elastic IP address with an instance or network interface
    that has an existing Elastic IP address.

    More details: https://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.Client.associate_address
    """
    eip_info = find_elastic_ip(elastic_ip)
    allocation_id = eip_info["Addresses"][0]["AllocationId"]
    instance_ids = get_instance_ids("Name", instance_name)
    if instance_ids and allocation_id:
        ec2_client = boto3.client("ec2")
        ec2_client.associate_address(
            AllocationId=allocation_id, InstanceId=instance_ids[0])


def has_tags(instance_id, tag_key, tag_values):
    ec2_client = boto3.client("ec2")
    response = ec2_client.describe_tags(
        Filters=[
            {
                "Name": "resource-id",
                "Values": [instance_id]
            }
        ]
    )
    for item in response['Tags']:
        if item['Key'] == tag_key and item['Value'] in tag_values:
            return True
    return False
