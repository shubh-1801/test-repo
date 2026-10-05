from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Welcome to the webpage, Jaya Narayana!" in response.text
    assert 'href="/docs"' in response.text


def test_checksum():
    response = client.post("/checksum", json={"content": "Hello, world!"})
    assert response.status_code == 200
    assert response.json() == {"checksum": "6cd3556deb0da54bca060b4c39479839"}


def test_empty_checksum():
    assert client.post("/checksum", json={"content": ""}).json() == {
        "checksum": "d41d8cd98f00b204e9800998ecf8427e"
    }


def test_unicode_checksum():
    response = client.post("/checksum", json={"content": "\u00e9"})
    assert response.json() == {"checksum": "66ddcd97cfdeabb2f6fb8a999b4bc76f"}


def test_generate():
    first = client.post("/generate", json={"content": "Jaya"})
    second = client.post("/generate", json={"content": "Jaya"})
    assert first.status_code == 200
    assert len(first.json()["token"]) == 43
    assert first.json()["token"] != second.json()["token"]


def test_invalid_requests():
    for route in ("/generate", "/checksum"):
        for payload in ({}, {"content": None}, {"content": 123}):
            assert client.post(route, json=payload).status_code == 422
        assert client.post(route, content="invalid JSON").status_code == 422


def test_swagger():
    assert client.get("/docs").status_code == 200
    schema = client.get("/openapi.json").json()
    assert set(schema["paths"]) == {"/", "/generate", "/checksum"}
    assert "post" in schema["paths"]["/generate"]
    assert "post" in schema["paths"]["/checksum"]


def test_static_assets():
    assert client.get("/static/styles.css").status_code == 200
    response = client.get("/static/rocket.png")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"


def test_project_source(monkeypatch):
    monkeypatch.delenv("PROJECT_SOURCE_URL", raising=False)
    assert "app = FastAPI" in client.get("/source").text
    monkeypatch.setenv("PROJECT_SOURCE_URL", "https://github.com/example/project")
    response = client.get("/source", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://github.com/example/project"