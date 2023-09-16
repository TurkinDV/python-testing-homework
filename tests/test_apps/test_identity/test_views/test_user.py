from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Callable, TypeAlias

import pytest
from django.urls import reverse
from factory.faker import faker

if TYPE_CHECKING:
    from django.test import Client

    from tests.plugins.identity.user_factory import UserFactory

pytestmark = pytest.mark.django_db


UserAssertion: TypeAlias = Callable[['UserFactory', dict[str, Any]], None]


def user_model_to_dict(user: 'UserFactory') -> dict[str, Any]:
    """Converter User model to dict."""
    return {
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'date_of_birth': user.date_of_birth,
        'address': user.address,
        'job_title': user.job_title,
        'phone': user.phone,
    }


@pytest.fixture()
def assert_update_user() -> UserAssertion:
    """Assert change data user."""

    def factory(user: 'UserFactory', cleaned_data: dict[str, Any]) -> None:
        for field, value in cleaned_data.items():  # noqa: WPS110
            assert getattr(user, field) == value

    return factory


def test_user_update_get_template(
    client: 'Client',
    authorized_user: 'UserFactory',
) -> None:
    """Test get template for update user."""
    response = client.get(reverse('identity:user_update'))

    assert response.status_code == HTTPStatus.OK
    assert 'identity/pages/user_update.html' in response.template_name  # type: ignore[attr-defined]  # noqa:E501


FAKE = faker.Faker()


@pytest.mark.parametrize(  # noqa: WPS317
    ('fields', 'values'), [
        (('first_name', 'last_name'), (FAKE.first_name(), FAKE.last_name())),
        (('date_of_birth',), (FAKE.date_object(),)),
        (
            ('address', 'job_title', 'phone'),
            (FAKE.address(), FAKE.job(), FAKE.phone_number()),
        ),
    ],
)
def test_user_update_post_view(
    fields: tuple[str],
    values: tuple[str],  # noqa: WPS110
    client: 'Client',
    authorized_user: 'UserFactory',
    assert_update_user: UserAssertion,
) -> None:
    """Test update user data."""
    cleaned_data = {
        **user_model_to_dict(authorized_user),
        **dict(zip(fields, values)),
    }
    response = client.post(reverse('identity:user_update'), data=cleaned_data)

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('identity:user_update')

    authorized_user.refresh_from_db()
    assert_update_user(authorized_user, cleaned_data)
