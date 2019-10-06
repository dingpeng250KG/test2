import datetime

import xlwt

from backend.models import Emp, Dept
from teamproject import app


@app.task
def auto_export_excel():
    """导出Excel报表的定时任务"""
    # 创建Excel工作簿
    workbook = xlwt.Workbook()
    # 向工作簿中添加工作表
    sheet = workbook.add_sheet('员工详细信息')
    # 设置表头
    titles = ('编号', '姓名', '职位', '主管', '工资', '部门')
    for col, title in enumerate(titles):
        sheet.write(0, col, title)
    # 可以通过only()或者defer()方法来进行SQL投影操作
    props = ('no', 'name', 'job', 'mgr', 'sal', 'dept')
    emps = Emp.objects.all().only(*props)\
        .select_related('mgr').select_related('dept')\
        .order_by('-sal')
    # 通过数据库获得的员工数据填写Excel表格
    for row, emp in enumerate(emps):
        for col, prop in enumerate(props):
            # 通过getattr函数获取对象属性值
            val = getattr(emp, prop, '')
            if isinstance(val, (Emp, Dept)):
                val = getattr(val, 'name', '')
            sheet.write(row + 1, col, val)
    # 将Excel表格的数据写入内存中
    current_time = datetime.datetime.now()
    filename = f'员工信息表{current_time.strftime("%Y-%m-%d-%H-%M")}.xlsx'
    filepath = f'/Users/Hao/excel/{filename}'
    workbook.save(filepath)
