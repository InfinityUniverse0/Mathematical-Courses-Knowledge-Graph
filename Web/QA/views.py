'''views.py
    视图函数
    若视图函数的处理逻辑太过复杂,可以先在 `backend.py` 中定义相关的后端处理函数,再在此处调用
    调用Neo4j数据库时, 导入 neo4j_db/course_graph.py 中的 CourseGraph类
'''

from django.shortcuts import render

# 导入backend.py中的所有函数
from .backend import *

# 导入neo4j_db/course_graph.py 中的 CourseGraph类
import sys
sys.path.append("..")
from neo4j_db.course_graph import CourseGraph

# Create your views here.
