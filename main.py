import os
import pygame_gui
import pygame
import sys
import ujson

#from scripts.cat.sprites.load_sprites import Sprites
#from scripts.cat.sprites.display_sprites import generate_sprite

from scripts.load_sprites import Sprites
from scripts.display_sprites import generate_sprite
from scripts.cats import Cat

# CONFIG
POSE = []
PELT = []
COLOR = []
EYE = None
SKIN = None
SIZE = None
WINDOW = (500, 500)
BACKGROUND = (150, 150, 150)

class SpriteData():
    def __init__ (self):
        pass

def print_help():
    print(
    "Commands:",
    "\n pose [<poses>] - set drawn poses",
    "\n pelt [<pelts>] - set drawn pelts",
    "\n color [<colors>] - set drawn colors",
    "\n eye [<color>] - set eye color",
    "\n skin [<color>] - set skin color",
    "\n size [<int>] - override automatically calculated sprite size",
    "\n window [<size> | <width, height>] - set window size",
    "\n background [grey | dark | light | <red, green, blue>] - set window color"
    "\n config [save | load] - save and load config options",
    "\n update - reload sprite and pelt data",
    "\n commands - print all commands",
    "\n draw - draw sprites"
    )

def draw():
    max_row = int((WINDOW[0] - 10)/SIZE)
    x, y = 10, 10
    row_index = 0
    pose_index = 0
    sprite_index = 0

    for sprite in CAT_SPRITES:
        if pose_index >= len(POSE):
            x += SIZE
            y = 10 + (SIZE * (len(POSE)) * (row_index))
            pose_index = 0
            sprite_index += 1

        if sprite_index >= max_row:
            x = 10
            y = 10 + (SIZE * (len(POSE)) * (row_index + 1))
            sprite_index = 0
            row_index += 1

        SCREEN.blit(sprite, (x, y))
        y += SIZE
        pose_index += 1

def generate_cat():
    if not SPRITES.sprites:
        load_sprite_data()
    for pelt in PELT:
        for color in COLOR:
            for pose in POSE:
                cat = Cat(SPRITE_DATA=SPRITE_DATA, pose=pose, pelt=pelt, color=color)
                cat.sprite = generate_sprite(
                    cat,
                    SPRITES,
                    life_state="adult",
                    scars_hidden=True,
                    acc_hidden=True,
                    disable_sick_sprite=True
                )
                CAT_SPRITES.append(cat.sprite)

def load_config_data():
    global POSE, PELT, COLOR, SIZE, WINDOW, BACKGROUND
    try:
        with open("./config.json", "r", encoding="utf-8") as read_file:
            config = ujson.loads(read_file.read())
        POSE = config["pose"]
        PELT = config["pelt"]
        COLOR = config["color"]
        EYE = config["eye_color"]
        SKIN = config["skin_color"]
        SIZE = config["sprite_size"]
        WINDOW = config["window_size"]
        BACKGROUND = config["background_color"]
    except:
        POSE = None
        PELT = None
        COLOR = None
        EYE = None
        SKIN = None
        SIZE = None
        WINDOW = (500, 500)
        BACKGROUND = (150, 150, 150)

def save_config_data():
    data = {
        "pose": POSE,
        "pelt": PELT,
        "color": COLOR,
        "eye_color": EYE,
        "skin_color": SKIN,
        "sprite_size": SIZE,
        "window_size": WINDOW,
        "background_color": BACKGROUND
    }

    _data = ujson.dumps(data, indent=4)
    with open("./config.json", "w", encoding="utf-8") as write_file:
        write_file.write(_data)
        write_file.flush()
        os.fsync(write_file.fileno())

def load_sprite_data():
    for x in (next(os.walk(SPRITE_DATA_DIR))[2]):
        with open(f"{SPRITE_DATA_DIR}/{x}", "r", encoding="utf-8") as read_file:
            name = x.split(".")
            setattr(SPRITE_DATA, f"{name[0]}", ujson.loads(read_file.read()))
    SPRITES.load_all()

# SETUP
pygame.init()
SCREEN = pygame.display.set_mode(WINDOW)
SCREEN_BACKGROUND = {
    "grey": (150, 150, 150),
    "dark": (57, 50, 36),
    "light": (206, 194, 168)
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
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                or event.type == pygame.QUIT
            ):
                pygame.quit()
                window = False
            MANAGER.process_events(event)

    if not window:
        inp = input()
        cmd = inp.split(" ")

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
                COLOR = [x for x in cmd if x != "color"]
                print(f"Set COLOR to {COLOR}.")
            case "color":
                print(f"COLOR: {COLOR}.")

            case "eye" if len(cmd) > 1:
                EYE = [x for x in cmd if x != "eye"]
                print(f"Set EYE color to {EYE}.")
            case "eye":
                print(f"EYE: {EYE}.")

            case "skin" if len(cmd) > 1:
                SKIN = [x for x in cmd if x != "skin"]
                print(f"Set SKIN color to {SKIN}.")
            case "skin":
                print(f"SKIN: {SKIN}.")

            case "size" if len(cmd) > 1:
                SIZE = int(cmd[1])
                print(f"Set SIZE to {SIZE}.")
            case "size":
                print(f"SIZE: {SIZE}.")

            case "window" if len(cmd) > 1:
                if len(cmd) == 2:
                    WINDOW = tuple((int(cmd[1]), int(cmd[1])))
                else:
                    WINDOW = tuple((int(cmd[1]), int(cmd[2])))
                print(f"Set WINDOW size to {WINDOW}.")
            case "window":
                print(f"WINDOW: {tuple(WINDOW)}.")

            case "background" if len(cmd) > 1:
                if cmd[1] in ("grey", "dark", "light"):
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
                if cmd[1] == "save":
                    save_config_data()
                elif cmd[1] == "load":
                    load_config_data()
            case "update":
                SCREEN = pygame.display.set_mode((500, 500))
                load_sprite_data()
                pygame.quit()

            # function
            case "commands":
                print_help()
            case "draw":
                generate_cat()

                SCREEN = pygame.display.set_mode((WINDOW))
                SCREEN.fill(BACKGROUND)
                window = True
                draw()

                CAT_SPRITES = []