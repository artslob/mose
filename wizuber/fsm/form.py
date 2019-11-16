from abc import ABCMeta, abstractmethod


class IForm(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def template_name(cls) -> str:
        pass

    @classmethod
    def get_full_template_name(cls) -> str:
        return f'wizuber/action/{cls.template_name()}.html'


class DeleteForm(IForm):
    @classmethod
    def template_name(cls) -> str:
        return 'delete'
