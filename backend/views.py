import os
from io import BytesIO
from urllib.parse import quote

import xlwt
from django.db import connections
from django.http import HttpResponse, StreamingHttpResponse
from reportlab.pdfgen import canvas
from requests import Response

from backend.models import Emp, Dept


def get_bar_data(request):
    """获取条状图数据"""
    names, totals = [], []
    with connections['default'].cursor() as cursor:
        cursor.execute('select name, total from tb_agent t1 '
                       ' left outer join '
                       ' (select agentid, count(agentid) as total '
                       ' from tb_agent_estate group by agentid) t2 '
                       ' on t1.agentid=t2.agentid')
        for row in cursor.fetchall():
            names.append(row[0])
            totals.append(row[1])
    return Response({'x_data': names, 'y_data': totals})


def download(request):
    """下载文件"""
    filename = os.path.join(os.path.dirname(__file__), 'resources/Docker.pdf')
    file_stream = open(filename, 'rb')
    file_iter = iter(lambda: file_stream.read(4096), b'')
    resp = StreamingHttpResponse(file_iter)
    # 设置内容的类型 - MIME类型
    resp['content-type'] = 'application/pdf'
    # 设置内容的处置方式（attachment表示下载；inline表示内联打开）
    target_file = quote('Docker从入门到实践.pdf')
    resp['content-disposition'] = f'attachment; filename={target_file}'
    return resp


def get_style(name, *, color=0, bold=False, italic=False):
    """按照指定的参数获得单元格样式"""
    font = xlwt.Font()
    font.name = name
    font.colour_index = color
    font.bold = bold
    font.italic = italic
    style = xlwt.XFStyle()
    style.font = font
    return style


# 如果导出的Excel报表文件很大而且生成报表的时间较长
# 最好的做法是提前生成好（使用定时任务）放到静态资源服务器上当成静态资源进行处理
def export_excel(request):
    """导出Excel报表"""
    page = int(request.GET.get('page', '1'))
    size = int(request.GET.get('size', '10'))
    # 创建Excel工作簿
    workbook = xlwt.Workbook()
    # 向工作簿中添加工作表
    sheet = workbook.add_sheet('员工详细信息')
    # 设置表头
    titles = ('编号', '姓名', '职位', '主管', '工资', '部门')
    for col, title in enumerate(titles):
        sheet.write(0, col, title, get_style('HanziPenSC-W3', color=2, bold=True))
    # 可以通过only()或者defer()方法来进行SQL投影操作
    props = ('no', 'name', 'job', 'mgr', 'sal', 'dept')
    emps = Emp.objects.all().only(*props)\
        .select_related('mgr').select_related('dept')\
        .order_by('-sal')[(page - 1) * size:page * size]
    # 通过数据库获得的员工数据填写Excel表格
    for row, emp in enumerate(emps):
        for col, prop in enumerate(props):
            # 通过getattr函数获取对象属性值
            val = getattr(emp, prop, '')
            if isinstance(val, (Emp, Dept)):
                val = getattr(val, 'name', '')
            sheet.write(row + 1, col, val)
    # 将Excel表格的数据写入内存中
    buffer = BytesIO()
    workbook.save(buffer)
    # 生成响应对象传输数据给浏览器
    resp = HttpResponse(buffer.getvalue())
    resp['content-type'] = 'application/msexcel'
    filename = quote('员工信息表.xls')
    resp['content-disposition'] = f'attachment; filename="{filename}"'
    return resp


def export_pdf(request):
    """导出PDF报表"""
    buffer = BytesIO()
    doc = canvas.Canvas(buffer)
    doc.setFont("Helvetica", 80)
    doc.setStrokeColorRGB(0.2, 0.5, 0.3)
    doc.setFillColorRGB(1, 0, 1)
    doc.drawString(10, 500, "Hello world!")
    # 最后通过showPage和save实现保存关闭
    doc.showPage()
    doc.save()
    resp = HttpResponse(buffer.getvalue())
    filename = quote('项目设计文档.pdf')
    resp['content-type'] = 'application/pdf'
    resp['content-disposition'] = f'attachment; filename="{filename}"'
    return resp
