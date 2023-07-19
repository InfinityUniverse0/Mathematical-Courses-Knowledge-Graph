'''views.py
    视图函数
    若视图函数的处理逻辑太过复杂,可以先在 `backend.py` 中定义相关的后端处理函数,再在此处调用
    调用Neo4j数据库时, 导入 neo4j_db/course_graph.py 中的 CourseGraph类
'''

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings

# 导入backend.py中的所有函数
from .backend import *
import jieba
import json

graph = init_neo4j()


# Create your views here.
def QA_normal(request):
    if request.method == 'POST':
        question = request.POST.get('question').strip()
        seg_list = jieba.cut(question)
    return render(request, 'QA.html')


def QA_advanced(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        try:
            data = json.loads(body)
            question = data['name']
        except json.JSONDecodeError:
            return JsonResponse({'ERROR': 'Invalid JSON data.'}, status=400)
        # 分词处理
        seg_list = jieba.cut(question)
        node_list = []
        for word in seg_list:
            # 对每个词，寻找相关的课程和知识模块和知识要点，以及附近的关系(不包括下一模块)
            cypher = '''MATCH (n:课程|知识模块|知识要点)
                        where n.name contains '{}'
                        optional match p = (n)-[r1]->()
                        where not '下一模块' in r1.LABELS
                        optional match q = ()-[r2]->(n)
                        where not '下一模块' in r2.LABELS
                        return n, p, q'''.format(word)
            cursor = graph.run(cypher).data()
            node_list.extend(nodes_to_list(cursor))
        # 节点去重
        node_list = unique_nodes(node_list)
        # 根据查询结果生成字符串数据发送给AI交互
        data = ''.join(str(node) for node in node_list)
        # 问答框架
        prompt = [
            '你现在是一个问答助手，我将给你提供一些从neo4j查询得到的节点数据，请你据此回答我的问题。',
            data,
            f'问题: {question}'
        ]
        # 调用AI交互
        answer = chat(prompt)
        return JsonResponse({'answer': answer}, status=200)

    return render(request, 'QA.html')
