"""
Reading Image is a text analysis tool for images files (png, jpg, jpeg) and pdf. The system will preform OCR on the
document and return details of the text within. Examples of analysis include text strings, page location and entity
analysis. Advanced OCR will also read and understand table formats, and translation is available to English from French.
"""

__version__ = "1.0.1"
__author__ = "Danny Hoskin"

from .Session import Session
from .Processed import Processed
