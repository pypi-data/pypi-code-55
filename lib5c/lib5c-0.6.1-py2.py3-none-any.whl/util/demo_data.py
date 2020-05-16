import os
import zlib
from six.moves.urllib.request import urlopen

from lib5c.contrib.luigi.config import drop_config_file
from lib5c.util.config import parse_config
from lib5c.util.system import check_outdir


DEMO_FILES = [
    (
        'http://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE68582&format=file&file=GSE68582%5FBED%5FES%2DNPC%2DiPS%2DLOCI%5Fmm9%2Ebed%2Egz',  # noqa: E501
        'BED_ES-NPC-iPS-LOCI_mm9.bed'
    ),
    (
        'http://www.ncbi.nlm.nih.gov/geo/download/?acc=GSM1974095&format=file&file=GSM1974095%5Fv65%5FRep1%2Ecounts%2Etxt%2Egz',  # noqa: E501
        'v65_Rep1.counts'
    ),
    (
        'http://www.ncbi.nlm.nih.gov/geo/download/?acc=GSM1974096&format=file&file=GSM1974096%5Fv65%5FRep2%2Ecounts%2Etxt%2Egz',  # noqa: E501
        'v65_Rep2.counts'
    ),
    (
        'http://www.ncbi.nlm.nih.gov/geo/download/?acc=GSM1974099&format=file&file=GSM1974099%5FpNPC%5FRep1%2Ecounts%2Etxt%2Egz',  # noqa: E501
        'pNPC_Rep1.counts'
    ),
    (
        'http://www.ncbi.nlm.nih.gov/geo/download/?acc=GSM1974100&format=file&file=GSM1974100%5FpNPC%5FRep2%2Ecounts%2Etxt%2Egz',  # noqa: E501
        'pNPC_Rep2.counts'
    )
]


def download_gzipped_file(url, target, chunk_size=16*1024):
    """
    Downloads and unzips a gzipped remote file.

    Parameters
    ----------
    url : str
        The URL of the remote file.
    target : str
        The complete path to write the unzipped file to.
    """
    d = zlib.decompressobj(16 + zlib.MAX_WBITS)
    response = urlopen(url)
    with open(target, 'wb') as handle:
        while True:
            data = response.read(chunk_size)
            if not data:
                break
            handle.write(d.decompress(data))


def ensure_demo_data(dest_dir='input'):
    """
    Downloads the demo data if it doesn't exist yet.

    The primerfile will be edited to remove regions other than Sox2 and Klf4.

    Parameters
    ----------
    dest_dir : str
        The directory to download the demo data to. Will be created if it
        doesn't exist.
    """
    # download
    for url, dest_filename in DEMO_FILES:
        dest_path = os.path.join(dest_dir, dest_filename)
        check_outdir(dest_path)
        if not os.path.exists(dest_path):
            download_gzipped_file(url, dest_path)

    # edit the primer bedfile in place
    # https://stackoverflow.com/a/2424410
    f = open(os.path.join(dest_dir, 'BED_ES-NPC-iPS-LOCI_mm9.bed'), 'r+')
    lines = [l for l in f.readlines() if 'Klf4' in l or 'Sox2' in l]
    f.seek(0)
    f.writelines(lines)
    f.truncate()
    f.close()


def edit_demo_config(config_file='luigi.cfg'):
    """
    Given the path to a default pipeline config file on disk, this function
    edits that default config file in place to prepare it for the pipeline
    tutorial.

    Parameters
    ----------
    config_file : str
        The path to a default pipeline config file.
    """
    config = parse_config(config_file)
    config.set('PipelineTask', 'tasks', '''[
"./raw/qnormed/jointexpress/bin_gmean_20_8/expected_donut/variance/pvalues/threshold"
]''')
    config.set('RawCounts', 'countsfiles', '''{
"ES_Rep1": "input/v65_Rep1.counts",
"ES_Rep2": "input/v65_Rep2.counts",
"pNPC_Rep1": "input/pNPC_Rep1.counts",
"pNPC_Rep2": "input/pNPC_Rep2.counts"
}''')
    config.set('PrimerFile', 'primerfile', 'input/BED_ES-NPC-iPS-LOCI_mm9.bed')
    config.remove_option('MakeExpected', 'plot_outfile')
    config.set('MakeQnorm', 'heatmap', False)
    config.set('MakeJointExpress', 'heatmap', False)
    with open(config_file, 'w') as handle:
        config.write(handle)


def main():
    ensure_demo_data()
    if os.path.exists('luigi.cfg'):
        os.remove('luigi.cfg')
    drop_config_file()
    edit_demo_config()


if __name__ == '__main__':
    main()
