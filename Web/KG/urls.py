from django.urls import path
from . import views # 导入视图函数

urlpatterns = [
    path('query_course', views.query_course),
    path('query_all', views.query_all),
]
