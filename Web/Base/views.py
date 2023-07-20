'''views.py
    视图函数
    若视图函数的处理逻辑太过复杂, 可以先在 `backend.py` 中定义相关的后端处理函数, 再在此处调用
    调用Neo4j数据库时, 导入 neo4j_db/course_graph.py 中的 CourseGraph类
'''

from django.shortcuts import render

# 导入backend.py中的所有函数
from .backend import *

# Create your views here.

# 404
def page_not_found(request, exception):
    return render(request, '404.html')


# 500
def server_error(request):
    return render(request, '500.html')


# 欢迎页面
def welcome_page(request):
    return render(request, 'welcome.html')


# 主页
def index_page(request):
    return render(request, 'index.html')


