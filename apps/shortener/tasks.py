from config.celery import app

from .models import ShortenedURL, Visit


@app.task
def update_shortened_url(short_url_key, platform, browser, session_key):
    short_url = ShortenedURL.objects.get(short_url_key)
    visit = Visit.objects.create(short_url=short_url, platform=platform,
                                 browser=browser, session_key=session_key)

    return visit.id


