"""autoupgrade URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url

from autoupgrade.view import flowupdate
from autoupgrade.view import updateserver
from autoupgrade.view import updatedata
from autoupgrade.view import flowpage

urlpatterns = [
    url('getAppList', updatedata.getAppList),
    url('updateFlow', updateserver.upgradeApp),
    path('flow', flowpage.getUpdateFlowPage),
    url('getUpdatePer', updatedata.getUpdatePer),
    url('getVer', updatedata.getVer),
    #path('updateFlow', flowupdate.upgrade),
    path('admin/', admin.site.urls),
]
