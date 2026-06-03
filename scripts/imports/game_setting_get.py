settings = {
    "shaders": True,
    "special_dates": False
}

def game_setting_get(name, *, default=None):
    return settings.get(name, default)