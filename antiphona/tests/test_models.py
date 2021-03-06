from django.core.exceptions import ValidationError
from django.test import TestCase
import pytest

from antiphona.models import (
    VALID_LANGUAGES,
    Antiphona,
)


class TestAntiphona(TestCase):

    def test_create_with_empty_values(self) -> None:
        antiphona = Antiphona.objects.create()
        assert antiphona.link == ''
        assert antiphona.text == {}

    def test_text_must_be_a_dict(self) -> None:
        with pytest.raises(ValidationError, match='must be of type dict'):
            Antiphona.objects.create(text=['this is not a dict'])

    def test_text_keys_must_be_strings(self) -> None:
        with pytest.raises(ValidationError, match='must be of type str'):
            Antiphona.objects.create(text={123: "123", 456: "456"})

    def test_text_values_must_be_strings(self) -> None:
        with pytest.raises(ValidationError, match='must be of type str'):
            Antiphona.objects.create(text={"es_ES": 123, "es_AR": 456})

    def test_text_keys_must_be_one_of_a_valid_list(self) -> None:
        with pytest.raises(ValidationError, match='are invalid keys'):
            Antiphona.objects.create(text={"123": "123", "456": "456"})

    def test_link_must_be_valid_url(self) -> None:
        with pytest.raises(ValidationError, match='Enter a valid URL'):
            Antiphona.objects.create(link="an invalid url")

    def test_antiphona_with_valid_values(self) -> None:
        text = {
            key: "some text"
            for key in VALID_LANGUAGES
        }
        link = "https://gregobase.selapa.net/chant.php?id=7911"

        antiphona = Antiphona.objects.create(text=text, link=link)

        assert antiphona.text == text
        assert antiphona.link == link
