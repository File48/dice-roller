import typer
from .rollDice import dice_roll_cli

app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]}
)
app.command()(dice_roll_cli)

if __name__ == "__main__":
    app()
