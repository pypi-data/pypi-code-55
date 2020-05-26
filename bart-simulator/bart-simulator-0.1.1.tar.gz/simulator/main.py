""" module to methods to main  """
import sys
import logging


from simulator.tools import tools_parser

logger = logging.getLogger(__name__)


def main():
    try:
        sys.exit(tools_parser(sys.argv[1:]))
    except KeyboardInterrupt:
        # É convencionado no shell que o programa finalizado pelo signal de
        # código N deve retornar o código N + 128.
        sys.exit(130)
    except Exception as exc:
        logger.exception(
            "erro durante a execução da função " "'tools_parser' com os args %s",
            sys.argv[1:],
        )
        sys.exit("Um erro inexperado ocorreu: %s" % exc)


if __name__ == "__main__":
    sys.exit(tools_parser(sys.argv[1:]))
