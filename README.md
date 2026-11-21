# tiny-chess-01-entry

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/zrm4/tiny-chess-01-entry/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/zrm4/tiny-chess-01-entry/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in **4,039 bytes of Python** — under the 4,096-byte cap, with the search
shipped as an lzma-packed self-unpacking payload (the rules explicitly allow compressed
payloads; both count toward the cap).

## What is inside

- 10x12 board, full legal move generation (castling, en passant, promotions)
- Iterative-deepening alpha-beta search (PVS re-search, check extension, quiescence over
  captures and promotions), killers, history, transposition table
- Material + piece-square evaluation, repetition and fifty-move scoring inside the search
- Node budget from `TC_NODES` (default 300,000) — never a wall clock, so replays are
  byte-identical; practice runs at 250,000 nodes keep the slowest move under ~3.2 s
  against the 10 s limit

## Practice result

Scored against the kit's practice trial gauntlet (Elo anchored to the house engines:
depth-2 855, depth-3 1073, depth-4 1199, nodes-100k 1392, nodes-250k 1497,
nodes-500k 1596): **1 W, 3 D, 2 L ≈ 1191 Elo** at 250,000 nodes a move.

## Run it

```sh
python3 main.py
```

The engine talks to the make.fun env: it reads `MAKEFUN_ENV_URL`, asks for the game in
play (`POST /game`), answers with its move in UCI (`POST /move`) until the trial is done.

---

<sub>Entered on [make.fun](https://make.fun/?ref=th82f1sy&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
