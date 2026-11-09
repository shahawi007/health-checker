import time

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


def check_site(url, timeout=5):
    """Check one website and return its status."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    start = time.time()
    try:
        response = requests.get(url, timeout=timeout)
        elapsed_ms = round((time.time() - start) * 1000)
        return {
            "url": url,
            "up": response.status_code < 400,
            "status_code": response.status_code,
            "response_time_ms": elapsed_ms,
        }
    except requests.RequestException as error:
        return {
            "url": url,
            "up": False,
            "status_code": None,
            "response_time_ms": None,
            "error": type(error).__name__,
        }


@app.route("/health")
def health():
    # Used by Docker and monitoring tools to know the app itself is alive.
    return jsonify({"status": "ok"})


@app.route("/check")
def check():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "missing 'url' parameter"}), 400
    return jsonify(check_site(url))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
