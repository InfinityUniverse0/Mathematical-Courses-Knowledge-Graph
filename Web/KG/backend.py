'''backend.py
    This file contains the backend code for the web application.
    复杂的后端处理函数代码
    被views.py调用
'''

# Begin Here
from py2neo import Graph


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
        node_dict = {'id': node.identity}
        for key in node.keys():
            node_dict[key] = node[key]
        node_list.append(node_dict)
    return node_list


def paths_to_list(cursor_path, begin_id):
    '''将py2neo.Path对象转换为边集'''
    path_list = []
    cursor = cursor_path
    for path in cursor:
        path = path['p']
        path_dict = {
            'id': begin_id,
            'source': path.start_node.identity,
            'target': path.end_node.identity,
            'relation': list(path.types())[0],
            'value': 1
        }
        begin_id += 1
        path_list.append(path_dict)
    return path_list, begin_id
