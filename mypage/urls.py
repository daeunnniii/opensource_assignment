from django.urls import path
from . import views

app_name = 'mypage'

urlpatterns = [
    path('', views.password_edit_view, name='password_edit'),
    #path('', views.index, name='index'),
]
