from uuid import uuid1

from django.db import transaction
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from api.filters import HouseInfoFilter, EstateFilter, AgentFilter
from api.helpers import LoginAuthentication, CustomPermission, AllowGetAuthentication
from api.serializers import DistrictSimpleSerializer, DistrictDetailSerializer, EmpDetailSerializer, DeptSerializer, \
    AgentDetailSerializer, TagSerializer, UserSerializer, LoginLogSerializer, RoleSerializer, PrivilegeSerializer, \
    EstateBasicSerializer
from api.serializers import EstateDetailSerializer, HouseTypeSerializer, HouseInfoSerializer
from common.models import District, Estate, HouseType, HouseInfo, User, UserToken, LoginLog, Agent, Tag, Role, Privilege
from backend.models import Emp, Dept
from common.utils import to_md5_hex, get_ip_address


@api_view(['POST'])
def login(request):
    resp_dict = {'code': 30000, 'message': '用户登录成功'}
    username = request.data.get('username', '')
    password = request.data.get('password', '')
    password = to_md5_hex(password)
    user = User.objects.filter(username=username, password=password) \
        .only('userid').first()
    if user:
        request.session['userid'] = user.userid
        request.session['realname'] = user.realname
        with transaction.atomic():
            resp_dict['token'] = token = uuid1().hex
            UserToken.objects.update_or_create(user=user, defaults={'token': token})
            current_time = timezone.now()
            delta = current_time - user.lastvisit
            if delta.days >= 1:
                user.point += 5
                user.lastvisit = current_time
                user.save()
            log = LoginLog()
            log.user = user
            log.ipaddr = get_ip_address(request)
            log.save()
    else:
        resp_dict['code'] = '30001'
        resp_dict['message'] = '用户名或密码错误'
    return Response(resp_dict)


@api_view(['GET'])
@cache_page(timeout=86400 * 365, cache='api', key_prefix='provinces')
def get_provinces(request):
    queryset = District.objects.filter(parent__isnull=True).only('name')
    serializer = DistrictSimpleSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@cache_page(timeout=600, cache='api', key_prefix='cities')
def get_cities(request, pid):
    queryset = District.objects.filter(distid=pid).first()
    serializer = DistrictDetailSerializer(queryset)
    return Response(serializer.data)


# @method_decorator(decorator=cache_page(timeout=120, cache='api', key_prefix='estates'), name='get')
# class EstateView(RetrieveAPIView, ListCreateAPIView):
#     serializer_class = EstateDetailSerializer
#     pagination_class = CustomPagination
#
#     def get_queryset(self):
#         dist = self.request.GET.get('dist', None)
#         name = self.request.GET.get('name', None)
#         q = Q()
#         if dist:
#             q |= Q(district__distid=int(dist))
#         if name:
#             q |= Q(name__contains=name)
#         queryset = Estate.objects.filter(q) \
#             .select_related('district').prefetch_related('agents') \
#             .order_by('-hot')
#         return queryset
#
#     def get(self, request, *args, **kwargs):
#         return RetrieveAPIView.get(self, request, *args, **kwargs) \
#             if 'pk' in kwargs else ListCreateAPIView.get(self, request, *args, **kwargs)


class AgentViewSet(CacheResponseMixin, ModelViewSet):
    queryset = Agent.objects.all()\
        .prefetch_related('estates').order_by('agentid')
    serializer_class = AgentDetailSerializer
    authentication_classes = (AllowGetAuthentication, LoginAuthentication)
    permission_classes = (CustomPermission, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = AgentFilter


class EstateViewSet(CacheResponseMixin, ModelViewSet):
    queryset = Estate.objects.all()\
        .select_related('district').prefetch_related('agents')\
        .order_by('-hot')
    # serializer_class = EstateDetailSerializer
    authentication_classes = (AllowGetAuthentication, LoginAuthentication)
    permission_classes = (CustomPermission, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = EstateFilter

    def get_serializer_class(self):
        return EstateBasicSerializer if self.request.method == 'POST' \
            else EstateDetailSerializer


class HouseTypeViewSet(CacheResponseMixin, ModelViewSet):
    queryset = HouseType.objects.all().order_by('typeid')
    serializer_class = HouseTypeSerializer
    authentication_classes = (AllowGetAuthentication, LoginAuthentication)
    permission_classes = (CustomPermission, )
    pagination_class = None


class HouseInfoViewSet(CacheResponseMixin, ModelViewSet):
    queryset = HouseInfo.objects.all() \
        .select_related('type', 'district', 'estate', 'agent') \
        .prefetch_related('tags').order_by('-pubdate')
    serializer_class = HouseInfoSerializer
    authentication_classes = (AllowGetAuthentication, LoginAuthentication)
    permission_classes = (CustomPermission, )
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = HouseInfoFilter
    ordering = ('price',)
    ordering_fields = ('price', 'area')


class TagViewSet(CacheResponseMixin, ModelViewSet):
    queryset = Tag.objects.all().order_by('tagid')
    serializer_class = TagSerializer
    authentication_classes = (AllowGetAuthentication, LoginAuthentication)
    permission_classes = (CustomPermission, )
    pagination_class = None


class LoginLogViewSet(CacheResponseMixin, ModelViewSet):
    queryset = LoginLog.objects.all().order_by('logid')
    authentication_classes = (LoginAuthentication,)
    permission_classes = (CustomPermission, )
    serializer_class = LoginLogSerializer


class UserViewSet(CacheResponseMixin, ModelViewSet):
    queryset = User.objects.all().order_by('userid')
    serializer_class = UserSerializer
    authentication_classes = (LoginAuthentication,)
    permission_classes = (CustomPermission, )


class RoleViewSet(CacheResponseMixin, ModelViewSet):
    queryset = Role.objects.all().order_by('roleid')
    serializer_class = RoleSerializer
    authentication_classes = (LoginAuthentication,)
    permission_classes = (CustomPermission, )
    pagination_class = None


class PrivViewSet(CacheResponseMixin, ModelViewSet):
    queryset = Privilege.objects.all().order_by('privid')
    serializer_class = PrivilegeSerializer
    authentication_classes = (LoginAuthentication,)
    permission_classes = (CustomPermission, )


class EmpViewSet(ModelViewSet):
    queryset = Emp.objects.all().order_by('-no')
    serializer_class = EmpDetailSerializer
    authentication_classes = (LoginAuthentication,)
    permission_classes = (CustomPermission, )
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('dept', )


class DeptViewSet(ModelViewSet):
    queryset = Dept.objects.all().order_by('no')
    serializer_class = DeptSerializer
    authentication_classes = (LoginAuthentication,)
    permission_classes = (CustomPermission, )
    pagination_class = None
