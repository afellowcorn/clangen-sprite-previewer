import os
import pygame_gui
import pygame
import sys
import ujson

from scripts.load_sprites import Sprites
from scripts.display_sprites import generate_sprite
from scripts.cats import Cat
from scripts.pelt import Pelt

import collections

# CONFIG
POSE = []
PELT = []
COLOR = []
TINT = [None]
EYE = ["YELLOW"]
SKIN = "BLACK"
WHITE = None
SIZE = None
WINDOW = (500, 500)
BACKGROUND = (150, 150, 150)

class SpriteData():
	def __init__ (self):
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
		"\n edit [<file>] - edit sprite data file"
	)

def yes_no_prompt() -> bool:
	print("Proceed? [Y/N]")
	safe_inp = None
	while safe_inp not in ("Y", "N"):
		safe_inp = input().upper()
	if safe_inp == "Y":
		return True
	elif safe_inp == "N":
		print("Cancelled action.")
		return False

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
			for tint in TINT:
				if tint == "none":
					tint = None
				for eye_color in EYE:
					for pose in POSE:
						cat = Cat(
							pelt=Pelt(
								SPRITE_DATA=SPRITE_DATA,
								color=color,
								eye_color=eye_color,
								pelt=pelt,
								pose=pose,
								skin=SKIN,
								tint=tint,
								white_patches=WHITE
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
	global POSE, PELT, COLOR, EYE, SKIN, TINT, SIZE, WINDOW, BACKGROUND
	try:
		with open("./config.json", "r", encoding="utf-8") as read_file:
			config = ujson.loads(read_file.read())
		POSE = config["pose"]
		PELT = config["pelt"]
		COLOR = config["color"]
		EYE = config["eye_color"]
		SKIN = config["skin_color"]
		TINT = config["tint"]
		WHITE = config["white_patch"]
		SIZE = config["sprite_size"]
		WINDOW = config["window_size"]
		BACKGROUND = config["background_color"]
	except Exception as e:
		POSE = []
		PELT = []
		COLOR = []
		EYE = ["YELLOW"]
		SKIN = "BLACK"
		TINT = [None]
		WHITE = None
		SIZE = 50
		WINDOW = (500, 500)
		BACKGROUND = (150, 150, 150)

		print(f"Failed to load config: {e}")

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

def update():
	SCREEN = pygame.display.set_mode((500, 500))
	load_sprite_data()
	pygame.quit()

def edit_data(delete, data, dictionary):
	print(dictionary)
	for key, value in dictionary.items():
		data_value = data.get(key)
		if isinstance(value, collections.abc.Mapping) and isinstance(data_value, collections.abc.Mapping):
			edit_data(delete, data_value, value)
		else:
			if delete:
				del data[key]
			else:
				data[key] = value

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
DATA_FILE_ALIASES = {
	"group_data": "generation_group_data",
	"group": "generation_group_data",
	"pelt_color_palette": "pelt_color_palettes",
	"pelt_colour_palette": "pelt_color_palettes",
	"color_palettes": "pelt_color_palettes",
	"colour_palettes": "pelt_color_palettes",
	"color_palette": "pelt_color_palettes",
	"colour_palette": "pelt_color_palettes",
	"palettes": "pelt_color_palettes",
	"palette": "pelt_color_palettes",
	"color": "pelt_color_palettes",
	"colour": "pelt_color_palettes",
	"pelt_parts_data": "pelt_parts_masks_data",
	"pelt_part_data": "pelt_parts_masks_data",
	"pelt_masks_data": "pelt_parts_masks_data",
	"pelt_mask_data": "pelt_parts_masks_data",
	"masks": "pelt_parts_masks_data",
	"mask": "pelt_parts_masks_data",
	"pelt_recipe": "pelt_to_recipe",
	"recipe": "pelt_to_recipe",
	"tints": "tint"
}
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
				edit = True
				delete = False
				i = 0
				file = None
				dictionary = None

				if cmd[1] == "del":
					delete = True
					i = 1

				if cmd[1+i] in DATA_FILE_ALIASES:
					file = DATA_FILE_ALIASES[cmd[1+i]]
				else:
					file = cmd[1+i]

				## OPEN
				try:
					with open(f"{SPRITE_DATA_DIR}/{file}.json", "r", encoding="utf-8") as read_file:
						data = ujson.loads(read_file.read())
				except Exception as e:
					print(f"Failed to load data file {file}: {e}")

				## MODIFY
				match file:
					case "generation_group_data":
						if len(cmd) < 4+i:
							print(
								"edit generation_group_data colors [<color>] [<group>]"
								"\nedit generation_group_data pattern_types [<pelt>] [<group>]"
							)
							edit = False
						else:
							if cmd[2+i].lower() in ("colors", "color", "colours", "colour"):
								dictionary = {
									"pelts": {
										"colors": {
											cmd[3+i].upper(): cmd[4+i].lower() if len(cmd) >= 5+i else None
										}
									}
								}
							elif cmd[2+i].lower() in ("pattern_types", "pattern_type", "pattern", "type"):
								dictionary = {
									"pelts": {
										"pattern_types": {
											cmd[3+i]: cmd[4+i].lower() if len(cmd) >= 5+i else None
										}
									}
								}
							else:
								dictionary = {
									"pelts": {
										cmd[2+i]: {
											cmd[3+i]: cmd[4+i] if len(cmd) >= 5+i else None
										}
									}
								}
					case "pelt_color_palettes":
						if len(cmd) < 3+i:
							print("edit pelt_color_palettes [<color> | all] [<part>] [<hexcode>]")
							edit = False
						else:
							_has_part = len(cmd) >= 4+i
							_has_hexcode = len(cmd) >= 5+i
							if cmd[2+i].lower() == "all":
								if delete:
									if _has_part:
										print("WARNING: this will delete the specified part from ALL colors.")
									else:
										print("WARNING: this will delete ALL colors.")

									if not yes_no_prompt():
										edit = False
									else:
										dictionary = []
										for color in data:
											if _has_part:
												_dictionary = {
													color: {
														cmd[3+i].lower(): None
													}
												}
											else:
												_dictionary = {color: None}
											dictionary.append(_dictionary)
								elif _has_part:
									if _has_hexcode:
										print("WARNING: this will set the hexcode of ALL colors' specified part (or add the part if not present).")
									else:
										print("WARNING: this will add this part to ALL colors.")

									if not yes_no_prompt():
										edit = False
									else:
										dictionary = []
										for color in data:
											_dictionary = {
												color: {
													cmd[3+i].lower(): cmd[4+i] if len(cmd) >= 5+i else "#000000"
												}
											}
											dictionary.append(_dictionary)
								else:
									edit = False
							else:
								if _has_part:
									dictionary = {
										cmd[2+i].upper(): {
											cmd[3+i].lower(): cmd[4+i] if len(cmd) >= 5+i else "#000000"
										}
									}
								else:
									dictionary = {cmd[2+i].upper(): None}

					case "pelt_parts_masks_data":
						print("Currently not supported :(")
						# if len(cmd) < 4+i:
						# 	print(
						# 		"edit pelt_parts_masks_data spritesheet [<spritesheet>]"
						# 		"edit pelt_parts_masks_data sprite_list [<row>] [<sprite> | all]"
						# 	)
						# 	edit = False
						# else:
						# 	if cmd[2+i].lower() in ("spritesheet", "sheet"):
						# 		dictionary = {
						# 			"spritesheet": cmd[3+i:] if len(cmd) >= 4+i else "pelt_parts_masks"
						# 		}
						# 	elif cmd[2+i].lower() in ("sprite_list", "sprites_list", "sprites"):
						# 		_value = []
						# 		for x in range(int(cmd[3+i])):
						# 			if x == cmd[3+i]:
						# 				_value.append([cmd[4+i]])
						# 			else:
						# 				_value.append([])
						# 		dictionary = {
						# 			"sprite_list": _value
						# 		}

					case "pelt_to_recipe":
						if len(cmd) < 3+i:
							print("edit pelt_to_recipe [<pelt>] [<recipe>]")
							edit = False
						else:
							dictionary = {
								cmd[2+i]: cmd[3+i] if len(cmd) >= 4+i else f"{cmd[2+i]}Recipe"
							}

					case "tint":
						if len(cmd) < 4+i:
							print(
								"edit tint colour_groups [<color>] [<group>]"
								"\nedit tint possible_tints [<group>] [<tints>]"
								"\nedit tint [tint_colours | dilute_tint_colours] [<color>] [<red, green, blue>]"
							)
							edit = False
						else:
							if cmd[2+i].lower() in ("colour_groups", "color_groups", "groups"):
								dictionary = {
									"colour_groups": {
										cmd[3+i].upper(): cmd[4+i].lower() if len(cmd) >= 5+i else None
									}
								}
							elif cmd[2+i].lower() in ("possible_tints", "possible_tint"):
								dictionary = {
									"possible_tints": {
										cmd[3+i].lower(): cmd[4+i:] if len(cmd) >= 5+i else []
									}
								}
							elif cmd[2+i].lower() in ("tint_colours", "tint_colors", "dilute_tint_colours", "dilute_tint_colors"):
								dictionary = {
									"dilute_tint_colours" if "dilute" in cmd[2+i].lower() else "tint_colours": {
										cmd[3+i].lower(): cmd[4+i:] if len(cmd) >= 5+i else None
									}
								}
							else:
								dictionary = {
									cmd[2+i].lower(): {
										cmd[3+i].lower(): cmd[4+i:] if len(cmd) >= 5+i else None
									}
								}
				if edit and dictionary:
					if isinstance(dictionary, list):
						for _dictionary in dictionary:
							edit_data(delete, data, _dictionary)
					else:
			   			edit_data(delete, data, dictionary)

					## SAVE
					_data = ujson.dumps(data, indent=4)
					with open(f"{SPRITE_DATA_DIR}/{file}.json", "w", encoding="utf-8") as write_file:
						write_file.write(_data)
						write_file.flush()
						os.fsync(write_file.fileno())

					del _data, data, dictionary

					## RELOAD
					update()

