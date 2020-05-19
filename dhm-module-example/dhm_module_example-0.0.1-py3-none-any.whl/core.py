"""DHM Module example plugin."""
import logging
import click
from dhm_module_example import options

# Logger inherits color options from base_module
logger = logging.getLogger(__name__)


@click.command()
@click.argument("prop", type=str)
@click.option("-s", "--section", default="DEFAULT")
@click.pass_context
def configuration(ctx, section, prop):
    """Example command configuration.

    Use @click.pass_context to get the CLI context. The CLI context contains the configuration object
    """
    # The config object from the current context inherited from the base CLI
    config = ctx.obj["config"]

    click.echo(config.get(section, prop))


@click.command()
@click.argument("infile", type=click.File("rb"), nargs=-1)
@click.argument("outfile", type=click.File("wb"))
def inout(infile, outfile):
    """Example command inout.

    Writes the contents of infile to outfile. If outfile does not exist it is created,
    if it exists it is overwritten only if --overwrite is set explicitly to true.
    """
    for f in infile:
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            outfile.write(chunk)
            outfile.flush()


@click.command()
@click.argument("instream", type=click.File("rb"))
@click.argument("outstream", type=click.File("wb"))
@options.srs_opt  # Defined in options as a custom click option
@click.option(
    "-c",  # Shortname
    "--color",  # longname also used as argument name in command
    type=str,  # Datatype
    required=False,
    default="white",
    help="Color the output, with a click option",
)
def pipe(instream, outstream, srs, color="white"):
    """Example of a custom options handler being used along with a stream/file.

    Files can be opened for reading or writing.
    The special value - indicates stdin or stdout depending on the mode.

    Example: dhm_module_base proj --srs epsg:25832 - ./srs.txt

    Args:
        instream (click.File): click.File opened in binary mode, can be stdin depending on mode
        outstream ([type]): click.File opened in binary mode, can be stdout depending on mode
        srs (osr.SpatialReference): osr spatial reference
        color (str): Optional color to color the click output
    """
    click.echo(click.style("Here is your srs: %s" % srs, fg=color))
    click.echo(click.style("Writing it to the stream.", fg=color))
    outstream.write(str(srs).encode())
    while True:
        chunk = instream.read(1024)
        # Do something with either the stream or the srs
        # ...
        if not chunk:
            break
        # This can be stdout or a file
        outstream.write(chunk)
