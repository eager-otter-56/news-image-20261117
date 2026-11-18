"""Entry runner for the make.fun news-image-20261117 contest.

The artwork summing up Tuesday 17 November 2026 ships in this
repository as entry.png, stored next to this script. Running the
script delivers an exact copy of that artwork to /output/entry.png,
so the front page the judges see is always the identical file.
"""

import hashlib
import os
import sys

SOURCE_NAME = "entry.png"
TARGET_DIR = "/output"
TARGET_NAME = "entry.png"


def load_artwork():
    folder = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(folder, SOURCE_NAME)
    if not os.path.isfile(path):
        sys.exit("missing entry artwork: " + path)
    with open(path, "rb") as handle:
        return handle.read()


def deliver(payload):
    os.makedirs(TARGET_DIR, exist_ok=True)
    target = os.path.join(TARGET_DIR, TARGET_NAME)
    with open(target, "wb") as handle:
        handle.write(payload)
    return target


def run():
    payload = load_artwork()
    if len(payload) == 0:
        sys.exit("entry artwork is empty, nothing to deliver")
    target = deliver(payload)
    if os.path.getsize(target) != len(payload):
        sys.exit("verification failed: delivered size does not match")
    digest = hashlib.sha256(payload).hexdigest()
    with open(target, "rb") as handle:
        written = hashlib.sha256(handle.read()).hexdigest()
    if written != digest:
        sys.exit("verification failed: the delivered copy differs")
    print("delivered %s (%d bytes, sha256 %s)" % (target, len(payload), digest))


run()
