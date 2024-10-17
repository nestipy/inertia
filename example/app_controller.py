from typing import Annotated

from nestipy.common import Controller, Get, Response, Post
from nestipy.ioc import Inject, Res, Body
from pydantic import BaseModel, EmailStr

from app_service import AppService
from nestipy_inertia import InertiaResponse
from nestipy_inertia import lazy


class UserLogin(BaseModel):
    email: EmailStr
    password: str


@Controller()
class AppController:
    service: Annotated[AppService, Inject()]

    @Get()
    async def get(self, res: Annotated[InertiaResponse, Res()]) -> Response:
        props = {
            "message": "hello from index",
            "lazy_prop": lazy(lambda: "hello from lazy prop"),
        }
        return await res.inertia.render("Index", props)

    @Get('/2')
    async def get2(self, res: Annotated[InertiaResponse, Res()]) -> Response:
        res.inertia.flash("hello from index2 (through flash)", category="message")
        return await res.redirect('/3')

    @Get('/3')
    async def get3(self, res: Annotated[InertiaResponse, Res()]) -> Response:
        res.inertia.flash("hello from index3 (through flash)", category="message")
        return await res.inertia.render("Other", {})

    @Post("/login")
    async def some_form(self, user: Annotated[UserLogin, Body()], res: Annotated[InertiaResponse, Res()]) -> Response:
        res.inertia.flash("form submitted", category="message")
        return await res.inertia.back()
