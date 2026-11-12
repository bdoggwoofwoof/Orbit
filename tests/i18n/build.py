import json,re,glob,importlib.util
T={};B={}
for f in sorted(glob.glob('dict/d*.py')):
    spec=importlib.util.spec_from_file_location('m',f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    T.update(getattr(m,'T',{}));B.update(getattr(m,'B',{}))
for k in list(T):
    if re.search(r'Jonah|Maya',k):del T[k]
sp=json.load(open('split.json'))
need=[s for s in sp['t_static']+sp['a_static'] if len(s)>1]
extra=[l for l in open('extra.txt').read().split('\n') if l and re.match(r'^[A-Z“"(][^=<>{}]*$',l) and not re.match(r'^(BEGIN|END|DT|UID|SUMMARY|TRIGGER|VERSION|PRODID|CAL|TRANSP|DESCRIPTION|ACTION|Arrow|Enter|Escape|Tab$|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)',l)]
miss=[s for s in dict.fromkeys(need+extra) if s not in T]
bneed=sp['b_static']
bmiss=[s for s in bneed if s not in B]
print(len(T),'t entries;',len(miss),'missing;',len(B),'blocks;',len(bmiss),'block missing')
open('missing.txt','w').write('\n'.join(miss));open('bmissing.txt','w').write('\n'.join(bmiss))
json.dump({'t':T,'b':B},open('dict.json','w'),ensure_ascii=False)
