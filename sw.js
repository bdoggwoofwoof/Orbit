const CACHE='orbit-v8';
const SHELL=['./','index.html','manifest.json','icon-192.png','icon-512.png','icon-180.png','fonts/fraunces-latin-opsz-normal.woff2','fonts/inter-latin-400-normal.woff2','fonts/inter-latin-500-normal.woff2','fonts/inter-latin-600-normal.woff2','ar.js','fonts/ibm-plex-sans-arabic-arabic-400-normal.woff2','fonts/ibm-plex-sans-arabic-arabic-500-normal.woff2','fonts/ibm-plex-sans-arabic-arabic-600-normal.woff2','fonts/noto-naskh-arabic-arabic-wght-normal.woff2'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  const r=e.request;if(r.method!=='GET')return;
  if(r.mode==='navigate'){e.respondWith(fetch(r).then(res=>{const c=res.clone();caches.open(CACHE).then(x=>x.put('index.html',c));return res}).catch(()=>caches.match('index.html')));return}
  e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{if(res.ok&&new URL(r.url).origin===location.origin){const c=res.clone();caches.open(CACHE).then(x=>x.put(r,c))}return res}).catch(()=>m)));
});
