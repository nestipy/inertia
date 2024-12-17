import os

import uvicorn
from nestipy.common import session
from nestipy.core import NestipyFactory

from app_module import AppModule

app = NestipyFactory.create(AppModule)

# set view engine mini jinja and
app.set_base_view_dir(os.path.join(os.path.dirname(__file__), "views"))

app.use(session())

if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
