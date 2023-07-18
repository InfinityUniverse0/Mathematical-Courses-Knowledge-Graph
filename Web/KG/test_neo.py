from backend import *
graph = init_neo4j()

course_name = '数学分析'
# 寻找课程节点，可以有多个
cypher = "MATCH (n:课程) " \
         "WHERE n.name CONTAINS '{}' " \
         "RETURN n".format(course_name)
cursor = graph.run(cypher).data()
node_dict = nodes_to_list(cursor)
pnt = 1
for node in node_dict:
    print(node)
    # 寻找每个课程节点的关联节点
    cypher2 = '''
            MATCH (n:课程)
            WHERE n.name = '{}' 
            with n
            OPTIONAL MATCH p = (m)-[r]->(k)
            WHERE exists((m)-[:属于]->(n))
            RETURN p
              '''.format(node['name'])
    cursor2 = graph.run(cypher2).data()
    path_dict, pnt = paths_to_list(cursor2, pnt)
    for path in path_dict:
        print(path)
