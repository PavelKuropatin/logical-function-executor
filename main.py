from util.constants import DC
from util.expression_parser import ExpressionParser

if __name__ == '__main__':
    expression = "x3&((x1&x1)||(~x2||(x1&x2)))"
    # expression = "x1&x2||x3"
    variables = [
        {"x1": 1, "x2": 1},
        {"x1": 1, "x2": 0},
        {"x1": 1, "x2": DC},
        {"x1": 0, "x2": 1},
        {"x1": 0, "x2": 0},
        {"x1": 0, "x2": DC},
        {"x1": DC, "x2": 1},
        {"x1": DC, "x2": 0},
        {"x1": DC, "x2": DC},
    ]
    expression_parser = ExpressionParser(expression)
    stack = expression_parser.parse()
    print(stack)
