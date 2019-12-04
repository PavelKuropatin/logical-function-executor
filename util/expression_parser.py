import re

from util.constants import ALL_OPERATORS, BI_OPERATORS
from util.operator_utils import find_brackets_i, split_by_operator, find_operator, is_variable, is_unary


class ParseException(Exception):
    pass


class ExpressionParser:

    def __init__(self, ):
        self.__operator = None
        self.__vars: dict = dict()
        self.__stack: list = None

    def parse(self, expression):
        expression = re.sub(r"\s*", "", expression)
        stack = self.__parse(expression)
        return stack

    def __parse(self, expr: str) -> list:
        stack = []
        while expr:
            start_i, end_i = find_brackets_i(expr)

            if start_i is not None and end_i is None:
                raise ParseException(f"{expr} has unclosed bracket")
            if start_i is None:
                out = split_by_operator(expr)
                if stack:
                    stack.append(out)
                    break
                return out
            else:
                # if brackets exist
                # if expression starts with bracket
                # extract expression standing before brackets
                expr_before_brackets = expr[:start_i]
                op, op_length, i = find_operator(expr_before_brackets, from_start=False)
                brackets_expr = expr[start_i + 1:end_i]
                if op:
                    if op in BI_OPERATORS:
                        if not expr_before_brackets.endswith(op) or len(expr_before_brackets) == op_length:
                            raise ParseException(f"{expr_before_brackets} like <operator><var>(...) or <operator>(...)")

                        expr_before_brackets = expr_before_brackets[:-op_length]
                        if is_variable(expr_before_brackets):
                            stack.append(expr_before_brackets)
                        else:
                            expr_before_brackets = split_by_operator(expr_before_brackets)
                            if len(expr_before_brackets) == 3:
                                stack.extend(expr_before_brackets)
                            else:
                                stack.append(expr_before_brackets)
                        stack.append(op)
                        stack.append(brackets_expr)
                    else:
                        stack.append([op, brackets_expr])
                else:
                    stack.append(brackets_expr)

                # extract expression standing after brackets
                expr = expr[end_i + 1:]
                op, op_length, i = find_operator(expr, from_start=True)
                if op:
                    if not expr.startswith(op):
                        raise ParseException(f"{expr} like (...)<var><operator><end>")
                    stack.append(op)

                    expr = expr[op_length:]
                    if not expr:
                        raise ParseException(f"{expr} like (...)<operator><end>")

        new_stack = []
        for i, part in enumerate(stack):
            if is_unary(part):
                part[1] = self.__parse(part[1])
                new_stack.append(part)
            elif part in ALL_OPERATORS or is_variable(part):
                new_stack.append(part)
            else:
                new_stack.append(self.__parse(part))

        return new_stack
