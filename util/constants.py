from domain.operator import *

U_OPERATORS = [
    Not.lit()
]

BI_OPERATORS = [
    Conjunction.lit(),
    Disjunction.lit(),
    Xor.lit(),
    Implication.lit(),
    Equivalence.lit(),
    PeirceArrow.lit(),
    SchaefferBar.lit()
]

OP_MAPPING = {
    Conjunction.lit(): Conjunction,
    Disjunction.lit(): Disjunction,
    Xor.lit(): Xor,
    Implication.lit(): Implication,
    Equivalence.lit(): Equivalence,
    Not.lit(): Not,
    PeirceArrow.lit(): PeirceArrow,
    SchaefferBar.lit(): SchaefferBar
}

ALL_OPERATORS = OP_MAPPING.keys()
