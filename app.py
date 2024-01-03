from fastapi import FastAPI

app = FastAPI()


@app.get('/ping')
def pint():
    return "pong"


@app.post('/invocations')
def invoke():
    return {"testing": 'testing'}
