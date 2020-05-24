"""
__main__.py for tzview
"""

import sys
import tzview.app

if __name__ == '__main__':
    parser = tzview.app.create_parser()
    args = parser.parse_args()
    sys.exit(tzview.app.main(args))
