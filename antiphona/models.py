from django.utils.translation import gettext_lazy as _
from djongo import models


class Antiphona(models.Model):
    text = models.JSONField()
    link = models.URLField()


class LiturgicalSeasons(models.TextChoices):
    ADVENT = 'advent', _('Advent')
    CHRISTMAS = 'christmas', _('Christmas')
    LENT = 'lent', _('Lent')
    EASTER = 'easter', _('Easter')
    ORDINARY = 'ordinary', _('Ordinary Time')


class Celebration(models.Model):
    liturgical_season = models.CharField(
        choices=LiturgicalSeasons.choices,
        max_length=9,
    )
    name = models.CharField(max_length=40)
    antiphonas = models.ArrayReferenceField(
        to=Antiphona,
        on_delete=models.DO_NOTHING,
    )
