from django.urls import path
from . import views

app_name = 'mynote'

urlpatterns = [
    path('', views.index, name='index'),
    path('result', views.result, name='result'),
    path('vis', views.view_network, name='view_network')
]
