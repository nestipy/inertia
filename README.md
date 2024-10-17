<p align="center">
  <a target="_blank"><img src="https://raw.githubusercontent.com/nestipy/nestipy/release-v1/nestipy.png" width="200" alt="Nestipy Logo" /></a></p>
<p align="center">
    <a href="https://pypi.org/project/nestipy">
        <img src="https://img.shields.io/pypi/v/nestipy?color=%2334D058&label=pypi%20package" alt="Version">
    </a>
    <a href="https://pypi.org/project/nestipy">
        <img src="https://img.shields.io/pypi/pyversions/nestipy.svg?color=%2334D058" alt="Python">
    </a>
    <a href="https://github.com/tsiresymila1/nestipy/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/tsiresymila1/nestipy" alt="License">
    </a>
</p>

## Description

<p>Nestipy is a Python framework built on top of FastAPI that follows the modular architecture of NestJS</p>
<p>Under the hood, Nestipy makes use of <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a>, but also provides compatibility with a wide range of other libraries, like <a href="https://fastapi.tiangolo.com/" target="_blank">Blacksheep</a>, allowing for easy use of the myriad of third-party plugins which are available.</p>

## Getting started

```cmd
pip install nestipy-inertia
```
## Full example
`main.py`
```python
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


```
`app_module.py`
```python
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

```

`vite.config.ts`
```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import nestipyVite from "./nestipy.inertia";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        react(),
        nestipyVite({
            entry: './src/main.tsx',
            ssr: './src/ssr.tsx'
        }),
    ],
})

```

`nestipy.inertia.ts`
```ts
import { PluginOption } from "vite";

type Input = {
    entry: string,
    ssr?: string,
    manifest?: string
}
type NestipyPlugin = (options: Input) => PluginOption
const nestipyVite: NestipyPlugin = ({entry, ssr, manifest = "manifest.json"}) => {
    return {
        name: "nestipy-vite-plugin",
        config: (config, env) => {
            return {
                ...config,
                build: {
                    manifest: env.isSsrBuild ? false: manifest,
                    outDir: env.isSsrBuild ? "dist/ssr" : "dist",
                    rollupOptions: {
                        input: env.isSsrBuild && ssr ? ssr : entry,
                    },
                },
                ssr: {
                    noExternal: ['@inertiajs/server']
                }
            }
        }
    }
}

export default nestipyVite

```
Viw full exapmle code [here](https://github.com/nestipy/inertia/tree/main/example).
## Support

Nestipy is an MIT-licensed open source project. It can grow thanks to the sponsors and support from the amazing backers.
If you'd like to join them, please [read more here].

## Stay in touch

- Author - [Tsiresy Mila](https://tsiresymila.vercel.app)

## License

Nestipy is [MIT licensed](LICENSE).