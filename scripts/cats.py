class Cat:
    def __init__(self, pelt: None):
        self.pelt = pelt
        self.status = Status()
        self.dead = False
        self.prevent_fading = True
        self.sprite = None

    def not_working():
        return False


class Status:
    def __init__(self):
        self.group = "player_clan"
