from typing import Annotated

from nestipy.common import Injectable, HttpStatus
from nestipy.common import NestipyMiddleware
from nestipy.common import Request
from nestipy.ioc import Inject
from nestipy.types_ import NextFn
from pydantic import ValidationError

from .builder import INERTIA_MODULE_OPTION_TOKEN
from .config import InertiaConfig
from .exceptions import InertiaVersionConflictException
from .inertia import Inertia
from .response import InertiaResponse


@Injectable()
class InertiaMiddleware(NestipyMiddleware):
    _config: Annotated[InertiaConfig, Inject(INERTIA_MODULE_OPTION_TOKEN)]

    async def use(self, req: Request, res: InertiaResponse, next_fn: NextFn):

        try:
            setattr(res, 'inertia', Inertia(request=req, response=res, config=self._config))
        except InertiaVersionConflictException:
            return res.status(HttpStatus.CONFLICT).header("X-Inertia-Location", str(res.inertia.get_full_url()))
        try:
            return await next_fn()
        except ValidationError as ex:
            validation_errors = ex.errors()
            is_inertia = req.headers.get("x-inertia", False)
            if is_inertia:
                errors = {}
                error_bag = req.headers.get("x-inertia-error-bag", None)
                for error in validation_errors:
                    error_loc = error["loc"][1] if len(error["loc"]) > 1 else error["loc"][0]

                    if error_bag is None:
                        errors[error_loc] = error["msg"]
                    else:
                        if error_bag not in errors:
                            errors[error_bag] = {}
                        errors[error_bag][error_loc] = error["msg"]

                req.session["_errors"] = errors
                status_code = (
                    HttpStatus.TEMPORARY_REDIRECT
                    if req.method == "GET"
                    else HttpStatus.SEE_OTHER
                )
                res.status(status_code)
                return await res.inertia.back()
            else:
                raise ex
