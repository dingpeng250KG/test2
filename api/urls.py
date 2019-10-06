from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import get_provinces
from api.views import get_cities
from api.views import login
from api.views import AgentViewSet
from api.views import EstateViewSet
from api.views import HouseTypeViewSet
from api.views import HouseInfoViewSet
from api.views import TagViewSet
from api.views import UserViewSet
from api.views import RoleViewSet
from api.views import PrivViewSet
from api.views import LoginLogViewSet
from api.views import EmpViewSet
from api.views import DeptViewSet

urlpatterns = [
    path('login/', login, name='login'),
    path('districts/', get_provinces, name='districts'),
    path('districts/<int:pid>/', get_cities, name='district'),
]

router = DefaultRouter()
viewset_dict = {
    'agents': AgentViewSet,
    'estates': EstateViewSet,
    'housetypes': HouseTypeViewSet,
    'houseinfos': HouseInfoViewSet,
    'tags': TagViewSet,
    'users': UserViewSet,
    'roles': RoleViewSet,
    'privs': PrivViewSet,
    'loginlogs': LoginLogViewSet,
    'emps': EmpViewSet,
    'depts': DeptViewSet,
}
for key, value in viewset_dict.items():
    router.register(key, value)
urlpatterns += router.urls
