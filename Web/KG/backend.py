'''backend.py
    This file contains the backend code for the web application.
    复杂的后端处理函数代码
    被views.py调用
'''

# Begin Here
from py2neo import Graph
level_dict = {
    '课程模块': 0,
    '课程': 1,
    '知识模块': 2,
    '知识要点': 3
}


def init_neo4j():
    config = {
        'profile': 'bolt://localhost:7687',
        'auth': ('neo4j', '12345678')
    }
    return Graph(config['profile'], auth=config['auth'])


def nodes_to_list(cursor_node):
    '''将py2neo.Node对象转换为点集'''
    node_list = []
    cursor = cursor_node
    for node in cursor:
        node = node['n']
        node_dict = {
            'id': node.identity,
            'level': level_dict[list(node.labels)[0]]
        }
        for key in node.keys():
            node_dict[key] = node[key]
        node_list.append(node_dict)
    return node_list


def paths_to_list(cursor_path):
    '''将py2neo.Path对象转换为边集'''
    path_list = []
    cursor = cursor_path
    for p in cursor:
        path, relation = p['p'], p['r']
        rel = list(path.types())[0]
        path_dict = {
            'id': relation.identity,
            'source': path.start_node.identity,
            'target': path.end_node.identity,
            'relation': rel,
            'value': 1.618 if rel == '先导' else 1.0
        }
        path_list.append(path_dict)
    return path_list
