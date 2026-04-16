import pytest


@pytest.mark.asyncio
async def test_create_referral(client, auth_headers, test_job, test_referrer):
    response = await client.post(
        "/api/v1/referrals",
        json={
            "job_id": str(test_job.id),
            "referrer_id": str(test_referrer.id),
            "message": "I'd love a referral for this role!",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "pending"
    assert data["job_id"] == str(test_job.id)


@pytest.mark.asyncio
async def test_get_my_referrals(client, auth_headers):
    response = await client.get("/api/v1/referrals/my", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "sent" in data
    assert "received" in data


@pytest.mark.asyncio
async def test_create_referral_unauthorized(client, test_job, test_referrer):
    response = await client.post(
        "/api/v1/referrals",
        json={
            "job_id": str(test_job.id),
            "referrer_id": str(test_referrer.id),
        },
    )
    assert response.status_code in [401, 403]


@pytest.mark.asyncio
async def test_create_referral_job_not_found(client, auth_headers, test_referrer):
    response = await client.post(
        "/api/v1/referrals",
        json={
            "job_id": "00000000-0000-0000-0000-000000000000",
            "referrer_id": str(test_referrer.id),
        },
        headers=auth_headers,
    )
    assert response.status_code == 404
