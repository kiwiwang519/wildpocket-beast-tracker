import json
from pathlib import Path
raw='''lion|狮子|Lion|Panthera leo|猫科|体形厚实，尾端黑色毛簇|成年雄狮通常有鬃毛，雌狮没有。;成年个体通常没有明显斑纹。;尾巴末端有一撮深色毛。|leopard,cheetah
leopard|花豹|Leopard|Panthera pardus|猫科|玫瑰状花斑，体形结实|花纹多为中间较浅的环状玫瑰斑。;四肢粗壮，头部比猎豹宽。;脸上没有猎豹那样明显的黑色泪痕。|cheetah,lion
cheetah|猎豹|Cheetah|Acinonyx jubatus|猫科|黑色泪痕，实心圆斑|从眼角到嘴角有明显黑色泪痕。;身上是实心黑色圆点，不是玫瑰状环斑。;身材纤细、腿长，头相对小。|leopard,hyena
hyena|斑鬣狗|Spotted hyena|Crocuta crocuta|其他哺乳类|圆耳，前高后低的背线|圆耳、宽口鼻，颈肩粗壮。;前肢较长，背部向臀部倾斜。;黄灰色皮毛上散布深色斑点。|cheetah
elephant|非洲草原象|African bush elephant|Loxodonta africana|大型动物|大耳朵，长鼻子|耳朵非常大，轮廓宽阔。;长鼻可卷曲，成年个体常有象牙。;幼象象牙可能不明显。|rhino
buffalo|非洲水牛|African buffalo|Syncerus caffer|大型动物|深色身体，粗壮弯角|体形敦实，身体多为深褐或黑色。;角向两侧伸出，再向上弯。;成年雄性额头常有厚实相连的角基。|wildebeest
rhino|黑犀牛|Black rhinoceros|Diceros bicornis|大型动物|两只鼻角，尖上唇|鼻上通常有前后两只角，前角较长。;上唇较尖，适合抓取枝叶。;肤色不能可靠区分黑犀牛和白犀牛。|hippo
hippo|河马|Hippopotamus|Hippopotamus amphibius|大型动物|圆桶身材，眼鼻长在头顶|身体巨大、腿短，皮肤几乎无毛。;眼睛、耳朵和鼻孔位置较高。;常见于水中，露出的头部也很宽厚。|rhino
giraffe|马赛长颈鹿|Masai giraffe|Giraffa tippelskirchi|大型动物|长脖子，锯齿状斑块|脖子和腿特别长，头顶有皮毛覆盖的小角。;深色斑块通常边缘不规则、呈锯齿状。;不同长颈鹿种类可相似，地点和花纹需一起看。|
zebra|平原斑马|Plains zebra|Equus quagga|大型动物|黑白条纹，体形像马|全身黑白条纹，直立的短鬃毛。;耳朵相对较小，不像细纹斑马那样大而圆。;幼驹深色条纹可能偏棕色。|wildebeest
wildebeest|蓝角马|Blue wildebeest|Connochaetes taurinus|有角的|牛一样的头，披着鬃毛|头宽、肩高，有鬃毛和喉下长毛。;双角向侧面伸出再向上弯。;灰褐色身体常有较暗的竖纹。|buffalo,topi
impala|黑斑羚|Impala|Aepyceros melampus|有角的|红棕背毛，臀部黑色竖纹|体色红棕，腹部白色。;臀部有黑色竖纹，与尾部一起形成醒目标记。;雄性有细长弯曲的角，雌性无角。|thomson,grant
thomson|汤氏瞪羚|Thomson’s gazelle|Eudorcas thomsonii|有角的|体形小，侧腹黑色横带|身体较小，背部黄褐、腹部白色。;身体侧面通常有一道明显黑色横带。;臀部白色区域通常不向上延伸过尾根。|grant,impala
grant|格兰特瞪羚|Grant’s gazelle|Nanger granti|有角的|较大瞪羚，白臀延伸过尾根|通常比汤氏瞪羚大。;臀部白色斑块向上延伸到尾根上方。;成年个体侧腹通常没有汤氏瞪羚那样粗重的黑带。|thomson,impala
topi|托皮转角牛羚|Topi|Damaliscus lunatus complex|有角的|棕红身体，大腿有深色斑|身体棕红色，肩部及大腿常有深色斑块。;脸部较长，角向后弯。;前肩较高，常站在开阔地或土丘上。|wildebeest,eland
eland|大羚羊|Common eland|Taurotragus oryx|有角的|巨大的羚羊，短螺旋角|体形很大，外形有些像牛。;雌雄通常都有较直的螺旋角。;喉下有垂皮，体侧竖纹明显程度因个体而异。|topi,buffalo
warthog|普通疣猪|Common warthog|Phacochoerus africanus|其他哺乳类|脸有疣突，獠牙向上弯|头大，面部两侧有明显的疣状突起。;上獠牙向两侧、向上弯曲。;奔跑时尾巴常像小旗杆一样竖起来。|
baboon|东非狒狒|Olive baboon|Papio anubis|其他哺乳类|长口鼻，橄榄灰色毛|吻部突出，像狗的长口鼻。;体毛灰绿至灰褐色，成年雄性更粗壮。;尾巴有明显弯折，不是抓握用的尾巴。|
ostrich|普通鸵鸟|Common ostrich|Struthio camelus|鸟类与爬行类|很大的鸟，长腿长脖子|体形巨大，无法飞行，颈和腿很长。;成年雄鸟通常黑身白翼，雌鸟多灰褐色。;每只脚只有两趾。|
crocodile|尼罗鳄|Nile crocodile|Crocodylus niloticus|鸟类与爬行类|长吻、背甲、粗壮长尾|身体贴地，背部有成排隆起的鳞甲。;长而有力的尾巴帮助游泳。;常在岸边晒太阳或只露出水面的眼鼻。|hippo'''
a=[]
for row in raw.splitlines():
 id,name,en,latin,group,hint,traits,similar=row.split('|')
 a.append(dict(id=id,name=name,en=en,latin=latin,groups=[group]+(['有角的'] if id in ['buffalo','rhino','giraffe'] else []),label=group,hint=hint,traits=traits.split(';'),similar=similar.split(',') if similar else [],tags='羚羊' if group=='有角的' else '',image=f'./assets/{id}.jpg',source='https://en.wikipedia.org/wiki/'+en.replace('’',"'").replace(' ','_')))
Path('dist/animals.js').write_text('const ANIMALS = '+json.dumps(a,ensure_ascii=False)+';\n')
