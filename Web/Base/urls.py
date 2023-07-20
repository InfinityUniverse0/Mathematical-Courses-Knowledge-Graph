from django.urls import path
from . import views # 导入视图函数

urlpatterns = [
    path('', views.welcome_page),
    path('welcome/', views.welcome_page),
    path('index/', views.index_page),
]
