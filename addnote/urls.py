from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'addnote'

urlpatterns = [
    path('', views.index, name='index'),
    path('saveNote/', views.saveNote, name='savenote'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
