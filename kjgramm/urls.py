"""kjgramm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import django.contrib.auth
import views

from django.conf.urls import url


urlpatterns = [
    url(r'add_photo/', views.add_photo),
    url(r'photo_id/like', views.like),
    url(r'photo_id/comments', views.comments),
    url(r'people/?search=''', views.people_search),
    url(r'photo_id/comments/add_comment', views.add_comment),
    url(r'login/', django.contrib.auth.login),
    url(r'register/', views.register_user),
    url(r'feed/', views.feed)
]
