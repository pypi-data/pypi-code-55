from io import BytesIO
import pkgutil
__version__ = '0.1.0'

def get_template():
    """Returns docx bytes"""
    return BytesIO(pkgutil.get_data(__name__, 'data/template.docx'))
