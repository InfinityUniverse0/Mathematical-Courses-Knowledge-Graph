from backend import *
from py2neo import Graph
from django.conf import settings

graph = init_neo4j()

word = '分析'

cypher = '''MATCH (n:课程|知识模块|知识要点)
            WHERE n.name CONTAINS '{}'
            RETURN n'''.format(word)
cursor = graph.run(cypher).data()
node_list = nodes_to_list(cursor)
for node in node_list:
    print(node)