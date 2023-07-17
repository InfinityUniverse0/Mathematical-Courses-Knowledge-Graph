# Mathematical-Courses-Knowledge-Graph

高等教育数学课程体系知识图谱

**特别注意**：

## 项目介绍

## 项目结构

```shell
.
├── README.md
├── neo4j // neo4j图数据库
│   ├── data // 数据文件
│   │   ├── 课程模块.csv
│   │   ├── 课程.csv
│   │   ├── 知识模块.csv
│   │   ├── 知识要点.csv
│   │   └── 数学人物.csv
│   └── course_graph.py // 生成并初始化图数据库
└── Web // Django Web项目
    ├── manage.py
    ├── Web // Django项目
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── static // 静态文件
    │   ├── css
    │   ├── fonts
    │   ├── img
    │   └── js
    ├── templates // 模板文件
    │   └── index.html
    └── webapp // Django应用：根据实际需要自行创建对应app应用文件，使用`python manage.py startapp webapp`命令创建(尚未创建，仅作示例)
        ├── __init__.py
        ├── __pycache__
        ├── admin.py
        ├── apps.py
        ├── migrations
        ├── models.py
        ├── tests.py
        ├── urls.py
        └── views.py
```
