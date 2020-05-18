import boto3
import hyron
import tempfile
from botocore.exceptions import ClientError
from .operation import Operation
from ..errors import ValidationError


class S3PublishArtifacts(Operation, register="s3publish"):
    """
        Package all artifacts in a rulebook and publish them to Amazon S3.
        Filename format will be prefix/artifactname.tar.gz
        Usage: hyrontools publish [rulebookfile] [bucket] [prefix]
    """

    ARGC = 3

    @staticmethod
    def get_key(prefix, filename):
        return f"{prefix}/{filename}"

    def get_s3_resource(self):
        aws = boto3.Session()
        return aws.resource("s3")

    def prepare_args(self, args: tuple):
        loader = hyron.rulebooks.RulebookLoader()
        resource = self.get_s3_resource()

        return {
            "rulebook": loader.load(args[0]),
            "bucket": resource.Bucket(args[1]),
            "prefix": args[2]
        }

    def postvalidate(
            self,
            rulebook: hyron.rulebooks.Rulebook,
            bucket,
            prefix: str):
        self.assert_artifacts(rulebook)
        try:
            bucket.put_object(
                Key=self.get_key(
                    prefix,
                    ".test"),
                Body=b"test",
                ACL="bucket-owner-full-control")
        except ClientError:
            raise ValidationError(
                f"Unable to write to {bucket.name}, check your credentials.",
                False
            )

    def run(self, rulebook: hyron.rulebooks.Rulebook, bucket, prefix: str):
        self.console.print("Rendering all artifacts...")
        artifacts = rulebook.build_all()
        count = len(artifacts)
        self.console.print(f"Rendering complete: {count} artifacts created.")
        self.console.newln()
        self.console.print("Starting package and publish sequence")
        with tempfile.TemporaryDirectory() as tmpdir:
            for job, (name, artifact) in enumerate(artifacts.items()):
                self.console.print(
                    f"Beginning processing for '{name}' artifact.")
                key = self.get_key(prefix, f"{name}.tar.gz")
                local_package = artifact.to_archive(tmpdir)
                self.console.print(f"Package built: {local_package}")
                self.console.print(
                    f"Uploading package to s3://{bucket.name}/{key}...")
                with open(local_package, "rb") as infile:
                    bucket.put_object(
                        Key=key, Body=infile, ACL="bucket-owner-full-control")
                self.console.print(
                    f"Upload complete - {job+1}/{count} packages have been published."  # noqa
                )
        self.console.print("All packages have been published")
