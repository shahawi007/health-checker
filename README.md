# Website Health Checker

A small Flask API that checks whether a website is up. It is containerized with Docker and built and published automatically with GitHub Actions.

## Features

- `GET /health` – confirms the app itself is running.
- `GET /check?url=example.com` – checks a website and returns its status code and response time.

Example:

```bash
curl "http://localhost:5000/check?url=google.com"
```

```json
{"url": "https://google.com", "up": true, "status_code": 200, "response_time_ms": 150}
```

## Tech stack

Python · Flask · Docker · Docker Compose · GitHub Actions · GitHub Container Registry (GHCR) · Linux

## Project structure

```
.
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── Dockerfile              # How to build the image
├── docker-compose.yml      # How to run the container
└── .github/workflows/
    └── ci.yml              # CI pipeline
```

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:5000/health`.

## Run with Docker

Build and run the image yourself:

```bash
docker build -t health-checker .
docker run -d -p 5000:5000 --name hc health-checker
```

Or pull the prebuilt image from GHCR:

```bash
docker pull ghcr.io/shahawi007/health-checker:latest
docker run -d -p 5000:5000 --name hc ghcr.io/shahawi007/health-checker:latest
```

Useful commands:

```bash
docker ps              # list running containers
docker logs hc         # view logs
docker stop hc         # stop the container
docker rm hc           # remove the container
```

## Run with Docker Compose

```bash
docker compose up -d
docker compose logs -f
docker compose down
```

## CI pipeline

On every push to `main`, GitHub Actions runs `.github/workflows/ci.yml`:

```
push ──▶ GitHub Actions ──▶ build Docker image ──▶ push to GHCR
```

1. Check out the code.
2. Log in to GitHub Container Registry using the built-in `GITHUB_TOKEN`.
3. Build the Docker image.
4. Push the image to `ghcr.io/shahawi007/health-checker:latest`.

If the `Dockerfile` is broken, the pipeline fails and the image is not published.



