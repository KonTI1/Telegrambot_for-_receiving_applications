from aiogram import Router
from aiogram.filters import Command

import handlers.user.message as user_message
import handlers.user.callback as user_callback


def setup_router():
    router = Router()
    
    routers = [user_message, user_callback]
    for _router in routers:
        _router.register_handlers()
    
    router.include_routers(*[_router.router for _router in routers])
    return router