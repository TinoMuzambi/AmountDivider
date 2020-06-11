# Tino Muzambi
import sys
import math
from random import randint
from random import seed
from flask import Flask, request, render_template
from wtforms import Form, FloatField, validators, IntegerField

class InputForm(Form):
    amount = FloatField(
        label="amount to divide up",
        validators=[validators.InputRequired()])
    partitions = IntegerField(
        label="number of partitions",
        validators=[validators.InputRequired()])


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        result = get_bins_alt4(form.amount.data, form.partitions.data)
    else:
        result = None

    return render_template('index.html', form=form, result=result)


def get_bins_alt(full_amount, no_bins):
    bins = []

    sub_amount = 0
    if full_amount % no_bins == 0:
        for i in range(no_bins):
            bins.append(full_amount / no_bins)
        for i in range(no_bins - 1, 0, -1):
            sub_amount = 0.75 * bins[i]
            bins[i] -= sub_amount
            bins[i - 1] += sub_amount

    bins[0] -= sub_amount
    return bins


def get_bins_alt2(full_amount, no_bins):
    bins = []

    sub_amount = 0
    if full_amount % no_bins == 0:
        for i in range(no_bins):
            bins.append(full_amount / no_bins)
        for i in range(no_bins - 1, 0, -1):
            sub_amount = 0.75 * bins[i]
            bins[i] -= sub_amount
            for j in range(i):
                bins[j] += sub_amount * (1 / i)

    bins[0] -= sub_amount
    return bins


def get_bins_alt3(full_amount, no_bins):
    bins = []

    seed(1)
    randoms = []

    for i in range(no_bins):
        randoms.append(randint(0, 100))
    tot_rand = sum(randoms)
    for i in range(no_bins):
        bins.append((randoms[i] / tot_rand) * full_amount)

    return sorted(bins)


def get_bins_alt4(full_amount, no_bins):
    bins = []

    for i in range(no_bins):
        bins.append(full_amount / no_bins)
    for i in range(no_bins):
        cum_sum = 0
        for j in range(i, no_bins):
            sub_amount = 0.1 * bins[j]
            cum_sum += sub_amount
            bins[j] -= sub_amount
        bins[i] += cum_sum

    out = ""
    for i in range(len(bins)):
        out += "Partition " + str(i + 1) + " - " + "{:.2f}\n".format(bins[i])
    return out


def get_bins(full_amount, no_bins):
    bins = []
    first_ratio = math.ceil(no_bins / 2)
    for i in range(no_bins):
        bins.append(full_amount * (first_ratio / 10))
        first_ratio -= no_bins / 10
    return bins


def main():
    full_amount = int(sys.argv[1])
    num_bins = int(sys.argv[2])
    out_bins = get_bins_alt4(full_amount, num_bins)
    print(out_bins)
    print(sum(out_bins))


if __name__ == '__main__':
    app.run(debug=True)
