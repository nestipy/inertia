import os
from typing import Annotated

from nestipy.common import Module
from nestipy.core import HttpAdapter
from nestipy.dynamic_module import NestipyModule, MiddlewareConsumer
from nestipy.ioc import Inject

from .config import InertiaConfig
from .templating import inertia_head, inertia_body, vite_react_refresh
from .builder import ConfigurableModuleClass, INERTIA_MODULE_OPTION_TOKEN
from .middleware import InertiaMiddleware


@Module(
    is_global=True
)
class InertiaModule(ConfigurableModuleClass, NestipyModule):
    _config: Annotated[InertiaConfig, Inject(INERTIA_MODULE_OPTION_TOKEN)]
    http_adapter: Annotated[HttpAdapter, Inject()]

    async def on_startup(self):
        engine = self.http_adapter.get_template_engine()
        if engine.name == "minijinja":
            env = engine.get_env()
            env.add_function("inertiaHead", inertia_head)
            env.add_function("inertiaBody", inertia_body)
            env.add_function("viteReactRefresh", vite_react_refresh)

        front_dir = (
            os.path.join(self._config.root_dir, self._config.build_dir)
            if self._config.environment != "development" or self._config.ssr_enabled is True
            else os.path.join(self._config.root_dir, self._config.src_dir)
        )
        self.http_adapter.static(f"/{self._config.assets_prefix}", front_dir)
        self.http_adapter.static("/assets", os.path.join(front_dir, "assets"))
        if self._config.environment == "development":
            self.http_adapter.static("/node_modules", os.path.join(self._config.root_dir, "node_modules"))

    def configure(self, consumer: MiddlewareConsumer):
        consumer.apply(InertiaMiddleware)
