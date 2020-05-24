import argparse
import html
import logging
from pathlib import Path
import xml.dom.minidom

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='count', default=0)
parser.add_argument('-o', '--out-dir', type=Path, default=Path.cwd() / "testinfo")
parser.add_argument('pytest_xunit2_xml', type=Path)

def main(args):

    logging.basicConfig(level=logging.WARN if args.verbose==0 else logging.INFO if args.verbose==1 else logging.DEBUG)

    t = xml.dom.minidom.parse(args.pytest_xunit2_xml.open())

    RESOURCES_DIR = Path(__file__).parent/'resources'
    PASS_IMG = (RESOURCES_DIR / 'check_16x16.png').read_bytes()
    FAIL_IMG = (RESOURCES_DIR / 'cross_16x16.png').read_bytes()

    for testcase in t.getElementsByTagName('testcase'):
        classname = testcase.getAttribute("classname")
        basename = testcase.getAttribute("name")
        logger.info(f"processing {classname}/{basename}")

        subdir = args.out_dir / classname
        subdir.mkdir(parents=True, exist_ok=True)
        failures = testcase.getElementsByTagName('failure')
        if failures:
            logger.warning(f"{classname}/{basename} had {len(failures)} failures")

        (subdir / f'{basename}.png').write_bytes(FAIL_IMG if failures else PASS_IMG)  # TODO: what about "skipped"?
        (subdir / f'{basename}.html').write_text(
            "Failures: <ul>" + "\n".join(
                f"<li><pre>{html.escape(failure.childNodes[0].wholeText)}</pre></li>"
                for failure in failures
            ) + "</ul>"
        )

if __name__ == '__main__':
    main(parser.parse_args())
