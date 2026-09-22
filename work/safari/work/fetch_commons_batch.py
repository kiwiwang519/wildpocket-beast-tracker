import json, requests, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANIMALS_PATH = ROOT / 'dist' / 'animals.js'
ASSETS = ROOT / 'dist' / 'assets'
API = 'https://commons.wikimedia.org/w/api.php'

def query_file(term):
    params = {'action':'query','generator':'search','gsrsearch':term,'gsrnamespace':6,'gsrlimit':8,'prop':'imageinfo|info','iiprop':'url|extmetadata','iiurlwidth':1200,'format':'json'}
    data = requests.get(API, params=params, timeout=25, headers={'User-Agent':'WildPocketOfflineGuide/1.0'}).json()
    pages = list(data.get('query', {}).get('pages', {}).values())
    for page in pages:
        title = page.get('title', '').lower()
        if title.endswith(('.svg', '.ogg', '.oga', '.webm', '.pdf')):
            continue
        info = (page.get('imageinfo') or [{}])[0]
        url = info.get('thumburl') or info.get('url')
        meta = info.get('extmetadata', {})
        license_name = meta.get('LicenseShortName', {}).get('value', '')
        artist = meta.get('Artist', {}).get('value', 'Wikimedia Commons')
        if url and license_name:
            return url, page.get('title','').replace('File:',''), license_name, artist, 'https://commons.wikimedia.org/wiki/' + page.get('title','').replace(' ','_')
    return None

def main():
    raw = ANIMALS_PATH.read_text()
    animals = json.loads(raw.split('=',1)[1].strip().rstrip(';'))
    session = requests.Session(); session.headers['User-Agent']='WildPocketOfflineGuide/1.0'
    for a in animals:
        if not a.get('commonsQuery'):
            continue
        target = ASSETS / f"{a['id']}.jpg"
        if target.exists() and target.read_bytes()[:4] in (b'\xff\xd8\xff\xe0', b'\xff\xd8\xff\xe1', b'\x89PNG'):
            continue
        if target.exists():
            target.unlink()
        found = None
        for attempt in range(3):
            try:
                found = query_file(a['commonsQuery'])
                break
            except (requests.RequestException, ValueError):
                time.sleep(2 + attempt)
        if not found:
            print('not found', a['id']); continue
        url, title, license_name, artist, source = found
        try:
            response = session.get(url, timeout=45)
            response.raise_for_status()
            if not response.headers.get('content-type','').startswith('image/'):
                raise ValueError('not a raster image')
            target.write_bytes(response.content)
            a['credit'] = {'author': artist, 'license': license_name, 'source': source, 'licenseUrl': 'https://commons.wikimedia.org/wiki/Commons:Licensing'}
            print('saved', a['id'], title)
        except Exception as exc:
            print('failed', a['id'], exc)
    ANIMALS_PATH.write_text('const ANIMALS = ' + json.dumps(animals, ensure_ascii=False) + ';\n')

if __name__ == '__main__': main()
