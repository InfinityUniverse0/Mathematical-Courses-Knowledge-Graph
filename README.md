# Mathematical-Courses-Knowledge-Graph

## 项目名称

高等教育数学课程体系知识图谱

<!-- 
**特别注意**(务必阅读此部分！！！)：

- 本仓库主要有两条branch：`main`和`dev`

- `main`主要用来提交一些比较有里程碑意义的代码

- `dev`主要用于日常的开发(develop)提交，每个人在开发时，都应该在`dev`分支上进行，开发完成后，再合并到`main`分支上。

- 省流：也就是说平时就在`dev`分支开发，觉得开发的差不多了，没有什么大的Bug了，算是一个比较有里程碑意义的阶段性成果就可以合并到`main`分支上了。

- 具体操作示例如下：

   1. 首先切换到`dev`分支上：

        ```git
        git checkout dev
        ```

   2. 然后在`dev`分支上进行开发，开发完成后，提交到`dev`分支上：

        ```git
        git add . // 将所有修改的文件添加到暂存区
        git commit -m "这里填写提交信息" // 将暂存区的文件提交到本地仓库
        git push origin dev // 将本地仓库的文件推送到远程仓库的dev分支上
        ```

   3. 感觉没啥Bug，差不多算是个里程碑之后，就可以合并到`main`分支上了：

        ```git
        git checkout main // 切换到main分支上
        git merge --no-ff dev // 将dev分支上的内容合并到main分支上，同时采取 no fast-forward 形式进行merge操作
        git push origin main // 将本地仓库的文件推送到远程仓库的main分支上
        ```

   4. 注意：

      - 由于仓库设置了对`main`分支的保护，因此在合并`dev`分支到`main`分支时，可能需要进行pull request操作。

      - 有可能会进入一个类似于`vim`之类的界面，操作如下：
        - 按下`i`键或`Insert`键，进入编辑模式
        - 编辑完成后，按下`Esc`键，退出编辑模式
        - 然后输入`:wq`，保存并退出即可

      - 如下图所示：
        ![pull request](https://pic.imgdb.cn/item/64b547b51ddac507cc83193e.jpg)

      - 有可能需要审核，所以可能GitHub不会立即更新

- **请务必时刻注意自己当前所在分支，避免产生不恰当的提交**

  - 一般会在自己的Git中有明确显示当前所在分支，如下图所示：
  ![分支查看示例](https://pic.imgdb.cn/item/64b543981ddac507cc71aea0.jpg)

  - 可以使用`git branch`命令查看当前所在分支

  - 也可以使用`git status`查看当前所在分支
-->

## 项目介绍

本项目构建了一个高等教育数学课程体系知识图谱的Web系统（Demo版），以方便学生、教师、研究人员等人群对高等教育数学课程体系有一个更加直观的认识。

## 项目结构

```
.
├── README.md
├── neo4j_db // neo4j图数据库
│   ├── data // 数据文件
│   │   ├── 课程模块.csv
│   │   ├── 课程.csv
│   │   ├── 知识模块.csv
│   │   ├── 知识要点.csv
│   ├── __init__.py
│   └── course_graph.py // 生成并初始化图数据库, 并用于后续操作数据库
└── Web // Django Web项目
    ├── manage.py
    ├── Web // Django项目
    │   ├── __init__.py
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
    │   ├── welcome.html
    │   ├── index.html
    │   ├── info_query.html
    │   ├── study_route.html
    │   ├── question_answer.html
    │   ├── courses_overview.html
    │   ├── 404.html
    │   └── 500.html
    ├── Base // Django应用: 基础应用，用于处理一些基础的请求，包括欢迎页面、404、500等
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py
    │   ├── tests.py
    │   ├── urls.py // 路由
    │   ├── backend.py // 复杂的后端处理函数
    │   └── views.py // 视图函数
    ├── KG // Django应用: KnowledgeGraph，用于处理知识图谱相关的基本请求，包括基于知识图谱的实体查询、关系查询等
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py
    │   ├── tests.py
    │   ├── urls.py // 路由
    │   ├── backend.py // 复杂的后端处理函数
    │   └── views.py // 视图函数
    └── QA // Django应用: Question Answering System，用于处理问答系统相关的基本请求
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── migrations
        ├── models.py
        ├── tests.py
        ├── urls.py // 路由
        ├── backend.py // 复杂的后端处理函数
        └── views.py // 视图函数
```

<!-- 
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
-->

## 项目依赖项

> - Django 4.2.3
> - pandas 2.0.3
> - py2neo 2021.2.3
> - mysqlclient 2.2.0
> - D3.js v5
> - jieba 0.42.1
> - openai 0.27.8
> - urllib3 1.26.16
