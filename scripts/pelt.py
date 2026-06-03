class Pelt:
    def __init__(
        self,
        SPRITE_DATA: None,
        pose: None,
        pelt: None,
        color: None
    ):
        self.name = pelt
        self.colour = color.upper()
        self.cat_sprites = {
            "adult": pose
        }
        self.eye_colour = "YELLOW"
        self.skin = "BLACK"
        self.eye_colour2 = None
        self.tint = None
        self.white_patches = None
        self.points = None
        self.vitiligo = None
        self.paralyzed = False
        self.opacity = 100
        self.reverse = False

         # pelt name used in save files: pelt's spritesheet
        self.pattern_sprite_names: dict = {}
        for sheet, names in SPRITE_DATA.pelt_sprite_data["spritesheet"].items():
            for name in names:
                self.pattern_sprite_names.update({name: sheet})

    def get_sprites_name(self):
        return self.pattern_sprite_names[self.name]