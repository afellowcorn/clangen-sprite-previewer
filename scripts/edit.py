import os
import ujson
import collections

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
    "tints": "tint",
}

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

def edit_data(delete, data, dictionary) -> None:
    for key, value in dictionary.items():
        data_value = data.get(key)
        if isinstance(value, collections.abc.Mapping) and isinstance(
            data_value, collections.abc.Mapping
        ):
            edit_data(delete, data_value, value)
        else:
            if delete:
                del data[key]
            else:
                data[key] = value

def edit(cmd) -> bool:
    edit = True
    delete = False
    i = 0
    file = None
    dictionary = None

    if cmd[1] == "del":
        delete = True
        i = 1

    if cmd[1 + i] in DATA_FILE_ALIASES:
        file = DATA_FILE_ALIASES[cmd[1 + i]]
    else:
        file = cmd[1 + i]

    ## OPEN
    try:
        with open(
            f"{SPRITE_DATA_DIR}/{file}.json", "r", encoding="utf-8"
        ) as read_file:
            data = ujson.loads(read_file.read())
    except Exception as e:
        print(f"Failed to load data file {file}: {e}")

    ## MODIFY
    match file:
        case "generation_group_data":
            if len(cmd) < 4 + i:
                print(
                    "edit generation_group_data colors [<color>] [<group>]"
                    "\nedit generation_group_data pattern_types [<pelt>] [<group>]"
                )
                edit = False
            else:
                if cmd[2 + i].lower() in (
                    "colors",
                    "color",
                    "colours",
                    "colour",
                ):
                    dictionary = {
                        "pelts": {
                            "colors": {
                                cmd[3 + i].upper(): cmd[4 + i].lower()
                                if len(cmd) >= 5 + i
                                else None
                            }
                        }
                    }
                elif cmd[2 + i].lower() in (
                    "pattern_types",
                    "pattern_type",
                    "pattern",
                    "type",
                ):
                    dictionary = {
                        "pelts": {
                            "pattern_types": {
                                cmd[3 + i]: cmd[4 + i].lower()
                                if len(cmd) >= 5 + i
                                else None
                            }
                        }
                    }
                else:
                    dictionary = {
                        "pelts": {
                            cmd[2 + i]: {
                                cmd[3 + i]: cmd[4 + i]
                                if len(cmd) >= 5 + i
                                else None
                            }
                        }
                    }
        case "pelt_color_palettes":
            if len(cmd) < 3 + i:
                print(
                    "edit pelt_color_palettes [<color> | all] [<part>] [<hexcode>]"
                )
                edit = False
            else:
                _has_part = len(cmd) >= 4 + i
                _has_hexcode = len(cmd) >= 5 + i
                if cmd[2 + i].lower() == "all":
                    if delete:
                        if _has_part:
                            print(
                                "WARNING: this will delete the specified part from ALL colors."
                            )
                        else:
                            print("WARNING: this will delete ALL colors.")

                        if not yes_no_prompt():
                            edit = False
                        else:
                            dictionary = []
                            for color in data:
                                if _has_part:
                                    _dictionary = {
                                        color: {cmd[3 + i].lower(): None}
                                    }
                                else:
                                    _dictionary = {color: None}
                                dictionary.append(_dictionary)
                    elif _has_part:
                        if _has_hexcode:
                            print(
                                "WARNING: this will set the hexcode of ALL colors' specified part (or add the part if not present)."
                            )
                        else:
                            print(
                                "WARNING: this will add this part to ALL colors."
                            )

                        if not yes_no_prompt():
                            edit = False
                        else:
                            dictionary = []
                            for color in data:
                                _dictionary = {
                                    color: {
                                        cmd[3 + i].lower(): cmd[4 + i]
                                        if len(cmd) >= 5 + i
                                        else "#000000"
                                    }
                                }
                                dictionary.append(_dictionary)
                    else:
                        edit = False
                else:
                    if _has_part:
                        dictionary = {
                            cmd[2 + i].upper(): {
                                cmd[3 + i].lower(): cmd[4 + i]
                                if len(cmd) >= 5 + i
                                else "#000000"
                            }
                        }
                    else:
                        dictionary = {cmd[2 + i].upper(): None}

        case "pelt_parts_masks_data":
            print("Currently not supported :(")
            # if len(cmd) < 4+i:
            #   print(
            #       "edit pelt_parts_masks_data spritesheet [<spritesheet>]"
            #       "edit pelt_parts_masks_data sprite_list [<row>] [<sprite> | all]"
            #   )
            #   edit = False
            # else:
            #   if cmd[2+i].lower() in ("spritesheet", "sheet"):
            #       dictionary = {
            #           "spritesheet": cmd[3+i:] if len(cmd) >= 4+i else "pelt_parts_masks"
            #       }
            #   elif cmd[2+i].lower() in ("sprite_list", "sprites_list", "sprites"):
            #       _value = []
            #       for x in range(int(cmd[3+i])):
            #           if x == cmd[3+i]:
            #               _value.append([cmd[4+i]])
            #           else:
            #               _value.append([])
            #       dictionary = {
            #           "sprite_list": _value
            #       }

        case "pelt_to_recipe":
            if len(cmd) < 3 + i:
                print("edit pelt_to_recipe [<pelt>] [<recipe>]")
                edit = False
            else:
                dictionary = {
                    cmd[2 + i]: cmd[3 + i]
                    if len(cmd) >= 4 + i
                    else f"{cmd[2+i]}Recipe"
                }

        case "tint":
            if len(cmd) < 4 + i:
                print(
                    "edit tint colour_groups [<color>] [<group>]"
                    "\nedit tint possible_tints [<group>] [<tints>]"
                    "\nedit tint [tint_colours | dilute_tint_colours] [<color>] [<red, green, blue>]"
                )
                edit = False
            else:
                if cmd[2 + i].lower() in (
                    "colour_groups",
                    "color_groups",
                    "groups",
                ):
                    dictionary = {
                        "colour_groups": {
                            cmd[3 + i].upper(): cmd[4 + i].lower()
                            if len(cmd) >= 5 + i
                            else None
                        }
                    }
                elif cmd[2 + i].lower() in (
                    "possible_tints",
                    "possible_tint",
                ):
                    dictionary = {
                        "possible_tints": {
                            cmd[3 + i].lower(): cmd[4 + i :]
                            if len(cmd) >= 5 + i
                            else []
                        }
                    }
                elif cmd[2 + i].lower() in (
                    "tint_colours",
                    "tint_colors",
                    "dilute_tint_colours",
                    "dilute_tint_colors",
                ):
                    dictionary = {
                        "dilute_tint_colours"
                        if "dilute" in cmd[2 + i].lower()
                        else "tint_colours": {
                            cmd[3 + i].lower(): cmd[4 + i :]
                            if len(cmd) >= 5 + i
                            else None
                        }
                    }
                else:
                    dictionary = {
                        cmd[2 + i].lower(): {
                            cmd[3 + i].lower(): cmd[4 + i :]
                            if len(cmd) >= 5 + i
                            else None
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
        with open(
            f"{SPRITE_DATA_DIR}/{file}.json", "w", encoding="utf-8"
        ) as write_file:
            write_file.write(_data)
            write_file.flush()
            os.fsync(write_file.fileno())

        del _data, data, dictionary
    return edit