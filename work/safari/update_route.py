from pathlib import Path
import json
p=Path('dist')
f=p/'index.html';s=f.read_text().replace('东非动物离线图鉴：','坦桑尼亚 Safari 离线动物图鉴：').replace('KENYA &amp; TANZANIA','TANZANIA · SAFARI').replace('KENYA & TANZANIA','TANZANIA · SAFARI').replace('东非随身动物图鉴','9.25—10.1 · 你的 Safari 随身图鉴').replace('01 / 东非','02 / 坦桑尼亚')
s=s.replace('<label class="search">','<div class="route-picker"><label for="route">按行程找</label><select id="route"><option value="all">整本图鉴 · 全部动物</option><option value="tarangire">9.25 · 塔兰吉雷</option><option value="night">9.25 晚 · 夜游辨认</option><option value="central">9.27 / 9.30 · 塞伦盖蒂中部</option><option value="mara">9.28—29 · 北部 / 马拉河</option><option value="crater">10.1 · 恩戈罗恩戈罗火山口</option></select></div><p id="routeNote" class="route-note">按当天地点缩小查找范围，也可以浏览全部动物。</p><label class="search">')
s=s.replace('照片帮助初步辨认 · 不确定时请向导确认','行程重点清单，并非当地全部物种或目击保证<br>照片帮助初步辨认 · 不确定时请向导确认')
s=s.replace('<h3>添加到手机主屏幕</h3>','<p class="muted">本版按塔兰吉雷、塞伦盖蒂和恩戈罗恩戈罗路线整理，包含夜游辨认重点。更新后请补全新增照片，再检查离线状态。</p><h3>添加到手机主屏幕</h3>')
s=s.replace('来源链接需联网。</p>','来源链接需联网。</p><p class="muted">地点资料：<a href="https://www.tanzaniaparks.go.tz/tarangire" target="_blank" rel="noopener">TANAPA 塔兰吉雷</a> · <a href="https://www.my.tzembassy.go.tz/uploads/NCAA_English_Brochure.pdf" target="_blank" rel="noopener">NCAA 恩戈罗恩戈罗指南</a>。图鉴中的路线重点为根据栖息地整理的辨认清单，不是实时动物位置。</p>')
f.write_text(s)
f=p/'app.js';s=f.read_text();s=s.replace("let category='全部',onlySeen=false", "let route='all',category='全部',onlySeen=false")
routes={
'all':{'note':'按当天地点缩小查找范围，也可以浏览全部动物。','ids':[]},
 'tarangire':{'note':'象群与疏林草原：先看大象、长颈鹿和各种羚羊。鸟类也值得留意。','ids':['elephant','giraffe','impala','waterbuck','dikdik','zebra','wildebeest','buffalo','lion','leopard','cheetah','hyena','warthog','baboon','ostrich','bustard','secretary','jackal','serval']},
 'night':{'note':'夜间先看耳朵、尾巴、体形和斑纹；仅靠反光眼睛不能确定物种。以下是辨认备选，并非保证目击。','ids':['serval','bateared','jackal','hyena','leopard','lion','dikdik','hippo']},
 'central':{'note':'中部草原与林地：优先区分狮子、花豹和猎豹，再看角马与羚羊。','ids':['lion','leopard','cheetah','hyena','serval','wildebeest','zebra','thomson','grant','impala','topi','hartebeest','eland','giraffe','elephant','buffalo','hippo','crocodile','waterbuck','dikdik','jackal','bateared','warthog','baboon','ostrich','secretary','bustard','crane']},
 'mara':{'note':'北部与马拉河：优先辨认角马、斑马、河马和尼罗鳄。渡河时机取决于现场兽群与水情。','ids':['wildebeest','zebra','hippo','crocodile','topi','impala','thomson','grant','eland','giraffe','elephant','buffalo','lion','leopard','cheetah','hyena','warthog','baboon','ostrich']},
 'crater':{'note':'火山口底：重点留意黑犀牛、狮子、斑鬣狗，以及灰冠鹤、柯利鸟。此清单针对谷底，不包含途经的火山口外缘。','ids':['rhino','lion','hyena','buffalo','wildebeest','zebra','thomson','grant','hartebeest','eland','hippo','elephant','warthog','jackal','serval','cheetah','ostrich','crane','bustard','secretary','waterbuck','baboon']}}
s=s.replace("const cats=",'const ROUTES='+json.dumps(routes,ensure_ascii=False)+";$('#route').onchange=e=>{route=e.target.value;$('#routeNote').textContent=ROUTES[route].note;render()};const cats=")
s=s.replace("const list=ANIMALS.filter(a=>(category", "const order=ROUTES[route].ids;const list=ANIMALS.filter(a=>(route==='all'||order.includes(a.id))&&(category")
s=s.replace(".includes(q));$('#count')", ".includes(q)).sort((a,b)=>route==='all'?0:order.indexOf(a.id)-order.indexOf(b.id));$('#count')")
s=s.replace("`已完整保存 ${ANIMALS.length} 种动物", "`本版已完整保存 ${ANIMALS.length} 种动物")
f.write_text(s)
f=p/'style.css';f.write_text(f.read_text()+'\n.route-picker{display:flex;gap:14px;align-items:center;margin:0 0 8px}.route-picker label{font-size:14px;color:var(--muted);white-space:nowrap}.route-picker select{font:inherit;min-width:0;flex:1;padding:11px 14px;border:1px solid #cbd3c6;border-radius:10px;color:var(--ink);background:white;max-width:440px}.route-note{font-size:14px;color:var(--muted);margin:0 0 20px;max-width:750px}.route-picker select:focus-visible{outline:3px solid #738c32}\n')
f=p/'sw.js';s=f.read_text().replace("wild-pocket-v1","wild-pocket-v2");s=s.replace("'crocodile'].map", "'crocodile','waterbuck','hartebeest','dikdik','jackal','serval','bateared','crane','secretary','bustard'].map")
s=s.replace('await c.addAll(SHELL);await self.skipWaiting()',"await c.addAll(SHELL);const oldKeys=(await caches.keys()).filter(k=>k.startsWith('wild-pocket-')&&k!==CACHE);for(const path of PHOTOS){for(const key of oldKeys){const hit=await (await caches.open(key)).match(path);if(hit){await c.put(path,hit);break}}}await self.skipWaiting()")
s=s.replace("event.waitUntil(self.clients.claim())", "event.waitUntil((async()=>{await self.clients.claim();const windows=await self.clients.matchAll({type:'window'});await Promise.all(windows.map(w=>w.navigate(w.url).catch(()=>{})))})())")
f.write_text(s)
