from django.urls import path
from . import views

urlpatterns = [
    path('', views.translate_image, name='translate_image'),
]
