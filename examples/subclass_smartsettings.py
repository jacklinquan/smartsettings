import smartsettings as ss


class ChildSettings(ss.SmartSettings):
    def __init__(self, name: str, value: int) -> None:
        self.name = name
        self.value = value


class ParentSettings(ss.SmartSettings):
    def __init__(self, name: str, children: list[ChildSettings]) -> None:
        self.name = name
        self.children = children


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
