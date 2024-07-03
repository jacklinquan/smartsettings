from pathlib import Path
import smartsettings as ss

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
