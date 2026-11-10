"""Checks Orbit's color pairs against WCAG AA. python3 tests/contrast.py"""
import re,sys,os
h=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','index.html')).read()
def L(x):
    x=x.lstrip('#');r,g,b=[int(x[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c:c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    return .2126*f(r)+.7152*f(g)+.0722*f(b)
def cr(a,b):x,y=sorted([L(a),L(b)],reverse=True);return (x+.05)/(y+.05)
tiers=re.search(r"const TIER_COLORS=\{([^}]*)\}",h).group(1);tc=re.findall(r"#([0-9A-Fa-f]{6})",tiers)
gc=re.findall(r"#([0-9A-Fa-f]{6})",re.search(r"const GROUP_COLORS=\[([^\]]*)\]",h).group(1))
light=dict(re.findall(r"--(paper|stone|ink2):#([0-9A-Fa-f]{6})",h[h.index(':root{'):h.index(':root[data-theme=dark]')]))
dark=dict(re.findall(r"--(paper|stone|ink2):#([0-9A-Fa-f]{6})",h[h.index(':root[data-theme=dark]'):h.index('@media (prefers-color-scheme:dark)')]))
bad=0
def need(v,mn,msg):
    global bad
    ok=v>=mn;bad+=not ok;print(('PASS' if ok else 'FAIL'),f'{v:.2f} >= {mn}',msg)
for c in tc+gc:
    need(cr('FFFFFF',c),4.5,f'white initials on #{c}');need(cr(c,dark['paper']),3,f'#{c} dot on dark paper');need(cr(c,light['paper']),3,f'#{c} dot on light paper')
for k in ('stone','ink2'):need(cr(light[k],light['paper']),4.5,f'light {k} text');need(cr(dark[k],dark['paper']),4.5,f'dark {k} text')
sys.exit(1 if bad else 0)
