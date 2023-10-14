
from api.user_api import router as router_users
from api.login_router import router as router_login
from api.room_api import router as router_rooms


all_routers = [
    router_users,
    router_login,
    router_rooms
]