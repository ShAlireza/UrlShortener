from config.celery import app


@app.task('test')
def test(string):
    print(string)
