"""firstsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import logout
from firstapp.views import index, detail, comment, index_login, index_register, vote, myinfo, collection

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index, name='index'),
    path('', index, name='index'),
    path('detail/<int:id>', detail, name='detail'),
    path('comment/<int:id>', comment, name='comment'),
    path('login/', index_login, name='login'),
    path('register/', index_register, name='register'),
    path('logout', logout, {'next_page': '/index'}, name='logout'),
    path('vote/<int:id>', vote, name='vote'),
    path('vote/<int:id>', vote, name='vote'),
    path('myinfo', myinfo, name='myinfo'),
    path('collection', collection, name='collection'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
