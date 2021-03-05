from django.urls import path

from antiphona import views

urlpatterns = [
    path('', views.index, name='index'),
]
