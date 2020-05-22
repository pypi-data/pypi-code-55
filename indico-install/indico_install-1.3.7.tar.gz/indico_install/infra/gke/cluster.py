import sys
import time
import click
from indico_install.utils import run_cmd
from indico_install.cluster_manager import ClusterManager


@click.group("cluster")
@click.pass_context
def cluster(ctx):
    """
    Manage up and down state of cluster
    """
    pass


def get_node_pools_for_scaling(cluster_name):
    cluster_found = run_cmd(
        "gcloud container clusters list"
        " --filter=resourceLabels.ephemeral=true"
        f" --filter name={cluster_name}"
        " 2> /dev/null"
        " | tail -n 1 | awk '{print $1}'",
        silent=True,
    )

    if cluster_found != cluster_name:
        raise click.UsageError(
            f"Ephemeral Cluster {cluster_name} not found. Found {cluster_found}"
        )

    return run_cmd(
        f"gcloud container node-pools list"
        f" --cluster={cluster_name}"
        ' --quiet --format="value(name)"',
        silent=True,
    ).splitlines()


def wait_status(cluster_name):
    while True:
        status = run_cmd(
            f"gcloud container clusters describe {cluster_name}"
            f" --format 'value(status)'"
            f" --quiet",
            silent=True,
        ).lower()

        if status == "running":
            return
        elif status == "reconciling":
            pass
        else:
            click.secho(f"Unrecognized status: {status}", fg="yellow")

        time.sleep(5)


@cluster.command("up")
@click.option("-c", "--cluster-name", required=True, help="Name of cluster")
@click.pass_context
def up(ctx, cluster_name):
    """
    Turn scale existing node pools back up from down state by configuration or defaults
    Example Config:
    nodePools:
        default-gpu-pool:
            size: 2
            autoscale: false
        default-gpu-pvm-pool:
            size: 0
            autoscale:
                min: 0
                max: 6
        default-pool:
            size: 2
            autoscale: false
        default-pvm-pool:
            size: 0
            autoscale:
                min: 0
                max: 6
    """
    config = ClusterManager().to_dict()
    node_pool_configs = config["cluster_config"].get("nodePools", {})
    node_pools = get_node_pools_for_scaling(cluster_name)

    for pool in node_pools:
        wait_status(cluster_name)
        pool_config = node_pool_configs.get(pool)
        if pool_config is None:
            pool_config = {
                "size": 0 if "pvm" in pool else 2,
                "autoscale": {"min": 0, "max": 6} if "pvm" in pool else False,
            }

        run_cmd(
            f"gcloud container clusters resize {cluster_name}"
            f" --node-pool={pool}"
            f" --num-nodes={pool_config['size']}"
            " --quiet"
        )

        autoscale_config = pool_config["autoscale"]
        if autoscale_config:
            max_size = autoscale_config["max"]
            min_size = autoscale_config["min"]
            wait_status(cluster_name)
            run_cmd(
                f"gcloud container clusters update {cluster_name}"
                f" --node-pool={pool}"
                " --enable-autoscaling"
                f" --max-nodes {max_size}"
                f" --min-nodes {min_size}"
                " --quiet"
            )


@cluster.command("down")
@click.option("-c", "--cluster-name", required=True, help="Name of cluster")
@click.pass_context
def down(ctx, cluster_name):
    """
    Turn scale existing node pools down from up state
    """
    node_pools = get_node_pools_for_scaling(cluster_name)
    for pool in node_pools:
        wait_status(cluster_name)
        run_cmd(
            f"gcloud container clusters update {cluster_name}"
            f" --node-pool={pool}"
            " --no-enable-autoscaling"
            " --quiet"
        )

        wait_status(cluster_name)
        run_cmd(
            f"gcloud container clusters resize {cluster_name}"
            f" --node-pool={pool}"
            " --num-nodes=0"
            " --quiet"
        )
