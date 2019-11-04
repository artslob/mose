from abc import ABC, abstractmethod
from enum import Enum


class ChoicesEnumMeta(type(Enum), type(ABC)):
    pass


class ChoicesEnum(Enum, metaclass=ChoicesEnumMeta):
    """
    Enum to be used with choices argument for field. Use like this:

    class MyCustomEnum(ChoicesEnum):
        CAR = 'car'
        VEHICLE = 'vehicle'

        @classmethod
        def default(cls):
            return cls.CAR.name

    class SomeModel(models.Model):
        field = models.CharField(
            max_length=MyCustomEnum.max_length(), choices=MyCustomEnum.choices(), default=MyCustomEnum.default()
        )
    """

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def max_length(cls):
        return max(len(i.name) for i in cls)

    @classmethod
    @abstractmethod
    def default(cls):
        raise NotImplementedError
