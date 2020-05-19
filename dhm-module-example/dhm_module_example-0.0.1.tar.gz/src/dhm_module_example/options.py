import logging
import click
from osgeo import osr


logger = logging.getLogger(__name__)


def srs_handler(_ctx, param, value):
    """Handle srs as a click.option callback enabling custom option validation.

    Args:
        _ctx (click.Context): The context holds the state for the script execution at every single level. (UNUSED)
        param (str): The parameter used (ie. --srs)
        value (str): The value for the parameter (ie. EPSG:25832)

    Raises:
        ValueError: Raised when an operation or function receives an argument that has the right type but an inappropriate value

    Returns:
        srs: The corrected osr.SpatialReference()
    """
    logger.debug("click.option callback for param: %s and value: %s", param, value)
    out_srs = osr.SpatialReference()
    out_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    if out_srs.SetFromUserInput(value) != 0:
        raise ValueError("Failed to process SRS definition: %s" % value)
    return out_srs


srs_opt = click.option(
    "--srs",
    type=str,
    required=True,
    callback=srs_handler,
    help=(
        "Spatial reference system. Can be a full WKT definition (hard to escape properly),"
        " or a well known definition (i.e. EPSG:4326) or a file with a WKT definition."
    ),
)
