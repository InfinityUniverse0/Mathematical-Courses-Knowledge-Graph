"""
URL configuration for Web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Base.views import page_not_found, server_error, welcome_page, index_page, chat

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", welcome_page),
    # path("base/", include("Base.urls")),
    # path("kg/", include("KG.urls")),
    # path("qa/", include("QA.urls")),
    path("index/", index_page),
    path('chat/', chat)
]

handler404 = page_not_found
handler500 = server_error
