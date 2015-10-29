

import math


def mean(samples):
    if len(samples) == 0:
        return 0
    sum = 0
    for s in samples:
        sum += s
    return sum / len(samples)


def variance(samples):
    if len(samples) == 0:
        return 0

    meanv = mean(samples)
    sum = 0
    for s in samples:
        sum += math.pow(s - meanv,2)

    return sum / len(samples)


def stand_deviation(samples):
    return math.sqrt(variance(samples))