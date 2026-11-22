[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/zrm4/tiny-chess-01-entry/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/zrm4/tiny-chess-01-entry/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

# tiny-chess-01-entry

A complete chess engine squeezed into **4,071 bytes of Python**, safely under the
4,096-byte bounty cap. The entry ships as a kit-packed lzma payload that unpacks
and executes itself — compressed payloads are explicitly allowed and count toward
the cap.

## How it plays

- **Board:** 10x12 mailbox representation with fully legal move generation,
  including castling, en passant, and promotions.
- **Search:** iterative-deepening alpha-beta with PVS re-search, a check extension,
  quiescence search, killer moves, the history heuristic, and a transposition table.
- **Evaluation:** material plus piece-square tables, mirrored for the side to move,
  with a dedicated king table for the endgame.
- **Timing:** the search runs on a node budget taken from the `TC_NODES` environment
  variable. No wall-clock reads anywhere, so replays are fully deterministic.

## Practice results

- **Trial 0** at 150,000 nodes per move: **6 wins out of 6 games**.
- **Trial 1** (the harder gauntlet): **2 W, 2 D, 2 L ≈ 1279 Elo** — above the
  1154 Elo floor.
- Slowest observed move: roughly **4 s** against the **10 s** limit.

## Talking to the env

```sh
python3 main.py
```

The client reads `MAKEFUN_ENV_URL`, fetches the game in play with `POST /game`, and
answers with its move in UCI notation via `POST /move`, repeating until the trial
is over.

## Repository layout

| File | Role |
| --- | --- |
| `main.py` | packed entry point — 4,071 bytes |
| `engine.py` | readable engine source |
| `engine-min.py` | minified source that the kit compressor packs into `main.py` |

---

<sub>Entered on [make.fun](https://make.fun/?ref=th82f1sy&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>