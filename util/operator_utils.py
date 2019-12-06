import re
from functools import cmp_to_key
from typing import Union, List

from util.constants import BI_OPERATORS, U_OPERATORS, ALL_OPERATORS, OP_MAPPING

RE_BRACKETS = re.compile("[()]")
REG_U_OP = re.compile("|".join([re.escape(_) for _ in U_OPERATORS]))
REG_BI_OP = re.compile("|".join([re.escape(_) for _ in BI_OPERATORS]))
REG_ALL_OP = re.compile("|".join([re.escape(_) for _ in ALL_OPERATORS]))


def find_operator(expression, from_start=True, operators=ALL_OPERATORS):
    if operators == ALL_OPERATORS:
        pattern = REG_ALL_OP
    elif operators == BI_OPERATORS:
        pattern = REG_BI_OP
    elif operators == U_OPERATORS:
        pattern = REG_U_OP
    else:
        raise RuntimeError(f"no pattern for operators: {str(operators)}")
    try:
        search_result = re.finditer(pattern, expression)
    except TypeError as e:
        raise TypeError(expression)
    re_operators = [
        (m.group(), m.end() - m.start(), m.start())
        for m in search_result
    ]
    out = (None, None, None)
    if re_operators:
        index = 0 if from_start else -1
        return re_operators[index]
    return out


def __operator_cmp(item1, item2) -> int:
    op1 = item1[0]
    op2 = item2[0]
    if op1.priority() > op2.priority():
        return 1
    elif op1.priority() < op2.priority():
        return -1
    else:
        return 1 if item1[1] < item2[1] else -1


def find_operator_by_priority(stack: List):
    operators = [
        (OP_MAPPING[part], i)
        for i, part in enumerate(stack)
        if isinstance(part, str) and part in OP_MAPPING
    ]

    operators = sorted(operators, key=cmp_to_key(__operator_cmp), reverse=True)
    print(operators)
    return operators[0]


def is_variable(expression: str) -> bool:
    return find_operator(expression) == (None, None, None)


def is_unary(stack: list):
    return len(stack) == 2 and stack[0] in U_OPERATORS


def find_brackets_i(expression):
    brackets = []
    try:
        res = RE_BRACKETS.finditer(expression)
    except TypeError:
        raise TypeError(expression)
    for m in res:
        brackets.append((m.start(), expression[m.start()]))
    if not brackets:
        return None, None

    start_i = brackets[0][0]
    end_i = None
    brackets_count = 0
    for op, br in brackets:
        if br == "(":
            brackets_count += 1
        else:
            brackets_count -= 1
        if brackets_count == 0:
            end_i = op
            break

    if not end_i:
        return start_i, None
    return start_i, end_i


def split_by_operator(expression: str) -> Union[List[str], str]:
    if is_variable(expression) or expression in ALL_OPERATORS:
        return expression
    if not expression:
        return []

    stack = __split_by_operators(expression, operators=BI_OPERATORS)
    for i, part in enumerate(stack):
        # todo maybe delete the same unary operators, e.g. ~~x => x
        out = __split_by_operators(part, operators=U_OPERATORS)
        if isinstance(out, str) or len(out) == 2:
            stack[i] = out
        else:
            stack[i] = make_cascade_unary(out)

    return stack if len(stack) != 1 else stack[0]


def __split_by_operators(expression, operators=None):
    if is_variable(expression) or expression in ALL_OPERATORS:
        return expression
    if not expression or not operators:
        return []
    stack = []
    while expression:
        op, op_len, i = find_operator(expression, from_start=True, operators=operators)
        if not op:
            if stack:
                stack.append(expression)
            else:
                stack = [expression]
            break
        if i:
            stack.append(expression[:i])
        stack.append(op)
        expression = expression[i + op_len:]
    return stack


def make_cascade_unary(stack: list):
    if len(stack) == 2:
        return stack
    return [stack[0], make_cascade_unary(stack[1:])]
