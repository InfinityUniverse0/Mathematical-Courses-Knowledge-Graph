
import openai
openai.api_key = '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'

from backend import *

graph = init_neo4j()

question = '我想学习更多解方程组的方法，我应该如何进行学习？'

prompt = [
    '''
    分词是指把一个长句子进行拆分，并且不保留"我","是","一名"类似的无意义词汇,
    我接下来将给你一个长句子，请你进行分词，并向我提供Python列表格式的分词结果,
    注意，请你不要保留无意义词汇，删去重复的词汇，并着重保留重要词汇，另外完整的词汇不要拆分，
    如"数学分析"不需要拆分为"数学"和"分析", 依此类推。
    必须以Python列表形式返回，列表内元素为字符串，直接给出列表即可
    句子:{}
    '''.format(question)
]

answer = chat(prompt)
print("GPT分词结果: ", answer)

seg_list = eval(answer)

node_list, path_list = [], []
for word in seg_list:
    print('当前词: ', word)
    # 对每个词，寻找相关的课程和知识模块和知识要点
    cypher = '''MATCH (n:课程|知识模块|知识要点)
                where n.name contains '{}'
                optional match p = (n)-[r:先导|含于|属于]->()
                return p, r'''.format(word)
    cursor = graph.run(cypher).data()
    paths, nodes = paths_to_list(cursor)
    node_list.extend(nodes)
    path_list.extend(paths)

    cypher = '''MATCH (n:课程|知识模块|知识要点)
                        where n.name contains '{}'
                        optional match p = ()-[r:先导|含于|属于]->(n)
                        return p, r'''.format(word)
    cursor = graph.run(cypher).data()
    paths, nodes = paths_to_list(cursor)
    node_list.extend(nodes)
    path_list.extend(paths)



# 去重
node_list = unique_nodes(node_list)
path_list = unique_paths(path_list)

print('查询到的节点: ', node_list)
print('查询到的路径: ', path_list)

# 根据查询结果生成字符串数据发送给AI交互
data_node = ','.join(str(node) for node in node_list)
data_path = ','.join(str(path) for path in path_list)
data = data_node + data_path
print('查询到的数据: ', data)
# 问答框架
prompt = [
    '你现在是一个学习问答助手，我将给你提供一些从neo4j查询得到的节点和边数据，请你据此回答我的问题',
    '数据如下:' + data,
    '注意，请你回答的问题要和我提供的数据相关，并且回答要规范严谨',
    f'问题: {question}'
]

print("问答 PROMPT: ")
for p in prompt:
    print(p)

# 调用AI交互
answer = chat(prompt)

print("回答: \n", answer)
