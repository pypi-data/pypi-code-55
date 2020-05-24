"""
Core scripts to handle cli instructions
"""

class Commands:
    """
    """
    def  __init__(self, *args, **kwargs):
        print(kwargs.get('nest'))
        while True:
            chunk = nest.read(1024)
            if not chunk:
                break
        print(chunk)
