import math
import os
from pathlib import Path

import boto3
import botocore
import paramiko
from typer import Exit
from wasabi import Printer

from .sftp import SFTP

msg = Printer()


class Hal9000:
    def __init__(self, config, set_up_ssh=False, set_up_sftp=False):
        self.config = config
        self.credentials = self.get_credentials()

        self.ssh_key_path = Path(self.config["ssh_key_path"]).expanduser()
        self.key_name = Path(self.ssh_key_path).name

        boto3.setup_default_session(region_name=self.config["region"])

        self.client = boto3.client(
            "ec2",
            aws_access_key_id=self.credentials["AccessKeyId"],
            aws_secret_access_key=self.credentials["SecretAccessKey"],
            aws_session_token=self.credentials["SessionToken"],
        )
        self.resource = boto3.resource(
            "ec2",
            aws_access_key_id=self.credentials["AccessKeyId"],
            aws_secret_access_key=self.credentials["SecretAccessKey"],
            aws_session_token=self.credentials["SessionToken"],
        )

        self.volume = self.get_volume(self.config["volume_id"])

        # if an instance is already running, assign it to the controller
        try:
            self.instance = self.get_running_instances()

            # set up connections to instance if required
            if set_up_sftp or set_up_ssh:
                self.ssh = self.set_up_ssh(self.instance)
                if set_up_sftp:
                    self.sftp = SFTP(self.ssh)
                else:
                    self.sftp = None
            else:
                self.ssh, self.sftp = None, None

        except AttributeError:
            self.instance, self.ssh, self.sftp = None, None, None

    def get_running_instances(self):
        """
        Returns any instances which are already running
        """
        try:
            instances = list(
                self.resource.instances.filter(
                    Filters=[
                        {"Name": "tag:hal", "Values": ["true"]},
                        {
                            "Name": "tag:username",
                            "Values": [self.config["username"]],
                        },
                        {"Name": "instance-state-name", "Values": ["running"]},
                    ]
                )
            )
            if len(instances) == 0:
                raise AttributeError("No running instances!")
        except TypeError:
            raise AttributeError("No running instances!")

        instance = list(instances)[0]
        return instance

    def get_credentials(self):
        sts = boto3.client("sts")
        try:
            assumed_role_object = sts.assume_role(
                RoleArn=self.config["role_arn"], RoleSessionName="session",
            )
        except botocore.exceptions.ClientError:
            msg.fail("The AWS credentials for this profile have expired!")
            msg.fail("Aborted!")
            raise Exit()

        return assumed_role_object["Credentials"]

    def get_spot_price(self, instance_type, multiplier=1.1):
        """
        Returns a bid base on the most recent spot price history for
        the specified instance_type
        """
        response = self.client.describe_spot_price_history(
            InstanceTypes=[instance_type],
            MaxResults=1,
            ProductDescriptions=["Linux/UNIX (Amazon VPC)"],
            AvailabilityZone=self.config["region"] + "b",
        )

        base_price = float(response["SpotPriceHistory"][0]["SpotPrice"])
        # multiply base price by factor (default 1.1x), rounded up to 2dp
        bid_price = math.ceil(base_price * multiplier * 100.0) / 100.0
        return bid_price

    def construct_spot_launch_spec(self, instance_type):
        """
        Builds a launch specification for a spot instance request with a
        specified instance type and a small ephemeral EBS volume.
        """
        launch_spec = {
            "ImageId": self.config["image_id"],
            "InstanceType": instance_type,
            "KeyName": self.key_name,
            "IamInstanceProfile": {"Arn": self.config["instance_profile_arn"]},
            "NetworkInterfaces": [
                {
                    "DeviceIndex": 0,
                    "SubnetId": self.config["subnet_id"],
                    "Groups": [self.config["security_group"]],
                    "AssociatePublicIpAddress": True,
                }
            ],
        }
        return launch_spec

    def create_instance(self, instance_type, instance_name, spot_price):
        """
        Makes a spot request for an specified instance type, at a specified
        price, and tags it with a name
        """
        if self.instance:
            msg.warn("It looks like you already have an instance running!")
            self.describe_instances()
            msg.fail("Aborted!")
            raise Exit()

        with msg.loading(f"Creating a {instance_type} instance"):
            launch_spec = self.construct_spot_launch_spec(instance_type)

            request_id = self.client.request_spot_instances(
                LaunchSpecification=launch_spec,
                InstanceInterruptionBehavior="terminate",
                SpotPrice=str(spot_price),
                Type="one-time",
            )["SpotInstanceRequests"][0]["SpotInstanceRequestId"]

            self.client.get_waiter("spot_instance_request_fulfilled").wait(
                SpotInstanceRequestIds=[request_id],
                WaiterConfig={"Delay": 3, "MaxAttempts": 20},
            )

            instance_id = self.client.describe_spot_instance_requests(
                SpotInstanceRequestIds=[request_id]
            )["SpotInstanceRequests"][0]["InstanceId"]

            self.client.get_waiter("instance_running").wait(
                InstanceIds=[instance_id],
                WaiterConfig={"Delay": 3, "MaxAttempts": 20},
            )

            self.client.create_tags(
                Resources=[instance_id],
                Tags=[
                    {"Key": "instance_name", "Value": instance_name},
                    {"Key": "hal", "Value": "true"},
                    {"Key": "spot_price", "Value": str(spot_price)},
                    {"Key": "username", "Value": self.config["username"]},
                ],
            )

            instance = self.get_instance(instance_id)

        msg.good(f"Successfully created a {instance_type} instance")
        return instance

    def start_instance(self, instance_type, instance_name, spot_price=None):
        """
        Starts a specified instance type with an optionally dynamically
        calculated spot price, based on the most recent available data
        """
        if not spot_price:
            spot_price = self.get_spot_price(instance_type)

        self.instance = self.create_instance(
            instance_type, instance_name, spot_price
        )
        self.describe_instances()
        self.ssh = self.set_up_ssh(self.instance)
        self.attach_volume()
        self.mount_volume()
        self.fix_dns()
        self.start_jupyterlab()

    def describe_instances(self):
        """
        Displays the status of a running instance
        """
        if self.instance:
            msg.table(
                {
                    "Instance ID": self.instance.instance_id,
                    "Instance name": [
                        tag["Value"]
                        for tag in self.instance.tags
                        if tag["Key"] == "instance_name"
                    ][0],
                    "User name": [
                        tag["Value"]
                        for tag in self.instance.tags
                        if tag["Key"] == "username"
                    ][0],
                    "Spot price": "£"
                    + [
                        tag["Value"]
                        for tag in self.instance.tags
                        if tag["Key"] == "spot_price"
                    ][0],
                    "State": self.instance.state["Name"],
                },
                header=["Instance details:", ""],
            )
        else:
            msg.good("There are currently no running instances!")

    def get_instance(self, instance_id):
        """
        Returns a specified EC2 instance object which can be subsequently
        manipulated
        """
        response = self.resource.instances.filter(
            Filters=[{"Name": "instance-id", "Values": [instance_id]}]
        )
        return next(iter(response))

    def shut_down_instance(self):
        if self.instance:
            with msg.loading("Shutting down instance"):
                instance_id = self.instance.id
                self.instance.terminate()
            msg.good(f"Successfully shut down instance: {instance_id}")
        else:
            msg.fail("There are currently no running instances!")
            msg.fail("Aborted!")
            raise Exit()

    def set_up_ssh(self, instance):
        """
        Return a paramiko SSH connection objected connected to the instance
        """
        with msg.loading("Creating an SSH connection to the instance"):
            key = paramiko.RSAKey.from_private_key_file(
                self.ssh_key_path, password=self.config["ssh_password"]
            )
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                client.connect(
                    hostname=instance.public_ip_address,
                    username="ec2-user",
                    pkey=key,
                    password=self.config["ssh_password"],
                )
                client.raise_stderr = True
            except paramiko.ssh_exception.NoValidConnectionsError:
                msg.fail(
                    "Couldn't establish an SSH connection to the instance!"
                )
                msg.fail("Aborted!")
                raise Exit()

        msg.good("Successfully created an SSH connection to the instance")
        return client

    def run_command_on_instance(self, command):
        """
        Run a command on the remote instance via SSH
        """
        _, stdout, stderr = self.ssh.exec_command(command)
        stdout_str = stdout.read().decode()
        stderr_str = stderr.read().decode()
        if stdout.channel.recv_exit_status() != 0:
            raise Exception(stderr_str)
        if self.ssh.raise_stderr:
            if stderr_str:
                raise Exception(stderr_str)
            return stdout_str
        return stdout_str, stderr_str

    def get_volume(self, volume_id):
        """
        Returns a specified EBS volume object which can be subsequently
        manipulated
        """
        response = self.resource.volumes.filter(
            Filters=[{"Name": "volume-id", "Values": [volume_id]}]
        )
        return next(iter(response))

    def attach_volume(self):
        try:
            with msg.loading("Attaching your storage volume to the instance"):
                self.volume.attach_to_instance(
                    Device="/dev/xvdf", InstanceId=self.instance.id
                )
                self.client.get_waiter("volume_in_use").wait(
                    VolumeIds=[self.volume.id],
                    WaiterConfig={"Delay": 3, "MaxAttempts": 20},
                )
        except:  # noqa: E722
            msg.fail("Failed to attach your storage volume to the instance")
        msg.good("Successfully attached your storage volume to the instance")

    def mount_volume(self):
        try:
            with msg.loading("Mounting your storage volume to the instance"):
                commands = [
                    "sudo mkdir /storage",
                    "sudo mount /dev/xvdf /storage",
                ]
                for command in commands:
                    self.run_command_on_instance(command)
        except:  # noqa: E722
            msg.fail("Failed to mount your storage volume to the instance")
        msg.good("Successfully mounted your storage volume to the instance")

    def detach_volume(self):
        with msg.loading(
            "Unmounting and detaching your storage volume from the instance"
        ):
            self.run_command_on_instance("sudo umount -d /dev/xvdf")
            self.volume.detach_from_instance()
            self.client.get_waiter("volume_available").wait(
                VolumeIds=[self.volume.id],
                WaiterConfig={"Delay": 3, "MaxAttempts": 20},
            )
        msg.good(
            "Successfully unmounted and detached your storage volume "
            "from the instance"
        )

    def start_jupyterlab(self):
        os.system(
            f"ssh ec2-user@{self.instance.public_ip_address} "
            f"-i {self.ssh_key_path} -NfL 8888:localhost:8888"
        )

        self.run_command_on_instance(
            "nohup jupyter lab --no-browser "
            '--port=8888 --notebook-dir="/storage" &'
        )

    def open_connection_to_instance(self):
        """
        Replaces the current python process with an SSH process connected
        to the specified instance.
        """
        os.system(
            f"ssh ec2-user@{self.instance.public_ip_address} "
            f"-i {self.ssh_key_path} -L 8888:localhost:8888"
        )

    def put(self, local_path, remote_path):
        self.sftp.put(local_path, remote_path)

    def get(self, local_path, remote_path):
        self.sftp.get(local_path, remote_path)

    def fix_dns(self):
        self.run_command_on_instance("sudo chmod a+rwx /etc/resolv.conf")
        self.run_command_on_instance(
            'printf "nameserver 169.254.169.253" >> /etc/resolv.conf'
        )
