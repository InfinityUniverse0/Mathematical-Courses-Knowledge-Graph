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
# 提供精确查询，用户输入一个课程名，查出该课程的所有知识模块，以及知识模块之间的关系
def query_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name').strip()
        # 寻找课程节点，可以有多个
        cypher = '''MATCH (n:课程) 
                 WHERE n.name CONTAINS '{}'
                 RETURN n'''.format(course_name)
        cursor = graph.run(cypher).data()
        node_list = nodes_to_list(cursor)
        node_other = []
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
            path_list, nodes = paths_to_list(cursor)
            node_other.extend(nodes)
        node_list.extend(node_other)

        # 构建返回的数据字典
        response_data = {
            'nodes': json.dumps(node_list, ensure_ascii=False),
            'edges': json.dumps(path_list, ensure_ascii=False)
        }
        return render(request, 'info_query.html', {'search': response_data})
    return render(request, 'info_query.html')

# 提供模糊查询，用户输入一个字符串，查出所有包含该字符串的节点，已经周围节点
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
        response_data = {
            'course': [],
            'module': [],
            'point': []
        }
        for node in node_list:
            response_data[level_list[node['level']]].append(node['name'])

        return render(request, 'info_query.html', response_data)
    return render(request, 'info_query.html')


# 提供学习路径的查询，用户选择一个课程，查出所有的先导课程
def learn_path(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name').strip()
        # 寻找课程节点，可以有多个
        cypher = '''MATCH (n:课程) 
                 WHERE n.name CONTAINS '{}'
                 RETURN n'''.format(course_name)
        cursor = graph.run(cypher).data()
        node_list = nodes_to_list(cursor)
        node_other = []
        for node in node_list:
            # 寻找每个课程的知识模块
            cypher = '''
                    MATCH (n)
                    WHERE id(n) = {}
                    with n
                    OPTIONAL MATCH p = (n)-[r:先导*]->(predecessork)
                    RETURN p, r
                      '''.format(node['id'])
            cursor = graph.run(cypher).data()
            path_list, nodes = paths_to_list(cursor)
            node_other.extend(nodes)
        node_list.extend(node_other)

        # 构建返回的数据字典
        response_data = {
            'nodes': json.dumps(node_list, ensure_ascii=False),
            'edges': json.dumps(path_list, ensure_ascii=False)
        }
        return render(request, 'query_path.html', {'search': response_data})
    return render(request, 'query_path.html')
