from yektanet.celery import app

from .models import ShortenedURL, Visit, Analytic


@app.task
def update_shortened_url(short_url_key, platform, browser, session_key):
    print('Add visit')
    short_url = ShortenedURL.objects.get(key=short_url_key)
    print(short_url, platform, browser, session_key)
    visit = Visit.objects.create(short_url=short_url, platform=platform,
                                 browser=browser, session_key=session_key)
    print('Visit added')

    return visit.id


# Async periodic task for updating the analytics of each url
@app.task
def update():
    print("updating..")
    for analytic in Analytic.objects.all():
        analytic.update_analytic()
    print("updated successfully")
