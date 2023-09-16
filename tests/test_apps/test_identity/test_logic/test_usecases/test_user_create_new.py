from typing import TYPE_CHECKING

import pytest

from server.apps.identity.container import container
from server.apps.identity.logic.usecases.user_create_new import UserCreateNew

if TYPE_CHECKING:
    from server.apps.identity.intrastructure.services.placeholder import (
        UserResponse,
    )
    from tests.plugins.identity.user_factory import UserFactory

pytestmark = pytest.mark.django_db


def test_user_create_new(
    user: 'UserFactory',
    mock_api_create_lead: 'UserResponse',
) -> None:
    """Test create user in external service."""
    user_create_new = container.instantiate(UserCreateNew)
    user_create_new(user)

    user.refresh_from_db()
    assert user.lead_id is not None
