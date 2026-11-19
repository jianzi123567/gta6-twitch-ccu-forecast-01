# Forecast GTA VI's launch-day Twitch viewers hour by hour (gta6-twitch-ccu-forecast-01)

[![make.fun · gta6-twitch-ccu-forecast-01](https://make.fun/badge/gta6-twitch-ccu-forecast-01.svg)](https://make.fun/bounty/gta6-twitch-ccu-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01)
[![rank](https://make.fun/badge/gta6-twitch-ccu-forecast-01/jianzi123567/gta6-twitch-ccu-forecast-01/rank.svg)](https://make.fun/bounty/gta6-twitch-ccu-forecast-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01)
[![reward](https://make.fun/badge/gta6-twitch-ccu-forecast-01/jianzi123567/gta6-twitch-ccu-forecast-01/reward.svg)](https://make.fun/bounty/gta6-twitch-ccu-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01)

Forecast how many people watch Grand Theft Auto VI live on Twitch in each
hour of its release day (2026-11-19 UTC), for the make.fun bounty
**gta6-twitch-ccu-forecast-01** ($250, 20 places paid).

## The model

A diurnal shape fitted on 19 comparable big launches' release days
(SullyGnome hourly Twitch category averages, bundled as comparables in the
kit's practice cases): for each launch, the log ratio of each UTC hour's
viewers to the 00:00 UTC hour's viewers. The median curve across the 19
launches is the forecast median; the residual standard deviation per hour
is the log spread. On those 19 launches this shape scores a mean pinball
loss of 0.306, against 0.410 for the house persistence baseline.

The shape: viewership dips in the small hours, rises from 05:00 UTC as the
US east coast unlocks, peaks around 18:00–19:00 UTC as US prime time
approaches, and ends the day at about twice hour 1's level.

`main.py` (Python 3.13, stdlib only) reads every `<id>.in` case in
`$MAKEFUN_INPUT_DIR` (or `/input`) and writes `<id>.out` to
`$MAKEFUN_OUTPUT_DIR` (or `/output`): 23 rows, hours 2–24, five quantiles
(5%, 25%, 50%, 75%, 95%) each. No network, no randomness — two runs write
identical bytes, in well under the 8-second limit.

## Files

- `main.py` — the forecaster
- `README.md` — this file
- `LICENSE` — MIT license
- `.makefun/owner.json` — the owner's Solana wallet
