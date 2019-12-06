from domain.value import ZERO, DC, ONE, VALUES


class LogicalException(BaseException):
    pass


class Operator:

    def __init__(self, *args):
        self._args = args

    def compute(self):
        raise LogicalException("Not implemented")

    @staticmethod
    def priority() -> int:
        raise LogicalException("Not implemented")

    @staticmethod
    def lit() -> str:
        raise LogicalException("Not implemented")

    @staticmethod
    def _get_arg_value(arg):
        if isinstance(arg, Operator):
            return arg.compute()
        elif isinstance(arg, Variable):
            return arg.value()
        elif arg in VALUES:
            return arg
        else:
            raise LogicalException(f"Unknown arg: {arg}")


class Variable:

    def __init__(self, arg):
        self.__value = arg

    def value(self):
        if callable(self.__value):
            return self.__value()
        return self.__value


class Conjunction(Operator):

    def __init__(self, *args):
        super().__init__(*args)

    def compute(self):
        if len(self._args) != 2:
            raise LogicalException("args count is not 2")

        arg1 = self._get_arg_value(self._args[0])
        arg2 = self._get_arg_value(self._args[1])
        if ZERO in (arg1, arg2):
            value = ZERO
        elif DC in (arg1, arg2):
            value = DC
        else:
            value = ONE
        return value

    @staticmethod
    def priority() -> int:
        return 1

    @staticmethod
    def lit() -> str:
        return "&&"


class Disjunction(Operator):

    def __init__(self, *args):
        super().__init__(*args)

    def compute(self):
        if len(self._args) != 2:
            raise LogicalException("args count is not 2")

        arg1 = self._get_arg_value(self._args[0])
        arg2 = self._get_arg_value(self._args[1])
        if ONE in (arg1, arg2):
            value = ONE
        elif DC in (arg1, arg2):
            value = DC
        else:
            value = ZERO
        return value

    @staticmethod
    def priority():
        return 2

    @staticmethod
    def lit() -> str:
        return "||"


class Xor(Operator):

    def __init__(self, *args):
        super().__init__(*args)

    def compute(self):
        if len(self._args) != 2:
            raise LogicalException("args count is not 2")

        arg1 = self._get_arg_value(self._args[0])
        arg2 = self._get_arg_value(self._args[1])
        if arg1 == arg2 and DC not in (arg1, arg2):
            value = ZERO
        elif arg1 != arg2 and DC not in (arg1, arg2):
            value = ONE
        else:
            value = DC
        return value

    @staticmethod
    def priority():
        return 2

    @staticmethod
    def lit() -> str:
        return "~"


class Implication(Operator):

    def __init__(self, *args):
        super().__init__(*args)

    def compute(self):
        if len(self._args) != 2:
            raise LogicalException("args count is not 2")

        arg1 = self._get_arg_value(self._args[0])
        arg2 = self._get_arg_value(self._args[1])
        if arg1 == ZERO:
            value = ONE
        elif (arg1, arg2) == (ONE, ONE):
            value = ONE
        elif (arg1, arg2) == (ONE, ZERO):
            value = ZERO
        else:
            value = DC
        return value

    @staticmethod
    def priority():
        return 3

    @staticmethod
    def lit() -> str:
        return "-->"


class Equivalence(Operator):

    def __init__(self, *args):
        super().__init__(*args)

    def compute(self):
        if len(self._args) != 2:
            raise LogicalException("args count is not 2")

        arg1 = self._get_arg_value(self._args[0])
        arg2 = self._get_arg_value(self._args[1])
        if arg1 == arg2 and DC not in (arg1, arg2):
            value = ONE
        elif arg1 != arg2 and DC not in (arg1, arg2):
            value = ZERO
        else:
            value = DC
        return value

    @staticmethod
    def priority():
        return 3

    @staticmethod
    def lit() -> str:
        return "<->"


class Not(Operator):

    def __init__(self, *args):
        super().__init__(*args)

    def compute(self):
        # if len(self._args) != ONE:
        #     raise LogicalException("args count is not 1")

        arg = self._get_arg_value(self._args[0])
        if arg == ONE:
            value = ZERO
        elif arg == ZERO:
            value = ONE
        else:
            value = DC
        return value

    @staticmethod
    def priority():
        return 0

    @staticmethod
    def lit() -> str:
        return "!"
