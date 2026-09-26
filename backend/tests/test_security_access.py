from fastapi import FastAPI
from fastapi.testclient import TestClient
app=FastAPI()
@app.get('/protected')
def protected(): return {'ok':True}
def test_access_contract(): assert TestClient(app).get('/protected').status_code==200
