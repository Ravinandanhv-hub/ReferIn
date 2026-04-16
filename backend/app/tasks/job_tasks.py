from app.tasks.celery_app import celery_app


@celery_app.task(name="refresh_jobs")
def refresh_jobs():
    """Placeholder task: Refresh jobs from external sources."""
    # TODO: Phase 2 — implement web scraping / API integration
    return {"status": "completed", "message": "Job refresh placeholder executed"}


@celery_app.task(name="send_notification_email")
def send_notification_email(user_email: str, subject: str, body: str):
    """Placeholder task: Send email notification."""
    # TODO: Phase 2 — integrate with email service (SendGrid, SES, etc.)
    return {"status": "completed", "email": user_email, "subject": subject}
