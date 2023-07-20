'''backend.py
    This file contains the backend code for the web application.
    复杂的后端处理函数代码
    被views.py调用
'''

# Begin Here
# 导入neo4j_db/course_graph.py 中的 CourseGraph类
import sys
sys.path.append("..")
from neo4j_db.course_graph import CourseGraph

# Config
level_dict = {
    '课程模块': 0,
    '课程': 1,
    '知识模块': 2,
    '知识要点': 3
}

level_list = ['course_module', 'course', 'module', 'point']

name_map = {
    '课程模块': 'course_module',
    '课程': 'course',
    '知识模块': 'module',
    '知识要点': 'point'
}

# Functions
def nodes_to_list(cursor_node, table=False):
    '''将py2neo.Node对象转换为点集'''
    node_list = []
    cursor = cursor_node
    for node in cursor:
        node = node['n']
        node_dict = {
            'id': node.identity,
            'level': level_dict[list(node.labels)[0]],
            'name': node['name']
        }
        if table:
            node_dict.update({
                'refer': node['references'],
                'intro': node['intro']
            })
        node_list.append(node_dict)
    return node_list

# 节点集去重
def unique_nodes(node_list):
    unique_list = []
    for node in node_list:
        if node not in unique_list:
            unique_list.append(node)
    return unique_list


def paths_to_list(cursor_path):
    '''将py2neo.Path对象转换为边集'''
    path_list, node_list = [], []
    cursor = cursor_path
    for p in cursor:
        if p['p'] is None:
            continue
        path, relation = p['p'], p['r']
        start_node, end_node = path.start_node, path.end_node
        node_list.append({'n': start_node})
        node_list.append({'n': end_node})
        rel = list(path.types())[0]
        if isinstance(relation, list):
            relation = relation[0]
        path_dict = {
            'id': relation.identity,
            'source': start_node.identity,
            'target': end_node.identity,
            'relation': rel,
            'value': 1.618 if rel == '先导' else 1.0
        }
        path_list.append(path_dict)
    return path_list, nodes_to_list(node_list)


# 边集去重
def unique_paths(path_list):
    unique_list = []
    edges = []
    for path in path_list:
        edge = (path['source'], path['target'], path['relation'])
        if edge not in edges:
            unique_list.append(path)
            edges.append(edge)
    return unique_list
