"""
项目规模较大且有专业的DBA设计数据库 - 反向工程
python manage.py inspectdb > common/models.py

项目规模较小没有专业的DBA设计数据库 - 正向工程
python manage.py makemigrations common
python manage.py migrate

如果要优化数据库性能，就要减少不必要的数据库外键约束，可以通过代码层面的约束来保证参照完整性
使用正向工程时，可以给ForeignKey添加一个db_constraint=False的设定来取消外键约束
"""
from django.db import models


class Agent(models.Model):
    """经纪人"""
    agentid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    tel = models.CharField(max_length=20)
    servstar = models.IntegerField(default=0)
    realstar = models.IntegerField(default=0)
    profstar = models.IntegerField(default=0)
    certificated = models.BooleanField(default=False)
    estates = models.ManyToManyField('Estate', through='AgentEstate')

    def __str__(self):
        return self.name or ''

    class Meta:
        # managed = False
        db_table = 'tb_agent'


class AgentEstate(models.Model):
    """经纪人楼盘"""
    agent_estate_id = models.AutoField(primary_key=True)
    estate = models.ForeignKey('Estate', models.DO_NOTHING, db_column='estateid')
    agent = models.ForeignKey('Agent', models.DO_NOTHING, db_column='agentid')

    class Meta:
        # managed = False
        db_table = 'tb_agent_estate'
        unique_together = (('estate', 'agent'),)


class District(models.Model):
    """地区"""
    distid = models.IntegerField(primary_key=True)
    parent = models.ForeignKey('self', models.DO_NOTHING, db_column='pid', blank=True, null=True)
    name = models.CharField(max_length=255)
    intro = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name or ''

    class Meta:
        # managed = False
        db_table = 'tb_district'


class Estate(models.Model):
    """楼盘"""
    estateid = models.AutoField(primary_key=True)
    district = models.ForeignKey(District, models.DO_NOTHING, db_column='distid')
    name = models.CharField(max_length=255)
    hot = models.IntegerField(default=0, blank=True, null=True)
    intro = models.CharField(max_length=511, blank=True, null=True)
    agents = models.ManyToManyField('Agent', through='AgentEstate')

    def __str__(self):
        return self.name or ''

    class Meta:
        # managed = False
        db_table = 'tb_estate'


class HouseInfo(models.Model):
    """房源信息"""
    houseid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    area = models.IntegerField()
    floor = models.IntegerField()
    totalfloor = models.IntegerField()
    direction = models.CharField(max_length=10)
    price = models.IntegerField()
    priceunit = models.CharField(max_length=10)
    detail = models.TextField(max_length=10240, blank=True, null=True)
    mainphoto = models.CharField(max_length=255)
    pubdate = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    street = models.CharField(max_length=255)
    hassubway = models.BooleanField(default=False)
    isshared = models.BooleanField(default=False)
    hasagentfees = models.BooleanField(default=False)
    type = models.ForeignKey('HouseType', models.DO_NOTHING, db_column='typeid')
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='userid')
    district = models.ForeignKey('District', models.DO_NOTHING, db_column='distid')
    estate = models.ForeignKey('Estate', models.DO_NOTHING, db_column='estateid', blank=True, null=True)
    agent = models.ForeignKey('Agent', models.DO_NOTHING, db_column='agentid', blank=True, null=True)
    tags = models.ManyToManyField('Tag', through='HouseTag')

    class Meta:
        # managed = False
        db_table = 'tb_house_info'


class HousePhoto(models.Model):
    """房源照片"""
    photoid = models.AutoField(primary_key=True)
    house = models.ForeignKey('HouseInfo', on_delete=models.DO_NOTHING, db_column='houseid')
    path = models.CharField(max_length=255)

    class Meta:
        # managed = False
        db_table = 'tb_house_photo'


class HouseTag(models.Model):
    """房源标签"""
    house_tag_id = models.AutoField(primary_key=True)
    tag = models.ForeignKey('Tag', on_delete=models.DO_NOTHING, db_column='tagid')
    house = models.ForeignKey('HouseInfo', on_delete=models.DO_NOTHING, db_column='houseid')

    class Meta:
        # managed = False
        db_table = 'tb_house_tag'
        unique_together = (('tag', 'house'),)


class HouseType(models.Model):
    """房源户型"""

    typeid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name or ''

    class Meta:
        # managed = False
        db_table = 'tb_house_type'


class LoginLog(models.Model):
    """登录日志"""

    logid = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING, db_column='userid')
    ipaddr = models.CharField(max_length=255)
    logdate = models.DateTimeField(auto_now_add=True)
    devcode = models.CharField(max_length=255, default='')

    class Meta:
        # managed = False
        db_table = 'tb_login_log'


class Record(models.Model):
    """浏览记录"""

    recordid = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING, db_column='userid')
    house = models.ForeignKey('HouseInfo', on_delete=models.DO_NOTHING, db_column='houseid')
    recorddate = models.DateTimeField(auto_now=True)

    class Meta:
        # managed = False
        db_table = 'tb_record'
        unique_together = (('user', 'house'),)


class Tag(models.Model):
    """标签"""

    tagid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name or ''

    class Meta:
        # managed = False
        db_table = 'tb_tag'


class User(models.Model):
    """用户"""

    userid = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=32)
    realname = models.CharField(max_length=20)
    tel = models.CharField(unique=True, max_length=20)
    email = models.CharField(unique=True, max_length=255)
    createdate = models.DateTimeField(auto_now_add=True)
    point = models.IntegerField(default=0)
    lastvisit = models.DateTimeField(null=True, blank=True)
    is_authenticated = models.BooleanField(null=False, default=False)
    roles = models.ManyToManyField('Role', through='UserRole')

    def __str__(self):
        return self.username

    class Meta:
        # managed = False
        db_table = 'tb_user'


class UserToken(models.Model):
    """用户令牌"""

    tokenid = models.AutoField(primary_key=True)
    token = models.CharField(max_length=32)
    user = models.OneToOneField('User', on_delete=models.CASCADE, db_column='userid')

    class Meta:
        # managed = False
        db_table = 'tb_user_token'


class Role(models.Model):
    """角色"""

    roleid = models.AutoField(primary_key=True)
    rolename = models.CharField(max_length=255, null=False)
    privileges = models.ManyToManyField('Privilege', through='RolePrivilege')

    class Meta:
        # managed = False
        db_table = 'tb_role'


class UserRole(models.Model):
    """用户角色（中间实体）"""
    urid = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='userid', null=False)
    role = models.ForeignKey('Role', on_delete=models.CASCADE, db_column='roleid', null=False)

    class Meta:
        # managed = False
        db_table = 'tb_user_role'
        unique_together = (('user', 'role'), )


class Privilege(models.Model):
    """权限"""

    privid = models.AutoField(primary_key=True)
    url = models.CharField(max_length=1024, null=False)
    method = models.CharField(max_length=15, null=False)

    class Meta:
        # managed = False
        db_table = 'tb_privilege'


class RolePrivilege(models.Model):
    """角色权限（中间实体）"""

    rpid = models.AutoField(primary_key=True)
    role = models.ForeignKey('Role', on_delete=models.CASCADE, db_column='roleid', null=False)
    privilege = models.ForeignKey('Privilege', on_delete=models.CASCADE, db_column='privid', null=False)

    class Meta:
        # managed = False
        db_table = 'tb_role_privilege'
        unique_together = (('role', 'privilege'), )
