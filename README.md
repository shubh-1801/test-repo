# Containerized Python API

A FastAPI app with the welcome screen from the reference, interactive Swagger
documentation, token generation, and text checksums.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Open http://localhost:8000 for the welcome page or http://localhost:8000/docs
to try the API in Swagger. Alternative ReDoc documentation is at `/redoc`.

## API

| Method | Path | Behavior |
| --- | --- | --- |
| GET | `/` | HTML welcome page |
| POST | `/generate` | New random, URL-safe token: `{"token": "..."}` |
| POST | `/checksum` | UTF-8 text MD5 digest: `{"checksum": "..."}` |

Both POST endpoints require a JSON body with a string `content` property:

```bash
curl -X POST http://localhost:8000/checksum \
	-H 'Content-Type: application/json' \
	-d '{"content":"Hello, world!"}'
```

Expected response: `{"checksum":"6cd3556deb0da54bca060b4c39479839"}`.
Empty strings are accepted. Invalid or missing content returns HTTP 422.

The supplied screenshots do not specify the generation algorithm. `/generate`
returns a fresh random token on each request; content is accepted but not encoded
in the token. These tokens are not persisted or usable as authentication tokens.
MD5 matches the illustrated 32-character checksum format and must not be used
for passwords or security-sensitive integrity checks.

The Project source button serves the app's source by default. Set
`PROJECT_SOURCE_URL=https://github.com/your-org/your-repo` to link to your repository.

## Test

```bash
python -m pytest -q
```

## Docker

```bash
docker build -t containerized-python-api .
docker run --rm -p 8000:8000 containerized-python-api
```

The container runs as a non-root user and listens on `PORT` (default: `8000`).
For Azure App Service, configure the container's target port to `8000`.
No Azure resources are provisioned by this project.

## Assets

The rocket is from Twitter's Twemoji project, licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Source: https://github.com/twitter/twemoji.
The welcome page uses Lato from Google Fonts, with a local font fallback.