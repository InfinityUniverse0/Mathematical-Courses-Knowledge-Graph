'''backend.py
    This file contains the backend code for the web application.
    复杂的后端处理函数代码
    被views.py调用
'''

import openai
# from django.conf import settings
from py2neo import Graph

# openai.api_key = settings.OPENAI_API_KEY

# 初始化neo4j数据库
def init_neo4j():
    config = {
        'profile': 'bolt://localhost:7687',
        'auth': ('neo4j', '12345678')
    }
    return Graph(config['profile'], auth=config['auth'])


# 和AI交互的接口，输入格式：[message1, message2, ...]
def chat(message_list: list):
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        for msg in message_list:
            messages.append({"role": "user", "content": msg})
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
        )
        completion = response['choices'][0]['message']['content']
    except Exception as e:
        completion = 'ERROR: ' + str(e)
    return completion


# Node查询的cursor转化为list节点集
def nodes_to_list(cursor_node):
    '''将py2neo.Node对象转换为点集'''
    node_list = []
    cursor = cursor_node
    for node in cursor:
        node = node['n']
        node_dict = {
            'name': node['name'],
            'label': list(node.labels)[0]
        }
        for key in node.keys():
            node_dict[key] = node[key]
        node_list.append(node_dict)
    return node_list

# 节点集去重
def unique_nodes(node_list):
    unique_list = []
    for node in node_list:
        if node not in unique_list:
            unique_list.append(node)
    return unique_list


