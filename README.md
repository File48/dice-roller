### Installation

Run with pipx: `pipx install git+https://github.com/File48/dice-roller.git`

Or, with pip: `pip install git+https://github.com/File48/dice-roller.git`

### Example uses
- `roll d4` -> Returns the roll of a 4 sided die.
- `roll 2d6` -> Returns sum of 2 rolls of a 6 sided die.
- `roll 3d8+1` -> Returns the sum of 3 rolls of a 8 sided die, with a +1 modifier.
- `roll d20-3` -> Returns the roll of a 20 sided die, with a -3 modifier.
- `roll 2d6kh` -> Returns the highest value of 2 rolls of 6 sided die (_advantage_). 
- `roll 2d6kl` -> Returns the lowest value of 2 rolls of 6 sided die (_disadvantage_). 
- `roll 3d10kh2` -> Returns the sum of the 2 highest values of 3 rolls of a 10 sided die (_advanced advantage_). 
