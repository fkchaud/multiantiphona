import random

import factory
from factory import fuzzy
import faker
from faker.config import AVAILABLE_LOCALES

from antiphona import models


class TextFactory(fuzzy.BaseFuzzyAttribute):
    def fuzz(self) -> dict[str, str]:
        language_quantity = random.randint(0, len(models.VALID_LANGUAGES))
        languages = random.sample(list(models.VALID_LANGUAGES), k=language_quantity)
        faker_languages = {
            language: language if language in AVAILABLE_LOCALES else language[:2]
            for language in languages
        }
        faker_generator = faker.Faker(list(faker_languages.values()))
        text = {
            language: faker_generator[faker_languages[language]].sentence()
            for language in languages
        }
        return text


class AntiphonaFactory(factory.django.DjangoModelFactory):
    link = factory.Faker('url')
    text = TextFactory()

    class Meta:
        model = models.Antiphona
