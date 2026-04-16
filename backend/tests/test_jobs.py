import pytest


@pytest.mark.asyncio
async def test_list_jobs_empty(client):
    response = await client.get("/api/v1/jobs")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_list_jobs_with_data(client, test_job):
    response = await client.get("/api/v1/jobs")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1


@pytest.mark.asyncio
async def test_get_job_detail(client, test_job):
    response = await client.get(f"/api/v1/jobs/{test_job.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Backend Developer"
    assert data["company"] == "Test Corp"


@pytest.mark.asyncio
async def test_get_job_not_found(client):
    response = await client.get("/api/v1/jobs/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_recommended_jobs(client, auth_headers, test_job):
    response = await client.get("/api/v1/jobs/recommended", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data


@pytest.mark.asyncio
async def test_list_jobs_filter_type(client, test_job):
    response = await client.get("/api/v1/jobs?type=full_time")
    assert response.status_code == 200
    data = response.json()
    for job in data["items"]:
        assert job["type"] == "full_time"


@pytest.mark.asyncio
async def test_list_jobs_pagination(client, test_job):
    response = await client.get("/api/v1/jobs?page=1&size=5")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["size"] == 5
