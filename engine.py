"""tiny-chess-01 entry: compact alpha-beta engine, packed to under 4096 bytes."""
import json, os, urllib.request

ENV = os.environ["MAKEFUN_ENV_URL"]

KNIGHT = [-21, -19, -12, -8, 8, 12, 19, 21]
KING = [-11, -10, -9, -1, 1, 9, 10, 11]
BISHOP = [-11, -9, 9, 11]
ROOK = [-10, -1, 1, 10]
QUEEN = ROOK + BISHOP

def sq64(pos120):
    r = (pos120 - 21) // 10
    f = (pos120 - 21) % 10
    return r * 8 + f


def parse_fen(fen):
    b = [' '] * 120
    for r in range(2, 10):
        for f in range(1, 9):
            b[r*10+f] = '.'
    board, turn, cast, ep, half, full = fen.split()
    rows = board.split('/')
    for i, row in enumerate(rows):  # rows[0] = rank 8
        f = 1
        for ch in row:
            if ch.isdigit():
                for k in range(int(ch)):
                    b[(2+i)*10+f] = '.'
                    f += 1
            else:
                b[(2+i)*10+f] = ch
                f += 1
    ep120 = -1
    if ep != '-':
        f = ord(ep[0]) - 97
        rk = int(ep[1])
        ep120 = 21 + (8 - rk) * 10 + f
    cr = ('K' in cast) + 2 * ('Q' in cast) + 4 * ('k' in cast) + 8 * ('q' in cast)
    return b, (turn == 'w'), cr, ep120, int(half)

T = "abcdefgh"
T2 = "87654321"
VAL = {'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 0}

def _D(s):
    return [[int(s[r*16+f*2:r*16+f*2+2], 36) - 60 for f in range(8)] for r in range(8)]
TABLES = {'P': _D('3c3c3c3c3c3c3c3c4q4q4q4q4q4q4q4q3m3m3w46463w3m3m3h3h3m41413m3h3h3c3c3c3w3w3c3c3c3h37323c3c32373h3h3m3m2s2s3m3m3h3c3c3c3c3c3c3c3c'), 'N': _D('1y282i2i2i2i281y282s3c3c3c3c2s282i3c3m3r3r3m3c2i2i3h3r3w3w3r3h2i2i3c3r3w3w3r3c2i2i3h3r3w3w3r3h2i282s3c3h3h3c2s281y282i2i2i2i281y'), 'B': _D('2s3232323232322s323c3c3c3c3c3c32323c3h3m3m3h3c32323h3h3m3m3h3h32323c3m3m3m3m3c32323m3m3m3m3m3m32323h3c3c3c3c3h322s3232323232322s'), 'R': _D('3c3c3c3c3c3c3c3c3h3m3m3m3m3m3m3h373c3c3c3c3c3c37373c3c3c3c3c3c37373c3c3c3c3c3c37373c3c3c3c3c3c37373c3c3c3c3c3c373c3c3c3h3h3c3c3c'), 'Q': _D('2s3232373732322s323c3c3c3c3c3c32323c3h3h3h3h3c32373c3h3h3h3h3c373c3c3h3h3h3h3c37323h3h3h3h3h3c32323c3h3c3c3c3c322s3232373732322s'), 'K': _D('2i28281y1y28282i2i28281y1y28282i2i28281y1y28282i2i28281y1y28282i2s2i2i28282i2i2s322s2s2s2s2s2s323w3w3c3c3c3c3w3w3w463m3c3c3m463w'), 'KE': _D('1y282i2s2s2i281y2i2s323c3c322s2i2i323w46463w322i2i32464g4g46322i2i32464g4g46322i2i323w46463w322i2i2i3c3c3c3c2i2i1y2i2i2i2i2i2i1y')}


def pst_val(b, p, white, endgame):
    ch = b[p].upper()
    q = sq64(p)
    if not white:
        r, f = divmod(q, 8)
        q = (7 - r) * 8 + f
    t = TABLES['KE'] if (ch == 'K' and endgame) else TABLES[ch]
    return t[q // 8][q % 8]

MATE = 100000

def attacked(b, p, w):
    P = 'P' if w else 'p'
    N = 'N' if w else 'n'
    K = 'K' if w else 'k'
    for d in ((9, 11) if w else (-9, -11)):
        if b[p + d] == P:
            return True
    for d in KNIGHT:
        if b[p + d] == N:
            return True
    for d in KING:
        if b[p + d] == K:
            return True
    BQ = ('B', 'Q') if w else ('b', 'q')
    RQ = ('R', 'Q') if w else ('r', 'q')
    for dirs, pcs in ((BISHOP, BQ), (ROOK, RQ)):
        for d in dirs:
            q = p + d
            while b[q] == '.':
                q += d
            if b[q] in pcs:
                return True
    return False

def king_pos(b, white):
    return b.index('K' if white else 'k')

def gen_moves(b, white, cr, ep):
    moves = []  # (frm,to,promo,flag) flag: 0 normal,1 ep,2 castle,3 double
    own = str.isupper if white else str.islower
    enemy = str.islower if white else str.isupper
    for p in range(21, 99):
        c = b[p]
        if c == '.' or c == ' ' or (not own(c)):
            continue
        u = c.upper()
        if u == 'P':
            fwd = -10 if white else 10
            start_row = 8 if white else 3
            promo_row = 2 if white else 9
            one = p + fwd
            if b[one] == '.':
                if (one // 10) == promo_row:
                    for pr in ('q', 'r', 'b', 'n'):
                        moves.append((p, one, pr, 0))
                else:
                    moves.append((p, one, None, 0))
                    if (p // 10) == start_row:
                        two = one + fwd
                        if b[two] == '.':
                            moves.append((p, two, None, 3))
            for d in (fwd - 1, fwd + 1):
                q = p + d
                if enemy(b[q]) and b[q] != '.' and b[q] != ' ':
                    if (q // 10) == promo_row:
                        for pr in ('q', 'r', 'b', 'n'):
                            moves.append((p, q, pr, 0))
                    else:
                        moves.append((p, q, None, 0))
                if q == ep and ep > 0:
                    moves.append((p, q, None, 1))
        elif u == 'N':
            for d in KNIGHT:
                q = p + d
                if b[q] == '.' or enemy(b[q]):
                    moves.append((p, q, None, 0))
        elif u == 'K':
            for d in KING:
                q = p + d
                if b[q] == '.' or enemy(b[q]):
                    moves.append((p, q, None, 0))
            if white and p == 95:
                if cr & 1 and b[96] == '.' and b[97] == '.' and b[98] == 'R':
                    if not attacked(b, 95, False) and not attacked(b, 96, False) and not attacked(b, 97, False):
                        moves.append((95, 97, None, 2))
                if cr & 2 and b[94] == '.' and b[93] == '.' and b[92] == '.' and b[91] == 'R':
                    if not attacked(b, 95, False) and not attacked(b, 94, False) and not attacked(b, 93, False):
                        moves.append((95, 93, None, 2))
            if not white and p == 25:
                if cr & 4 and b[26] == '.' and b[27] == '.' and b[28] == 'r':
                    if not attacked(b, 25, True) and not attacked(b, 26, True) and not attacked(b, 27, True):
                        moves.append((25, 27, None, 2))
                if cr & 8 and b[24] == '.' and b[23] == '.' and b[22] == '.' and b[21] == 'r':
                    if not attacked(b, 25, True) and not attacked(b, 24, True) and not attacked(b, 23, True):
                        moves.append((25, 23, None, 2))
        else:
            dirs = QUEEN if u == 'Q' else (BISHOP if u == 'B' else ROOK)
            for d in dirs:
                q = p + d
                while b[q] == '.' or enemy(b[q]):
                    moves.append((p, q, None, 0))
                    if b[q] != '.':
                        break
                    q += d
    return moves

def make(b, m, cr, ep, half):
    frm, to, promo, flag = m
    piece = b[frm]
    cap = b[to]
    newcr = cr
    newep = -1
    nhalf = half + 1
    if cap != '.':
        nhalf = 0
    b[to] = piece
    b[frm] = '.'
    if flag == 1:  # ep capture
        cap = 'p' if piece == 'P' else 'P'
        b[to + (10 if piece == 'P' else -10)] = '.'
        nhalf = 0
    if flag == 3:
        newep = frm + (10 if piece == 'P' else -10)
    if promo:
        b[to] = promo.upper() if piece.isupper() else promo
    if flag == 2:
        if to == 97: b[96] = 'R'; b[98] = '.'
        elif to == 93: b[94] = 'R'; b[91] = '.'
        elif to == 27: b[26] = 'r'; b[28] = '.'
        elif to == 23: b[24] = 'r'; b[21] = '.'
    if piece == 'K':
        newcr &= ~3
    if piece == 'k':
        newcr &= ~12
    if frm == 98 or to == 98: newcr &= ~1
    if frm == 91 or to == 91: newcr &= ~2
    if frm == 28 or to == 28: newcr &= ~4
    if frm == 21 or to == 21: newcr &= ~8
    if piece.upper() == 'P':
        nhalf = 0
    return cap, newcr, newep, nhalf

def unmake(b, m, cap):
    frm, to, promo, flag = m
    piece = b[to]
    b[frm] = piece
    b[to] = cap if cap != '.' else '.'
    if flag == 1:
        b[to] = '.'
        b[to + (10 if piece == 'P' else -10)] = 'p' if piece == 'P' else 'P'
    if flag == 2:
        if to == 97: b[96] = '.'; b[98] = 'R'; b[frm] = 'K'
        elif to == 93: b[94] = '.'; b[91] = 'R'; b[frm] = 'K'
        elif to == 27: b[26] = '.'; b[28] = 'r'; b[frm] = 'k'
        elif to == 23: b[24] = '.'; b[21] = 'r'; b[frm] = 'k'
    if promo:
        b[frm] = 'P' if piece.isupper() else 'p'

def eval_board(b):
    wm = bm = 0
    wmats = bmats = 0
    for p in range(21, 99):
        c = b[p]
        if c == '.' or c == ' ':
            continue
        u = c.upper()
        if c.isupper():
            wm += VAL[u]
            wmats += pst_val(b, p, True, False)
        else:
            bm += VAL[u]
            bmats += pst_val(b, p, False, False)
    endgame = (wm + bm) < 2400
    if endgame:
        wmats = bmats = 0
        for p in range(21, 99):
            c = b[p]
            if c == '.' or c == ' ':
                continue
            u = c.upper()
            if c.isupper():
                wmats += pst_val(b, p, True, True)
            else:
                bmats += pst_val(b, p, False, True)

    return (wm - bm) + (wmats - bmats)

def search(b, white, depth, cr, ep, half, alpha, beta, ply):
    chk()
    key = (''.join(b), white, cr, ep)
    if key in PATH:
        return 0
    if half >= 100:
        return 0
    in_check = attacked(b, king_pos(b, white), not white)
    if in_check:
        depth += 1
    if depth <= 0:
        return quiesce(b, white, alpha, beta, ply)
    e = TT.get(key)
    hmove = e[1] if e is not None else None
    k1, k2 = KILL.get(ply, (None, None))
    def score_move(m):
        frm, to, promo, flag = m
        s = 0
        if b[to] != '.':
            s += 100000 + 10 * VAL[b[to].upper()] - VAL[b[frm].upper()]
        if flag == 1:
            s += 100000 + 100
        if promo:
            s += 90000 + VAL[promo.upper()]
        if m == hmove:
            s += 200000
        elif m == k1:
            s += 8000
        elif m == k2:
            s += 7000
        else:
            s += HIST.get((frm, to, flag), 0)
        return s
    moves = gen_moves(b, white, cr, ep)
    moves.sort(key=score_move, reverse=True)
    best = -MATE * 2
    bestm = None
    any_legal = False
    a0 = alpha
    PATH.append(key)
    kp = king_pos(b, white)
    for i, m in enumerate(moves):
        quiet = b[m[1]] == '.' and m[3] == 0 and not m[2]
        cap, ncr, nep, nh = make(b, m, cr, ep, half)
        kq = king_pos(b, white) if m[0] == kp else kp
        if attacked(b, kq, not white):
            unmake(b, m, cap)
            chk()
            continue
        any_legal = True
        chk()
        if i == 0 or not quiet or in_check or depth < 3:
            sc = -search(b, not white, depth - 1, ncr, nep, nh, -beta, -alpha, ply + 1)
        else:
            red = 0
            sc = -search(b, not white, depth - 1 - red, ncr, nep, nh, -alpha - 1, -alpha, ply + 1)
            if sc > alpha:
                sc = -search(b, not white, depth - 1, ncr, nep, nh, -beta, -alpha, ply + 1)
        unmake(b, m, cap)
        if sc > best:
            best = sc
            bestm = m
        if sc > alpha:
            alpha = sc
        if alpha >= beta:
            if quiet:
                KILL[ply] = (m, k1)
                hk = (m[0], m[1], 0)
                HIST[hk] = HIST.get(hk, 0) + depth * depth
            break
    PATH.pop()
    if not any_legal:
        return -(MATE - ply) if in_check else 0
    if bestm is not None and (e is None or e[0] < depth):
        TT[key] = (depth, bestm)
    return best

def quiesce(b, white, alpha, beta, ply):
    chk()
    stand = eval_board(b) if white else -eval_board(b)
    best = stand
    if stand > alpha:
        alpha = stand
    if ply > 32 or stand >= beta:
        return best
    moves = gen_moves(b, white, -1, -1)
    caps = [m for m in moves if b[m[1]] != '.' or m[3] == 1 or m[2]]
    def score_move(m):
        frm, to, promo, flag = m
        s = 0
        if b[to] != '.':
            s += 1000 + VAL[b[to].upper()] - VAL[b[frm].upper()]
        if flag == 1:
            s += 1100
        if promo:
            s += 900
        return s
    caps.sort(key=score_move, reverse=True)
    kp = king_pos(b, white)
    for m in caps:
        cap, ncr, nep, nh = make(b, m, 0, -1, 0)
        kq = king_pos(b, white) if m[0] == kp else kp
        if attacked(b, kq, not white):
            unmake(b, m, cap)
            chk()
            continue
        chk()
        sc = -quiesce(b, not white, -beta, -alpha, ply + 1)
        unmake(b, m, cap)
        if sc > best:
            best = sc
        if sc > alpha:
            alpha = sc
        if alpha >= beta:
            break
    return best

class Budget(Exception):
    pass

NODE_BUDGET = int(os.environ.get("TC_NODES", "300000"))
NODES = [0]
TT = {}
KILL = {}
HIST = {}
PATH = []

def chk():
    NODES[0] += 1
    if NODES[0] > NODE_BUDGET:
        raise Budget()

def best_move(fen, white):
    NODES[0] = 0
    b, w, cr, ep, half = parse_fen(fen)
    best = None
    root_moves = []
    try:
        root_moves = []
        for m in gen_moves(b, w, cr, ep):
            cap, ncr, nep, nh = make(b, m, cr, ep, half)
            ok = not attacked(b, king_pos(b, w), not w)
            unmake(b, m, cap)
            if ok:
                root_moves.append(m)
        if not root_moves:
            return None
        for d in range(1, 8):
            alpha = -MATE * 2
            scored = []
            for m in root_moves:
                cap, ncr, nep, nh = make(b, m, cr, ep, half)
                sc = -search(b, not w, d - 1, ncr, nep, nh, -MATE * 2, MATE * 2, 1)
                unmake(b, m, cap)
                scored.append((sc, m))
                if sc > alpha:
                    alpha = sc
            scored.sort(key=lambda t: -t[0])
            root_moves = [mm for _, mm in scored]
            best = scored[0][1]
            if abs(scored[0][0]) > MATE - 100:
                break
    except Budget:
        PATH.clear()
        if best is None and root_moves:
            best = root_moves[0]
    if best is None:
        return None
    frm, to, promo, flag = best
    a, c = sq64(frm), sq64(to)
    return T[a % 8] + T2[a // 8] + T[c % 8] + T2[c // 8] + (promo or "")

def post(path, obj):
    return json.load(urllib.request.urlopen(urllib.request.Request(ENV + path, data=json.dumps(obj).encode(), headers={"Content-Type": "application/json"}), timeout=30))

def main():
    while True:
        g = post("/game", {})
        if g["status"] == "done":
            return
        if g["status"] == "over":
            continue
        fen = g["fen"]
        legal = set(g["legal_moves"])
        uci = best_move(fen, g["colour"] == "white")
        if uci is None or uci not in legal:
            uci = sorted(legal)[0]
        post("/move", {"game": g["game"], "move": uci})

if len(__name__) > 7:
    main()
