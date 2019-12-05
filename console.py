import sys

from domain.value import as_str
from util.expression_parser import ExpressionParser
from util.generate_utils import generate_variables

if __name__ == '__main__':

    # expressions = [
    #         "(x1&&x2)||x2",
    #         "(x1&&x2)",
    #         "x1&&(x2||x3)",
    #         "!(x1&&(x2||x3&&x4))",
    #         "x1 && ( (x2&& x3) || (!x4 || (x5&&x6) ) )",
    #         "x0||x1&&((x2&& x3)||(!x4||(x5&&x6)))||x7",
    #         "x3 || x4  && ((x 1&& x1) || (!x2 || (x1&&x2) ) )",
    #         "((x2 && ( (x 1&& x1) || (!!x2 || (x1&&x2) ) )))",
    #         "!(x1||!!!!!x2)||!x3",
    #         "!(x1)||!x3",
    #         "((x3 && ( (x1 && x1) || (!!!(!x2&&x5) || (x1&&x2) ) )))",
    #         "((x3 && ( (x1 && x1) || (!!!(!x2) || (x1&&x2) ) )))",
    #         "(( ((x3)) && ( (x1 && x1) || (!!!(x2) || (x1&&x2) ) )))",
    #         " x3 && ( (x1 && x1) || (!!!(x2) || ((((((x1))&&((x2)))))) ) )"
    #     ]

    args = sys.argv[1:]
    if not args:
        sys.exit(1)

    expressions = args

    expression_parser = ExpressionParser()

    for e in expressions:
        print("input        :", e)
        expression_parser.parse(e)
        var_names = expression_parser.variables
        data = generate_variables(var_names)
        print("result stack :", expression_parser.stack)
        print("vars         :", expression_parser.variables)
        for variables in data:
            print("value        :", as_str(expression_parser.compute(variables)), variables)
        print("-" * 70)
