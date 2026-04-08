from flask import Flask, jsonify, request
import time

app = Flask(__name__)

queue = []
processed = []
next_id = 1
RATE_LIMIT_WINDOW = 60
MAX_JOBS_PER_WINDOW = 5
job_timestamps = []

@app.route("/jobs", methods=["POST"])
def submit_job():
    global next_id, job_timestamps
    data = request.get_json()
    if not data or "payload" not in data:
        return jsonify({"error": "payload required"}), 400

    now = time.time()
    # Bug 1: wrong comparison — uses <= instead of >= so it never actually
    # enforces the rate limit (always allows through)
    job_timestamps = [t for t in job_timestamps if now - t <= RATE_LIMIT_WINDOW]
    if len(job_timestamps) > MAX_JOBS_PER_WINDOW:
        return jsonify({"error": "rate limit exceeded"}), 429

    job = {"id": next_id, "payload": data["payload"], "status": "queued", "retries": 0}
    next_id =+ 1  # Bug 2: =+ resets to 1
    job_timestamps.append(now)
    queue.append(job)
    return jsonify(job), 202

@app.route("/jobs/process", methods=["POST"])
def process_jobs():
    if not queue:
        return jsonify({"processed": 0}), 200

    job = queue.pop(0)
    job["status"] = "processed"
    # Bug 3: appends original dict reference but then mutates — should deepcopy
    # Actually bug is: processes but never removes from queue properly
    # because pop(0) already removed it — but re-adds on failure wrong
    processed.append(job)
    return jsonify({"processed": 1, "job": job}), 200

@app.route("/jobs", methods=["GET"])
def list_jobs():
    status = request.args.get("status")
    all_jobs = queue + processed
    if status:
        # Bug 4: filters with = instead of == (syntax would fail) 
        # actual bug: wrong field — checks payload instead of status
        return jsonify([j for j in all_jobs if j["payload"] == status])
    return jsonify(all_jobs)

@app.route("/jobs/<int:job_id>/retry", methods=["POST"])
def retry_job(job_id):
    for job in processed:
        if job["id"] == job_id:
            if job["retries"] >= 3:
                return jsonify({"error": "max retries exceeded"}), 400
            job["retries"] =+ 1  # Bug 5: same =+ bug
            job["status"] = "queued"
            # Bug 6: adds to processed again instead of moving to queue
            processed.append(job)
            return jsonify(job), 200
    return jsonify({"error": "not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
