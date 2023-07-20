'''views.py
    视图函数
    若视图函数的处理逻辑太过复杂,可以先在 `backend.py` 中定义相关的后端处理函数,再在此处调用
    调用Neo4j数据库时, 导入 neo4j_db/course_graph.py 中的 CourseGraph类
'''

from django.shortcuts import render
from django.http import JsonResponse

# 导入backend.py中的所有函数
from .backend import *
import jieba
import json

# 初始化neo4j数据库
Graph = CourseGraph()

# Create your views here.

# 跳转到QA系统
def jump_ques_ans(request):
    return render(request, 'question_answer.html')

# 智能问答系统
def AIchat(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        try:
            data = json.loads(body)
            question = data['message']
        except json.JSONDecodeError:
            return JsonResponse({'ERROR': 'Invalid JSON data.'}, status=400)
        # 分词处理
        prompt = [
            '''
            分词是指把一个长句子进行拆分，并且不保留"我","是","一名"等无意义词汇,
            我接下来将给你一个长句子，请你进行分词，并向我提供Python列表格式的分词结果,
            注意，请你不要保留无意义词汇，删去重复的词汇，并着重保留重要词汇，另外完整的词汇不要拆分，
            如"数学分析"不需要拆分为"数学"和"分析", 依此类推。
            必须以Python列表形式返回，列表内元素为字符串，直接给出列表即可
            句子:{}
            '''.format(question)
        ]

        # 调用AI获取分词结果
        answer = chat(prompt, '帮助完成句子分词的助手')

        try:
            # 尝试使用AI生成的分词结果
            seg_list = eval(answer)
        except SyntaxError:
            # 若AI生成的分词结果无效，则使用jieba分词
            seg_list = jieba.cut(question)

        node_list, path_list = [], []
        for word in seg_list:
            # 对每个词，寻找相关的课程和知识模块和知识要点
            cypher = '''MATCH (n:课程|知识模块|知识要点)
                            where n.name contains '{}'
                            optional match p = (n)-[r:先导|含于|属于]->()
                            return p, r'''.format(word)
            cursor = graph.run(cypher).data()
            paths, nodes = paths_to_list(cursor)
            node_list.extend(nodes)
            path_list.extend(paths)

            # 反向查询
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


        # 根据查询结果生成字符串数据发送给AI交互
        data_node = ','.join(str(node) for node in node_list) or '无'
        data_path = ','.join(str(path) for path in path_list) or '无'
        data = '节点数据:' + data_node + '\n边数据:' + data_path

        # 问答框架
        prompt = [
            '我将给你提供一些从neo4j查询得到的节点和边数据，请你据此回答我的问题',
            '数据如下:' + data,
            '注意，请你回答的问题要和我提供的数据相关，并且回答要规范严谨，如果数据不足以支撑你完成回答，'
            '请你根据尝试给出相对可信的回答',
            '直接进行回答即可，不需要写"回答:", "答案:"类似的开头'
            f'问题: {question}'
        ]

        # 调用AI交互，获得回答
        answer = chat(prompt, '高等数学教育智能问答系统')

        return JsonResponse({'completion': answer}, status=200)
    return render(request, 'question_answer.html')
