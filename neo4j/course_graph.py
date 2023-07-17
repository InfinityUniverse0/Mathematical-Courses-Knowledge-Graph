'''course_graph.py
高等教育数学课程图谱类
'''

# 导入所需的模块
from py2neo import Graph
from py2neo import Node, Relationship
from py2neo import NodeMatcher, RelationshipMatcher
from os.path import join
import pandas as pd
from copy import deepcopy

class CourseGraph:
    '''
    高等教育数学课程图谱
    '''

    # 相关配置(默认)
    config = {
        'profile': 'bolt://localhost:7687',
        'auth': ('neo4j', '12345678')
    }

    def __init__(self, profile = config['profile'], auth = config['auth']):
        '''
        初始化
        '''

        # 重新设置配置信息
        self.config['profile'] = profile
        self.config['auth'] = auth

        # 图数据库
        self.graph = Graph(profile, auth = auth)
    
    def initial(self):
        '''
        初始化图数据库中的 架构(节点 & 关系) 和 数据

        数据文件保存在./data目录下
        包括：
        - 课程模块.csv
        - 课程.csv
        - 知识模块.csv
        - 知识要点.csv
        - 数学人物.csv
        '''

        # 首先，清空数据库
        clear = '''
        Match (n)
        Optional Match (n)-[r]-()
        Delete n, r
        '''
        self.graph.run(clear)

        # 执行初始化操作
        path = './data'

        # 1. 初始化`课程模块`节点
        course_module = pd.read_csv(join(path, '课程模块.csv'))
        for _, row in course_module.iterrows():
            node = Node('课程模块', **row)
            self.graph.create(node)
        
        # 2. 初始化`课程`节点
        course = pd.read_csv(join(path, '课程.csv'))
        for _, row in course.iterrows():
            # `tags`列作为`课程`节点与`课程模块`节点的关系，不需要作为`课程`节点的属性
            attrs = deepcopy(row)
            # 删除`pre_courses`列
            del attrs['pre_courses']
            # 删除`tags`列
            del attrs['tags']
            # 将`references`列的数据格式转换为列表
            try:
                attrs['references'] = attrs['references'].split('|')
            except:
                attrs['references'] = []
            node = Node('课程', **attrs)
            self.graph.create(node)
            # 增加`课程`节点与`课程模块`节点的关系
            tags = row['tags'].split('|')
            for tag in tags:
                course_module = NodeMatcher(self.graph).match('课程模块', name = tag).first()
                rel = Relationship(node, '类别', course_module)
                self.graph.create(rel)
        
        # 3. 初始化课程之间的先导关系
        pre_courses_relationship = pd.read_csv(join(path, '课程.csv'))[['name', 'pre_courses']]
        for _, row in pre_courses_relationship.iterrows():
            course = NodeMatcher(self.graph).match('课程', name = row['name']).first()
            # `pre_courses`列可能为空
            if not pd.isna(row['pre_courses']):
                # `pre_courses`列的数据格式为字符串，每门课程以`|`分割
                pre_courses = row['pre_courses'].split('|')
                for pre_course in pre_courses:
                    pre_course = NodeMatcher(self.graph).match('课程', name = pre_course).first()
                    rel = Relationship(course, '先导', pre_course)
                    self.graph.create(rel)
        
        # 4. 初始化`知识模块`节点
        knowledge_module = pd.read_csv(join(path, '知识模块.csv'))
        for _, row in knowledge_module.iterrows():
            # `course`列作为`知识模块`节点与`课程`节点的关系，不需要作为`知识模块`节点的属性
            attrs = deepcopy(row)
            # 删除`course`列
            del attrs['course']
            node = Node('知识模块', **attrs)
            self.graph.create(node)
            # 增加`知识模块`节点与`课程`节点的关系
            course = NodeMatcher(self.graph).match('课程', name = row['course']).first()
            rel = Relationship(node, '属于', course)
            self.graph.create(rel)
        
        # 5. 将同一`课程`的`知识模块`按照`no`列从小到大的顺序连接起来
        course = pd.read_csv(join(path, '课程.csv'))
        for _, row in course.iterrows():
            course_name = row['name']
            match = '''
            Match (n:知识模块)-[r:属于]->(c:课程)
            Where c.name = '{}'
            With n, c
            Match (m:知识模块)-[r:属于]->(c)
            Where m.no = n.no + 1
            with n, m
            Create p = (n)-[:`下一模块`]->(m)
            '''.format(course_name)
            self.graph.run(match)
        
        # 6. 初始化`知识要点`节点
        knowledge_point = pd.read_csv(join(path, '知识要点.csv'))
        for _, row in knowledge_point.iterrows():
            # `module`列作为`知识要点`节点与`知识模块`节点的关系，不需要作为`知识要点`节点的属性
            attrs = deepcopy(row)
            # 删除`module`列和`course`列
            del attrs['module']
            del attrs['course']
            node = Node('知识要点', **attrs)
            self.graph.create(node)
            # 增加`知识要点`节点与`知识模块`节点的关系
            cypher = '''
            Match (n:知识模块)-[:属于]->(m:课程)
            Where n.name = $module and m.name = $course
            Return n
            '''
            knowledge_module = self.graph.run(cypher, module = row['module'], course = row['course']).data()[0]['n']
            rel = Relationship(node, '含于', knowledge_module)
            self.graph.create(rel)
            
        # 7. 初始化`数学人物`节点
        # math_person = pd.read_csv(join(path, '数学人物.csv'))
        # for _, row in math_person.iterrows():
        #     node = Node('数学人物', **row)
        #     self.graph.create(node)
        
        # 8. 待定：数学人物与知识要点的关系
        pass

    def create_node(self, tag, attrs = {}):
        '''
        增加节点操作：向图数据库中增加一个节点
        - 若标签`tag`不满足要求，抛出`ValueError`异常

        :params `tag` 增加的节点的标签，须是 `['课程模块', '课程', '知识模块', '知识要点', '数学人物']` 其中之一
        :params `attrs` 增加的节点的属性，`dict`类型，默认为空字典

        :return `py2neo.data.Node`
        '''
        
        if tag in ['课程模块', '课程', '知识模块', '知识要点', '数学人物']:
            # 设置标签及属性
            node = Node(tag, **attrs)
            # 保存到图数据库
            self.graph.create(node)
            # 返回Node
            return node
        raise ValueError("节点的标签必须是 `['课程模块', '课程', '知识模块', '知识要点', '数学人物']` 其中之一")
    
    def create_relationship(self, node_start, node_end, tag, attrs = {}):
        '''
        增加关系操作：向图数据库中增加一条关系边(有向边)
        - tips: 使用前，可以先自行创建`py2neo.data.Node`作为节点参数传入
        - 若节点不满足要求，抛出`ValueError`异常
        
        :params `node_start` 关系边的起点，`py2neo.data.Node`类型
        :params `node_end` 关系边的终点，`py2neo.data.Node`类型
        :params `tag` 增加的关系的标签
        :params `attrs` 增加的关系的属性，`dict`类型，默认为空字典

        :return `py2neo.data.关系标签`
        '''

        # 匹配首尾节点
        matcher = NodeMatcher(self.graph)
        node_s = matcher.match(str(node_start.labels).split(':')[1], **dict(node_start.items())).first()
        node_t = matcher.match(str(node_end.labels).split(':')[1], **dict(node_end.items())).first()

        if node_s and node_t:
            # 设置关系的标签及属性
            relationship = Relationship(node_s, tag, node_t, **attrs)
            # 保存到图数据库
            self.graph.create(relationship)
            # 返回
            return relationship
        raise ValueError("无效的节点！")
    
    def exec_cypher(self, cypher):
        '''
        执行Cypher语句

        :params `cypher` 待执行的Cypher语句
        
        :return `py2neo.cypher.Cursor`
        '''

        return self.graph.run(cypher)
    

# 用于测试：
if __name__ == '__main__':
    mygraph = CourseGraph()
    mygraph.initial()
    print('Init Done!')
    # cypher = "Match p = ()-[]-() Return p"
    # cur = mygraph.exec_cypher(cypher)
    # for iten in cur:
    #     print(cur)
    pass
