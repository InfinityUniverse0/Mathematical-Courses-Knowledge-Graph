'''views.py
    视图函数
    若视图函数的处理逻辑太过复杂,可以先在 `backend.py` 中定义相关的后端处理函数,再在此处调用
    调用Neo4j数据库时, 导入 neo4j_db/course_graph.py 中的 CourseGraph类
'''

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings


# 导入backend.py中的所有函数
from .backend import *
import jieba


# Create your views here.
def QA_normal(request):
    if request.method == 'POST':
        question = request.POST.get('question').strip()
        seg_list = jieba.cut(question)
    return render(request, 'QA.html')



def QA_advanced(request):
    if request.method == 'POST':
        question = request.POST.get('question').strip()
    return render(request, 'QA.html')