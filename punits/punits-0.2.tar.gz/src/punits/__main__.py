"""
__main__.py for punits
"""

__version__ = "0.0.2"
__author__ = "Julin S"

import sys
import punits.app

if __name__ == "__main__":
    parser = punits.app.create_parser()
    args = parser.parse_args()
    sys.exit(punits.app.main(args))
