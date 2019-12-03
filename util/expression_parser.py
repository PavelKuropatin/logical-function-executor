import re

from util.constants import SUPPORTED_OPERATORS
from util.operator_utils import find_brackets_i, find_bi_operator, split_by_operator


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

    def __parse(self, expression: str) -> list:
        stack = []
        while expression:
            start_i, end_i = find_brackets_i(expression)

            if start_i is not None and end_i is None:
                raise ParseException("=(")
            if start_i is None:
                if stack:
                    stack.extend(split_by_operator(expression))
                    break
                return split_by_operator(expression), True
            else:
                # if brackets exist
                # if expression starts with bracket

                # extract expression standing before brackets
                tmp = expression[:start_i]
                op, op_len, i = find_bi_operator(tmp, start=False)
                if op:
                    if not tmp.endswith(op):
                        # raise if expression like ||y(...)
                        raise ParseException("=(")

                    out = tmp[:-op_len]
                    if not out:
                        # raise exception if expression like ||(...)
                        import time
                        time.sleep(1)
                        raise ParseException(f"no value before operator: {tmp}")
                    stack.append(out)
                    stack.append(op)

                # add part with brackets
                stack.append(expression[start_i + 1:end_i])

                # extract expression standing after brackets
                expression = expression[end_i + 1:]
                op, op_len, i = find_bi_operator(expression, start=True)
                if op:
                    if not expression.startswith(op):
                        # raise exception if expression like (...)y||
                        raise ParseException("=(")

                    stack.append(op)

                    expression = expression[op_len:]
                    if not expression:
                        # raise exception if expression like (...)||
                        raise ParseException("=(")

        new_stack = []
        for i, part in enumerate(stack):
            out = self.__parse(part)
            if part in SUPPORTED_OPERATORS:
                new_stack.append(part)
                continue

            if isinstance(out, list):
                # if origin stack part is expression containing the brackets
                new_stack.append(out)
            else:
                # if out should be added by item
                # e. g. x1&x2&x3 => ['x1', '&', 'x2', '&', 'x3'] (not [['x1', '&', 'x2'], '&', 'x3'])
                new_stack.extend(out[0])

        return new_stack
