import json
import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()

app = Flask(__name__)

DATABASE_FILE = os.path.join(os.environ["DATA_DIR"], "data.json")
SECRET_CRON_URL_PATH = os.environ["SECRET_CRON_URL_PATH"]


def get_data():
    if not os.path.exists(DATABASE_FILE):
        return None
    with open(DATABASE_FILE, "r") as f:
        return json.load(f)


@app.route("/")
def index():
    nmb_unique_threads = get_data()
    if nmb_unique_threads:
        nmb_unique_threads = nmb_unique_threads["nmb_unique_threads"]
    else:
        nmb_unique_threads = "N/A"
    return render_template("index.html", nmb_unique_threads=nmb_unique_threads)


@app.route(SECRET_CRON_URL_PATH, methods=["POST"])
def cron():
    from common import gmail_authenticate
    from how_many_emails_in_my_inbox import get_all_unique_thread_ids_from_inbox

    service = gmail_authenticate()
    nmb_unique_threads = len(get_all_unique_thread_ids_from_inbox(service))

    data = {
        "nmb_unique_threads": nmb_unique_threads,
        "timestamp": datetime.now().isoformat(),
    }

    with open(DATABASE_FILE, "w+") as f:
        json.dump(data, f)

    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
