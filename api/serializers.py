from rest_framework import serializers

from backend.models import Emp, Dept
from common.models import District, Estate, Agent, HouseType, HouseInfo, Tag, User, LoginLog, Role, Privilege


class DeptSerializer(serializers.ModelSerializer):
    """部门序列化器"""

    class Meta:
        model = Dept
        fields = '__all__'


class EmpSimpleSerilizer(serializers.ModelSerializer):
    """员工基本信息序列化器"""

    class Meta:
        model = Emp
        fields = ('no', 'name', 'job')


class EmpDetailSerializer(serializers.ModelSerializer):
    """员工详情序列化器"""

    mgr = serializers.SerializerMethodField()
    dept = serializers.SerializerMethodField()

    @staticmethod
    def get_mgr(emp):
        return EmpSimpleSerilizer(emp.mgr).data

    @staticmethod
    def get_dept(emp):
        return DeptSerializer(emp.dept).data

    class Meta:
        model = Emp
        fields = '__all__'


class DistrictSimpleSerializer(serializers.ModelSerializer):
    """地区基本信息序列化器"""

    class Meta:
        model = District
        fields = ('distid', 'name')


class DistrictDetailSerializer(serializers.ModelSerializer):
    """地区详情信息序列化器"""

    cities = serializers.SerializerMethodField()

    @staticmethod
    def get_cities(district):
        queryset = District.objects.filter(parent__distid=district.distid)
        return DistrictSimpleSerializer(queryset, many=True).data

    class Meta:
        model = District
        fields = ('distid', 'name', 'intro', 'cities')


class AgentSimpleSerializer(serializers.ModelSerializer):
    """经理人基本信息序列化器"""

    class Meta:
        model = Agent
        fields = ('agentid', 'name', 'tel', 'servstar')


class AgentDetailSerializer(serializers.ModelSerializer):
    """经理人详情信息序列化器"""

    estates = serializers.SerializerMethodField()

    @staticmethod
    def get_estates(agent):
        return EstateSimpleSerializer(agent.estates, many=True).data

    class Meta:
        model = Agent
        fields = '__all__'


class EstateSimpleSerializer(serializers.ModelSerializer):
    """楼盘基本信息序列化器"""

    class Meta:
        model = Estate
        fields = ('estateid', 'name', 'hot')


class EstateBasicSerializer(serializers.ModelSerializer):
    district = serializers.IntegerField(source='district.distid')

    def create(self, validated_data):
        district = District.objects.get(distid=validated_data['district']['distid'])
        validated_data['district'] = district
        return Estate.objects.create(**validated_data)

    class Meta:
        model = Estate
        fields = ('estateid', 'district', 'name', 'hot', 'intro')


class EstateDetailSerializer(serializers.ModelSerializer):
    """楼盘详细信息序列化器"""

    district = serializers.SerializerMethodField()
    agents = serializers.SerializerMethodField()

    @staticmethod
    def get_district(estate):
        return DistrictSimpleSerializer(estate.district).data

    @staticmethod
    def get_agents(estate):
        return AgentSimpleSerializer(estate.agents, many=True).data

    class Meta:
        model = Estate
        fields = '__all__'


class HouseTypeSerializer(serializers.ModelSerializer):
    """户型序列化器"""

    class Meta:
        model = HouseType
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """标签序列化器"""

    class Meta:
        model = Tag
        fields = '__all__'


class HouseInfoSerializer(serializers.ModelSerializer):
    """房源信息序列化器"""

    price = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    estate = serializers.SerializerMethodField()
    agent = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    @staticmethod
    def get_price(houseinfo):
        return f'{houseinfo.price} {houseinfo.priceunit}'

    @staticmethod
    def get_type(houseinfo):
        return houseinfo.type.name

    @staticmethod
    def get_district(houseinfo):
        return DistrictSimpleSerializer(houseinfo.district).data

    @staticmethod
    def get_estate(houseinfo):
        return EstateSimpleSerializer(houseinfo.estate).data

    @staticmethod
    def get_agent(houseinfo):
        return AgentSimpleSerializer(houseinfo.agent).data

    @staticmethod
    def get_tags(houseinfo):
        results = []
        for tag in houseinfo.tags.all():
            results.append(tag.name)
        return results

    class Meta:
        model = HouseInfo
        fields = ('houseid', 'title', 'area', 'floor', 'totalfloor',
                  'direction', 'price', 'detail', 'mainphoto', 'pubdate',
                  'street', 'type', 'district', 'estate', 'agent', 'tags')


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""

    class Meta:
        model = User
        fields = '__all__'


class LoginLogSerializer(serializers.ModelSerializer):
    """登录日志序列化器"""

    class Meta:
        model = LoginLog
        fields = '__all__'


class PrivilegeSerializer(serializers.ModelSerializer):
    """权限序列化器"""

    class Meta:
        model = Privilege
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    """角色序列化器"""

    privs = serializers.SerializerMethodField()

    @staticmethod
    def get_privs(role):
        return PrivilegeSerializer(role.privileges, many=True).data

    class Meta:
        model = Role
        fields = ('roleid', 'rolename', 'privs')
