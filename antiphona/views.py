from django.http import (
    HttpRequest,
    HttpResponse,
)
from rest_framework import viewsets

from antiphona.models import (
    Antiphona,
    Celebration,
)
from antiphona.serializers import (
    AntiphonaSerializer,
    CelebrationSerializer,
)


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello, world. You're at the polls index.")


class AntiphonaViewSet(viewsets.ModelViewSet):
    queryset = Antiphona.objects.all()
    serializer_class = AntiphonaSerializer


class CelebrationViewSet(viewsets.ModelViewSet):
    queryset = Celebration.objects.all()
    serializer_class = CelebrationSerializer
