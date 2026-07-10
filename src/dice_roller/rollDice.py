"""
1d6 = 1 roll of 6 sided
2d10 = 2 rolls of 10 sided

2d6+5 = 2 rolls of 6 sided, add 5
1d4-1 = 1 roll of 4 sided, minus 1

2d6kl = 2 rolls of 6 sided, keep the lowest value
4d10kl2 = 4 rolls of 10 sided, sum 2 lowest values

2d6kh = 2 rolls of 6 sided, keep the highest value
3d10kh2 = 2 rolls of 10 sided, sum 2 highest values

4d10kl2+5 = 4 rolls of 10 sided, sum 2 lowest values, add 5
2d12kh-3 = 2 rolls of 12 sided, take the highest values, minus 3
"""
from random import randrange
import typer
from typing_extensions import Annotated


def keep_count_separation(_roll_string, kh_kl) -> tuple:
    _keepCount = 0
    for char in _roll_string[_roll_string.index(kh_kl) + 2:]:
        if char.isnumeric():
            _keepCount = _keepCount * 10 + int(char)
        else:
            break

    if _keepCount == 0:
        _roll_string = _roll_string.replace(kh_kl, "")
        _keepCount = 1
    else:
        _roll_string = _roll_string.replace(kh_kl + str(_keepCount), "")

    return _roll_string, _keepCount


def roll_dice(roll_string):
    is_advantage = False
    is_disadvantage = False
    keep_count = 0
    modifier = 0
    modifier_is_negative = False

    # Parsing
    roll_string = str(roll_string).lower().strip()

    if "d" not in roll_string:
        return "Roll string must contain the character 'd' (e.g. 2d6 or d10)",

    if "kh" in roll_string or "kl" in roll_string:
        if "kh" in roll_string and "kl" in roll_string:
            return "Roll string must only contain 'kh' or 'kl' (e.g. 2d6kh)",

        if "kh0" in roll_string or "kl0" in roll_string:
            return "'kh' or 'kl' can't be followed by a 0.",

        if "kh" in roll_string:
            is_advantage = True
            roll_string, keep_count = keep_count_separation(roll_string, "kh")

        elif "kl" in roll_string:
            is_disadvantage = True
            roll_string, keep_count = keep_count_separation(roll_string, "kl")

    if "+" in roll_string or "-" in roll_string:
        if "+" in roll_string and "-" in roll_string:
            return "Roll string can only contain either a + or a -, not both (e.g. 2d6+3).",

        if "+" in roll_string:
            modifier_idx = roll_string.index("+")
            modifier = roll_string[modifier_idx + 1:]
            roll_string = roll_string[:modifier_idx]

        if "--" in roll_string:
            return "Roll string can only contain a single - (e.g. 2d6-3).",

        elif "-" in roll_string:
            modifier_is_negative = True
            modifier_idx = roll_string.index("-")
            modifier = roll_string[modifier_idx + 1:]
            roll_string = roll_string[:modifier_idx]

    if roll_string[0] != "d":
        roll_amount, _, dice_value = roll_string.partition("d")
    else:
        roll_amount = 1
        dice_value = roll_string[1:]

    # Type validation
    try:
        roll_amount = int(roll_amount)
        dice_value = int(dice_value)
        modifier = int(modifier)

    except ValueError:
        return "Invalid roll string. See 'dice --help' for examples.",

    if roll_amount < keep_count:
        return "Keep count has to be less than the amount of rolls. (e.g. 5d6kh2)",

    if roll_amount <= 0:
        return "Roll amount must be greater than 0.",

    if dice_value <= 0:
        return "Dice value must be greater than 0.",

    if modifier_is_negative:
        modifier = -modifier
    return [roll_amount, dice_value, modifier, is_advantage, is_disadvantage, keep_count]


def dice_roll_cli(
        roll_string: Annotated[str, typer.Argument(help="Your dice roll. E.g 'd6' or '4d6+1' or '2d6kh'")] = ""
):
    """
    1d6 = 1 roll of 6 sided
    2d10 = 2 rolls of 10 sided

    2d6+5 = 2 rolls of 6 sided, add 5
    1d4-1 = 1 roll of 4 sided, minus 1

    2d6kl = 2 rolls of 6 sided, keep the lowest value
    4d10kl2 = 4 rolls of 10 sided, sum 2 lowest values

    2d6kh = 2 rolls of 6 sided, keep the highest value
    3d10kh2 = 2 rolls of 10 sided, keep the 2 highest values

    4d10kl2+5 = 4 rolls of 10 sided, keep the 2 lowest values, add 5
    2d12kh-3 = 2 rolls of 12 sided, keep the highest value, minus 3
    """

    try:
        dice_roll = roll_dice(roll_string)
    except (ValueError, IndexError):
        typer.echo("Invalid roll string. See 'dice --help' for examples.", err=True)
        raise typer.Exit(code=1)

    if len(dice_roll) == 1:
        typer.echo(dice_roll[0], err=True)
        raise typer.Exit(code=1)

    roll_amount, dice_value, modifier, is_advantage, is_disadvantage, keep_count = dice_roll
    rolled_dice = []
    for _ in range(roll_amount):
        rolled_dice.append(randrange(1, dice_value+1))
    if len(rolled_dice) != 1:
        print("Rolled dice: ", rolled_dice)

    if is_advantage:
        rolled_dice = sorted(rolled_dice, reverse=False)[-keep_count:]

    if is_disadvantage:
        rolled_dice = sorted(rolled_dice, reverse=True)[-keep_count:]

    roll_value = sum(rolled_dice)
    roll_value += modifier

    print("Roll value: ", roll_value)
