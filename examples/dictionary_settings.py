import smartsettings as ss

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
