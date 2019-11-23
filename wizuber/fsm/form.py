from abc import ABCMeta


class IForm(metaclass=ABCMeta):
    pass


class DeleteForm(IForm):
    pass


class PayForm(IForm):
    pass


class OwnForm(IForm):
    pass
