import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANIMALS = ROOT / 'dist' / 'animals.js'

# First expansion batch: conspicuous or often-requested safari species.
SPECIES = [
  ('wilddog','非洲野犬','African wild dog','Lycaon pictus','其他哺乳类','群居犬科，花斑皮毛和大圆耳','wild dogs africans', ['tarangire','central','north','mara','rim'], ['day','night']),
  ('vervet','绿猴','Vervet monkey','Chlorocebus pygerythrus','其他哺乳类','灰绿色毛，黑脸边缘有白色鬓毛','vervet monkey', ['tarangire','central','north','mara','rim','crater'], ['day']),
  ('reedbuck','山苇羚','Mountain reedbuck','Redunca fulvorufula','有角的','灰褐色小羚羊，雄性角向前弯','mountain reedbuck', ['rim'], ['day']),
  ('bushbuck','薮羚','Bushbuck','Tragelaphus sylvaticus','有角的','红褐到深褐色，体侧常有白色条纹','bushbuck', ['tarangire','central','north','mara','rim'], ['day','night']),
  ('kudu','大捻角羚','Greater kudu','Tragelaphus strepsiceros','有角的','雄性长螺旋角，体侧细白条纹','greater kudu', ['tarangire','rim'], ['day','night']),
  ('gerenuk','长颈羚','Gerenuk','Litocranius walleri','有角的','颈和腿很长，常以后腿站立取食','gerenuk', ['tarangire'], ['day']),
  ('duiker','普通小羚羊','Common duiker','Sylvicapra grimmia','有角的','小型灰褐羚羊，受惊时钻入灌丛','common duiker', ['tarangire','central','north','mara','rim'], ['day','night']),
  ('genet','非洲灵猫','African genet','Genetta genetta','其他哺乳类','细长身形，长环纹尾，常夜行','common genet', ['tarangire','central','north','mara','rim'], ['night']),
  ('civet','非洲麝猫','African civet','Civettictis civetta','其他哺乳类','体侧黑白斑纹，背上有竖起的鬃毛','african civet', ['tarangire','central','north','mara','rim'], ['night']),
  ('honeybadger','蜜獾','Honey badger','Mellivora capensis','其他哺乳类','背部灰白、腹部黑，低矮粗壮','honey badger', ['tarangire','central','north','mara','rim'], ['day','night']),
  ('mongoose','条纹獴','Banded mongoose','Mungos mungo','其他哺乳类','成群活动，背部有横向深色条纹','banded mongoose', ['tarangire','central','north','mara','rim','crater'], ['day']),
  ('caracal','狞猫','Caracal','Caracal caracal','猫科','红褐色，耳尖有明显黑色长簇毛','caracal', ['tarangire','central','north','mara','rim','crater'], ['day','night']),
  ('aardwolf','土狼','Aardwolf','Proteles cristata','其他哺乳类','像小鬣狗，前肢条纹明显，主食白蚁','aardwolf', ['tarangire','central','north','mara','crater'], ['night']),
  ('flamingo','小火烈鸟','Lesser flamingo','Phoeniconaias minor','鸟类与爬行类','粉红色群鸟，黑色喙尖，常在碱湖活动','lesser flamingo', ['crater'], ['day']),
  ('groundhornbill','南方地犀鸟','Southern ground hornbill','Bucorvus leadbeateri','鸟类与爬行类','大型黑鸟，脸和喉部鲜红，常在地面行走','southern ground hornbill', ['tarangire','central','north','mara'], ['day']),
  ('martialeagle','猛雕','Martial eagle','Polemaetus bellicosus','鸟类与爬行类','大型猛禽，腹部有深色斑点','martial eagle', ['tarangire','central','north','mara','rim','crater'], ['day']),
  ('bateleur','短尾雕','Bateleur','Terathopius ecaudatus','鸟类与爬行类','翼下黑白分明，尾很短，常低空盘旋','bateleur eagle', ['tarangire','central','north','mara','rim','crater'], ['day']),
  ('fisheagle','非洲鱼鹰','African fish eagle','Icthyophaga vocifer','鸟类与爬行类','白头白胸、栗色身体，常停在水边高枝','african fish eagle', ['tarangire','central','north','mara','crater'], ['day']),
  ('roller','丁香胸佛法僧','Lilac-breasted roller','Coracias caudatus','鸟类与爬行类','胸部丁香紫、翅膀亮蓝绿','lilac breasted roller', ['tarangire','central','north','mara','rim','crater'], ['day']),
  ('starling','艳丽椋鸟','Superb starling','Lamprotornis superbus','鸟类与爬行类','蓝绿色背，橙色腹部并有白胸带','superb starling', ['tarangire','central','north','mara','rim','crater'], ['day']),
]

def main():
    raw = ANIMALS.read_text()
    existing = json.loads(raw.split('=', 1)[1].strip().rstrip(';'))
    existing_ids = {item['id'] for item in existing}
    for ident, cn, en, latin, label, hint, query, locations, periods in SPECIES:
        if ident in existing_ids:
            continue
        existing.append({
            'id': ident, 'name': cn, 'en': en, 'latin': latin, 'groups': [label], 'label': label,
            'hint': hint, 'traits': [hint, '请结合栖息地、体形和活动时段综合判断。'],
            'similar': [], 'tags': '扩展图鉴', 'image': f'./assets/{ident}.jpg',
            'source': '', 'credit': {'author': 'Wikimedia Commons', 'license': '待核对', 'source': '', 'licenseUrl': ''},
            'locations': locations, 'periods': periods, 'commonsQuery': query,
        })
    ANIMALS.write_text('const ANIMALS = ' + json.dumps(existing, ensure_ascii=False) + ';\n')

if __name__ == '__main__':
    main()
