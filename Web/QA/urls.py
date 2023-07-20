from django.urls import path
from . import views # 导入视图函数

urlpatterns = [
    path('ques_ans', views.turn_ques_ans),
    path('ques_ans/chat', views.AIchat),
]
