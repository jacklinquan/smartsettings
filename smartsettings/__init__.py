"""Smart Settings

Easy to use, flexible and versitile settings.
It can be serialized to json format, and even encrypted.
The `updatable` feature makes it suitable for value bindings.

- Author: Quan Lin
- License: MIT
"""

from .smartsettings import (
    UTC_TIME_STRING_FORMAT,
    SmartSettings,
    from_string,
    from_file,
    to_string,
    to_file,
)

__all__ = [
    "UTC_TIME_STRING_FORMAT",
    "SmartSettings",
    "from_string",
    "from_file",
    "to_string",
    "to_file",
]

# Project version
__version__ = "0.1.0"
