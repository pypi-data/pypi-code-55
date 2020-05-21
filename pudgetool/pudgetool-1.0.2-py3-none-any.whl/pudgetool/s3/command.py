import click
from . import utils

params = {
    "endpoint_url": "http://ceph-s3.rokid-inc.com:8443",
    "access_key": "Z4UYWCVHBN6L6CVLKPYG",
    "secret_key": "ldiCSWX6raIcAeubEcp7pQs8uC2ipgtzOfRgM9QL"
}

@click.group()
def s3():
    pass

@s3.group()
def buckets():
    pass

@buckets.command()
@click.option('--name', '-n', help='bucket name')
def create(name):
    pass

@buckets.command()
@click.option('--name', '-n', help='bucket name')
def delete(name):
    pass

@buckets.command()
@click.option('--name', '-n', help='bucket name')
def list(name):
    pass

@s3.group()
def objects():
    pass

@objects.command()
@click.option('--bucket', '-b', help='bucket name')
@click.option('--prefix', '-p', help='prefix path')
@click.option('--file', '-f', help='file name')
def put(bucket, prefix, file):
    import os
    s3c = utils.get_s3client(params["endpoint_url"], params["access_key"], params["secret_key"])
    file_name = os.path.basename(file)
    with open(file, 'rb') as f:
        s3c.upload_fileobj(f, bucket, file_name)

@objects.command()
@click.option('--bucket', '-b', help='bucket name')
@click.option('--prefix', '-p', default="", help='prefix path')
@click.option('--file', '-f', help='file name')
def get(bucket, prefix, file):
    s3c = utils.get_s3client(params["endpoint_url"], params["access_key"], params["secret_key"])
    with open(file, 'wb') as f:
        s3c.download_fileobj(bucket, file, f)

@objects.command()
@click.option('--bucket', '-b', help='bucket name')
@click.option('--prefix', '-p', help='prefix path')
def list(bucket, prefix):
    pass
