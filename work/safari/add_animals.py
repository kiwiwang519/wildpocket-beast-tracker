from pathlib import Path
import json
p=Path('dist/animals.js');data=json.loads(p.read_text().removeprefix('const ANIMALS = ').strip().removesuffix(';'))
raw='''waterbuck|水羚|Waterbuck|Kobus ellipsiprymnus|有角的|毛发蓬松，臀部白环或白斑|毛色灰褐，毛发比许多羚羊更粗长。;雄性有长而向后弯的环纹角，雌性无角。;不同亚种臀部有白环或整片白斑，不能只记住白环。|impala,eland
hartebeest|狷羚|Hartebeest|Alcelaphus buselaphus|有角的|脸长、肩高，角有折弯|脸部细长，额头较高，前肩明显高于臀部。;雌雄通常都有角，角在高额头上向外或向后弯折。;东非常见科氏狷羚；不同亚种角形和毛色有差异。|topi,wildebeest
 dikdik|柯氏犬羚|Kirk’s dik-dik|Madoqua kirkii|有角的|小巧羚羊，尖长鼻和大眼睛|体形很小，腿纤细，常在灌丛边出现。;眼睛大，口鼻尖长，头顶有小毛簇。;雄性有短小的角，可能被毛簇遮住。|thomson,impala
jackal|黑背胡狼|Black-backed jackal|Lupulella mesomelas|其他哺乳类|黑银色背鞍，尖耳长口鼻|背部有明显黑银色的鞍状毛区。;体侧和腿多为红棕色，耳朵尖而直立。;尾巴蓬松、末端黑色，不是斑鬣狗的圆耳壮肩。|bateared,hyena
serval|薮猫|Serval|Leptailurus serval|猫科|大耳朵、长腿、短尾巴|耳朵相对于头部特别大，腿很长。;金黄色身体带黑色斑点与短条纹。;尾巴较短，体形比猎豹小，脸上没有明显黑色泪痕。|cheetah,leopard
bateared|大耳狐|Bat-eared fox|Otocyon megalotis|其他哺乳类|一对巨大的耳朵，黑色腿脚|耳朵又大又宽，外形像蝙蝠耳。;身体灰黄，口鼻及腿脚偏黑。;体形小，尾巴蓬松，常低头在地面觅食。|jackal,hyena
crane|灰冠鹤|Grey crowned crane|Balearica regulorum|鸟类与爬行类|金色羽冠，灰色长脖子|头顶是一圈放射状金色羽毛。;长脖子灰色，脸颊有醒目的白色区域。;喉下有红色肉垂，翅上有白色与褐金色羽区。|secretary
secretary|蛇鹫|Secretarybird|Sagittarius serpentarius|鸟类与爬行类|长腿猛禽，脑后黑色翎羽|身体灰白，腿很长，大腿黑色像穿了短裤。;后脑有向后伸出的黑色羽簇。;脸部裸皮橙红色，喙弯曲，常在草地上行走。|crane,bustard
bustard|柯利鸟|Kori bustard|Ardeotis kori|鸟类与爬行类|体形粗壮的大鸟，灰颈褐背|背部褐色斑驳，颈部灰白并有细纹。;体形厚重、长腿，常在地上缓慢行走。;头顶有黑色羽冠，和长脖子鸵鸟的体态不同。|ostrich,secretary'''
for row in raw.splitlines():
 id,name,en,latin,group,hint,traits,similar=row.strip().split('|')
 if any(x['id']==id for x in data):continue
 data.append(dict(id=id,name=name,en=en,latin=latin,groups=[group],label=group,hint=hint,traits=traits.split(';'),similar=similar.split(','),tags='羚羊' if group=='有角的' else '',image=f'./assets/{id}.jpg',source='https://en.wikipedia.org/wiki/'+en.replace('’',"'").replace(' ','_')))
for a in data:
 if a['id']=='cheetah':a['similar']=['leopard','serval']
 if a['id']=='topi':a['similar']=['hartebeest','wildebeest']
 if a['id']=='hyena':a['similar']=['jackal','bateared']
p.write_text('const ANIMALS = '+json.dumps(data,ensure_ascii=False)+';\n')
