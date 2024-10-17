import os

from nestipy.common import Module

from app_controller import AppController
from app_service import AppService
from nestipy_inertia import InertiaModule, InertiaConfig

inertia_config = InertiaConfig(
    manifest_json_path=os.path.join(
        os.path.dirname(__file__), "inertia", "dist", "manifest.json"
    ),
    environment="development",
    use_flash_messages=True,
    use_flash_errors=True,
    entrypoint_filename="main.tsx",
    ssr_enabled=False,
    assets_prefix="/dist",
)


@Module(
    imports=[
        InertiaModule.register(
            inertia_config
        )
    ],
    controllers=[AppController],
    providers=[
        AppService,
    ]
)
class AppModule:
    ...
