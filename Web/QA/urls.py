from django.urls import path
from . import views # 导入视图函数

urlpatterns = [
    path('QA1', views.QA_normal),
    path('QA2', views.QA_advanced),
]
