import pytest
from httpx import AsyncClient
from fastapi import FastAPI


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient) -> None:
    """
    Test registering a new user
    """
    data = {
        "email": "test@example.com",
        "password": "TestPassword123",
    }
    
    response = await client.post("/auth/register", json=data)
    assert response.status_code == 201, response.text
    user_data = response.json()
    assert user_data["email"] == data["email"]
    assert "id" in user_data
    assert "is_active" in user_data
    assert "is_verified" in user_data
    assert "is_superuser" in user_data


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient) -> None:
    """
    Test user login
    """
    # First register a user
    register_data = {
        "email": "login_test@example.com",
        "password": "TestPassword123",
    }
    
    register_response = await client.post("/auth/register", json=register_data)
    assert register_response.status_code == 201
    
    # Login with the registered user
    login_data = {
        "username": register_data["email"],
        "password": register_data["password"],
    }
    
    login_response = await client.post("/auth/jwt/login", data=login_data)
    assert login_response.status_code == 200
    login_result = login_response.json()
    assert "access_token" in login_result
    assert login_result["token_type"] == "bearer"
