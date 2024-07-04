import smartsettings as ss

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

# Non-existing attribute with indexing operator returns `None`
print(f"{settings['fifth_value'] = }")

# Non-existing attribute raises `AttributeError`
try:
    print(f"{settings.fifth_value = }")
except AttributeError as ae:
    print(ae)
