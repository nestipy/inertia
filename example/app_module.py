import os.path

from nestipy.common import Module

from app_controller import AppController
from app_service import AppService
from nestipy_inertia import InertiaModule, InertiaConfig
from nestipy.common import Module

from app_controller import AppController
from app_service import AppService
from nestipy_inertia import InertiaModule, InertiaConfig


@Module(
    imports=[
        InertiaModule.register(
            InertiaConfig(
                root_dir=os.path.join(os.getcwd(), "inertia")
            )
        )
    ],
    controllers=[AppController],
    providers=[
        AppService,
    ]
)
class AppModule:
    ...
