import json
import os

from dotenv import load_dotenv

from common import gmail_authenticate
from how_many_emails_in_my_inbox import get_all_unique_thread_ids_from_inbox

load_dotenv()

DATA_FILE = os.path.join(os.environ["DATA_DIR"], "data.json")

service = gmail_authenticate()
nmb_unique_threads = len(get_all_unique_thread_ids_from_inbox(service))

data = {
    "nmb_unique_threads": nmb_unique_threads,
}

with open(DATA_FILE, "a") as f:
    json.dump(data, f)
