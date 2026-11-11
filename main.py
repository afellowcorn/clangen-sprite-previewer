import os
import pygame_gui
import pygame
import sys
import ujson

from scripts.edit import edit
from scripts.load_sprites import Sprites
from scripts.display_sprites import generate_sprite
from scripts.cats import Cat
from scripts.pelt import Pelt

# CONFIG
POSE = []
PELT = []
COLOR = []
TINT = [None]
EYE = ["YELLOW"]
SKIN = "BLACK"
WHITE = None
SIZE = None
SCALE = 1.0
WINDOW = (500, 500)
BACKGROUND = (150, 150, 150)


class SpriteData:
    def __init__(self):
        pass


def print_help():
    print(
        "Commands:",
        "\n -- GENERAL --",
        "\n background [grey | dark | light | <red, green, blue>] - set window color",
        "\n commands - print all commands",
        "\n config [save | load] - save and load config options",
        "\n draw - draw sprites",
        "\n size [<int>] - override automatically calculated sprite size",
        "\n scale [<float>] - scale at which sprites are drawn"
        "\n update - reload sprite and pelt data",
        "\n window [<size> | <width, height>] - set window size",
        "\n -- CAT --",
        "\n color [<colors>] - set drawn colors",
        "\n eye [<colors>] - set eye colors",
        "\n pelt [<pelts>] - set drawn pelts",
        "\n pose [<poses>] - set drawn poses",
        "\n skin [<color>] - set skin color",
        "\n tint [<tints>] - set cat tints",
        "\n white [<white>] - make cat display with a white patch"
        "\n -- EDIT --",
        "\n NOTE: editing json files will alter their formatting. If you have manual formatting you want to retain, don't use this command."
        "\n edit [<file>] - edit sprite data file",
    )


def draw():
    max_row = int((WINDOW[0] - 10) / (SIZE * SCALE))
    x, y = 10, 10
    row_index = 0
    pose_index = 0
    sprite_index = 0

    for sprite in CAT_SPRITES:
        sprite = pygame.transform.scale_by(sprite, SCALE)
        if pose_index >= len(POSE):
            x += SIZE * SCALE
            y = 10 + (SIZE * SCALE * (len(POSE)) * (row_index))
            pose_index = 0
            sprite_index += 1

        if sprite_index >= max_row:
            x = 10
            y = 10 + (SIZE * SCALE * (len(POSE)) * (row_index + 1))
            sprite_index = 0
            row_index += 1

        SCREEN.blit(sprite, (x, y))
        y += SIZE * SCALE
        pose_index += 1


def generate_cat():
    if not SPRITES.sprites:
        load_sprite_data()
    print(SPRITES.size)
    _PELT = PELT
    _COLOR = COLOR
    _TINT = TINT
    _EYE = EYE
    _POSE = POSE
    if _PELT[0].upper() == "ALL":
        _PELT = [str(x) for x in SPRITE_DATA.generation_group_data["pelts"]["pattern_types"].keys() if x not in ("Tortie", "Calico")]
    if _COLOR[0].upper() == "ALL":
        _COLOR = [str(x) for x in SPRITE_DATA.generation_group_data["pelts"]["colors"].keys()]
    if _TINT != [None] and _TINT[0].upper() == "ALL":
        _TINT = list(SPRITE_DATA.tint["tint_colours"].keys()) + list(SPRITE_DATA.tint["dilute_tint_colours"].keys()) + list(SPRITE_DATA.tint["remove_tone_tint_colours"].keys())
    if _EYE[0].upper() == "ALL":
        _EYE = []
        for d in SPRITE_DATA.eye_sprite_data["sprite_list"]:
            for x in d.keys():
                _EYE.append(str(x))
    if _POSE[0].upper() == "ALL":
        _POSE = [str(x) for x in SPRITE_DATA.pose_sprite_data["poses"] if x != ""]

    for pelt in _PELT:
        for color in _COLOR:
            for tint in _TINT:
                if tint == "none":
                    tint = None
                for eye_color in _EYE:
                    for pose in _POSE:
                        cat = Cat(
                            pelt=Pelt(
                                SPRITE_DATA=SPRITE_DATA,
                                color=color,
                                eye_color=eye_color,
                                pelt=pelt,
                                pose=pose,
                                skin=SKIN,
                                tint=tint,
                                white_patches=WHITE,
                            )
                        )
                        cat.sprite = generate_sprite(
                            cat,
                            SPRITES,
                            life_state="adult",
                            scars_hidden=True,
                            acc_hidden=True,
                            disable_sick_sprite=True,
                        )
                        CAT_SPRITES.append(cat.sprite)


def load_config_data():
    global POSE, PELT, COLOR, EYE, SKIN, TINT, SIZE, SCALE, WINDOW, BACKGROUND
    try:
        with open("./config.json", "r", encoding="utf-8") as read_file:
            config = ujson.loads(read_file.read())
        POSE = config.get("pose", [])
        PELT = config.get("pelt", [])
        COLOR = config.get("color", [])
        EYE = config.get("eye_color", ["YELLOW"])
        SKIN = config.get("skin_color", "BLACK")
        TINT = config.get("tint", [None])
        WHITE = config.get("white_patch", None)
        SIZE = config.get("sprite_size", 50)
        SCALE = config.get("sprite_scale", 1.0)
        WINDOW = config.get("window_size", (500, 500))
        BACKGROUND = config.get("background_color", (150, 150, 150))
    except:
        POSE = []
        PELT = []
        COLOR = []
        EYE = ["YELLOW"]
        SKIN = "BLACK"
        TINT = [None]
        WHITE = None
        SIZE = 50
        SCALE = 1.0
        WINDOW = (500, 500)
        BACKGROUND = (150, 150, 150)

        print(f"Failed to load config")


def save_config_data():
    data = {
        "pose": POSE,
        "pelt": PELT,
        "color": COLOR,
        "eye_color": EYE,
        "skin_color": SKIN,
        "tint": TINT,
        "white_patch": WHITE,
        "sprite_size": SIZE,
        "sprite_scale": SCALE,
        "window_size": WINDOW,
        "background_color": BACKGROUND,
    }

    _data = ujson.dumps(data, indent=4)
    with open("./config.json", "w", encoding="utf-8") as write_file:
        write_file.write(_data)
        write_file.flush()
        os.fsync(write_file.fileno())


def load_sprite_data():
    for x in next(os.walk(SPRITE_DATA_DIR))[2]:
        with open(f"{SPRITE_DATA_DIR}/{x}", "r", encoding="utf-8") as read_file:
            name = x.split(".")
            setattr(SPRITE_DATA, f"{name[0]}", ujson.loads(read_file.read()))
    SPRITES.sprites.clear()
    SPRITES.load_all()


def update():
    SCREEN = pygame.display.set_mode((500, 500))
    load_sprite_data()
    pygame.quit()


# SETUP
pygame.init()
SCREEN = pygame.display.set_mode(WINDOW)
SCREEN_BACKGROUND = {
    "grey": (150, 150, 150),
    "dark": (57, 50, 36),
    "light": (206, 194, 168),
}
MANAGER = pygame_gui.UIManager(WINDOW)
CAT_SPRITES = []

SPRITES = Sprites()
SPRITE_DATA = SpriteData()
SPRITE_DATA_DIR = "sprites/dicts"
load_sprite_data()
load_config_data()
if not SIZE:
    if SPRITES.size:
        SIZE = int(SPRITES.size)
    else:
        SIZE = 50
pygame.quit()
print_help()

window = False
while 1:
    if window:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
                pygame.quit()
                window = False
            MANAGER.process_events(event)

    if not window:
        inp = input()
        cmd = inp.split(" ")
        del inp

        match cmd[0]:
            # config
            case "pose" if len(cmd) > 1:
                POSE = [x for x in cmd if x != "pose"]
                print(f"Set POSE to {POSE}.")
            case "pose":
                print(f"POSE: {POSE}.")

            case "pelt" if len(cmd) > 1:
                PELT = [x for x in cmd if x != "pelt"]
                print(f"Set PELT to {PELT}.")
            case "pelt":
                print(f"PELT: {PELT}.")

            case "color" if len(cmd) > 1:
                COLOR = [x.upper() for x in cmd if x != "color"]
                print(f"Set COLOR to {COLOR}.")
            case "color":
                print(f"COLOR: {COLOR}.")

            case "eye" if len(cmd) > 1:
                EYE = [x.upper() for x in cmd if x != "eye"]
                print(f"Set EYE color to {EYE}.")
            case "eye":
                print(f"EYE: {EYE}.")

            case "skin" if len(cmd) > 1:
                SKIN = cmd[1].upper()
                print(f"Set SKIN color to {SKIN}.")
            case "skin":
                print(f"SKIN: {SKIN}.")

            case "tint" if len(cmd) > 1:
                TINT = [x.lower() for x in cmd if x != "tint"]
                print(f"Set TINT color to {TINT}.")
            case "tint":
                print(f"TINT: {TINT}.")

            case "white" if len(cmd) > 1:
                WHITE = cmd[1].upper() if cmd[1].lower() != "none" else None
                print(f"Set WHITE color to {WHITE}.")
            case "white":
                print(f"WHITE: {WHITE}.")

            case "size" if len(cmd) > 1:
                SIZE = int(cmd[1])
                SPRITES.size = SIZE
                update()
                print(f"Set SIZE to {SIZE}.")
            case "size":
                print(f"SIZE: {SIZE}.")

            case "scale" if len(cmd) > 1:
                SCALE = float(cmd[1])
                print(f"Set SCALE to {SCALE}.")
            case "scale":
                print(f"SCALE: {SCALE}.")

            case "window" if len(cmd) > 1:
                if len(cmd) == 2:
                    WINDOW = tuple((int(cmd[1]), int(cmd[1])))
                else:
                    WINDOW = tuple((int(cmd[1]), int(cmd[2])))
                print(f"Set WINDOW size to {WINDOW}.")
            case "window":
                print(f"WINDOW: {tuple(WINDOW)}.")

            case "background" if len(cmd) > 1:
                if cmd[1].lower() in ("grey", "dark", "light"):
                    BACKGROUND = SCREEN_BACKGROUND[cmd[1]]
                elif len(cmd) > 3:
                    BACKGROUND = tuple(int(cmd[1]), int(cmd[2]), int(cmd[3]))
                else:
                    BACKGROUND = BACKGROUND
                    print("Must provide three values to set RGB color.")
                print(f"Set BACKGROUND color to {BACKGROUND}.")
            case "background":
                print(f"BACKGROUND: {tuple(BACKGROUND)}.")

            # save n load
            case "config":
                if len(cmd) == 1:
                    pass
                elif cmd[1] == "save":
                    save_config_data()
                elif cmd[1] == "load":
                    load_config_data()
            case "update":
                update()

            # function
            case "commands":
                print_help()
            case "draw":
                SCREEN = pygame.display.set_mode((WINDOW))
                SCREEN.fill(BACKGROUND)
                window = True
                generate_cat()
                draw()

                CAT_SPRITES = []

            # edit
            case "edit" if len(cmd) > 1:
                    edited = edit(cmd)
                    if edited:
                        update()
            case "edit":
                print("edit [<file>]")