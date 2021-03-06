from typing import (
    Any,
    Callable,
)

from django.utils.translation import gettext_lazy as _
from djongo import models

from antiphona import validators


VALID_LANGUAGES = {'es_AR', 'es_MX', 'es_ES', 'es_US', 'en_US', 'la'}


def inject_validator_enforcement(field: models.Field) -> models.Field:
    def decorate(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            field.run_validators(*args, **kwargs)
            return func(*args, **kwargs)
        return wrapper

    field.get_prep_value = decorate(field.get_prep_value)
    field.to_python = decorate(field.to_python)
    return field


class SupportARFQuerySet(models.QuerySet):
    def create(self, **kwargs: Any) -> models.Model:
        # We pop and save the values sent to ArrayReferenceFields
        array_reference_field_values = dict()
        for field in self.model._meta.fields:
            if not isinstance(field, models.ArrayReferenceField):
                continue
            if field.name in kwargs:
                array_reference_field_values[field.name] = kwargs.pop(field.name)

        # Create the object without the ArrayReferenceFields
        created = super().create(**kwargs)

        # Set the saved values using the .set method of each field
        for name, value in array_reference_field_values.items():
            getattr(created, name).set(value, clear=True)

        return created


SupportARFManager = models.Manager.from_queryset(SupportARFQuerySet)


class Antiphona(models.Model):
    text = inject_validator_enforcement(
        models.JSONField(
            default={},
            validators=[
                validators.TypeValidator(dict),
                validators.KeysTypeValidator(str),
                validators.ValuesTypeValidator(str),
                validators.ValidKeyValidator(valid_keys=VALID_LANGUAGES),
            ],
        ),
    )
    link = inject_validator_enforcement(models.URLField())


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

    objects = SupportARFManager()
