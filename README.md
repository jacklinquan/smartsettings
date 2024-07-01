# Smart Settings

[![PyPI version][pypi_img]][pypi_link]
[![Downloads][downloads_img]][downloads_link]

  [pypi_img]: https://badge.fury.io/py/smartsettings.svg
  [pypi_link]: https://badge.fury.io/py/smartsettings
  [downloads_img]: https://pepy.tech/badge/smartsettings
  [downloads_link]: https://pepy.tech/project/smartsettings

Easy to use, flexible and versitile settings.
It can be serialized to json format, and even encrypted.
The `updatable` feature makes it suitable for value bindings.

## Installation

`pip install smartsettings`

## Usage

```python
>>> import smartsettings as ss
>>> settings = ss.SmartSettings(name="Settings", value=100)
>>> settings
{'name': 'Settings', 'value': 100}
>>> settings_string = ss.to_string(settings)
>>> settings_string
'{"py/object": "smartsettings.smartsettings.SmartSettings", "name": "Settings", "value": 100}'
>>> loaded_settings = ss.from_string(settings_string)
>>> loaded_settings
{'name': 'Settings', 'value': 100}
>>> loaded_settings == settings
True
```
