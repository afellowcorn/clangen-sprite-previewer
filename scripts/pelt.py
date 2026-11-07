class Pelt:
    def __init__(
        self,
        SPRITE_DATA: None,
        color: None,
        eye_color: None,
        pelt: None,
        pose: None,
        skin: None,
        tint: None,
        white_patches: None,
    ):
        self.name = pelt
        self.colour = color
        self.cat_sprites = {"adult": pose}
        self.eye_colour = eye_color
        self.skin = skin
        self.eye_colour2 = None
        self.tint = tint
        self.white_patches = white_patches
        self.white_patches_tint = None
        self.points = None
        self.vitiligo = None
        self.paralyzed = False
        self.opacity = 100
        self.reverse = False

        # WHITE MARKINGS
        self.little_white: list = list(
            SPRITE_DATA.white_patches_combos.get("little", {}).keys()
        )
        for sprite_list in SPRITE_DATA.white_patches_little_sprite_data["sprite_list"]:
            self.little_white.extend(sprite_list)
        self.mid_white: list = list(
            SPRITE_DATA.white_patches_combos.get("mid", {}).keys()
        )
        for sprite_list in SPRITE_DATA.white_patches_mid_sprite_data["sprite_list"]:
            self.mid_white.extend(sprite_list)
        self.high_white: list = list(
            SPRITE_DATA.white_patches_combos.get("high", {}).keys()
        )
        for sprite_list in SPRITE_DATA.white_patches_high_sprite_data["sprite_list"]:
            self.high_white.extend(sprite_list)
        self.mostly_white: list = list(
            SPRITE_DATA.white_patches_combos.get("mostly", {}).keys()
        )
        for sprite_list in SPRITE_DATA.white_patches_mostly_sprite_data["sprite_list"]:
            # have to remove FULLWHITE as it's handled special
            self.mostly_white.extend([x for x in sprite_list if x != "FULLWHITE"])
        self.vitiligo_markings: list = []
        for sprite_list in SPRITE_DATA.white_patches_vitiligo_sprite_data[
            "sprite_list"
        ]:
            self.vitiligo_markings.extend(sprite_list)
        self.point_markings: list = []
        for sprite_list in SPRITE_DATA.white_patches_points_sprite_data["sprite_list"]:
            self.point_markings.extend(sprite_list)
