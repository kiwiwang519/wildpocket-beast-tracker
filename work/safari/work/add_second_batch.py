import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'dist' / 'animals.js'

SPECIES = [
 ('bushbuck','薮羚','Bushbuck','Tragelaphus sylvaticus','有角的','红褐到深褐色，体侧常有白色条纹','bushbuck', ['tarangire','central','north','mara','rim'], ['day','night']),
 ('genet','非洲灵猫','Common genet','Genetta genetta','其他哺乳类','细长身形，长环纹尾，常夜行','common genet', ['tarangire','central','north','mara','rim'], ['night']),
 ('civet','非洲麝猫','African civet','Civettictis civetta','其他哺乳类','体侧黑白斑纹，背上有竖起的鬃毛','african civet', ['tarangire','central','north','mara','rim'], ['night']),
 ('groundhornbill','南方地犀鸟','Southern ground hornbill','Bucorvus leadbeateri','鸟类与爬行类','大型黑鸟，脸和喉部鲜红，常在地面行走','southern ground hornbill', ['tarangire','central','north','mara'], ['day']),
 ('martialeagle','猛雕','Martial eagle','Polemaetus bellicosus','鸟类与爬行类','大型猛禽，腹部有深色斑点','martial eagle', ['tarangire','central','north','mara','rim','crater'], ['day']),
 ('bateleur','短尾雕','Bateleur','Terathopius ecaudatus','鸟类与爬行类','翼下黑白分明，尾很短，常低空盘旋','bateleur eagle', ['tarangire','central','north','mara','rim','crater'], ['day']),
 ('fisheagle','非洲鱼鹰','African fish eagle','Icthyophaga vocifer','鸟类与爬行类','白头白胸、栗色身体，常停在水边高枝','african fish eagle', ['tarangire','central','north','mara','crater'], ['day']),
 ('roller','丁香胸佛法僧','Lilac-breasted roller','Coracias caudatus','鸟类与爬行类','胸部丁香紫、翅膀亮蓝绿','lilac breasted roller', ['tarangire','central','north','mara','rim','crater'], ['day']),
 ('starling','艳丽椋鸟','Superb starling','Lamprotornis superbus','鸟类与爬行类','蓝绿色背，橙色腹部并有白胸带','superb starling', ['tarangire','central','north','mara','rim','crater'], ['day']),
 ('greaterflamingo','大火烈鸟','Greater flamingo','Phoenicopterus roseus','鸟类与爬行类','粉白色体羽，喙尖黑，颈很长','greater flamingo', ['crater'], ['day']),
 ('vulture','白背兀鹫','White-backed vulture','Gyps africanus','鸟类与爬行类','大型褐色食腐鸟，背部有浅色羽毛','white backed vulture', ['tarangire','central','north','mara','rim','crater'], ['day']),
 ('egyptiangoose','埃及雁','Egyptian goose','Alopochen aegyptiaca','鸟类与爬行类','眼周深色斑，水边常成对出现','egyptian goose', ['tarangire','central','north','mara','crater'], ['day']),
 ('yellowstork','黄嘴鹳','Yellow-billed stork','Mycteria ibis','鸟类与爬行类','白色大鹳，黄嘴略向下弯','yellow billed stork', ['tarangire','central','north','mara','crater'], ['day']),
 ('ibis','非洲圣鹮','African sacred ibis','Threskiornis aethiopicus','鸟类与爬行类','白色身体、黑色头颈和长弯喙','african sacred ibis', ['tarangire','central','north','mara','crater'], ['day']),
 ('monitor','尼罗巨蜥','Nile monitor','Varanus niloticus','鸟类与爬行类','体长而粗壮，黄黑斑纹，常在水边','nile monitor', ['tarangire','central','north','mara','crater'], ['day']),
]

def main():
 raw=PATH.read_text(); data=json.loads(raw.split('=',1)[1].strip().rstrip(';')); ids={a['id'] for a in data}
 for ident,cn,en,latin,label,hint,query,locations,periods in SPECIES:
  if ident not in ids:
   data.append({'id':ident,'name':cn,'en':en,'latin':latin,'groups':[label],'label':label,'hint':hint,'traits':[hint,'请结合栖息地、体形和活动时段综合判断。'],'similar':[],'tags':'扩展图鉴','image':f'./assets/{ident}.jpg','source':'','credit':{'author':'Wikimedia Commons','license':'待核对','source':'','licenseUrl':''},'locations':locations,'periods':periods,'commonsQuery':query})
 PATH.write_text('const ANIMALS = '+json.dumps(data,ensure_ascii=False)+';\n')

if __name__=='__main__': main()
