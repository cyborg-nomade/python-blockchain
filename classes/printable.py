"""Printable class"""


class Printable:
    """Printable class"""

    def __repr__(self) -> str:
        return str(self.__dict__)
