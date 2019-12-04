from util.constants import DC
from util.expression_parser import ExpressionParser

if __name__ == '__main__':
    variables = [
        {"x1": 0, "x2": 0},
        {"x1": 1, "x2": 0},
        {"x1": 0, "x2": 1},
        {"x1": 1, "x2": 1},
        {"x1": 0, "x2": DC},
        {"x1": 1, "x2": DC},
        {"x1": DC, "x2": 1},
        {"x1": DC, "x2": 0},
        {"x1": DC, "x2": DC},
    ]

    expressions = [
        "(x1&x2)|x3"
        ,
        # "x1&(x2|x3)"
        # ,
        # "~(x1&(x2|x3&x4))"
        # ,
        # "x1 & ( (x2& x3) | (~x4 | (x5&x6) ) )"
        # ,
        # "x0|x1&((x2& x3)|(~x4|(x5&x6)))|x7"
        # ,
        # "x3 | x4  & ((x 1& x1) | (~x2 | (x1&x2) ) )"
        # ,
        # "((x3 & ( (x 1& x1) | (~~x2 | (x1&x2) ) )))"
        # ,
        # "~(x1|~~~~~x2)|~x3"
        # ,
        # "~(x1)|~x3"
        # ,
        # "((x3 & ( (x1 & x1) | (~~~(~x2&x5) | (x1&x2) ) )))"
        # ,
        # "((x3 & ( (x1 & x1) | (~~~(~x2) | (x1&x2) ) )))"
        # ,
        # "(( ((x3)) & ( (x1 & x1) | (~~~(x2) | (x1&x2) ) )))"
        # ,
        # " x3 & ( (x1 & x1) | (~~~(x2) | ((((((x1))&((x2)))))) ) )"
    ]
    expression_parser = ExpressionParser()

    for e in expressions:
        print("input  :", e)
        expression_parser.parse(e)
        print("result :", expression_parser.stack)
        print("vars   :", expression_parser.variables)
        print("-" * 70)
