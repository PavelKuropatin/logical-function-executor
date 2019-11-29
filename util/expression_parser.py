import re

from util.constants import SUPPORTED_OPERATORS, BI_OPERATORS


class ExpressionParser:

    def __init__(self, expression: str):
        self.__expression: str = expression
        self.__operator = None
        self.__vars: dict = dict()

    def parse(self):
        # todo add try catch
        operation_stack = self.__parse(self.__expression)
        operation_stack = operation_stack[0]
        self.__move_up_bi_operators(operation_stack)
        return operation_stack

    @staticmethod
    def __split_by_bi_operator(expression: str):
        if expression in BI_OPERATORS:
            return expression, False
        operation_stack = []
        while expression:
            i, operator = ExpressionParser.__find_nearest_bi_operator(expression)
            if not operator:
                operation_stack.append(expression)
                break
            operation_stack.append(expression[:i])
            operation_stack.append(operator)
            expression = expression[i + len(operator):]
        return operation_stack, len(operation_stack) < 3

    @staticmethod
    def __parse(expression: str):
        brackets = []
        res = re.finditer("[()]", expression)
        for m in res:
            brackets.append((m.start(), expression[m.start()]))
        brackets = sorted(brackets, key=lambda x: x[0])
        brackets_count = 0
        if not brackets:
            return ExpressionParser.__split_by_bi_operator(expression)
        start_i = brackets[0][0]
        for i, br in brackets:
            if br == "(":
                brackets_count += 1
            else:
                brackets_count -= 1
            if brackets_count == 0:
                end_i = i
                break

        expression = [expression[0: start_i], expression[start_i + 1: end_i], expression[end_i + 1:]]
        tmp = [ExpressionParser.__parse(e) for e in expression if e]
        expression = []
        for e, need_destructure in tmp:
            if need_destructure:
                expression += e
            else:
                expression.append(e)
        return expression, False

    @staticmethod
    def __move_up_bi_operators(stack, parent=None, index=None):
        op = stack[0]
        if op in SUPPORTED_OPERATORS:
            parent.insert(index, parent[index][0])
            del parent[index + 1][0]
            if len(parent[index + 1]) == 1:
                parent[index + 1] = parent[index + 1][0]
            return
        for i, op in enumerate(stack):
            if isinstance(op, list):
                ExpressionParser.__move_up_bi_operators(op, stack, i)

    @staticmethod
    def __find_nearest_bi_operator(expression):
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
            i = min(search.keys())
            return i, search[i]
        return None, None

    def compute(self, variables: dict):
        variables = {
            key: lambda: variable
            for key, variable in variables.items()
        }
        self.__vars.update(variables)
        pass
