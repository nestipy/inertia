from abc import abstractmethod
from typing import Union, TYPE_CHECKING

from nestipy.common import Response, TemplateEngine

if TYPE_CHECKING:
    from .inertia import Inertia


class InertiaResponse(Response):
    def __init__(self, template_engine: Union["TemplateEngine", None] = None):
        super().__init__(template_engine=template_engine)

    @property
    @abstractmethod
    def inertia(self) -> "Inertia":
        pass
