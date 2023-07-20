from django.urls import path
from . import views # 导入视图函数

urlpatterns = [
    path('info_query/', views.turn_info_query),
    path('study_route/', views.turn_study_route),
    path('study_route/post1', views.learn_path),
    path('info_query/post1', views.query_course),
    path('info_query/post2', views.query_vague),
    path('info_query/post3', views.query_course_one),
    path('courses_overview/', views.courses_overview),
    path('courses_overview/details', views.get_course_knowledge),
]

