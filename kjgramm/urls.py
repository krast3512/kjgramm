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
from django.conf.urls.static import static
import django.contrib.auth
from kjgramm import views

from django.conf.urls import url
from kjgramm import settings


urlpatterns = [
    url(r'(?P<photo_id>\d{0,50})/like', views.like),
    url(r'(?P<photo_id>\d{0,50})/comments', views.comments),
    url(r'people/', views.people_search),
    url(r'(?P<photo_id>\d{0,50})/comments/add_comment', views.add_comment),
    url(r'login/', django.contrib.auth.login),
    url(r'register/', views.register_user),
    url(r'feed/', views.feed)
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
