from django.urls import path
from . import views # 导入视图函数

urlpatterns = [
    path('question_answer', views.turn_ques_ans),
    path('question_answer/chat', views.AIchat),
]
