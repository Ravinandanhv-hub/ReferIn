import pytest


@pytest.mark.asyncio
async def test_register(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "name": "New User",
            "email": "new@example.com",
            "password": "password123",
            "role": "job_seeker",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"
    assert data["name"] == "New User"
    assert data["role"] == "job_seeker"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    await client.post(
        "/api/v1/auth/register",
        json={"name": "User1", "email": "dup@example.com", "password": "password123", "role": "job_seeker"},
    )
    response = await client.post(
        "/api/v1/auth/register",
        json={"name": "User2", "email": "dup@example.com", "password": "password123", "role": "job_seeker"},
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login(client):
    await client.post(
        "/api/v1/auth/register",
        json={"name": "Login User", "email": "login@example.com", "password": "password123", "role": "job_seeker"},
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_password(client):
    await client.post(
        "/api/v1/auth/register",
        json={"name": "Bad Pass", "email": "badpass@example.com", "password": "password123", "role": "job_seeker"},
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "badpass@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client, auth_headers):
    response = await client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "auth@example.com"


@pytest.mark.asyncio
async def test_get_me_unauthorized(client):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code in [401, 403]
