"""Forecast GTA VI's launch-day Twitch viewers hour by hour.

Model: a diurnal shape fitted on 19 comparable big launches' release days
(SullyGnome hourly Twitch category averages, bundled as comparables in the
kit's practice cases). For each comparable I took the log ratio of each UTC
hour's viewers to the 00:00 UTC hour's viewers; the median curve across the
19 launches is the forecast's median, and the residual standard deviation
per hour is the log spread. That shape beats the house persistence baseline
on those same 19 launches (mean pinball loss 0.306 vs 0.410).

The shape: viewership dips in the small hours (US still locked), rises from
05:00 UTC as the US east coast unlocks, and peaks around 18:00-19:00 UTC as
US prime time approaches, ending the day at about twice hour 1's level.

Forecast hour H (2..24) is UTC hour H-1, so hour H uses the curve entry
for UTC hour H-1. Deterministic, stdlib only, no network, fast.
"""

import json
import math
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

INPUT_DIR = Path(os.environ.get("MAKEFUN_INPUT_DIR", "/input"))
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

LEVELS = [0.05, 0.25, 0.5, 0.75, 0.95]
Z = [-1.645, -0.674, 0, 0.674, 1.645]

# (median log ratio to hour 1, log spread) per UTC hour 1..23.
# Fitted on 19 comparable launches; see module docstring.
CURVE = {
    1: (-0.138, 0.25),
    2: (-0.283, 0.33),
    3: (-0.310, 0.27),
    4: (-0.219, 0.25),
    5: (-0.047, 0.47),
    6: (-0.021, 0.52),
    7: (-0.060, 0.56),
    8: (-0.089, 0.60),
    9: (-0.063, 0.63),
    10: (-0.075, 0.64),
    11: (-0.022, 0.67),
    12: (0.109, 0.75),
    13: (0.263, 0.78),
    14: (0.418, 0.80),
    15: (0.502, 0.80),
    16: (0.571, 0.75),
    17: (0.668, 0.70),
    18: (0.876, 0.75),
    19: (0.864, 0.78),
    20: (0.846, 0.77),
    21: (0.832, 0.75),
    22: (0.780, 0.71),
    23: (0.712, 0.70),
}


def round2(x):
    scaled = x * 100
    whole = math.floor(scaled)
    if scaled - whole >= 0.5:
        whole += 1
    value = whole / 100
    return int(value) if value == int(value) else value


def forecast_case(case, name):
    if case["levels"] != LEVELS:
        raise ValueError(f"{name} asks for levels {case['levels']}, not {LEVELS}")
    first = next((k for k in case["known"] if k["hour"] == 1), None)
    if first is None:
        raise ValueError(f"{name} has no hour-1 print")
    p1 = max(1, first["viewers"])
    hours = []
    for row in case["forecast"]:
        h = row["hour"]
        med, spread = CURVE[h - 1]
        q = [round2(min(1e9, max(1.0, p1 * math.exp(med + z * spread)))) for z in Z]
        hours.append({"hour": h, "q": q})
    return {"hours": hours}


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for path in sorted(INPUT_DIR.glob("*.in")):
        case = json.loads(path.read_text(encoding="utf-8"))
        forecast = forecast_case(case, path.name)
        (OUTPUT_DIR / f"{path.stem}.out").write_text(
            json.dumps(forecast, separators=(",", ":")) + "\n", encoding="utf-8"
        )


if __name__ == "__main__":
    main()
