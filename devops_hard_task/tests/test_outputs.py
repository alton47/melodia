import subprocess
import sys
import time

subprocess.run([sys.executable, "-m", "ensurepip"], check=False)
subprocess.run([sys.executable, "-m", "pip", "install", "flask==3.0.3", "requests==2.31.0", "-q", "--break-system-packages"], check=False)

import requests

BASE = "http://localhost:5000"

def start_server():
    proc = subprocess.Popen(["python", "/app/app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3)
    return proc

def test_unique_ids():
    proc = start_server()
    try:
        r1 = requests.post(f"{BASE}/jobs", json={"payload": "task_a"})
        r2 = requests.post(f"{BASE}/jobs", json={"payload": "task_b"})
        r3 = requests.post(f"{BASE}/jobs", json={"payload": "task_c"})
        assert r1.status_code == 202
        assert r2.status_code == 202
        assert r3.status_code == 202
        ids = [r1.json()["id"], r2.json()["id"], r3.json()["id"]]
        assert len(set(ids)) == 3, f"IDs not unique: {ids}"
        assert ids == sorted(ids), f"IDs not incrementing: {ids}"
    finally:
        proc.terminate()

def test_filter_by_status():
    proc = start_server()
    try:
        requests.post(f"{BASE}/jobs", json={"payload": "j1"})
        requests.post(f"{BASE}/jobs", json={"payload": "j2"})
        requests.post(f"{BASE}/jobs/process")

        queued = requests.get(f"{BASE}/jobs?status=queued").json()
        done = requests.get(f"{BASE}/jobs?status=processed").json()

        assert len(queued) == 1, f"Expected 1 queued, got {len(queued)}"
        assert len(done) == 1, f"Expected 1 processed, got {len(done)}"
        assert all(j["status"] == "queued" for j in queued)
        assert all(j["status"] == "processed" for j in done)
    finally:
        proc.terminate()

def test_retry_moves_to_queue():
    proc = start_server()
    try:
        r = requests.post(f"{BASE}/jobs", json={"payload": "retryable"})
        job_id = r.json()["id"]
        requests.post(f"{BASE}/jobs/process")

        rr = requests.post(f"{BASE}/jobs/{job_id}/retry")
        assert rr.status_code == 200, f"Retry failed: {rr.text}"
        assert rr.json()["retries"] == 1, f"Retries not incremented: {rr.json()}"
        assert rr.json()["status"] == "queued"

        queued = requests.get(f"{BASE}/jobs?status=queued").json()
        assert any(j["id"] == job_id for j in queued), "Job not back in queue"

        still_processed = requests.get(f"{BASE}/jobs?status=processed").json()
        assert not any(j["id"] == job_id for j in still_processed), "Job still in processed"
    finally:
        proc.terminate()

def test_retry_counter_increments():
    proc = start_server()
    try:
        r = requests.post(f"{BASE}/jobs", json={"payload": "counter_test"})
        job_id = r.json()["id"]
        requests.post(f"{BASE}/jobs/process")

        for expected in range(1, 4):
            rr = requests.post(f"{BASE}/jobs/{job_id}/retry")
            assert rr.status_code == 200
            assert rr.json()["retries"] == expected, f"Expected {expected} got {rr.json()['retries']}"
            requests.post(f"{BASE}/jobs/process")

        rr = requests.post(f"{BASE}/jobs/{job_id}/retry")
        assert rr.status_code == 400, "Should be blocked after 3 retries"
    finally:
        proc.terminate()
