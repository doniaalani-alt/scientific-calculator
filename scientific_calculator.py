

import pygame, math, sys, re
pygame.init()
W,H=480,720;S=pygame.display.set_mode((W,H))
pygame.display.set_caption("Scientific Calculator")
F=pygame.font.SysFont(None,36);B=pygame.font.SysFont(None,48)
BG=(30,30,30);BBG=(50,50,50);BH=(80,80,80);T=(230,230,230);A=(45,120,230);DB=(20,20,20)
ROWS=[["sin","cos","tan","(",")"],["asin","acos","atan","pi","e"],["log","log10","sqrt","^","ans"],["7","8","9","/","C"],["4","5","6","*","⌫"],["1","2","3","-","±"],["0",".","%","+","="],["AC"]]
class Bttn:
    def __init__(s,r,l):s.r=pygame.Rect(r);s.l=l
    def d(s,sv,m):
        c=BH if s.r.collidepoint(m)else BBG
        pygame.draw.rect(sv,c,s.r,border_radius=8)
        if s.l in ("=", "C", "AC"):pygame.draw.rect(sv,A,s.r,3,border_radius=8)
        txt=F.render(s.l,1,T);sv.blit(txt,txt.get_rect(center=s.r.center))
B_LIST=[]
pad=10
cols=5
btn_w=(W-(pad*(cols+1)))//cols
btn_h=(H-240-(pad*(len(ROWS)+1)))//len(ROWS)
y=240+pad
for r in ROWS:
    x=pad
    for l in r:
        B_LIST.append(Bttn((x,y,btn_w,btn_h),l))
        x+=btn_w+pad
    y+=btn_h+pad
expr="";ans=0.0
def safe_eval(x,a):x=x.replace("^","**").replace("×","*").replace("÷","/");d={k:getattr(math,k)for k in dir(math)if not k.startswith("__")};d["ans"]=a;return eval(x,{"__builtins__":None},d)
def disp(sv,txt):
    dr=pygame.Rect(10,10,W-20,220)
    pygame.draw.rect(sv,DB,dr,border_radius=8)
    ts=F.render(txt if len(txt)<32 else txt[-32:],1,T)
    sv.blit(ts,ts.get_rect(right=dr.right-12,centery=dr.centery-24))
    a=B.render(f"ans = {ans}",1,T)
    sv.blit(a,a.get_rect(right=dr.right-12,centery=dr.centery+36))
def app(t):global expr;expr+=t
def bs():global expr;expr=expr[:-1]
def clr():global expr;expr=""
def clr_all():global expr,ans;expr="";ans=0.0
def sign():
    global expr
    if not expr:
        expr="-"
        return
    m = re.search(r"([-+]?\d*\.?\d+([eE][-+]?\d+)?)$", expr)
    if m:
        n = m.group(1)
        s_pos = m.start(1)
        expr = expr[:s_pos] + (n[1:] if n.startswith("-") else "-" + n)
    else:
        expr = "-" + expr
def hbtn(l):
    global expr,ans
    if l=="=":
        if not expr.strip():return
        try:v=safe_eval(expr,ans);ans=v;expr=str(v)
        except:expr="Error"
    elif l=="C":clr()
    elif l=="AC":clr_all()
    elif l=="⌫":bs()
    elif l=="±":sign()
    elif l=="ans":app("ans")
    elif l in("sin","cos","tan","asin","acos","atan","sqrt","log","log10"):app(l+"(")
    elif l in("pi","e","%"):app(l)
    else:app(l)
def hkey(e):
    global expr
    if e.key==pygame.K_RETURN:hbtn("=")
    elif e.key==pygame.K_BACKSPACE:bs()
    elif e.key==pygame.K_ESCAPE:clr_all()
    else:
        ch=e.unicode
        if ch:
            if ch=="^":app("^")
            elif ch in"0123456789.+-*/()%":app(ch)
            elif ch.lower()=="p":app("pi")
            elif ch.lower()=="e":app("e")
clk=pygame.time.Clock()
run=True
while run:
    m=pygame.mouse.get_pos()
    for ev in pygame.event.get():
        if ev.type==pygame.QUIT:run=False
        elif ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
            for bt in B_LIST:
                if bt.r.collidepoint(ev.pos):hbtn(bt.l);break
        elif ev.type==pygame.KEYDOWN:hkey(ev)
    S.fill(BG)
    disp(S,expr)
    for bt in B_LIST:bt.d(S,m)
    pygame.display.flip();clk.tick(60)
pygame.quit();sys.exit()
