from pathlib import Path
import json,shutil
p=Path('dist')
s=p.joinpath('stories.js').read_text(); data=json.loads(s[len('const STORIES = '):].rstrip().rstrip(';'))
# Keep the same names as the identification cards, with useful common synonyms.
data['grant']['lead']=data['grant']['lead'].replace('格氏瞪羚','格兰特瞪羚（也称格氏瞪羚）',1)
data['baboon']['lead']=data['baboon']['lead'].replace('橄榄狒狒','东非狒狒（也称橄榄狒狒）',1)
data['bateared']['lead']=data['bateared']['lead'].replace('蝠耳狐','大耳狐（也称蝠耳狐）',1)
for section in ['lead','watch']:
 data['bustard'][section]=data['bustard'][section].replace('柯利灰鹭鸨','柯利鸟')
for x in data['bustard']['sections']:x['text']=x['text'].replace('柯利灰鹭鸨','柯利鸟')
data['warthog']['sources'][1]={'title':'圣迭戈动物园 · Warthog','url':'https://animals.sandiegozoo.org/animals/warthog'}
# No implication of personally conducted fieldwork, or access to full books/videos.
data['giraffe']['lead']=data['giraffe']['lead'].replace('参考文章里植物的“防卫战”，到了这里，就出现了另一个主角。','金合欢的刺是保护，长颈鹿的嘴却有另一套办法。每天的一顿饭，就是两种生存本领相遇的地方。')
photos=json.loads(Path('/tmp/safari-story-assets/manifest.json').read_text())
for f in photos:
 name=f['animalId']+'-story.jpg';shutil.copyfile(f['path'],p/'assets'/name)
 data[f['animalId']]['photo']={'image':'./assets/'+name,'caption':f['caption'],'author':f['author'],'license':f['license'],'licenseUrl':f['licenseUrl'],'source':f['sourcePage']}
p.joinpath('stories.js').write_text('const STORIES = '+json.dumps(data,ensure_ascii=False,indent=2)+';\n')
a=p.joinpath('app.js').read_text()
start=a.index('function showAnimal(');end=a.index("document.querySelectorAll('dialog')",start)
new=r'''function storyHTML(a){
 const s=STORIES[a.id];if(!s)return '';
 const textLength=s.lead.length+s.sections.reduce((n,x)=>n+x.text.length,0);
 const sourceLink=(n)=>{const source=s.sources[n-1];return `<a class="reference" href="${escapeHtml(source.url)}" target="_blank" rel="noopener" aria-label="资料 ${n}：${escapeHtml(source.title)}">[${n}]</a>`};
 const photo=s.photo?`<figure class="story-photo"><img src="${escapeHtml(s.photo.image)}" alt="${escapeHtml(s.photo.caption)}" loading="lazy" width="1200" height="800"><figcaption>${escapeHtml(s.photo.caption)}<small>摄影：${escapeHtml(s.photo.author)} · <a href="${escapeHtml(s.photo.licenseUrl)}" target="_blank" rel="noopener">${escapeHtml(s.photo.license)}</a> · <a href="${escapeHtml(s.photo.source)}" target="_blank" rel="noopener">原图与授权 ↗</a> · 已缩小及压缩</small></figcaption></figure>`:'';
 return `<article class="wild-story" aria-label="${escapeHtml(a.name)}的野外故事"><p class="eyebrow">野外故事 · 约 ${Math.max(2,Math.ceil(textLength/350))} 分钟</p><h3 class="story-title">${escapeHtml(s.title)}</h3><p class="story-lead">${escapeHtml(s.lead)}</p>${s.sections.map((section,i)=>`<section><h4>${escapeHtml(section.title)}</h4><p>${escapeHtml(section.text)} <span class="story-refs">${section.refs.map(sourceLink).join(' ')}</span></p></section>${i===0?photo:''}`).join('')}<aside class="field-note"><p class="eyebrow">在现场，多看一眼</p><p>${escapeHtml(s.watch)}</p></aside><details class="story-sources"><summary>资料与延伸阅读 · ${s.sources.length} 篇</summary><p>正文与照片可离线阅读，以下外部链接需联网。观察场景为科普引导，不是个人实地经历；比喻不代表动物具有人的想法。</p><ol>${s.sources.map(source=>`<li><a href="${escapeHtml(source.url)}" target="_blank" rel="noopener">${escapeHtml(source.title)} ↗</a></li>`).join('')}</ol><p>资料整理：2026 年 9 月。优先采用保护机构、研究机构与论文；较早的物种档案用于基础生活史，不据此推断当前数量或保护等级。</p></details></article>`;
}
function showAnimal(id){
 const a=ANIMALS.find(x=>x.id===id);if(!a)return;
 const similar=a.similar.map(id=>ANIMALS.find(x=>x.id===id)).filter(Boolean);
 $('#detailContent').innerHTML=`<img class="detailPhoto" src="${a.image}" alt="${a.name}"><div class="pad"><p class="eyebrow">${a.label}</p><h2 id="detailName">${a.name}</h2><p class="en">${a.en} <span class="latin"> / ${a.latin}</span></p><section class="quick-identify"><h3>认准这几个特征</h3><ul class="traits">${a.traits.map(t=>`<li>${t}</li>`).join('')}</ul></section><button id="markSeen" class="primary" aria-pressed="${seen.has(id)}">${seen.has(id)?'✓ 见过 · 点击取消':'＋ 见过'}</button>${storyHTML(a)}${similar.length?`<h3>和它们比一比</h3><div class="compare">${similar.map(b=>`<button data-compare="${b.id}"><img src="${b.image}" alt="${b.name}"><span><b>${b.name}</b><br>${b.hint}</span></button>`).join('')}</div>`:''}<p class="credit">识别照片：${escapeHtml(a.credit?.author)} · <a href="${escapeHtml(a.credit?.licenseUrl)}" target="_blank" rel="noopener">${escapeHtml(a.credit?.license)}</a><br><a href="${escapeHtml(a.credit?.source)}" target="_blank" rel="noopener">照片来源与授权 ↗</a><br>照片以缩略图展示，部分已缩小尺寸及压缩。照片为物种示例；雌雄、年龄和个体外观可能不同。</p></div>`;
 $('#markSeen').onclick=()=>{toggleSeen(id);$('#markSeen').textContent=seen.has(id)?'✓ 见过 · 点击取消':'＋ 见过';$('#markSeen').setAttribute('aria-pressed',seen.has(id))};
 $('#detailContent').querySelectorAll('[data-compare]').forEach(b=>b.onclick=()=>showAnimal(b.dataset.compare));
 if(!$('#detail').open)$('#detail').showModal();$('#detail').scrollTop=0;
}
'''
a=a[:start]+new+a[end:]
a=a.replace('种动物的照片和资料。','种动物的照片、识别特征和完整故事。')
p.joinpath('app.js').write_text(a)
i=p.joinpath('index.html').read_text().replace('03 / 坦桑尼亚','04 / 野外故事').replace('照片、名字和识别特征都能离线查看。','29 种动物的照片、名字、识别特征和完整故事都能离线查看。').replace('更新后请补全新增照片，再检查离线状态。','本次加入 29 篇野外故事和 4 张场景照片。更新后请补全离线资料，再检查状态。').replace('<dialog id="detail">','<dialog id="detail" aria-labelledby="detailName">').replace('<script src="./app.js">','<script src="./stories.js"></script><script src="./app.js">')
i=i.replace('<p>9.25—10.1 · 你的 Safari 随身图鉴</p>','<p>9.25—10.1 · 你的 Safari 随身图鉴</p><p class="story-intro">29 种动物 · 看特征认名字，读故事懂生活</p>')
p.joinpath('index.html').write_text(i)
sw=p.joinpath('sw.js').read_text().replace("wild-pocket-v3","wild-pocket-v4").replace("'./habitats.js',","'./habitats.js','./stories.js',")
sw=sw.replace(";const ALL=[...SHELL,...PHOTOS];",";PHOTOS.push(...['elephant','giraffe','wildebeest','ostrich'].map(id=>'./assets/'+id+'-story.jpg'));const ALL=[...SHELL,...PHOTOS];")
p.joinpath('sw.js').write_text(sw)
with p.joinpath('style.css').open('a') as f:f.write('''\n/* Long-form field stories remain part of the offline guide. */
#detail{max-width:700px}.story-intro{font-size:13px!important;margin-top:8px!important}.quick-identify h3{margin-top:22px}.wild-story{border-top:1px solid #ccd5c5;margin-top:32px;padding-top:28px}.wild-story .story-title{font-size:clamp(23px,4.6vw,29px);line-height:1.5;letter-spacing:-.4px;margin:12px 0 18px;text-wrap:pretty}.story-lead{font-size:17px;line-height:1.9;color:#344c3e;border-left:3px solid #acbd68;padding-left:16px}.wild-story section{margin-top:28px}.wild-story h4{font-size:19px;line-height:1.55;margin:0 0 10px}.wild-story section p{font-size:16px;line-height:1.95;margin:0;text-align:left;overflow-wrap:break-word}.story-refs{white-space:nowrap}.reference{font-size:12px;text-decoration:none;color:#516a36;padding:3px 1px}.wild-story a:focus-visible,.wild-story summary:focus-visible{outline:3px solid #738c32;outline-offset:3px}.story-photo{margin:25px -26px;background:#e8ecdf}.story-photo img{width:100%;height:auto;display:block}.story-photo figcaption{font-size:13px;line-height:1.7;padding:13px 26px;color:#52614e}.story-photo small{display:block;font-size:11px;overflow-wrap:anywhere;margin-top:6px}.wild-story a{color:#435b30;text-underline-offset:3px}.field-note{margin:28px 0;padding:20px;background:#e7ecd8;border-radius:12px}.field-note p:last-child{margin:6px 0 0;font-size:15px;line-height:1.85}.story-sources{border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:15px 0;margin:24px 0 30px;font-size:13px;color:var(--muted)}.story-sources summary{cursor:pointer;font-size:14px;font-weight:600;color:var(--ink);min-height:24px}.story-sources p{margin:14px 0 8px;line-height:1.8}.story-sources ol{padding-left:23px}.story-sources li{margin:12px 0;overflow-wrap:anywhere}@media(min-width:561px){#detail .pad{padding:30px 38px}.story-photo{margin-left:-38px;margin-right:-38px}.story-photo figcaption{padding-left:38px;padding-right:38px}}@media(max-width:560px){.story-photo{margin-left:-22px;margin-right:-22px}.story-photo figcaption{padding-left:22px;padding-right:22px}.wild-story{padding-top:24px}.story-lead{font-size:16px}.field-note{padding:17px}.wild-story h4{font-size:18px}}
''')
print('Integrated 29 stories and 4 scene photos.')
