import sys
from fastapi import FastAPI
from os import path

sys.path.append(path.dirname(__file__))

app = FastAPI(
    title="API graficacion",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"Mi API de graficas": "running!"}
