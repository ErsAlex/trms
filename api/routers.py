
from api.user_api import router as router_users
from api.login_router import router as router_login


all_routers = [
    router_users,
    router_login
]