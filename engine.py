import os, json, urllib.request as U
SQ = [21 + 10 * r + f for r in range(8) for f in range(8)]
ND = (21, 19, 12, 8, -8, -12, -19, -21)
KD = (10, -10, 1, -1, 11, 9, -9, -11)
BD = (11, 9, -9, -11)
RD = (10, -10, 1, -1)
DR = {'B': BD, 'R': RD, 'Q': KD, 'b': BD, 'r': RD, 'q': KD}
V = {'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 0}
A = {}
M = {}
for c in 'PNBRQKpnbrqk':
 A[c] = V[c.upper()]
 M[c] = 10 * A[c]
MT = 100000
P = {
'P': (0,0,0,0,0,0,0,0, 50,50,50,50,50,50,50,50, 10,10,20,30,30,20,10,10,
 5,5,10,25,25,10,5,5, 0,0,0,20,20,0,0,0, 5,-5,-10,0,0,-10,-5,5,
 5,10,10,-20,-20,10,10,5, 0,0,0,0,0,0,0,0),
'N': (-50,-40,-30,-30,-30,-30,-40,-50, -40,-20,0,0,0,0,-20,-40,
 -30,0,10,15,15,10,0,-30, -30,5,15,20,20,15,5,-30,
 -30,0,15,20,20,15,0,-30, -30,5,10,15,15,10,5,-30,
 -40,-20,0,5,5,0,-20,-40, -50,-40,-30,-30,-30,-30,-40,-50),
'B': (-20,-10,-10,-10,-10,-10,-10,-20, -10,0,0,0,0,0,0,-10,
 -10,0,5,10,10,5,0,-10, -10,5,5,10,10,5,5,-10,
 -10,0,10,10,10,10,0,-10, -10,10,10,10,10,10,10,-10,
 -10,5,0,0,0,0,5,-10, -20,-10,-10,-10,-10,-10,-10,-20),
'R': (0,0,0,0,0,0,0,0, 5,10,10,10,10,10,10,5, -5,0,0,0,0,0,0,-5,
 -5,0,0,0,0,0,0,-5, -5,0,0,0,0,0,0,-5, -5,0,0,0,0,0,0,-5,
 -5,0,0,0,0,0,0,-5, 0,0,0,5,5,0,0,0),
'Q': (-20,-10,-10,-5,-5,-10,-10,-20, -10,0,0,0,0,0,0,-10,
 -10,0,5,5,5,5,0,-10, -5,0,5,5,5,5,0,-5, 0,0,5,5,5,5,0,-5,
 -10,5,5,5,5,5,0,-10, -10,0,5,0,0,0,0,-10, -20,-10,-10,-5,-5,-10,-10,-20),
'K': (20,30,10,0,0,10,30,20, 20,20,0,0,0,0,20,20,
 -10,-20,-20,-20,-20,-20,-20,-10, -20,-30,-30,-40,-40,-30,-30,-20,
 -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30,
 -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30),
'E': (-50,-40,-30,-20,-20,-30,-40,-50, -30,-20,-10,0,0,-10,-20,-30,
 -30,-10,20,30,30,20,-10,-30, -30,-10,30,40,40,30,-10,-30,
 -30,-10,30,40,40,30,-10,-30, -30,-10,20,30,30,20,-10,-30,
 -30,-30,0,0,0,0,-30,-30, -50,-30,-30,-30,-30,-30,-30,-50)}
T = {}
NP = {}
KM = ([0] * 120, [0] * 120)
KE = ([0] * 120, [0] * 120)
AW = [()] * 120
AB = [()] * 120
SW = [()] * 120
SB = [()] * 120
for t in 'PNBRQ':
 tw = [0] * 120
 tb = [0] * 120
 for sq in SQ:
  r, f = (sq - 21) // 10, (sq - 21) % 10
  tw[sq] = V[t] + P[t][(7 - r) * 8 + f]
  tb[sq] = -V[t] - P[t][r * 8 + f]
 T[t] = tw
 T[t.lower()] = tb
 NP[t] = NP[t.lower()] = V[t]
NP['P'] = NP['p'] = NP['K'] = NP['k'] = 0
T['K'] = T['k'] = [0] * 120
for sq in SQ:
 r, f = (sq - 21) // 10, (sq - 21) % 10
 KM[0][sq] = P['K'][(7 - r) * 8 + f]
 KM[1][sq] = -P['K'][r * 8 + f]
 KE[0][sq] = P['E'][(7 - r) * 8 + f]
 KE[1][sq] = -P['E'][r * 8 + f]
 AW[sq] = tuple(t for t in SQ if t > sq + 2 and abs(t % 10 - sq % 10) < 2)
 AB[sq] = tuple(t for t in SQ if t < sq - 2 and abs(t % 10 - sq % 10) < 2)
 SW[sq] = tuple(t for t in SQ if 2 < t - sq < 23 and abs(t % 10 - sq % 10) < 2)
 SB[sq] = tuple(t for t in SQ if -23 < t - sq < -2 and abs(t % 10 - sq % 10) < 2)
PA = (0, 5, 10, 20, 35, 60, 100, 0)
KP = {21: 'Q', 28: 'K', 91: 'q', 98: 'k'}

def us(s):
 return ord(s[0]) - 97 + 21 + 10 * (int(s[1]) - 1)

def su(i):
 return chr(97 + (i - 21) % 10) + str((i - 21) // 10 + 1)

def mu(m):
 return su(m[0]) + su(m[1]) + m[2].lower()

def parse(fen):
 f = fen.split()
 b = [' '] * 120
 sq = 91
 for ch in f[0]:
  if ch == '/':
   sq -= 18
  elif ch.isdigit():
   for _ in range(int(ch)):
    b[sq] = '.'
    sq += 1
  else:
   b[sq] = ch
   sq += 1
 st = [b, f[1] == 'w', '' if f[2] == '-' else f[2],
  0 if f[3] == '-' else us(f[3]), int(f[4]) if len(f) > 4 else 0,
  b.index('K'), b.index('k'), 0, 0, 0, 0]
 for sq in SQ:
  pc = b[sq]
  if pc not in '.Kk':
   st[7] += T[pc][sq]
   st[8] += NP[pc]
   st[9] += pc == 'B'
   st[10] += pc == 'b'
 return st

def key(st):
 ep = st[3]
 if ep:
  p, d = ('P', 9) if st[1] else ('p', -9)
  if st[0][ep - d] != p and st[0][ep - d - 2] != p:
   ep = 0
 return (''.join(st[0]), st[1], st[2], ep)

def attacked(b, sq, w):
 if w:
  if b[sq - 9] == 'P' or b[sq - 11] == 'P':
   return True
  n, k, bq, rq = 'N', 'K', 'BQ', 'RQ'
 else:
  if b[sq + 9] == 'p' or b[sq + 11] == 'p':
   return True
  n, k, bq, rq = 'n', 'k', 'bq', 'rq'
 for d in ND:
  if b[sq + d] == n:
   return True
 for d in KD:
  if b[sq + d] == k:
   return True
 for ds, pcs in ((BD, bq), (RD, rq)):
  for d in ds:
   t = sq + d
   while b[t] == '.':
    t += d
   if b[t] in pcs:
    return True
 return False

def gen(st, caps=False):
 b, w, ca, ep = st[0], st[1], st[2], st[3]
 mine = 'PNBRQK' if w else 'pnbrqk'
 foes = mine.swapcase()
 promos = 'QRBN' if w else 'qrbn'
 out = []
 for fr in SQ:
  pc = b[fr]
  if pc not in mine:
   continue
  if pc in 'Pp':
   d = 10 if w else -10
   to = fr + d
   last = to >= 91 if w else to <= 28
   if b[to] == '.':
    if last:
     for pr in promos:
      out.append((fr, to, pr, 0))
    elif not caps:
     out.append((fr, to, '', 0))
     if (31 <= fr <= 38 if w else 81 <= fr <= 88) and b[fr + 2 * d] == '.':
      out.append((fr, fr + 2 * d, '', 1))
   for dd in (d - 1, d + 1):
    to = fr + dd
    tc = b[to]
    if tc in foes:
     if last:
      for pr in promos:
       out.append((fr, to, pr, 0))
     else:
      out.append((fr, to, '', 0))
    elif ep and to == ep:
     out.append((fr, to, '', 2))
  elif pc in 'NnKk':
   for d in ND if pc in 'Nn' else KD:
    to = fr + d
    tc = b[to]
    if tc == '.':
     if not caps:
      out.append((fr, to, '', 0))
    elif tc in foes:
     out.append((fr, to, '', 0))
   if pc in 'Kk' and not caps and fr == (25 if w else 95) and not attacked(b, fr, not w):
    for sg, rch, n in ((1, 'K' if w else 'k', 2), (-1, 'Q' if w else 'q', 3)):
     if rch in ca and b[fr + sg * (n + 1)] == ('R' if w else 'r') \
       and all(b[fr + sg * i] == '.' for i in range(1, n + 1)) \
       and not any(attacked(b, fr + sg * i, not w) for i in range(1, n)):
      out.append((fr, fr + sg * 2, '', 3))
  else:
   for d in DR[pc]:
    to = fr + d
    while b[to] == '.':
     if not caps:
      out.append((fr, to, '', 0))
     to += d
    if b[to] in foes:
     out.append((fr, to, '', 0))
 return out

def make(st, m):
 fr, to, pr, fl = m
 b, w = st[0], st[1]
 pc = b[fr]
 cs = (to - 10 if w else to + 10) if fl == 2 else to
 cap = b[cs]
 u = (m, cs, cap, st[2], st[3], st[4], st[5], st[6], st[7], st[8], st[9], st[10])
 pl = pr if pr else pc
 b[cs] = '.'
 b[fr] = '.'
 b[to] = pl
 st[7] += T[pl][to] - T[pc][fr]
 st[8] += NP[pl] - NP[pc]
 if cap != '.':
  st[7] -= T[cap][cs]
  st[8] -= NP[cap]
 st[9] += (pl == 'B') - (pc == 'B') - (cap == 'B')
 st[10] += (pl == 'b') - (pc == 'b') - (cap == 'b')
 if pc == 'K':
  st[5] = to
 elif pc == 'k':
  st[6] = to
 if fl == 3:
  rf, rt = (fr + 3, fr + 1) if to > fr else (fr - 4, fr - 1)
  rk = b[rf]
  b[rt] = rk
  b[rf] = '.'
  st[7] += T[rk][rt] - T[rk][rf]
 ca = st[2]
 if pc == 'K':
  ca = ca.replace('K', '').replace('Q', '')
 elif pc == 'k':
  ca = ca.replace('k', '').replace('q', '')
 for q in (fr, to):
  if q in KP:
   ca = ca.replace(KP[q], '')
 st[2] = ca
 st[3] = (fr + to) // 2 if fl == 1 else 0
 st[4] = 0 if pc in 'Pp' or cap != '.' else st[4] + 1
 st[1] = not w
 return u

def unmake(st, u):
 m, cs, cap, ca, ep, hm, kw, kb, ps, nm, bw, bb = u
 fr, to, pr, fl = m
 b = st[0]
 st[1] = not st[1]
 pc = b[to]
 b[fr] = ('P' if pc.isupper() else 'p') if pr else pc
 b[to] = '.'
 b[cs] = cap
 if fl == 3:
  rf, rt = (fr + 3, fr + 1) if to > fr else (fr - 4, fr - 1)
  b[rf] = b[rt]
  b[rt] = '.'
 st[2], st[3], st[4], st[5], st[6] = ca, ep, hm, kw, kb
 st[7], st[8], st[9], st[10] = ps, nm, bw, bb

def ev(st):
 b = st[0]
 s = st[7]
 if st[9] > 1:
  s += 30
 if st[10] > 1:
  s -= 30
 if st[8] < 2400:
  s += KE[0][st[5]] + KE[1][st[6]]
  for sq in SQ:
   pc = b[sq]
   if pc == 'P':
    for t in AW[sq]:
     if b[t] == 'p':
      break
    else:
     s += PA[(sq - 21) // 10]
   elif pc == 'p':
    for t in AB[sq]:
     if b[t] == 'P':
      break
    else:
     s -= PA[7 - (sq - 21) // 10]
 else:
  s += KM[0][st[5]] + KM[1][st[6]]
  for t in SW[st[5]]:
   if b[t] == 'P':
    s += 8
  for t in SB[st[6]]:
   if b[t] == 'p':
    s -= 8
 return s if st[1] else -s

class Stop(Exception):
 pass

TT = {}

def um(st, u):
 fr, to = us(u[:2]), us(u[2:4])
 pr = u[4:].upper() if st[1] else u[4:]
 pc = st[0][fr]
 fl = 0
 if pc in 'Pp':
  if st[3] and to == st[3] and st[0][to] == '.':
   fl = 2
  elif abs(to - fr) == 20:
   fl = 1
 elif pc in 'Kk' and abs(to - fr) == 2:
  fl = 3
 return (fr, to, pr, fl)

def search(st, bg, pt, cn, rm):
 nc = 0
 kl = [[None, None] for _ in range(64)]
 hs = {}

 def push():
  k = key(st)
  pt.append(k)
  cn[k] = cn.get(k, 0) + 1

 def pop():
  k = pt.pop()
  cn[k] -= 1

 def order(ms, p, tm):
  b = st[0]
  k0, k1 = kl[p]

  def sc(m):
   fr, to, pr, fl = m
   if m == tm:
    return 10 ** 9
   s = 0
   cap = b[to]
   if cap != '.':
    s = 100000 + M[cap] - A[b[fr]]
   elif fl == 2:
    s = 101000
   if pr:
    s += 90000 + A[pr]
   if s == 0:
    if m == k0:
     s = 50000
    elif m == k1:
     s = 40000
    else:
     s = hs.get((fr, to), 0)
   return s
  ms.sort(key=sc, reverse=True)

 def q(a, b, p, ck):
  nonlocal nc
  nc += 1
  if nc > bg:
   raise Stop
  bt = -MT - 1
  sd = 0
  if not ck:
   sd = ev(st)
   bt = sd
   if bt >= b:
    return bt
   if bt > a:
    a = bt
  if p >= 60:
   return bt if not ck else ev(st)
  ms = gen(st, not ck)
  order(ms, p, None)
  n = 0
  for m in ms:
   if not ck and not m[2]:
    gn = 100 if m[3] == 2 else A[st[0][m[1]]]
    if sd + gn + 200 < a:
     continue
   u = make(st, m)
   kg = st[6] if st[1] else st[5]
   if attacked(st[0], kg, st[1]):
    unmake(st, u)
    continue
   n += 1
   s = -q(-b, -a, p + 1, False)
   unmake(st, u)
   if s > bt:
    bt = s
   if s >= b:
    return s
   if s > a:
    a = s
  if ck and n == 0:
   return -MT + p
  return bt

 def ab(d, a, b, p):
  nonlocal nc
  nc += 1
  if nc > bg:
   raise Stop
  if st[4] >= 100:
   return 0
  ky = key(st)
  if cn.get(ky, 0) > 1:
   return 0
  kg = st[5] if st[1] else st[6]
  ck = attacked(st[0], kg, not st[1])
  if ck:
   d += 1
  if d <= 0 or p >= 60:
   return q(a, b, p, ck)
  ent = TT.get(ky)
  tm = None
  if ent:
   ed, ef, es, tm = ent
   es = es - p if es > MT - 64 else es + p if es < -MT + 64 else es
   if ed >= d and (ef == 0 or (ef == 1 and es >= b) or (ef == 2 and es <= a)):
    return es
  a0 = a
  ms = gen(st)
  order(ms, p, tm)
  bt = -MT - 1
  bm = None
  n = 0
  for m in ms:
   u = make(st, m)
   kg = st[6] if st[1] else st[5]
   if attacked(st[0], kg, st[1]):
    unmake(st, u)
    continue
   n += 1
   push()
   s = -ab(d - 1, -b, -a, p + 1)
   pop()
   unmake(st, u)
   if s > bt:
    bt = s
    bm = m
   if s > a:
    a = s
   if a >= b:
    if st[0][m[1]] == '.' and not m[2] and m[3] != 2:
     if kl[p][0] != m:
      kl[p][1] = kl[p][0]
      kl[p][0] = m
     hs[(m[0], m[1])] = hs.get((m[0], m[1]), 0) + d * d
    break
  if n == 0:
   return -MT + p if ck else 0
  sv = bt + p if bt > MT - 64 else bt - p if bt < -MT + 64 else bt
  ef = 2 if bt <= a0 else 1 if bt >= b else 0
  if len(TT) > 65536:
   TT.clear()
  TT[ky] = (d, ef, sv, bm)
  return bt

 if not rm:
  return None
 if len(rm) == 1:
  return rm[0]
 save = [st[0][:]] + st[1:]
 plen = len(pt)
 ss = {}
 bt = rm[0]
 pv = 0

 def root(d, a, b):
  bs = -MT - 1
  bm = None
  for m in sorted(rm, key=lambda m: -ss.get(m, 0)):
   u = make(st, m)
   push()
   s = -ab(d - 1, -b, -a, 1)
   pop()
   unmake(st, u)
   ss[m] = s
   if s > bs:
    bs = s
    bm = m
   if s > a:
    a = s
  return bs, bm

 for d in range(1, 7):
  try:
   w = 50 if d >= 3 else MT + 1
   bs, bm = root(d, pv - w, pv + w)
   if d >= 3 and (bs <= pv - w or bs >= pv + w):
    bs, bm = root(d, -MT - 1, MT + 1)
  except Stop:
   st[0][:] = save[0]
   st[1:] = save[1:]
   while len(pt) > plen:
    pop()
   break
  bt = bm
  pv = bs
  if bs >= MT - 64:
   break
 return bt

def post(url, obj):
 req = U.Request(url, json.dumps(obj).encode(),
  {'Content-Type': 'application/json'})
 with U.urlopen(req, timeout=60) as r:
  return json.load(r)

def choose(g, bg):
 lu = g['legal_moves']
 st = parse(g['fen'])
 try:
  rm = [um(st, u) for u in lu]
  h = parse(g['start_fen'])
  pt = []
  cn = {}

  def add():
   k = key(h)
   pt.append(k)
   cn[k] = cn.get(k, 0) + 1

  add()
  for u in g['moves']:
   make(h, um(h, u))
   add()
  ky = key(st)
  if pt[-1][:3] == ky[:3]:
   if pt[-1] != ky:
    cn[pt[-1]] -= 1
    pt[-1] = ky
    cn[ky] = cn.get(ky, 0) + 1
  else:
   pt = [ky]
   cn = {ky: 1}
  m = search(st, bg, pt, cn, rm)
  u = mu(m) if m else None
  if u in lu:
   return u
 except Exception:
  pass
 return sorted(lu)[0]

def main():
 env = os.environ['MAKEFUN_ENV_URL']
 bg = int(os.environ.get('TC_NODES', '300000'))
 while True:
  g = post(env + '/game', {})
  if g.get('status') == 'done':
   print(json.dumps(g), flush=True)
   break
  if g.get('status') not in ('your_move', 'playing', 'over'):
   break
  while g.get('status') in ('your_move', 'playing'):
   mv = choose(g, bg)
   g = post(env + '/move', {'game': g['game'], 'move': mv})
  print('game', g.get('game'), g.get('opponent'), g.get('outcome'),
   g.get('reason'), 'plies', g.get('plies'), flush=True)

if __name__ == '__main__':
 main()