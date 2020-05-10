# Tino Muzambi
import sys


def get_bins(full_amount, no_bins):
    bins = []
    first_ratio = no_bins - 2 # TODO set this dynamically.
    for i in range(no_bins):
        bins.append(full_amount * (first_ratio / 10))
        first_ratio -= no_bins / 10
    return bins


def main():
    full_amount = int(sys.argv[1])
    num_bins = int(sys.argv[2])
    print(get_bins(full_amount, num_bins))


if __name__ == '__main__':
    main()
