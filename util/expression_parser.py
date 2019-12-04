import re
from typing import Union

from domain.operator import Operator
from util.constants import BI_OPERATORS, ALL_OPERATORS, MAPPING
from util.operator_utils import find_brackets_i, split_by_operator, find_operator, is_variable, is_unary, \
    make_cascade_unary


class ParseException(Exception):
    pass


class ExpressionParser:

    def __init__(self, ):
        self.__operator: Operator = None
        self.__variables: dict = dict()
        self.__stack: list = []

    @property
    def variables(self):
        return list(self.__variables.keys())

    @property
    def stack(self):
        return self.__stack

    def parse(self, expression):
        expression = re.sub(r"\s*", "", expression)
        stack = self.__parse(expression)
        stack = self.__refactor_stack(stack)

        self.__stack = stack
        self.__variables = self.__find_variable_names(stack)
        self.__operator = self.__build_operator(stack)

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
                        stack.append(self.__parse(brackets_expr))
                    else:
                        out = list(expr[:start_i])
                        if is_variable(brackets_expr):
                            out += [brackets_expr]
                        else:
                            brackets_expr = self.__parse(brackets_expr)
                            if is_unary(brackets_expr):
                                out.extend(brackets_expr)
                            else:
                                out.append(brackets_expr)
                        out = make_cascade_unary(out)
                        stack.append(out)
                else:
                    stack.append(self.__parse(brackets_expr))

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
                # if expr:
                #     print(expr)
                #     stack.extend(self.__parse(expr))

        new_stack = []
        new_stack = stack
        # for i, part in enumerate(stack):
        #     if is_unary(part):
        #         if isinstance(part[1], str):
        #             part[1] = self.__parse(part[1])
        #         new_stack.append(part)
        #     elif part in ALL_OPERATORS or is_variable(part):
        #         new_stack.append(part)
        #     else:
        #         new_stack.append(self.__parse(part))

        return new_stack

    def __refactor_stack(self, stack: Union[list, str]):
        if isinstance(stack, str):
            return stack
        if len(stack) == 1:
            return self.__refactor_stack(stack[0])
        return [
            self.__refactor_stack(part)
            for part in stack
        ]

    def __find_variable_names(self, stack):
        variables = dict()
        for part in stack:
            if isinstance(part, list):
                variables.update(self.__find_variable_names(part))
            elif part not in ALL_OPERATORS:
                variables.update({part: None})
        return {
            variable: None
            for variable in variables
        }

    def __build_operator(self, stack: Union[list, str]) -> Operator:
        if isinstance(stack, str):
            return lambda: self.__variables[stack]

        if len(stack) == 3:
            operator_class = MAPPING[stack[1]]
            arg1 = self.__build_operator(stack[0])
            arg2 = self.__build_operator(stack[2])
            return operator_class(arg1, arg2)

        # todo compute expression like x1&x2||x3 ( operation priority)

    def compute(self, variables):
        self.__variables.update(variables)
        return self.__operator.compute()
