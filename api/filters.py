from django_filters import rest_framework as drf
from common.models import Estate, HouseInfo, Agent


class AgentFilter(drf.FilterSet):
    """自定义经理人数据过滤器"""

    name = drf.CharFilter(lookup_expr='istartswith')
    star = drf.NumberFilter(field_name='servstar', lookup_expr='gte')
    cert = drf.BooleanFilter(field_name='certificated')

    class Meta:
        model = Agent
        fields = ('name', 'star', 'cert')


class EstateFilter(drf.FilterSet):
    """自定义楼盘数据过滤器"""

    name = drf.CharFilter(lookup_expr='contains')
    dist = drf.NumberFilter(field_name='district')

    class Meta:
        model = Estate
        fields = ('name', 'dist')


class HouseInfoFilter(drf.FilterSet):
    """自定义房源数据过滤器"""

    title = drf.CharFilter(lookup_expr='contains')
    dist = drf.NumberFilter(field_name='district')
    min_price = drf.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = drf.NumberFilter(field_name='price', lookup_expr='lte')
    type = drf.NumberFilter()

    class Meta:
        model = HouseInfo
        fields = ('title', 'district', 'min_price', 'max_price', 'type')
