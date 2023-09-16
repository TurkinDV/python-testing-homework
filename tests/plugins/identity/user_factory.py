from typing import Any, Callable, TypeAlias

import factory
import pytest

from server.apps.identity.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """Factory model User."""

    class Meta(object):
        """Indication Django model."""

        model = User

    class Params(object):  # noqa: WPS110
        superuser = factory.Trait(
            is_superuser=True,
            is_staff=True,
        )
        enabled = True

    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    date_of_birth = factory.Faker('date_object')
    address = factory.Faker('address')
    job_title = factory.Faker('job')
    phone = factory.Faker('phone_number')


UserFactoryType: TypeAlias = Callable[[], Callable[[], UserFactory]]


@pytest.fixture()
def user_model_factory() -> UserFactoryType:
    """Returns factory for fake random data for user model."""
    def factory(**fields: dict[str, Any]) -> Callable[[], UserFactory]:
        return UserFactory.create(**fields)
    return factory


@pytest.fixture()
def user(user_model_factory: UserFactory) -> UserFactory:
    """Model User."""
    return user_model_factory()
