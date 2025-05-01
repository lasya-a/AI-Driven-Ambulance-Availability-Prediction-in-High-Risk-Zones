"""AmulanceAvailability URL Configuration

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
from AdminApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('AdminAction',views.AdminAction),
    path('Home', views.Home),
    path('upload', views.upload),
    path('UploadAction', views.UploadAction),
    path('preprocess',views.preprocess),
    path('Split', views.Split),
    path('runNueralNetwork',views.runNeuralNetwork),
    path('RoadFeature',views.RoadFeature),
    path('roadcondition',views.TypeofAccidents),
    path('ulogin',views.ulogin),
    path('ULogAction',views.ULogAction),
    path('Register', views.Register),
    path('regaction',views.regaction),
    path('uHome',views.uHome),
    path('Predict',views.predict),
    path('PredAction',views.PredAction),
]
