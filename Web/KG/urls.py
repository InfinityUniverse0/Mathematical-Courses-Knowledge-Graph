from django.urls import path
from . import views # 导入视图函数

urlpatterns = [
    path('info_query/', views.turn_info_query),
    path('study_route/', views.turn_study_route),
    path('info_query/post1', views.query_course),
    path('info_query/post2', views.query_vague),
    path('study_route/post1', views.learn_path),
]

