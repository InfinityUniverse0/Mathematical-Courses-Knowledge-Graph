from backend import *
graph = init_neo4j()

course_name = '泛函分析'
# 寻找课程节点，可以有多个
cypher = '''MATCH (n:课程) 
         WHERE n.name CONTAINS '{}'
         RETURN n'''.format(course_name)
cursor = graph.run(cypher).data()
node_dict = nodes_to_list(cursor)
nd = []
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
    path_dict, nodes = paths_to_list(cursor2)
    nd.extend(nodes)
    for path in path_dict:
        print(path)
    for n in nodes:
        print(n)

    # 寻找每个课程节点的先导节点
    # cypher3 = '''
            # MATCH (n)
            # WHERE id(n) = {}
            # with n
            # OPTIONAL MATCH p = (n)-[r:先导*]->(predecessork)
            # RETURN p, r
              # '''.format(node['id'])
    # cursor3 = graph.run(cypher3).data()
    # path_dict, n_dict = paths_to_list(cursor3)
    # for path in path_dict:
        # print(path)
    # for n in n_dict:
        # print(n)
