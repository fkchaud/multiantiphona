from django.core.exceptions import ValidationError
from django.test import TestCase
import pytest

from antiphona.validators import (
    KeysTypeValidator,
    TypeValidator,
    ValidKeyValidator,
    ValuesTypeValidator,
)


class TestTypeValidator(TestCase):

    def test_raises_error_if_types_is_not_a_type(self) -> None:
        with pytest.raises(ValueError, match="Must provide an iterable of types"):
            TypeValidator(types="this is not a type")  # type: ignore

    def test_raises_error_if_types_is_not_an_iterable_of_types(self) -> None:
        with pytest.raises(ValueError, match="Must provide an iterable of types"):
            TypeValidator(types=(str, "this is not a type", int))  # type: ignore

    def test_can_receive_a_single_type(self) -> None:
        validator = TypeValidator(types=str)
        assert validator.types == (str,)

    def test_can_receive_multiple_types(self) -> None:
        validator = TypeValidator(types={int, str})
        assert validator.types == (int, str)

    def test_fails_when_value_is_not_of_single_type(self) -> None:
        value = 5
        with pytest.raises(ValidationError, match="must be of type str"):
            TypeValidator(types=str)(value)

    def test_fails_when_value_is_not_of_multiple_type(self) -> None:
        value = {"5": 5}
        with pytest.raises(ValidationError, match="must be of type str. int"):
            TypeValidator(types=(str, int))(value)

    def test_does_not_fail_when_value_is_of_single_type(self) -> None:
        value = "5"
        assert TypeValidator(types=str)(value) is None

    def test_does_not_fail_when_value_is_one_of_multiple_types(self) -> None:
        validator = TypeValidator(types=(str, int))
        validator("5")
        validator(5)


class TestKeysTypeValidator(TestCase):

    def test_raises_error_if_types_is_not_a_type(self) -> None:
        with pytest.raises(ValueError, match="Must provide an iterable of types"):
            KeysTypeValidator(types="this is not a type")  # type: ignore

    def test_raises_error_if_types_is_not_an_iterable_of_types(self) -> None:
        with pytest.raises(ValueError, match="Must provide an iterable of types"):
            KeysTypeValidator(types=(str, "this is not a type", int))  # type: ignore

    def test_can_receive_a_single_type(self) -> None:
        validator = KeysTypeValidator(types=str)
        assert validator.types == (str,)

    def test_can_receive_multiple_types(self) -> None:
        validator = KeysTypeValidator(types={int, str})
        assert validator.types == (int, str)

    def test_value_must_be_a_map(self) -> None:
        value = "not a map"
        with pytest.raises(ValidationError, match="must be of type Mapping"):
            # noinspection PyTypeChecker
            KeysTypeValidator(types=str)(value)  # type: ignore

    def test_fails_when_value_is_not_of_single_type(self) -> None:
        value = {5: "5"}
        with pytest.raises(ValidationError, match="must be of type str"):
            KeysTypeValidator(types=str)(value)

    def test_fails_when_value_is_not_of_multiple_type(self) -> None:
        value = {("5", 5): "5"}
        with pytest.raises(ValidationError, match="must be of type str, int"):
            KeysTypeValidator(types=(str, int))(value)

    def test_does_not_fail_when_value_is_of_single_type(self) -> None:
        value = {"5": "5"}
        assert KeysTypeValidator(types=str)(value) is None

    def test_does_not_fail_when_value_is_one_of_multiple_types(self) -> None:
        validator = KeysTypeValidator(types=(str, int))
        validator({"5": "5"})
        validator({5: "5"})


class TestValuesTypeValidator(TestCase):

    def test_raises_error_if_types_is_not_a_type(self) -> None:
        with pytest.raises(ValueError, match="Must provide an iterable of types"):
            ValuesTypeValidator(types="this is not a type")  # type: ignore

    def test_raises_error_if_types_is_not_an_iterable_of_types(self) -> None:
        with pytest.raises(ValueError, match="Must provide an iterable of types"):
            ValuesTypeValidator(types=(str, "this is not a type", int))  # type: ignore

    def test_can_receive_a_single_type(self) -> None:
        validator = ValuesTypeValidator(types=str)
        assert validator.types == (str,)

    def test_can_receive_multiple_types(self) -> None:
        validator = ValuesTypeValidator(types={int, str})
        assert validator.types == (int, str)

    def test_value_must_be_a_map(self) -> None:
        value = "not a map"
        with pytest.raises(ValidationError, match="must be of type Mapping"):
            # noinspection PyTypeChecker
            ValuesTypeValidator(types=str)(value)  # type: ignore

    def test_fails_when_value_is_not_of_single_type(self) -> None:
        value = {"5": 5}
        with pytest.raises(ValidationError, match="must be of type str"):
            ValuesTypeValidator(types=str)(value)

    def test_fails_when_value_is_not_of_multiple_type(self) -> None:
        value = {"5": ("5", 5)}
        with pytest.raises(ValidationError, match="must be of type str, int"):
            ValuesTypeValidator(types=(str, int))(value)

    def test_does_not_fail_when_value_is_of_single_type(self) -> None:
        value = {"5": "5"}
        assert ValuesTypeValidator(types=str)(value) is None

    def test_does_not_fail_when_value_is_one_of_multiple_types(self) -> None:
        validator = ValuesTypeValidator(types=(str, int))
        validator({"5": "5"})
        validator({"5": 5})


class TestValidKeyValidator(TestCase):

    def test_sent_keys_are_stored_as_a_set(self) -> None:
        keys = ("1", "2", "3")
        expected_keys = {"1", "2", "3"}

        validator = ValidKeyValidator(valid_keys=keys)

        assert validator.valid_keys == expected_keys

    def test_value_must_be_a_map(self) -> None:
        value = "not a map"
        with pytest.raises(ValidationError, match="must be of type Mapping"):
            # noinspection PyTypeChecker
            ValidKeyValidator(valid_keys="")(value)  # type: ignore

    def test_raises_error_for_all_invalid_keys(self) -> None:
        value = {
            "1": "1",
            "2": "2",
        }
        with pytest.raises(ValidationError, match="Value: 1, 2 are invalid keys."):
            ValidKeyValidator([])(value)

    def test_raises_error_only_for_invalid_keys(self) -> None:
        value = {
            "1": "1",
            "2": "2",
        }
        with pytest.raises(ValidationError, match="Value: 2 are invalid keys."):
            ValidKeyValidator(["1"])(value)

    def test_accepts_dict_with_all_keys(self) -> None:
        value = {
            "1": "1",
            "2": "2",
        }
        ValidKeyValidator(["1", "2"])(value)

    def test_accepts_dict_with_less_keys_than_the_valid_ones(self) -> None:
        value = {
            "1": "1",
            "2": "2",
        }
        ValidKeyValidator(["1", "2", "3"])(value)
