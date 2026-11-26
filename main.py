"""A one-line forecast for a town that was never built.

The bounty wants a single line, no more than 120 characters, forecasting
weather for an invented place. The humour has to live inside the weather
itself: an ordinary bulletin voice reporting something impossible, with a
place name that already sounds wet. Twelve contenders were drafted and
graded on those demands; the code below keeps the strongest and refuses
to print anything else, so every run emits identical bytes.
"""

import hashlib
import pathlib
import sys

_LEAD = "Cloudburst Creek: one raindrop "
_CENTER = "expected today, weighing four tonnes, "
_CLOSER = "due at 3pm. Bring a very large umbrella."
_CHOSEN = _LEAD + _CENTER + _CLOSER

_TIRED = ("knock knock", "as an ai", "lol", "haha", "😂", "pun")

_CANDIDATES = (
    {"town": "Cloudburst Creek", "body": "one raindrop expected today, weighing four tonnes, due at 3pm. Bring a very large umbrella.", "marks": 48},
    {"town": "Cloudburst Creek", "body": "rain expected in one single drop, weighing four tonnes, at 3pm sharp. Bring a very large umbrella.", "marks": 46},
    {"town": "Drizzlewick", "body": "rain today, tomorrow, and retroactively last Thursday. Umbrellas advised for the past.", "marks": 44},
    {"town": "Gloomsville", "body": "overcast with a 90% chance of Tuesday. Bring a coat and a calendar.", "marks": 42},
    {"town": "Blizzard Bay", "body": "snow expected, 3 feet by noon, 6 feet by tea. Shovels are sold out; doors open inward for a reason.", "marks": 42},
    {"town": "Mizzleport", "body": "drizzle expected all day, arriving from below. Residents are advised to wear their umbrellas upside down.", "marks": 41},
    {"town": "Rainport", "body": "showers expected, falling up. The town requests residents catch the rain before it leaves.", "marks": 41},
    {"town": "Hailbury", "body": "hailstones the size of grapefruit expected by noon. Please do not eat the weather.", "marks": 40},
    {"town": "Drizzlewick", "body": "rain falling sideways since Tuesday. The town has voted to rename gravity.", "marks": 38},
    {"town": "Heatstroke Hollow", "body": "48 degrees today, shade sold separately. Residents are advised to stay indoors.", "marks": 37},
    {"town": "Foggerton", "body": "dense fog, visibility 0 metres. If you can read this forecast, you are already lost.", "marks": 36},
    {"town": "Stormfield", "body": "thunderstorms all afternoon, lightning striking the same place twice, out of spite.", "marks": 33})


def _inspect(text):
    if len(text) < 1 or len(text) > 120:
        sys.exit("candidate breaks the 1-120 character ceiling")
    if text != text.strip() or "\n" in text or "\r" in text:
        sys.exit("candidate is padded or spills past one line")
    lowered = text.lower()
    for stale in _TIRED:
        if stale in lowered:
            sys.exit("candidate leans on a tired gag")


def _select_best(entries):
    for entry in entries:
        _inspect(entry["town"] + ": " + entry["body"])
    ranked = sorted(entries, key=lambda item: (-item["marks"], len(item["town"] + ": " + item["body"]), item["town"] + ": " + item["body"]))
    champion = ranked[0]
    return champion["town"] + ": " + champion["body"]


def _audit_winner(picked):
    if len(picked) != 109:
        sys.exit("winner failed the length check")
    if not picked.startswith("Cloudburst Creek:"):
        sys.exit("winner lost its invented town")
    if "one raindrop" not in picked:
        sys.exit("winner lost its single-drop turn")
    if "four tonnes" not in picked:
        sys.exit("winner lost its weight")
    if "due at 3pm" not in picked:
        sys.exit("winner lost its bulletin voice")
    if not picked.endswith("very large umbrella."):
        sys.exit("winner lost its closing advice")
    if "  " in picked:
        sys.exit("winner carries a doubled space")
    if picked.count("raindrop") != 1:
        sys.exit("winner mentions the raindrop twice")


def _emit():
    line = _select_best(_CANDIDATES)
    if line != _CHOSEN:
        sys.exit("selection drifted from the graded champion")
    _audit_winner(line)
    destination = pathlib.Path("/output/entry.txt")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(line.encode("utf-8"))
    stored = destination.read_bytes().decode("utf-8")
    if stored != line:
        sys.exit("stored bytes differ from the chosen line")
    fingerprint = hashlib.sha256(destination.read_bytes()).hexdigest()
    if fingerprint != hashlib.sha256(line.encode("utf-8")).hexdigest():
        sys.exit("stored sha-256 differs from the chosen line")
    if len(line) != len(_CHOSEN):
        sys.exit("chosen line is not 109 characters long")
    sys.stdout.write(line + "\n")
    sys.stdout.write("sha256: " + fingerprint + "\n")


_emit()
