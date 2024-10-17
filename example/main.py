import os

import uvicorn
from nestipy.core import NestipyFactory
from nestipy.common import session
from app_module import AppModule, inertia_config
from nestipy_inertia import inertia_head, inertia_body, vite_react_refresh

app = NestipyFactory.create(AppModule)

# set view engine mini jinja and
app.set_base_view_dir(os.path.join(os.path.dirname(__file__), "views"))

# app.use_static_assets()
env = app.get_template_engine().get_env()
env.add_function("inertiaHead", inertia_head)
env.add_function("inertiaBody", inertia_body)

# When using react
env.add_function("viteReactRefresh", vite_react_refresh)
# Inertia config

front_dir = (
    os.path.join(os.path.dirname(__file__), "inertia", "dist")
    if inertia_config.environment != "development" or inertia_config.ssr_enabled is True
    else os.path.join(os.path.dirname(__file__), "inertia", "src")
)

app.use_static_assets(front_dir, "/dist")
app.use_static_assets(os.path.join(front_dir, "assets"), "/assets")
app.use(session())

if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
