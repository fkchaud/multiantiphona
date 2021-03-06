from django.urls import (
    include,
    path,
)
from rest_framework import routers

from antiphona import views


router = routers.DefaultRouter()
router.register(r'antiphonas', views.AntiphonaViewSet)
router.register(r'celebrations', views.CelebrationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
