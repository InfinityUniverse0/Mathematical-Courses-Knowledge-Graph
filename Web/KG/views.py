'''views.py
    视图函数
    若视图函数的处理逻辑太过复杂,可以先在 `backend.py` 中定义相关的后端处理函数,再在此处调用
    调用Neo4j数据库时, 导入 neo4j_db/course_graph.py 中的 CourseGraph类
'''

from django.shortcuts import render
from django.http import JsonResponse


# 导入backend.py中的所有函数
from backend import *
graph = init_neo4j()

# Create your views here.
def query_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name').strip()
        # 寻找课程节点，可以有多个
        cypher = '''MATCH (n:课程) 
                 WHERE n.name CONTAINS {} 
                 RETURN n'''.format(course_name)
        cursor = graph.run(cypher).data()
        node_dict, pnt = nodes_to_list(cursor), 1
        for node in node_dict:
            # 寻找每个课程的知识模块
            cypher = '''
                    MATCH (n:课程)
                    WHERE n.name = '{}' 
                    with n
                    OPTIONAL MATCH p = (m)-[r]->(k)
                    WHERE exists((m)-[:属于]->(n))
                    RETURN p
                      '''.format(node['name'])
            cursor = graph.run(cypher).data()
            path_dict, pnt = paths_to_list(cursor, pnt)

        # 构建返回的数据字典
        response_data = {
            'nodes': node_dict,
            'edges': path_dict
        }
        return JsonResponse(response_data)
    return render(request, 'query.html')


def query_all(request):
    if request.method == 'POST':
        pass

