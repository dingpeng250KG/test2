from django.db import models


class Dept(models.Model):
    no = models.IntegerField(primary_key=True, db_column='dno')
    name = models.CharField(max_length=10, db_column='dname')
    loc = models.CharField(max_length=20, db_column='dloc')

    class Meta:
        managed = False
        db_table = 'tb_dept'
        app_label = 'hrs'


class Emp(models.Model):
    no = models.IntegerField(primary_key=True, db_column='eno')
    name = models.CharField(max_length=20, db_column='ename')
    job = models.CharField(max_length=20)
    mgr = models.ForeignKey('self', models.SET_NULL, db_column='mgr', blank=True, null=True)
    sal = models.IntegerField()
    comm = models.IntegerField(blank=True, null=True)
    dept = models.ForeignKey(Dept, models.PROTECT, db_column='dno', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_emp'
        app_label = 'hrs'
