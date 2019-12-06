from domain.operator import *

U_OPERATORS = [
    Not.lit()
]

BI_OPERATORS = [
    Conjunction.lit(),
    Disjunction.lit(),
    Xor.lit(),
    Implication.lit(),
    Equivalence.lit()
]

OP_MAPPING = {
    Conjunction.lit(): Conjunction,
    Disjunction.lit(): Disjunction,
    Xor.lit(): Xor,
    Implication.lit(): Implication,
    Equivalence.lit(): Equivalence,
    Not.lit(): Not
}

ALL_OPERATORS = OP_MAPPING.keys()
