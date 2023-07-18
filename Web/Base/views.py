'''views.py
    视图函数
    若视图函数的处理逻辑太过复杂, 可以先在 `backend.py` 中定义相关的后端处理函数, 再在此处调用
    调用Neo4j数据库时, 导入 neo4j_db/course_graph.py 中的 CourseGraph类
'''

from django.shortcuts import render

# 导入backend.py中的所有函数
from .backend import *

# 导入neo4j_db/course_graph.py 中的 CourseGraph类
import sys

sys.path.append("..")
from neo4j_db.course_graph import CourseGraph

from django.http import HttpResponse, JsonResponse
from django.conf import settings
from py2neo import Graph, Node, Relationship
import openai
import json

openai.api_key = settings.OPENAI_API_KEY


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


# 聊天页面
# - 暂时存放在此,以后可能会迁移到其他应用下
def chat(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')

        try:
            data = json.loads(body)
            message = data.get('message')
        except json.JSONDecodeError:
            return JsonResponse({'ERROR': 'Invalid JSON data.'}, status=400)

        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {'role': 'user', 'content': message}
                ]
            )
            completion = response['choices'][0]['message']['content']
        except Exception as e:
            completion = 'ERROR: ' + str(e)

        return JsonResponse({'completion': completion})

    return render(request, 'chat.html')
