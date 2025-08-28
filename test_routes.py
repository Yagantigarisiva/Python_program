from app import app

def test_home():
    client = app.test_client()
    r = client.get('/')
    assert r.status_code == 200

def test_search():
    client = app.test_client()
    r = client.get('/search?q=home')
    assert r.status_code == 200
