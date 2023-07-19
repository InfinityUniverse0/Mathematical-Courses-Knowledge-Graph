'''views.py
    视图函数
    若视图函数的处理逻辑太过复杂,可以先在 `backend.py` 中定义相关的后端处理函数,再在此处调用
    调用Neo4j数据库时, 导入 neo4j_db/course_graph.py 中的 CourseGraph类
'''

from django.shortcuts import render
from django.http import JsonResponse
import jieba
import json

# 导入backend.py中的所有函数
from backend import *

graph = init_neo4j()


# Create your views here.
def query_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name').strip()
        # 寻找课程节点，可以有多个
        cypher = '''MATCH (n:课程) 
                 WHERE n.name CONTAINS '{}'
                 RETURN n'''.format(course_name)
        cursor = graph.run(cypher).data()
        node_list = nodes_to_list(cursor)
        for node in node_list:
            # 寻找每个课程的知识模块
            cypher = '''
                    MATCH (n)
                    WHERE id(n) = {} 
                    with n
                    OPTIONAL MATCH p = (m)-[r]->(k)
                    WHERE exists((m)-[:属于]->(n))
                    RETURN p, r
                      '''.format(node['id'])
            cursor = graph.run(cypher).data()
            path_list = paths_to_list(cursor)

        # 构建返回的数据字典
        response_data = {
            'nodes': json.dumps(node_list, ensure_ascii=False),
            'edges': json.dumps(path_list, ensure_ascii=False)
        }
        return render(request, 'info_query.html', {'search': response_data})
    return render(request, 'info_query.html')


def query_vague(request):
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        seg_list = jieba.cut(name)
        # 根据分词结果，寻找对应节点(课程，知识模块，知识要点)
        node_list = []
        for word in seg_list:
            cypher = '''MATCH (n)
                        WHERE n.name CONTAINS '{}'
                        RETURN n'''.format(word)
            cursor = graph.run(cypher).data()
            node_list.extend(nodes_to_list(cursor))
        path_list = []
        for node in node_list:
            cypher = '''
                     MATCH (n:)
                     WHERE id(n) = {}
                     WITH n
                     OPTIONAL MATCH p = (m)-[r]->[n]
                     RETURN p, r
                     '''.format(node['id'])
            cursor = graph.run(cypher).data()
            path_list.extend(paths_to_list(cursor))
        # 构建返回的数据字典
        response_data = {
            'nodes': json.dumps(node_list, ensure_ascii=False),
            'edges': json.dumps(path_list, ensure_ascii=False)
        }
        return render(request, 'info_query.html', {'search': response_data})
    return render(request, 'info_query.html')
