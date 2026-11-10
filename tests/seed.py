import datetime as dt
T=dt.date(2026,11,9)
def d(n):return (T-dt.timedelta(days=n)).isoformat()
def C(n,w,m='Text',note=''):return {'id':f'c{n}{w}{m}','date':d(n),'who':w,'mode':m,'note':note}
def P(i,name,tier,contacts,**k):
    f={'id':f'p{i}','name':name,'tier':tier,'created':d(400),'contacts':contacts,'tierHistory':[],'notes':'','met':'','best':'','bestContext':'','birthday':'','cadence':None,'tempered':False,'soulmate':False,'dormant':False}
    f.update(k);return f
people=[
 P(1,'Maya','homie',[C(9,'them','Call'),C(20,'me','In person'),C(33,'mutual','In person')],best='overarching',tempered=True,soulmate=True,birthday='1998-11-21',followups=[{'id':'a','text':'How the move went','done':False}],gifts=[{'id':'g','text':'Film camera strap','done':False}]),
 P(2,'Jonah','good',[C(16,'me'),C(30,'me'),C(44,'me','Call'),C(60,'me'),C(75,'them'),C(90,'me')],followups=[{'id':'b','text':'His sister’s wedding','done':False}],expect='Text back within a day or two',tierHistory=[]),
 P(3,'Priya','friend',[C(25,'them','Video'),C(50,'me')],soulmate=True,created=d(40)),
 P(4,'Eli','friend',[C(19,'mutual','In person')]),
 P(5,'Sam (café)','casual',[C(30,'mutual','In person')]),
 P(6,'Rosa','good',[C(5,'them'),C(12,'me','Call'),C(26,'them')],best='temporal',bestContext='grad school'),
 P(7,'Dev','friend',[C(200,'mutual','In person')],dormant=True),
 P(8,'Hana','acq',[]),
 P(9,'Luis','casual',[]),
]
