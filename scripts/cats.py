from scripts.pelt import Pelt

class Cat:
    def __init__(
        self,
        SPRITE_DATA: None,
        pose: None,
        pelt: None,
        color: None,
    ):
        self.pelt = Pelt(SPRITE_DATA, pose, pelt, color)
        self.status = Status()
        self.dead = False
        self.prevent_fading = True
        self.sprite = None

    def not_working():
        return False

class Status:
    def __init__(self):
        self.group = "player_clan"