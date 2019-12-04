from itertools import combinations_with_replacement

from util.constants import DC

__VALUES = (0, 1, DC)


def generate_variables(names):
    return [
        {
            names[i]: values[i]
            for i in range(len(values))
        }
        for values in combinations_with_replacement(__VALUES, len(names))
    ]
