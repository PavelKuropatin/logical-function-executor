from typing import Union, List

from util.constants import BI_OPERATORS, RE_BRACKETS, U_OPERATORS


def find_bi_operator(expression, start=True):
    search = {
        operator: expression.find(operator)
        for operator in BI_OPERATORS
    }
    search = {
        i: operator
        for operator, i in search.items()
        if i != -1
    }
    if search:
        func = min if start else max
        i = func(search.keys())
        op = search[i]
        return op, len(op), i
    return None, None, None


def find_brackets_i(expression):
    brackets = []
    res = RE_BRACKETS.finditer(expression)
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
    if expression in U_OPERATORS or expression in BI_OPERATORS:
        return expression
    if not expression:
        return []
    stack = []
    while expression:
        op, op_len, i = find_bi_operator(expression, start=True)

        if not op:
            if stack:
                stack.append(expression)
            else:
                stack = [expression]
            return stack

        stack.append(expression[:i])
        stack.append(op)
        expression = expression[i + op_len:]
