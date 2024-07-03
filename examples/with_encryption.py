import smartsettings as ss

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
