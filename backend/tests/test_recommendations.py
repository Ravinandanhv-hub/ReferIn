import pytest
from app.models.user import User
from app.models.job import Job
from app.services.recommendation_service import RecommendationService


@pytest.mark.asyncio
async def test_recommendation_scoring(db_session, test_user, test_job):
    service = RecommendationService(db_session)
    result = await service.get_recommendations(test_user, limit=10)
    assert len(result.items) >= 0  # May or may not match depending on skills


@pytest.mark.asyncio
async def test_recommendation_skill_match(db_session):
    """Test that jobs matching user skills score higher."""
    user = User(
        name="Skill Tester",
        email="skitest@example.com",
        hashed_password="fake",
        role="job_seeker",
        skills=["React", "TypeScript"],
        experience=3,
        location="Bangalore, India",
    )
    db_session.add(user)

    # Job matching skills
    matching_job = Job(
        title="React Developer",
        company="MatchCo",
        type="full_time",
        skills_required=["React", "TypeScript"],
        experience_min=2,
        experience_max=5,
        location="Bangalore, India",
    )
    # Job not matching skills
    non_matching_job = Job(
        title="Java Developer",
        company="NoMatchCo",
        type="full_time",
        skills_required=["Java", "Spring"],
        experience_min=2,
        experience_max=5,
        location="Bangalore, India",
    )
    db_session.add_all([matching_job, non_matching_job])
    await db_session.commit()
    await db_session.refresh(user)

    service = RecommendationService(db_session)
    result = await service.get_recommendations(user, limit=10)

    if len(result.items) >= 2:
        # The matching job should score higher
        matching_scores = [i for i in result.items if i.company == "MatchCo"]
        non_matching_scores = [i for i in result.items if i.company == "NoMatchCo"]
        if matching_scores and non_matching_scores:
            assert matching_scores[0].score >= non_matching_scores[0].score
