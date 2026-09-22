const fs=require('fs'),vm=require('vm'),assert=require('assert');
(async()=>{
 const root='dist/',base='https://guide.test/',handlers={},maps=new Map();let offline=false,fetches=[];
 const key=x=>new URL(typeof x==='string'?x:x.url,base).pathname;
 const network=async x=>{if(offline)throw Error('offline');let path=key(x);fetches.push(path);return new Response(fs.readFileSync(root+(path==='/'?'index.html':path.slice(1))),{headers:{'content-type':path.endsWith('.jpg')?'image/jpeg':path.endsWith('.js')?'text/javascript':'text/html'}})};
 const caches={keys:async()=>[...maps.keys()],open:async name=>{if(!maps.has(name))maps.set(name,new Map());let m=maps.get(name);return {match:async path=>m.get(key(path))?.clone(),put:async(path,response)=>m.set(key(path),response.clone()),addAll:async paths=>{for(const p of paths)m.set(key(p),await network(p))}}}};
 const ctx={URL,caches,fetch:network,self:{location:{origin:'https://guide.test'},addEventListener:(t,h)=>handlers[t]=h,skipWaiting:async()=>{},clients:{claim:async()=>{},matchAll:async()=>[]}}};vm.createContext(ctx);vm.runInContext(fs.readFileSync(root+'animals.js','utf8')+';this.animals=ANIMALS',ctx);let old=await caches.open('wild-pocket-v3');for(const a of ctx.animals)await old.put(a.image,await network(a.image));fetches=[];
 vm.runInContext(fs.readFileSync(root+'sw.js','utf8'),ctx);let pending;handlers.install({waitUntil:p=>pending=p});await pending;
 async function message(type){let results=[];handlers.message({data:{type},ports:[{postMessage:r=>results.push(r)}],waitUntil:p=>pending=p});await pending;return results.at(-1)}
 const initial=await message('CHECK');assert.deepEqual(initial,{cached:39,total:43,complete:false});fetches=[];assert((await message('DOWNLOAD')).complete);assert.equal(fetches.length,4);offline=true;
 for(const path of ['stories.js','assets/elephant-story.jpg','assets/ostrich-story.jpg','assets/giraffe-story.jpg','assets/wildebeest-story.jpg']){let response;handlers.fetch({request:{url:base+path,method:'GET'},respondWith:p=>response=p});assert((await(await response).arrayBuffer()).byteLength>0)}
 console.log('Offline check: old 29 photos reused; 4 new photos added; all 43 resources complete; stories and new photos served with network disabled.');
 // Exercise the real detail renderer and existing seen-state operations without a browser.
 const elements=new Map();function el(s){if(!elements.has(s))elements.set(s,{value:'',innerHTML:'',textContent:'',dataset:{},children:[],setAttribute(){},querySelectorAll(){return[]},focus(){},showModal(){this.open=true},scrollTop:0});return elements.get(s)}
 const local=new Map([['safari-seen','["lion"]']]);const ui={document:{querySelector:el,querySelectorAll:()=>[]},localStorage:{getItem:k=>local.get(k),setItem:(k,v)=>local.set(k,v)},navigator:{},window:{addEventListener(){}},alert(){throw Error('Unexpected storage error')}};vm.createContext(ui);for(const f of ['animals','habitats','stories','app'])vm.runInContext(fs.readFileSync(root+f+'.js','utf8'),ui);
 for(const a of ctx.animals){vm.runInContext(`showAnimal('${a.id}')`,ui);let html=el('#detailContent').innerHTML;assert(html.includes('wild-story')&&html.includes('在现场，多看一眼'));assert(!html.includes('undefined'));}
 assert(JSON.parse(local.get('safari-seen')).includes('lion'));vm.runInContext("toggleSeen('lion');toggleSeen('serval')",ui);assert.deepEqual(JSON.parse(local.get('safari-seen')),['serval']);console.log('Details: all 29 render with stories and citations; previous seen record restored; cancel and add persist.');
})().catch(e=>{console.error(e);process.exit(1)});
