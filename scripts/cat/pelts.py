from scripts.load_sprites import sprites

class Pelt:
    # ACCESSORIES
    # make sure to add plural and singular forms of new accs to accessories.en.json so that they will display nicely

    # all acc sprites are labeled as occupying a specific part of the cat sprite and then appended into these three lists
    # collar_accessories are presumed to all occupy the neck area and are treated as the fourth of these lists
    tail_accessories = []
    body_accessories = []
    head_accessories = []

    # here we create the master lists of each accessory type
    plant_accessories = []
    for sprite_list in sprites.PLANT_DATA["sprite_list"]:
        plant_accessories.extend(sprite_list)
        for sprite in sprite_list:
            if sprite_list[sprite] == "tail":
                tail_accessories.append(sprite)
            elif sprite_list[sprite] == "body":
                body_accessories.append(sprite)
            elif sprite_list[sprite] == "head":
                body_accessories.append(sprite)

    wild_accessories = []
    for sprite_list in sprites.WILD_DATA["sprite_list"]:
        wild_accessories.extend(sprite_list)
        for sprite in sprite_list:
            if sprite_list[sprite] == "tail":
                tail_accessories.append(sprite)
            elif sprite_list[sprite] == "body":
                body_accessories.append(sprite)
            elif sprite_list[sprite] == "head":
                body_accessories.append(sprite)

    collar_accessories = []
    collar_styles = []
    if sprites.COLLAR_DATA["palette_map"]:
        for style_type in sprites.COLLAR_DATA["style_data"]:
            for style, color_list in style_type.items():
                collar_styles.append(style)
                for colour in color_list:
                    collar_accessories.append(f"{style}_{colour}")
    else:
        for sprite_list in sprites.COLLAR_DATA["sprite_list"]:
            collar_accessories.extend(sprite_list)

    # this is used for acc-giving events, only change if you're adding a new category tag to the event filter
    # adding a category here will automatically update the event editor's options
    acc_categories = {
        "PLANT": plant_accessories,
        "WILD": wild_accessories,
        "COLLAR": collar_accessories,
    }

    def __init__(self) -> None:
        pass