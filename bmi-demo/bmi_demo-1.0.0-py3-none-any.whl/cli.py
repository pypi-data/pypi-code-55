import typer
from bmi_demo.bmi import calculate_bmi, classify_bmi

app = typer.Typer()

weight_option = typer.Option(
        1, "-w", "--weight", help="Specify weight", show_default=True
)

height_option = typer.Option(
    1, "-h", "--height", help="Specify height", show_default=True
)

@app.command("calculate")
def calculate(
    weight: float = weight_option, 
    height: float = height_option):
    """Calculates the BMI of a certain weight and height."""
    bmi = calculate_bmi(weight, height)
    typer.echo(f"The BMI of weight {weight} and height {height} is {bmi}")


@app.command("classify")
def classify(
    weight: float = weight_option, 
    height: float = height_option):
    """Determines the BMI group of a certain weight and height."""
    classification = classify_bmi(weight, height)
    typer.echo(f"The BMI classification of weight {weight} and height {height} is {classification}")


def main():
    app()

if __name__ == "__main__":
    app()