"""Some definitions of datatype used in the module."""
from typing import Tuple, Dict, Union, Any

# The record queried from the airtable
Fields = Dict[str, Any]
Record = Dict[str, Union[str, Fields]]
# The key value pair of the data document
Pair = Tuple[str, dict]
