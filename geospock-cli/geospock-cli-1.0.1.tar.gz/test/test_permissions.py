# Copyright (c) 2014-2020 GeoSpock Ltd.

from geospock_cli.geospockcli import *
from click.testing import CliRunner


def test_ingest():
    runner = CliRunner()
    result = runner.invoke(run, ["dataset-create", "--profile", "local", "--dataset-id", "tweets", "--data-url", "s3://geospock-shared-vis-demo-data/tweet.txt", "--schema-file", "~/tweetSchema.json", "--cluster-size", "XSMALL"])
    jsonoutput = json.loads(result.output)
    items = jsonoutput["newDataset"]
    assert len(items) > 0
    if len(items) > 0:
        assert items[0]["id"] is not None

def test_create_group():
    runner = CliRunner()
    result = runner.invoke(run, ["groups-create", "--profile", "local", "--group-name", "datasetAccess"])
    jsonoutput = json.loads(result.output)
    assert len(jsonoutput) > 0

def test_add_username_to_group():
    runner = CliRunner()
    result = runner.invoke(run, ["groups-add-account", "--profile", "local", "--group-name", "datasetAccess", "--account-username", "test@geospock.com"])
    jsonoutput = json.loads(result.output)
    assert len(jsonoutput) > 0

def test_dataset_permissions_grant():
    runner = CliRunner()
    result = runner.invoke(run, ["dataset-permission-grant", "--profile", "local", "--dataset-id", "tweets", "--group-name", "datasetAccess"])
    jsonoutput = json.loads(result.output)
    assert len(jsonoutput) > 0
