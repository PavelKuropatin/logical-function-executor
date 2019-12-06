import re
from typing import Union

from domain.operator import Operator, Variable
from util.constants import BI_OPERATORS, OP_MAPPING
from util.operator_utils import find_brackets_i, split_by_operator, find_operator, is_variable, is_unary, \
    make_cascade_unary, find_operator_by_priority


class ParseException(Exception):
    pass


class ExpressionParser:

    def __init__(self, ):
        self.__operator = None
        self.__variables: dict = dict()
        self.__stack: list = []

    @property
    def variables(self):
        return list(self.__variables.keys())

    @property
    def stack(self):
        return self.__stack

    def parse(self, expression) -> None:
        self.__variables.clear()
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
                if out is None:
                    raise ParseException(f"Invalid expression: {expr}")
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

        return stack

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
        if isinstance(stack, str) and stack not in OP_MAPPING:
            return {
                stack: None
            }
        variables = dict()
        for part in stack:
            if isinstance(part, list):
                variables.update(self.__find_variable_names(part))
            elif isinstance(part, str) and part not in OP_MAPPING:
                variables.update({part: None})
        return {
            variable: None
            for variable in variables
        }

    def __build_operator(self, stack: Union[list, str]) -> Union[Operator, Variable]:
        if isinstance(stack, Operator):
            return stack

        if isinstance(stack, str):
            return Variable(lambda: self.__variables[stack])

        if len(stack) == 2:
            # build unary operator
            operator_class = OP_MAPPING[stack[0]]
            arg1 = self.__build_operator(stack[1])
            return operator_class(arg1)

        if len(stack) == 3:
            # build binary operator
            operator_class = OP_MAPPING[stack[1]]
            arg1 = self.__build_operator(stack[0])
            arg2 = self.__build_operator(stack[2])
            return operator_class(arg1, arg2)

        operator_class, i = find_operator_by_priority(stack)
        stack[i - 1: i + 2] = [self.__build_operator(stack[i - 1: i + 2])]

        return self.__build_operator(stack)

    def compute(self, variables):
        self.__variables.update(variables)
        if isinstance(self.__operator, Variable):
            return self.__operator.value()
        return self.__operator.compute()
