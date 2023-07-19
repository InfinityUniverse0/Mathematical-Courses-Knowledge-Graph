from backend import *
graph = init_neo4j()

course_name = '拓扑学'
# 寻找课程节点，可以有多个
cypher = '''MATCH (n:课程) 
         WHERE n.name CONTAINS '{}'
         RETURN n'''.format(course_name)
cursor = graph.run(cypher).data()
node_dict = nodes_to_list(cursor)
for node in node_dict:
    print(node)
    # 寻找每个课程节点的关联节点
    cypher2 = '''
            MATCH (n)
            WHERE id(n) = {}
            with n
            OPTIONAL MATCH p = (m)-[r]->(k)
            WHERE exists((m)-[:属于]->(n))
            RETURN p, r
              '''.format(node['id'])
    cursor2 = graph.run(cypher2).data()
    path_dict = paths_to_list(cursor2)
    for path in path_dict:
        print(path)
