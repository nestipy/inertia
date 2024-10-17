from nestipy.common import Module
from nestipy.dynamic_module import NestipyModule, MiddlewareConsumer

from .builder import ConfigurableModuleClass
from .middleware import InertiaMiddleware


@Module(
    is_global=True
)
class InertiaModule(ConfigurableModuleClass, NestipyModule):
    def configure(self, consumer: MiddlewareConsumer):
        consumer.apply(InertiaMiddleware)
