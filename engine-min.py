import os,json,urllib.request as U
e=[21+10*r+f for r in range(8)for f in range(8)]
j=(21,19,12,8,-8,-12,-19,-21)
l=(10,-10,1,-1,11,9,-9,-11)
o=(11,9,-9,-11)
v=(10,-10,1,-1)
x={'B':o,'R':v,'Q':l,'b':o,'r':v,'q':l}
V={'P':100,'N':320,'B':330,'R':500,'Q':900,'K':0}
A={}
M={}
for c in'PNBRQKpnbrqk':
 A[c]=V[c.upper()]
 M[c]=10*A[c]
y=100000
P={'P':(0,0,0,0,0,0,0,0,50,50,50,50,50,50,50,50,10,10,20,30,30,20,10,10,5,5,10,25,25,10,5,5,0,0,0,20,20,0,0,0,5,-5,-10,0,0,-10,-5,5,5,10,10,-20,-20,10,10,5,0,0,0,0,0,0,0,0),'N':(-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,0,0,0,-20,-40,-30,0,10,15,15,10,0,-30,-30,5,15,20,20,15,5,-30,-30,0,15,20,20,15,0,-30,-30,5,10,15,15,10,5,-30,-40,-20,0,5,5,0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50),'B':(-20,-10,-10,-10,-10,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,10,10,5,0,-10,-10,5,5,10,10,5,5,-10,-10,0,10,10,10,10,0,-10,-10,10,10,10,10,10,10,-10,-10,5,0,0,0,0,5,-10,-20,-10,-10,-10,-10,-10,-10,-20),'R':(0,0,0,0,0,0,0,0,5,10,10,10,10,10,10,5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,0,0,0,5,5,0,0,0),'Q':(-20,-10,-10,-5,-5,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,5,5,5,0,-10,-5,0,5,5,5,5,0,-5,0,0,5,5,5,5,0,-5,-10,5,5,5,5,5,0,-10,-10,0,5,0,0,0,0,-10,-20,-10,-10,-5,-5,-10,-10,-20),'K':(20,30,10,0,0,10,30,20,20,20,0,0,0,0,20,20,-10,-20,-20,-20,-20,-20,-20,-10,-20,-30,-30,-40,-40,-30,-30,-20,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30),'E':(-50,-40,-30,-20,-20,-30,-40,-50,-30,-20,-10,0,0,-10,-20,-30,-30,-10,20,30,30,20,-10,-30,-30,-10,30,40,40,30,-10,-30,-30,-10,30,40,40,30,-10,-30,-30,-10,20,30,30,20,-10,-30,-30,-30,0,0,0,0,-30,-30,-50,-30,-30,-30,-30,-30,-30,-50)}
T={}
z={}
B=([0]*120,[0]*120)
C=([0]*120,[0]*120)
D=[()]*120
E=[()]*120
F=[()]*120
G=[()]*120
for t in'PNBRQ':
 H=[0]*120
 I=[0]*120
 for J in e:
  r,f=(J-21)//10,(J-21)%10
  H[J]=V[t]+P[t][(7-r)*8+f]
  I[J]=-V[t]-P[t][r*8+f]
 T[t]=H
 T[t.lower()]=I
 z[t]=z[t.lower()]=V[t]
z['P']=z['p']=z['K']=z['k']=0
T['K']=T['k']=[0]*120
for J in e:
 r,f=(J-21)//10,(J-21)%10
 B[0][J]=P['K'][(7-r)*8+f]
 B[1][J]=-P['K'][r*8+f]
 C[0][J]=P['E'][(7-r)*8+f]
 C[1][J]=-P['E'][r*8+f]
 D[J]=tuple(t for t in e if t>J+2 and abs(t%10-J%10)<2)
 E[J]=tuple(t for t in e if t<J-2 and abs(t%10-J%10)<2)
 F[J]=tuple(t for t in e if 2<t-J<23 and abs(t%10-J%10)<2)
 G[J]=tuple(t for t in e if-23<t-J<-2 and abs(t%10-J%10)<2)
K=(0,5,10,20,35,60,100,0)
L={21:'Q',28:'K',91:'q',98:'k'}
def N(s):
 return ord(s[0])-97+21+10*(int(s[1])-1)
def O(i):
 return chr(97+(i-21)%10)+str((i-21)//10+1)
def Q(m):
 return O(m[0])+O(m[1])+m[2].lower()
def R(S):
 f=S.split()
 b=[' ']*120
 J=91
 for W in f[0]:
  if W=='/':
   J-=18
  elif W.isdigit():
   for _ in range(int(W)):
    b[J]='.'
    J+=1
  else:
   b[J]=W
   J+=1
 X=[b,f[1]=='w',''if f[2]=='-'else f[2],0 if f[3]=='-'else N(f[3]),int(f[4])if len(f)>4 else 0,b.index('K'),b.index('k'),0,0,0,0]
 for J in e:
  Y=b[J]
  if Y not in'.Kk':
   X[7]+=T[Y][J]
   X[8]+=z[Y]
   X[9]+=Y=='B'
   X[10]+=Y=='b'
 return X
def key(X):
 ep=X[3]
 if ep:
  p,d=('P',9)if X[1]else('p',-9)
  if X[0][ep-d]!=p and X[0][ep-d-2]!=p:
   ep=0
 return(''.join(X[0]),X[1],X[2],ep)
def Z(b,J,w):
 if w:
  if b[J-9]=='P'or b[J-11]=='P':
   return True
  n,k,aa,rq='N','K','BQ','RQ'
 else:
  if b[J+9]=='p'or b[J+11]=='p':
   return True
  n,k,aa,rq='n','k','bq','rq'
 for d in j:
  if b[J+d]==n:
   return True
 for d in l:
  if b[J+d]==k:
   return True
 for ac,ad in((o,aa),(v,rq)):
  for d in ac:
   t=J+d
   while b[t]=='.':
    t+=d
   if b[t]in ad:
    return True
 return False
def ae(X,caps=False):
 b,w,af,ep=X[0],X[1],X[2],X[3]
 ag='PNBRQK'if w else'pnbrqk'
 ah=ag.swapcase()
 ai='QRBN'if w else'qrbn'
 aj=[]
 for ak in e:
  Y=b[ak]
  if Y not in ag:
   continue
  if Y in'Pp':
   d=10 if w else-10
   to=ak+d
   al=to>=91 if w else to<=28
   if b[to]=='.':
    if al:
     for am in ai:
      aj.append((ak,to,am,0))
    elif not caps:
     aj.append((ak,to,'',0))
     if(31<=ak<=38 if w else 81<=ak<=88)and b[ak+2*d]=='.':
      aj.append((ak,ak+2*d,'',1))
   for an in(d-1,d+1):
    to=ak+an
    ao=b[to]
    if ao in ah:
     if al:
      for am in ai:
       aj.append((ak,to,am,0))
     else:
      aj.append((ak,to,'',0))
    elif ep and to==ep:
     aj.append((ak,to,'',2))
  elif Y in'NnKk':
   for d in j if Y in'Nn'else l:
    to=ak+d
    ao=b[to]
    if ao=='.':
     if not caps:
      aj.append((ak,to,'',0))
    elif ao in ah:
     aj.append((ak,to,'',0))
   if Y in'Kk'and not caps and ak==(25 if w else 95)and not Z(b,ak,not w):
    for ap,aq,n in((1,'K'if w else'k',2),(-1,'Q'if w else'q',3)):
     if aq in af and b[ak+ap*(n+1)]==('R'if w else'r')and all(b[ak+ap*i]=='.'for i in range(1,n+1))and not any(Z(b,ak+ap*i,not w)for i in range(1,n)):
      aj.append((ak,ak+ap*2,'',3))
  else:
   for d in x[Y]:
    to=ak+d
    while b[to]=='.':
     if not caps:
      aj.append((ak,to,'',0))
     to+=d
    if b[to]in ah:
     aj.append((ak,to,'',0))
 return aj
def ar(X,m):
 ak,to,am,fl=m
 b,w=X[0],X[1]
 Y=b[ak]
 at=(to-10 if w else to+10)if fl==2 else to
 au=b[at]
 u=(m,at,au,X[2],X[3],X[4],X[5],X[6],X[7],X[8],X[9],X[10])
 av=am if am else Y
 b[at]='.'
 b[ak]='.'
 b[to]=av
 X[7]+=T[av][to]-T[Y][ak]
 X[8]+=z[av]-z[Y]
 if au!='.':
  X[7]-=T[au][at]
  X[8]-=z[au]
 X[9]+=(av=='B')-(Y=='B')-(au=='B')
 X[10]+=(av=='b')-(Y=='b')-(au=='b')
 if Y=='K':
  X[5]=to
 elif Y=='k':
  X[6]=to
 if fl==3:
  aw,rt=(ak+3,ak+1)if to>ak else(ak-4,ak-1)
  ax=b[aw]
  b[rt]=ax
  b[aw]='.'
  X[7]+=T[ax][rt]-T[ax][aw]
 af=X[2]
 if Y=='K':
  af=af.replace('K','').replace('Q','')
 elif Y=='k':
  af=af.replace('k','').replace('q','')
 for q in(ak,to):
  if q in L:
   af=af.replace(L[q],'')
 X[2]=af
 X[3]=(ak+to)//2 if fl==1 else 0
 X[4]=0 if Y in'Pp'or au!='.'else X[4]+1
 X[1]=not w
 return u
def ay(X,u):
 m,at,au,af,ep,az,aA,aB,aC,aD,aE,bb=u
 ak,to,am,fl=m
 b=X[0]
 X[1]=not X[1]
 Y=b[to]
 b[ak]=('P'if Y.isupper()else'p')if am else Y
 b[to]='.'
 b[at]=au
 if fl==3:
  aw,rt=(ak+3,ak+1)if to>ak else(ak-4,ak-1)
  b[aw]=b[rt]
  b[rt]='.'
 X[2],X[3],X[4],X[5],X[6]=af,ep,az,aA,aB
 X[7],X[8],X[9],X[10]=aC,aD,aE,bb
def aF(X):
 b=X[0]
 s=X[7]
 if X[9]>1:
  s+=30
 if X[10]>1:
  s-=30
 if X[8]<2400:
  s+=C[0][X[5]]+C[1][X[6]]
  for J in e:
   Y=b[J]
   if Y=='P':
    for t in D[J]:
     if b[t]=='p':
      break
    else:
     s+=K[(J-21)//10]
   elif Y=='p':
    for t in E[J]:
     if b[t]=='P':
      break
    else:
     s-=K[7-(J-21)//10]
 else:
  s+=B[0][X[5]]+B[1][X[6]]
  for t in F[X[5]]:
   if b[t]=='P':
    s+=8
  for t in G[X[6]]:
   if b[t]=='p':
    s-=8
 return s if X[1]else-s
class aG(Exception):
 pass
aH={}
def aI(X,u):
 ak,to=N(u[:2]),N(u[2:4])
 am=u[4:].upper()if X[1]else u[4:]
 Y=X[0][ak]
 fl=0
 if Y in'Pp':
  if X[3]and to==X[3]and X[0][to]=='.':
   fl=2
  elif abs(to-ak)==20:
   fl=1
 elif Y in'Kk'and abs(to-ak)==2:
  fl=3
 return(ak,to,am,fl)
def aJ(X,aK,aL,aM,aN):
 aO=0
 aP=[[None,None]for _ in range(64)]
 aQ={}
 def aR():
  k=key(X)
  aL.append(k)
  aM[k]=aM.get(k,0)+1
 def pop():
  k=aL.pop()
  aM[k]-=1
 def aS(aT,p,tm):
  b=X[0]
  aU,k1=aP[p]
  def aV(m):
   ak,to,am,fl=m
   if m==tm:
    return 10**9
   s=0
   au=b[to]
   if au!='.':
    s=100000+M[au]-A[b[ak]]
   elif fl==2:
    s=101000
   if am:
    s+=90000+A[am]
   if s==0:
    if m==aU:
     s=50000
    elif m==k1:
     s=40000
    else:
     s=aQ.get((ak,to),0)
   return s
  aT.sort(key=aV,reverse=True)
 def q(a,b,p,aW):
  nonlocal aO
  aO+=1
  if aO>aK:
   raise aG
  aX=-y-1
  aY=0
  if not aW:
   aY=aF(X)
   aX=aY
   if aX>=b:
    return aX
   if aX>a:
    a=aX
  if p>=60:
   return aX if not aW else aF(X)
  aT=ae(X,not aW)
  aS(aT,p,None)
  n=0
  for m in aT:
   if not aW and not m[2]:
    aZ=100 if m[3]==2 else A[X[0][m[1]]]
    if aY+aZ+200<a:
     continue
   u=ar(X,m)
   a_=X[6]if X[1]else X[5]
   if Z(X[0],a_,X[1]):
    ay(X,u)
    continue
   n+=1
   s=-q(-b,-a,p+1,False)
   ay(X,u)
   if s>aX:
    aX=s
   if s>=b:
    return s
   if s>a:
    a=s
  if aW and n==0:
   return-y+p
  return aX
 def ba(d,a,b,p):
  nonlocal aO
  aO+=1
  if aO>aK:
   raise aG
  if X[4]>=100:
   return 0
  bc=key(X)
  if aM.get(bc,0)>1:
   return 0
  a_=X[5]if X[1]else X[6]
  aW=Z(X[0],a_,not X[1])
  if aW:
   d+=1
  if d<=0 or p>=60:
   return q(a,b,p,aW)
  bd=aH.get(bc)
  tm=None
  if bd:
   be,bf,bh,tm=bd
   bh=bh-p if bh>y-64 else bh+p if bh<-y+64 else bh
   if be>=d and(bf==0 or(bf==1 and bh>=b)or(bf==2 and bh<=a)):
    return bh
  bi=a
  aT=ae(X)
  aS(aT,p,tm)
  aX=-y-1
  bm=None
  n=0
  for m in aT:
   u=ar(X,m)
   a_=X[6]if X[1]else X[5]
   if Z(X[0],a_,X[1]):
    ay(X,u)
    continue
   n+=1
   aR()
   s=-ba(d-1,-b,-a,p+1)
   pop()
   ay(X,u)
   if s>aX:
    aX=s
    bm=m
   if s>a:
    a=s
   if a>=b:
    if X[0][m[1]]=='.'and not m[2]and m[3]!=2:
     if aP[p][0]!=m:
      aP[p][1]=aP[p][0]
      aP[p][0]=m
     aQ[(m[0],m[1])]=aQ.get((m[0],m[1]),0)+d*d
    break
  if n==0:
   return-y+p if aW else 0
  bj=aX+p if aX>y-64 else aX-p if aX<-y+64 else aX
  bf=2 if aX<=bi else 1 if aX>=b else 0
  if len(aH)>65536:
   aH.clear()
  aH[bc]=(d,bf,bj,bm)
  return aX
 if not aN:
  return None
 if len(aN)==1:
  return aN[0]
 bk=[X[0][:]]+X[1:]
 bl=len(aL)
 bn={}
 aX=aN[0]
 bo=0
 def bp(d,a,b):
  br=-y-1
  bm=None
  for m in sorted(aN,key=lambda m:-bn.get(m,0)):
   u=ar(X,m)
   aR()
   s=-ba(d-1,-b,-a,1)
   pop()
   ay(X,u)
   bn[m]=s
   if s>br:
    br=s
    bm=m
   if s>a:
    a=s
  return br,bm
 for d in range(1,7):
  try:
   w=50 if d>=3 else y+1
   br,bm=bp(d,bo-w,bo+w)
   if d>=3 and(br<=bo-w or br>=bo+w):
    br,bm=bp(d,-y-1,y+1)
  except aG:
   X[0][:]=bk[0]
   X[1:]=bk[1:]
   while len(aL)>bl:
    pop()
   break
  aX=bm
  bo=br
  if br>=y-64:
   break
 return aX
def bu(bv,bx):
 by=U.Request(bv,json.dumps(bx).encode(),{'Content-Type':'application/json'})
 with U.urlopen(by,timeout=60)as r:
  return json.load(r)
def bz(g,aK):
 bA=g['legal_moves']
 X=R(g['fen'])
 try:
  aN=[aI(X,u)for u in bA]
  h=R(g['start_fen'])
  aL=[]
  aM={}
  def bB():
   k=key(h)
   aL.append(k)
   aM[k]=aM.get(k,0)+1
  bB()
  for u in g['moves']:
   ar(h,aI(h,u))
   bB()
  bc=key(X)
  if aL[-1][:3]==bc[:3]:
   if aL[-1]!=bc:
    aM[aL[-1]]-=1
    aL[-1]=bc
    aM[bc]=aM.get(bc,0)+1
  else:
   aL=[bc]
   aM={bc:1}
  m=aJ(X,aK,aL,aM,aN)
  u=Q(m)if m else None
  if u in bA:
   return u
 except Exception:
  pass
 return sorted(bA)[0]
def bC():
 bD=os.environ['MAKEFUN_ENV_URL']
 aK=int(os.environ.get('TC_NODES','300000'))
 while True:
  g=bu(bD+'/game',{})
  if g.get('status')=='done':
   print(json.dumps(g),flush=True)
   break
  if g.get('status')not in('your_move','playing','over'):
   break
  while g.get('status')in('your_move','playing'):
   bE=bz(g,aK)
   g=bu(bD+'/move',{'game':g['game'],'move':bE})
  print('game',g.get('game'),g.get('opponent'),g.get('outcome'),g.get('reason'),'plies',g.get('plies'),flush=True)
if __name__=='__main__':
 bC()
