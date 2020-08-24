from config.celery import app


@app.task
def test(string):
    print(string)
