from sqlalchemy.orm import Session
from starlette.testclient import TestClient
from . import utils


def test_create_user(client: TestClient, db: Session):
    token = utils.get_superuser_access_token(db)
    token_headers = utils.get_token_headers(token)
    response = client.post(
        "/users/",
        json={"email": "john@example.com", "password": "johnpass"},
        headers=token_headers,
    )
    data = response.json()
    assert data["email"] == "john@example.com"
    assert "password" not in data
