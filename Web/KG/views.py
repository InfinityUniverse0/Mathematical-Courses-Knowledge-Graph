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
from .backend import *

Graph = CourseGraph()


# Create your views here.

def index(request):
    return render(request,'index.html')

# 为GET请求提供跳转接口
def jump_info_query(request):
    return render(request, 'info_query.html')

# 为GET请求提供跳转接口
def jump_study_route(request):
    return render(request, 'study_route.html')

# 为GET请求提供跳转接口
def jump_question_answer(request):
    return render(request, 'question_answer.html')

# 提供精确查询(子串查询)，用户输入一个课程名，查出该课程的所有知识模块，以及知识模块之间的关系
def query_course(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        try:
            data = json.loads(body)
            course_name = data['name']
            if course_name == '':
                return JsonResponse({'ERROR': 'Invalid JSON data.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'ERROR': 'Invalid JSON data.'}, status=400)
        # 寻找课程节点，可以有多个
        cypher = '''MATCH (n:课程) 
                 WHERE n.name CONTAINS '{}'
                 RETURN n'''.format(course_name)
        cursor = Graph.graph.run(cypher).data()
        node_list = nodes_to_list(cursor, table=True)
        node_other, path_list, path_other = [], [], []
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
            cursor = Graph.graph.run(cypher).data()
            paths, nodes = paths_to_list(cursor)
            node_other.extend(nodes)
            path_other.extend(paths)

        node_list.extend(node_other)
        path_list.extend(path_other)

        # 去重处理
        node_list = unique_nodes(node_list)
        path_list = unique_paths(path_list)

        # 构建返回的数据字典
        response_data = {
            'nodes': json.dumps(node_list, ensure_ascii=False),
            'links': json.dumps(path_list, ensure_ascii=False)
        }

        return JsonResponse({'search': response_data})
    return render(request, 'info_query.html')

# 提供模糊查询，用户输入一个字符串，查出所有包含该字符串的节点，以及周围节点
def query_vague(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        try:
            data = json.loads(body)
            name = data['name']
        except json.JSONDecodeError:
            return JsonResponse({'ERROR': 'Invalid JSON data.'}, status=400)
        seg_list = jieba.cut(name)
        # 根据分词结果，寻找对应节点(课程，知识模块，知识要点)
        node_list = []
        for word in seg_list:
            # 先找知识要点
            cypher = '''MATCH (n:知识要点)
                        WHERE n.name CONTAINS '{}'
                        RETURN n'''.format(word)
            cursor = Graph.graph.run(cypher).data()
            point_list = nodes_to_list(cursor)
            node_list.extend(point_list)
            for point in point_list:

                # 遍历每个知识要点，寻找对应的知识模块(唯一)
                cypher = '''
                        MATCH (m:知识要点)
                        WHERE id(m) = {}
                        with m
                        OPTIONAL MATCH p = (m)-[r:含于]->(n)
                        RETURN n'''.format(point['id'])
                cursor = Graph.graph.run(cypher).data()
                module = nodes_to_list(cursor)[0]
                node_list.append(module)

                # 根据该知识模块，寻找对应的课程(唯一)
                cypher = '''
                        MATCH (m:知识模块)
                        WHERE id(m) = {}
                        with m
                        OPTIONAL MATCH p = (m)-[r:属于]->(n)
                        RETURN n'''.format(module['id'])
                cursor = Graph.graph.run(cypher).data()
                course = nodes_to_list(cursor)[0]
                node_list.append(course)

        # 去重处理
        node_list = unique_nodes(node_list)

        response_data = {
            'course': [],
            'module': [],
            'point': []
        }

        for node in node_list:
            response_data[level_list[node['level']]].append(node['name'])

        return JsonResponse({'search': response_data})
    return render(request, 'info_query.html')


# 提供学习路径的查询，用户选择一个课程，查出所有的先导课程
def learn_path(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        try:
            data = json.loads(body)
            course_name = data['name']
        except json.JSONDecodeError:
            return JsonResponse({'ERROR': 'Invalid JSON data.'}, status=400)
        # 寻找课程节点，可以有多个
        cypher = '''MATCH (n:课程) 
                 WHERE n.name CONTAINS '{}'
                 RETURN n'''.format(course_name)
        
        cursor = Graph.graph.run(cypher).data()
        node_list = nodes_to_list(cursor)
        path_list, node_other = [], []
        for node in node_list:
            cypher = '''
                    MATCH (n)
                    WHERE id(n) = {}
                    with n
                    OPTIONAL MATCH p = (n)-[r:先导*]->(predecessork)
                    RETURN p, r
                      '''.format(node['id'])
            cursor = Graph.graph.run(cypher).data()
            paths, nodes = paths_to_list(cursor)

            node_other.extend(nodes)
            path_list.extend(paths)

        node_list.extend(node_other)

        # 去重处理
        node_list = unique_nodes(node_list)
        path_list = unique_paths(path_list)

        # 构建返回的数据字典
        response_data = {
            'nodes': json.dumps(node_list, ensure_ascii=False),
            'links': json.dumps(path_list, ensure_ascii=False)
        }
        return JsonResponse({'search': response_data})
    return render(request, 'study_route.html')

# 用于课程绘图
def query_course_one(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        try:
            data = json.loads(body)
            course_name = data['name']
            if course_name == '':
                return JsonResponse({'ERROR': 'Invalid JSON data.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'ERROR': 'Invalid JSON data.'}, status=400)
        # 寻找课程节点
        cypher = '''MATCH (n:课程) 
                    WHERE n.name = '{}'
                    RETURN n'''.format(course_name)
        cursor = Graph.graph.run(cypher).data()
        node_list = nodes_to_list(cursor, table=True)
        node_other, path_list, path_other = [], [], []
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
            cursor = Graph.graph.run(cypher).data()
            paths, nodes = paths_to_list(cursor)
            node_other.extend(nodes)
            path_other.extend(paths)

        node_list.extend(node_other)
        path_list.extend(path_other)

        # 去重处理
        node_list = unique_nodes(node_list)
        path_list = unique_paths(path_list)

        # 构建返回的数据字典
        response_data = {
            'nodes': json.dumps(node_list, ensure_ascii=False),
            'links': json.dumps(path_list, ensure_ascii=False)
        }

        return JsonResponse({'search': response_data})
    return render(request, 'info_query.html')


# 课程总览
def courses_overview(request):
    if request.method == 'GET':
        res_dict = {
            'nodes': [],
            'links': [],
            'courses': []
        }

        # 查询课程
        get_courses_cypher = '''
        Match (n: 课程)
        Return n
        '''
        courses = Graph.graph.run(get_courses_cypher).data()
        for course in courses:
            res_dict['courses'].append({
                'id': course['n'].identity,
                'level': level_dict[list(course['n'].labels)[0]],
                'name': course['n']['name']
            })
            res_dict['nodes'].append({
                'id': course['n'].identity,
                'level': level_dict[list(course['n'].labels)[0]],
                'name': course['n']['name']
            })
            # 查询课程的先导课程
            get_pre_courses_cypher = '''
            Match (n: 课程 {name: '%s'})-[r: 先导]->(m: 课程)
            Return r, m
            ''' % (course['n']['name'])
            pre_courses = Graph.graph.run(get_pre_courses_cypher).data()
            for pre_course in pre_courses:
                res_dict['links'].append({
                    'id': pre_course['r'].identity,
                    'source': course['n'].identity,
                    'target': pre_course['m'].identity,
                    'relation': str(list(pre_course['r'].types())[0]),
                    'value': 1.618
                })
                res_dict['nodes'].append({
                    'id': pre_course['m'].identity,
                    'level': level_dict[list(pre_course['m'].labels)[0]],
                    'name': pre_course['m']['name']
                })

        # 查询课程模块
        get_course_modules_cypher = '''
        Match path = (: 课程)-[r: 类别]->(: 课程模块)
        Return path, r
        '''
        course_modules = Graph.graph.run(get_course_modules_cypher).data()
        for course_module in course_modules:
            res_dict['links'].append({
                'id': course_module['r'].identity,
                'source': course_module['path'].start_node.identity,
                'target': course_module['path'].end_node.identity,
                'relation': str(list(course_module['path'].types())[0]),
                'value': 1.0
            })
            res_dict['nodes'].append({
                'id': course_module['path'].end_node.identity,
                'level': level_dict[list(course_module['path'].end_node.labels)[0]],
                'name': course_module['path'].end_node['name']
            })

        # 去重 + 转换为json
        res_dict = {
            'nodes': json.dumps(unique_nodes(res_dict['nodes']), ensure_ascii=False),
            'links': json.dumps(unique_paths(res_dict['links']), ensure_ascii=False),
            'courses': json.dumps(res_dict['courses'], ensure_ascii=False)
        }
        return render(request, 'courses_overview.html', {'overview': res_dict})
    return render(request, 'courses_overview.html')

# 课程总览中的课程详情
def get_course_knowledge(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        try:
            data = json.loads(body)
            course_name = data['name']
        except json.JSONDecodeError:
            return JsonResponse({'ERROR': 'Invalid JSON data.'}, status=400)
        # course_name = request.POST.get('updateInput')
        res_dict = {
            'nodes': [],
            'links': []
        }
        # 查询课程及其知识模块
        get_knowledge_modules_cypher = '''
        Match (n: 知识模块)-[r: 属于]->(m: 课程 {name: '%s'})
        Return n, r, m
        ''' % (course_name)
        knowledge_modules = Graph.graph.run(get_knowledge_modules_cypher).data()
        for idx, knowledege_module in enumerate(knowledge_modules):
            if idx == 0:
                res_dict['nodes'].append({
                    'id': knowledege_module['m'].identity,
                    'level': level_dict[list(knowledege_module['m'].labels)[0]],
                    'name': knowledege_module['m']['name']
                })
            res_dict['nodes'].append({
                'id': knowledege_module['n'].identity,
                'level': level_dict[list(knowledege_module['n'].labels)[0]],
                'name': knowledege_module['n']['name']
            })
            res_dict['links'].append({
                'id': knowledege_module['r'].identity,
                'source': knowledege_module['n'].identity,
                'target': knowledege_module['m'].identity,
                'relation': str(list(knowledege_module['r'].types())[0]),
                'value': 1.0
            })
        # 查询知识模块及其关系
        get_knowledge_modules_cypher = '''
        Match (n: 知识模块)-[r: 下一模块]->(m: 知识模块)
        Where Exists ((n)-[:属于]->(: 课程 {name: '%s'}))
        Return r,n,m
        ''' % (course_name)
        knowledge_modules = Graph.graph.run(get_knowledge_modules_cypher).data()
        for knowledge_module in knowledge_modules:
            res_dict['links'].append({
                'id': knowledge_module['r'].identity,
                'source': knowledge_module['n'].identity,
                'target': knowledge_module['m'].identity,
                'relation': str(list(knowledge_module['r'].types())[0]),
                'value': 1.0
            })
        # 查询知识要点及其所属知识模块
        get_knowledge_points_cypher = '''
        Match (n: 知识要点)-[r: 含于]->(m: 知识模块)-[: 属于]->(: 课程 {name: '%s'})
        Return n, r, m
        ''' % (course_name)
        knowledge_points = Graph.graph.run(get_knowledge_points_cypher).data()
        for knowledge_point in knowledge_points:
            res_dict['nodes'].append({
                'id': knowledge_point['n'].identity,
                'level': level_dict[list(knowledge_point['n'].labels)[0]],
                'name': knowledge_point['n']['name']
            })
            res_dict['links'].append({
                'id': knowledge_point['r'].identity,
                'source': knowledge_point['n'].identity,
                'target': knowledge_point['m'].identity,
                'relation': str(list(knowledge_point['r'].types())[0]),
                'value': 1.0
            })
        # (无重复) 转换为json
        res_dict = {
            'nodes': json.dumps(res_dict['nodes'], ensure_ascii=False),
            'links': json.dumps(res_dict['links'], ensure_ascii=False)
        }
        return JsonResponse({'search': res_dict})
        # return render(request, 'courses_overview.html', {'details': res_dict})
    return render(request, 'courses_overview.html')
