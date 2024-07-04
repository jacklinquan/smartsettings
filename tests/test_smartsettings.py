from pathlib import Path
import pytest
import smartsettings as ss


def test_use_smartsettings_directly():
    # Add attributes on initialization
    settings = ss.SmartSettings(name="settings", first_value=100)
    # Add attribute directly
    settings.second_value = 3.14
    # Add attribute with indexing operator
    settings["third_value"] = True
    # Add subsettings
    settings.fourth_value = ss.SmartSettings(name="subsettings", value=200)
    print(f"{settings = }")

    # Serialize settings to json string
    # The `indent` keyword argument is passed to `jsonpickle.encode`
    settings_string = ss.to_string(settings, indent=2)
    print("settings_string =", settings_string)

    # Deserialize settings from json string
    loaded_settings = ss.from_string(settings_string)
    print(f"{loaded_settings = }")

    # The 2 settings are equal
    print(loaded_settings == settings)

    assert loaded_settings == settings

    # Non-existing attribute with indexing operator returns `None`
    print(f"{settings['fifth_value'] = }")

    # Non-existing attribute raises `AttributeError`
    try:
        print(f"{settings.fifth_value = }")
    except AttributeError as ae:
        print(ae)

    with pytest.raises(AttributeError):
        settings.fifth_value


class ChildSettings(ss.SmartSettings):
    def __init__(self, name: str, value: int) -> None:
        self.name = name
        self.value = value


class ParentSettings(ss.SmartSettings):
    def __init__(self, name: str, children: list[ChildSettings]) -> None:
        self.name = name
        self.children = children


def test_subclass_smartsettings():
    parent_settings = ParentSettings(
        name="parent",
        children=[
            ChildSettings(name="first child", value=100),
            ChildSettings(name="second child", value=200),
            ChildSettings(name="third child", value=300),
        ],
    )
    print(f"{parent_settings = }")

    # Serialize settings to json string
    # The `indent` keyword argument is passed to `jsonpickle.encode`
    parent_settings_string = ss.to_string(parent_settings, indent=2)
    print("parent_settings_string =", parent_settings_string)

    # Deserialize settings from json string
    loaded_parent_settings = ss.from_string(parent_settings_string)
    print(f"{loaded_parent_settings = }")

    # The 2 settings are equal
    print(loaded_parent_settings == parent_settings)

    assert loaded_parent_settings == parent_settings


def test_with_encryption():
    # Add attributes on initialization
    settings = ss.SmartSettings(name="settings", value=100)
    print(f"{settings = }")

    # Serialize and encrypt settings to string
    settings_string = ss.to_string(settings, crypto_key="secret")
    print("settings_string =", settings_string)

    # Decrypt and deserialize settings from string
    loaded_settings = ss.from_string(settings_string, crypto_key="secret")
    print(f"{loaded_settings = }")

    # The 2 settings are equal
    print(loaded_settings == settings)

    assert loaded_settings == settings


def test_json_settings_file():
    # Settings file path
    JSON_SETTINGS_FILE_PATH = Path("settings/settings.json")

    # Default settings
    default_settings = ss.SmartSettings(name="default_settings", value=0)

    # Add attributes on initialization
    settings = ss.SmartSettings(name="settings", value=100)
    print(f"{settings = }")

    # Serialize settings to json file
    # The `backup_num` keyword argument controls the number of backup files
    # When `backup_num=None` (default), the number of backup files is unlimited
    # When `backup_num=0`, there is no backup file at all
    # The `indent` keyword argument is passed to `jsonpickle.encode`
    ss.to_file(
        settings,
        JSON_SETTINGS_FILE_PATH,
        backup_num=2,
        indent=2,
    )

    # Deserialize settings from json file
    # In case the settings file does not exist, the `default_settings` is loaded.
    loaded_settings = ss.from_file(
        JSON_SETTINGS_FILE_PATH,
        default_settings=default_settings,
    )
    print(f"{loaded_settings = }")

    # The 2 settings are equal
    print(loaded_settings == settings)

    assert loaded_settings == settings


def test_encrypted_settings_file():
    # Encrypted settings file path
    ENCRYPTED_SETTINGS_FILE_PATH = Path("settings/settings.txt")

    # Default settings
    default_settings = ss.SmartSettings(name="default_settings", value=0)

    # Add attributes on initialization
    settings = ss.SmartSettings(name="settings", value=100)
    print(f"{settings = }")

    # Serialize and encrypt settings to text file
    # The `backup_num` keyword argument controls the number of backup files
    # When `backup_num=None` (default), the number of backup files is unlimited
    # When `backup_num=0`, there is no backup file at all
    ss.to_file(
        settings,
        ENCRYPTED_SETTINGS_FILE_PATH,
        crypto_key="secret",
        backup_num=2,
    )

    # Decrypt and deserialize settings from text file
    # In case the settings file does not exist, the `default_settings` is loaded.
    loaded_settings = ss.from_file(
        ENCRYPTED_SETTINGS_FILE_PATH,
        crypto_key="secret",
        default_settings=default_settings,
    )
    print(f"{loaded_settings = }")

    # The 2 settings are equal
    print(loaded_settings == settings)

    assert loaded_settings == settings


def test_settings_update():
    # Settings
    settings = ss.SmartSettings(name="settings", value=100)
    print(f"{settings = }")

    # New settings
    new_settings = ss.SmartSettings(name="new_settings", value=200)
    print(f"{new_settings = }")

    # Update `settings` with `new_settings`
    # `<<` operator has the same effect as `_update_with` method
    # `settings._update_with(new_settings)`
    settings << new_settings
    print(f"{settings = }")

    # The 2 settings are equal
    print(settings == new_settings)

    assert settings == new_settings


def test_dictionary_settings():
    # Dictionary settings
    settings = dict(name="settings", first_value=100)
    settings["second_value"] = 3.14
    settings["third_value"] = True
    # Dictionary subsettings
    settings["fourth_value"] = dict(name="subsettings", value=200)
    print(f"{settings = }")

    # Serialize settings to json string
    # The `indent` keyword argument is passed to `jsonpickle.encode`
    settings_string = ss.to_string(settings, indent=2)
    print("settings_string =", settings_string)

    # Deserialize settings from json string
    loaded_settings = ss.from_string(settings_string)
    print(f"{loaded_settings = }")

    # The 2 settings are equal
    print(loaded_settings == settings)

    assert loaded_settings == settings
