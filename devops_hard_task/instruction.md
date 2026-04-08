## Objective

A job queue REST API at `/app/app.py` has several bugs causing incorrect behavior across multiple endpoints.

## Endpoints

- `POST /jobs` — submit a job `{"payload": "..."}` → `{"id": int, "payload": str, "status": "queued", "retries": 0}`
- `POST /jobs/process` — process the next queued job → `{"processed": 1, "job": {...}}`
- `GET /jobs?status=queued` — list jobs filtered by status
- `POST /jobs/<id>/retry` — retry a processed job (max 3 retries)

## Observed Problems

- Job IDs are not unique
- Filtering jobs by status returns wrong results
- Retrying a job does not move it back to the queue correctly
- Retry counter does not increment properly

## Your Goal

Fix all bugs in `/app/app.py`. The app should correctly manage job lifecycle: submit → process → retry.

Start with: `python /app/app.py`
