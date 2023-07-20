from django.urls import path
from . import views  # 导入视图函数

urlpatterns = [
    path('', views.index),
    path('index/',views.index),
    path('info_query/',views.jump_info_query),
    path('info_query/post1', views.query_course),
    path('info_query/post2', views.query_vague),
    path('info_query/post3',views.query_course_one),
    path('study_route/',views.jump_study_route),
    path('study_route/post1',views.learn_path),
    path('courses_overview/',views.courses_overview),
    path('courses_overview/details',views.get_course_knowledge),
    path('question_answer/',views.jump_question_answer),
]
