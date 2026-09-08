import os

from flask import Flask, render_template, request
from wtforms import FloatField, Form, IntegerField, validators

app = Flask(__name__)


class InputForm(Form):
    amount = FloatField(
        "Amount",
        validators=[
            validators.InputRequired(),
            validators.NumberRange(
                min=0.01,
                max=1_000_000_000_000,
                message="Amount must be between 0.01 and 1 trillion.",
            ),
        ],
    )
    partitions = IntegerField(
        "Partitions",
        validators=[
            validators.InputRequired(),
            validators.NumberRange(
                min=1,
                max=1_000,
                message="Partitions must be between 1 and 1,000.",
            ),
        ],
    )


@app.route("/", methods=["GET", "POST"])
def index():
    form = InputForm(request.form)
    result = None

    if request.method == "POST" and form.validate():
        result = format_partitions(divide_amount(form.amount.data, form.partitions.data))

    return render_template("index.html", form=form, result=result)


def divide_amount(full_amount: float, no_bins: int) -> list[float]:
    """Split an amount into decreasing partitions while preserving the total."""
    if full_amount <= 0:
        raise ValueError("full_amount must be positive")
    if not 1 <= no_bins <= 1_000:
        raise ValueError("no_bins must be between 1 and 1,000")

    bins = [full_amount / no_bins for _ in range(no_bins)]

    for index in range(no_bins):
        cumulative_amount = 0.0
        for candidate in range(index, no_bins):
            transferred_amount = 0.1 * bins[candidate]
            cumulative_amount += transferred_amount
            bins[candidate] -= transferred_amount
        bins[index] += cumulative_amount

    return bins


def format_partitions(partitions: list[float]) -> str:
    return "\n".join(
        f"Partition {index} - {amount:.2f}"
        for index, amount in enumerate(partitions, start=1)
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "4000")),
        debug=os.environ.get("FLASK_DEBUG") == "1",
    )
