"""Collects every English string Orbit shows (text nodes, mixed-content blocks, attributes) across views and sheets.
Serve the repo on :8765, then: python3 tests/i18n_crawl.py out.json"""
import asyncio,json,sys,os
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__));exec(open(os.path.join(HERE,'seed.py')).read())
U='http://localhost:8765/'
COLLECT=r"""(roots)=>{const T=new Set(),B=new Set(),A=new Set();
 const ctrl='input,select,textarea,form,details';const skip='textarea,input,select,script,style,.av,.arw,[data-noi18n]';
 const norm=s=>s.replace(/\s+/g,' ').trim();
 const isBlock=el=>{if(el.closest('svg')||el.closest(skip))return false;if(el.querySelector(ctrl)||el.matches(ctrl))return false;let txt=false,kid=false;for(const n of el.childNodes){if(n.nodeType===3&&n.nodeValue.trim())txt=true;if(n.nodeType===1)kid=true}return txt&&kid&&el.children.length<=8&&![...el.children].some(c=>/^(DIV|UL|OL|P|SECTION|DL|TABLE|H\d)$/.test(c.tagName))};
 for(const sel of roots){const r=document.querySelector(sel);if(!r)continue;
  const blocks=[...r.querySelectorAll('*')].filter(isBlock);blocks.forEach(b=>B.add(norm(b.innerHTML)));
  const w=document.createTreeWalker(r,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){const t=n.nodeValue.trim();if(!t)continue;const p=n.parentElement;if(p&&p.closest(skip))continue;if(blocks.some(b=>b.contains(n)))continue;T.add(t)}
  r.querySelectorAll('[placeholder],[aria-label],[title]').forEach(e=>['placeholder','aria-label','title'].forEach(k=>{const v=e.getAttribute(k);if(v&&v.trim())A.add(v.trim())}));
 }
 return {t:[...T],b:[...B],a:[...A]};}"""
async def main():
    out={'t':set(),'b':set(),'a':set()}
    rich=[dict(x) for x in people]
    rich[1]=dict(rich[1],plans=[{'id':'pl1','date':'2026-11-01','wants':['understand'],'type':'hurt','size':'medium','mood':'stirred','fair':'y','told':'n','path':'talk','what':'cancelled again','status':'open','when':'2026-11-09','how':'Call','opener':'Hey'}],
                 contacts=rich[1]['contacts']+[{'id':'w1','date':'2026-11-01','who':'me','mode':'Text','note':'','reply':'waiting'}],lastCheck={'date':'2026-10-01','suggested':2,'exp':'come to my party'},style='space')
    rich[0]=dict(rich[0],groups=['far','g1'],expectations=[{'id':'e1','text':'Call on my birthday','reasonable':True,'said':True,'agreed':True},{'id':'e2','text':'Visit','reasonable':True}],needs='text first',notes='x',followups=[{'id':'a','text':'move','done':True}],gifts=[{'id':'g','text':'strap','done':False}])
    st={'lang':'ar','onboarded':True,'toured':True,'groups':[{'id':'g1','name':'Denver','kind':'place','color':'#7B5CA2','cadence':30}],'me':{'answers':{},'anx':3,'avo':2,'style':'reassure','date':'2026-11-01'}}
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for w in (390,1440):
          ctx=await b.new_context(viewport={'width':w,'height':900})
          await ctx.add_init_script(f"if(!localStorage.getItem('orbit.v1'))localStorage.setItem('orbit.v1',{json.dumps(json.dumps({'friends':rich,'settings':st}))});")
          await ctx.add_init_script("window.NO_I18N=true;");
          await ctx.add_init_script("const _D=Date;Date=class extends _D{constructor(...a){if(a.length)super(...a);else super(2026,10,9,12)}static now(){return new _D(2026,10,9,12).getTime()}};")
          pg=await ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
          async def snap():
              r=await pg.evaluate(COLLECT,['#view','#sheet','#tabs','header','#toast','.tour-card'])
              for k in r:out[k].update(r[k])
          for names in ('english',):
            await pg.goto(U+'#reach');await pg.wait_for_timeout(300)
            await pg.evaluate(f"S.settings.ladderNames='{names}';render()")
            for v in ['reach','people','guide','more']:
                await pg.evaluate(f"location.hash='{v}'");await pg.wait_for_timeout(200);await snap()
            await pg.evaluate("ui.peopleMode='recent';render()");await snap();await pg.evaluate("ui.peopleMode='list';render()")
            js=["openSheet({type:'add'})","openSheet({type:'add'});document.querySelector('#nMode [data-m=many]').click();document.querySelector('[data-act=bnTog]').click()",
                "openSheet({type:'orbit'})","openSheet({type:'review'})","openSheet({type:'me',ans:{}})",
                "openSheet({type:'me',ans:{0:4,1:2,2:5,3:2,4:4,5:3,6:4,7:2}})"]
            js+=[f"openSheet({{type:'intro',step:{i}}})" for i in range(3)]
            js+=[f"openSheet({{type:'person',id:'p{i}',justAdded:true}})" for i in range(1,10)]
            js+=[f"openSheet({{type:'edit',id:'p{i}'}})" for i in (1,2,6,7)]
            js+=[f"openSheet({{type:'reflect',id:'p2',step:{i},ans:{{0:'y',1:'y',2:'n',3:'u',4:'y',5:'n',6:'n'}},fair:'n',exp:'come to my party'}})" for i in range(4)]
            js+=[f"openSheet({{type:'reflect',id:'p3',step:3,ans:{{0:'y',1:'y',2:'y',3:'y',4:'y',5:'y',6:'y'}},fair:'y'}})"]
            js+=["openSheet({type:'checkin',id:'p2',cid:'w1'})","openSheet({type:'plan',id:'p2',pid:'pl1'})","openSheet({type:'plan',id:'p2',pid:'pl1',resolve:1})"]
            for ty in ['hurt','me','misread','expect','drift','unsure']:
              for path in ['letgo','clarify','talk','apologize','boundary','expect','time']:
                for stp in range(7):
                  js.append(f"openSheet({{type:'repair',id:'p2',step:{stp},plan:{{id:'x',date:'2026-11-09',wants:['understand','change','apology'],type:'{ty}',size:'medium',mood:'stirred',fair:'y',told:'y',pattern:'often',path:'{path}',what:'x'}}}})")
            for j in js:
                try:
                    await pg.evaluate(j);await pg.wait_for_timeout(60);await snap()
                    await pg.evaluate("document.querySelectorAll('#sheet details').forEach(d=>d.open=true)");await snap()
                except Exception as e: print('ERR',j[:60],e)
            await pg.evaluate("closeSheet()")
            # toasts
            for j in ["toast('x')","toastLog(S.friends[0],{id:'c',who:'me',mode:'Text',date:'2026-11-09'})"]:
                await pg.evaluate(j);await snap()
            # tour
            await pg.evaluate("Tour.start()");await pg.wait_for_timeout(500)
            for i in range(7):
                await snap();await pg.evaluate("document.querySelector('.tour-next').click()");await pg.wait_for_timeout(700)
          print('errs',errs[:3]);await ctx.close()
        await b.close()
    json.dump({k:sorted(v) for k,v in out.items()},open(sys.argv[1],'w'),ensure_ascii=False,indent=0)
    print({k:len(v) for k,v in out.items()})
asyncio.run(main())
