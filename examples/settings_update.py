import smartsettings as ss

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
