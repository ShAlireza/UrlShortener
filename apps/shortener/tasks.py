from config.celery import app


@app.task
def test(string):
    print(string)


@app.task
def update_shortened_url():
    pass
