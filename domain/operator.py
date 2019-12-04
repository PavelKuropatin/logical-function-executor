from util import constants


class LogicalException(BaseException):
    pass


class Operator:

    def __init__(self, *args):
        self._args = args

    def compute(self):
        raise LogicalException("Not implemented")

    @staticmethod
    def _get_arg_value(arg):
        if isinstance(arg, Operator):
            return arg.compute()
        elif callable(arg):
            return arg()
        elif arg in (0, 1, constants.DC):
            return arg
        else:
            raise LogicalException(f"Unknown arg: {arg}")


class Conjunction(Operator):

    def __init__(self, *args):
        super().__init__(*args)

    def compute(self):
        if len(self._args) != 2:
            raise LogicalException("args count is not 2")

        arg1 = self._get_arg_value(self._args[0])
        arg2 = self._get_arg_value(self._args[1])
        if 0 in (arg1, arg2):
            value = 0
        elif constants.DC in (arg1, arg2):
            value = constants.DC
        else:
            value = 1
        return value


class Disjunction(Operator):

    def __init__(self, *args):
        super().__init__(*args)

    def compute(self):
        if len(self._args) != 2:
            raise LogicalException("args count is not 2")

        arg1 = self._get_arg_value(self._args[0])
        arg2 = self._get_arg_value(self._args[1])
        if 1 in (arg1, arg2):
            value = 1
        elif constants.DC in (arg1, arg2):
            value = constants.DC
        else:
            value = 0
        return value


class Xor(Operator):

    def __init__(self, *args):
        super().__init__(*args)

    def compute(self):
        if len(self._args) != 2:
            raise LogicalException("args count is not 2")

        arg1 = self._get_arg_value(self._args[0])
        arg2 = self._get_arg_value(self._args[1])
        if arg1 == arg2 and constants.DC not in (arg1, arg2):
            value = 0
        elif arg1 != arg2 and constants.DC not in (arg1, arg2):
            value = 1
        else:
            value = constants.DC
        return value


class Implication(Operator):

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
            value = constants.DC
        return value


class Equivalence(Operator):

    def __init__(self, *args):
        super().__init__(*args)

    def compute(self):
        if len(self._args) != 2:
            raise LogicalException("args count is not 2")

        arg1 = self._get_arg_value(self._args[0])
        arg2 = self._get_arg_value(self._args[1])
        if arg1 == arg2 and constants.DC not in (arg1, arg2):
            value = 1
        elif arg1 != arg2 and constants.DC not in (arg1, arg2):
            value = 0
        else:
            value = constants.DC
        return value


class Not(Operator):

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
