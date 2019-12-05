from domain.operator import *

CONJUNCTION = "&&"  # and
DISJUNCTION = "||"  # or
XOR = "~"
IMPLICATION = "-->"
EQUIVALENCE = "<->"
NOT = "!"

U_OPERATORS = [NOT]
BI_OPERATORS = [CONJUNCTION, DISJUNCTION, XOR, IMPLICATION, EQUIVALENCE]
ALL_OPERATORS = U_OPERATORS + BI_OPERATORS

MAPPING = {
    CONJUNCTION: Conjunction,
    DISJUNCTION: Disjunction,
    XOR: Xor,
    IMPLICATION: Implication,
    EQUIVALENCE: Equivalence,
    NOT: Not
}
