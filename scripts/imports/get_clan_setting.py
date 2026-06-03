clan_settings = {
    "fading": False
}

def get_clan_setting(name: str, *, default=None):
    return clan_settings.get(name, default)