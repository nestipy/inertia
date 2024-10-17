from nestipy.core import AppKey
from nestipy.dynamic_module import ConfigurableModuleBuilder

from nestipy_inertia.config import InertiaConfig

ConfigurableModuleClass, INERTIA_MODULE_OPTION_TOKEN = ConfigurableModuleBuilder[InertiaConfig]().build()

INERTIA_HTTPX_CLIENT = '__INERTIA_HTTPX_CLIENT__'

INERTIA_VERSION_CONFLICT_EXCEPTION_FILTER = AppKey.APP_FILTER
