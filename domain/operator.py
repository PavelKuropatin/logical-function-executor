from util.constants import DC, CONJUNCTION, DISJUNCTION, IMPLICATION, EQUIVALENCE, XOR, NOT


class LogicalException(BaseException):
    pass


class BaseOperator:
    mark = None

    def __init__(self, *args):
        self._args = args

    def compute(self):
        raise LogicalException("Not implemented")

    @staticmethod
    def _get_arg_value(arg):
        if isinstance(arg, BaseOperator):
            return arg.compute()
        elif callable(arg):
            return arg()
        elif arg in (0, 1, DC):
            return arg
        else:
            raise LogicalException(f"Unknown arg: {arg}")


class Conjunction(BaseOperator):
    mark = CONJUNCTION

    def __init__(self, *args):
        super().__init__(*args)

    def compute(self):
        if len(self._args) != 2:
            raise LogicalException("args count is not 2")

        arg1 = self._get_arg_value(self._args[0])
        arg2 = self._get_arg_value(self._args[1])
        if 0 in (arg1, arg2):
            value = 0
        elif DC in (arg1, arg2):
            value = DC
        else:
            value = 1
        return value


class Disjunction(BaseOperator):
    mark = DISJUNCTION

    def __init__(self, *args):
        super().__init__(*args)

    def compute(self):
        if len(self._args) != 2:
            raise LogicalException("args count is not 2")

        arg1 = self._get_arg_value(self._args[0])
        arg2 = self._get_arg_value(self._args[1])
        if 1 in (arg1, arg2):
            value = 1
        elif DC in (arg1, arg2):
            value = DC
        else:
            value = 0
        return value


class Xor(BaseOperator):
    mark = XOR

    def __init__(self, *args):
        super().__init__(*args)

    def compute(self):
        if len(self._args) != 2:
            raise LogicalException("args count is not 2")

        arg1 = self._get_arg_value(self._args[0])
        arg2 = self._get_arg_value(self._args[1])
        if arg1 == arg2 and DC not in (arg1, arg2):
            value = 0
        elif arg1 != arg2 and DC not in (arg1, arg2):
            value = 1
        else:
            value = DC
        return value


class Implication(BaseOperator):
    mark = IMPLICATION

    def __init__(self, *args):
        super().__init__(*args)

    def compute(self):
        if len(self._args) != 2:
            raise LogicalException("args count is not 2")

        arg1 = self._get_arg_value(self._args[0])
        arg2 = self._get_arg_value(self._args[1])
        if arg1 == 0:
            value = 1
        elif (arg1, arg2) == (1, 1):
            value = 1
        elif (arg1, arg2) == (1, 0):
            value = 0
        else:
            value = DC
        return value


class Equivalence(BaseOperator):
    mark = EQUIVALENCE

    def __init__(self, *args):
        super().__init__(*args)

    def compute(self):
        if len(self._args) != 2:
            raise LogicalException("args count is not 2")

        arg1 = self._get_arg_value(self._args[0])
        arg2 = self._get_arg_value(self._args[1])
        if arg1 == arg2 and DC not in (arg1, arg2):
            value = 1
        elif arg1 != arg2 and DC not in (arg1, arg2):
            value = 0
        else:
            value = DC
        return value


class Not(BaseOperator):
    mark = NOT

    def __init__(self, *args):
        super().__init__(*args)

    def compute(self):
        # if len(self._args) != 1:
        #     raise LogicalException("args count is not 1")

        arg = self._get_arg_value(self._args[0])
        if arg == 1:
            value = 0
        elif arg == 0:
            value = 1
        else:
            value = None
        return value
