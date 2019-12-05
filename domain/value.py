class __Value:
    def __init__(self, value):
        self.__val = value

    @property
    def val(self):
        return self.__val

    def __eq__(self, o: object) -> bool:
        return self is o

    def __str__(self) -> str:
        return "dc" if self.__val is None else str(self.__val)

    def __repr__(self):
        return self.__str__()


ONE = __Value(1)
ZERO = __Value(0)
DC = __Value(None)
VALUES = (ONE, ZERO, DC)
