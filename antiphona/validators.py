from collections.abc import Iterable
from typing import (
    Any,
    Mapping,
    Union,
)

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class TypeValidator:

    def __init__(self, types: Union[type, Iterable[type]]) -> None:
        if not isinstance(types, Iterable):
            types = (types,)

        if any(not isinstance(t, type) for t in types):
            raise ValueError("Must provide an iterable of types")

        self.types = tuple(types)

    def must_be_of_type(self, value: Any) -> None:
        if not isinstance(value, self.types):
            raise ValidationError(
                "Value {value} must be of type {types}".format(
                    value=value,
                    types=", ".join(t.__name__ for t in self.types),
                ),
                params={'value': value},
            )

    def __call__(self, value: Any) -> None:
        self.must_be_of_type(value)


class KeysTypeValidator(TypeValidator):

    def __call__(self, value: Mapping) -> None:
        if not isinstance(value, Mapping):
            raise ValidationError(f"Value: {value} must be of type Mapping.")
        for key in value.keys():
            self.must_be_of_type(key)


class ValuesTypeValidator(TypeValidator):

    def __call__(self, value: Mapping) -> None:
        if not isinstance(value, Mapping):
            raise ValidationError(f"Value: {value} must be of type Mapping.")
        for v in value.values():
            self.must_be_of_type(v)


@deconstructible
class ValidKeyValidator:

    def __init__(self, valid_keys: Iterable) -> None:
        self.valid_keys = set(valid_keys)

    def check_invalid_keys(self, value: Mapping) -> None:
        if not isinstance(value, Mapping):
            raise ValidationError(f"Value: {value} must be of type Mapping.")
        invalid_keys = set(value.keys()) - self.valid_keys
        if invalid_keys:
            raise ValidationError(
                'Value: {invalid_keys} are invalid keys. Only keys accepted are {valid_keys}'.format(
                    invalid_keys=', '.join(sorted(map(str, invalid_keys))),
                    valid_keys=', '.join(self.valid_keys),
                ),
                params={'value': value},
            )

    def __call__(self, value: Mapping) -> None:
        self.check_invalid_keys(value)
