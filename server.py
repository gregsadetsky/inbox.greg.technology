import json
import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask

load_dotenv()

app = Flask(__name__)

DATABASE_FILE = os.path.join(os.environ["DATA_DIR"], "data.json")


def get_data():
    if not os.path.exists(DATABASE_FILE):
        return None
    with open(DATABASE_FILE, "r") as f:
        return json.load(f)


@app.route("/")
def hello_world():
    return f"data: {get_data()}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
