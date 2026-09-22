// Downloads every photo and audio file to local storage on first launch, then
// serves everything from disk. Mirrors the web app's service-worker cache:
// only files missing locally are fetched, so app updates only pull deltas.

const ASSET_BASE = 'https://cdn.jsdelivr.net/gh/kiwiwang519/wildpocket-beast-tracker@main/work/safari/dist/assets/';
const ROOT = wx.env.USER_DATA_PATH + '/assets';

function relPath(p) {
  // "./assets/lion.jpg" -> "lion.jpg" ; "./assets/photos/lion-2.jpg" -> "photos/lion-2.jpg"
  return String(p || '').replace(/^\.\/assets\//, '');
}

function buildManifest(data) {
  const set = new Set();
  for (const a of data.animals) {
    set.add(relPath(a.image));
    const g = data.gallery[a.id] || [];
    for (const p of g) set.add(relPath(p.file));
    const s = data.stories[a.id];
    if (s && s.photo) set.add(relPath(s.photo.image));
    const c = data.calls[a.id];
    if (c) set.add(relPath(c.file));
  }
  return [...set];
}

function localFile(rel) {
  return ROOT + '/' + rel;
}

function exists(rel) {
  try {
    wx.getFileSystemManager().accessSync(localFile(rel));
    return true;
  } catch (e) {
    return false;
  }
}

// Returns a src usable directly in <image>/<audio> right now: the local
// cached copy if we have it, otherwise the CDN URL (still renders online;
// <image>/<audio> src is not subject to the request-domain whitelist).
function resolveSrc(originalPath) {
  const rel = relPath(originalPath);
  if (!rel) return originalPath;
  return exists(rel) ? localFile(rel) : ASSET_BASE + rel;
}

function ensureDirFor(rel) {
  const fs = wx.getFileSystemManager();
  const idx = rel.lastIndexOf('/');
  if (idx < 0) return;
  const dir = ROOT + '/' + rel.slice(0, idx);
  try { fs.mkdirSync(dir, true); } catch (e) { /* already exists */ }
}

function downloadOne(rel) {
  return new Promise((resolve) => {
    ensureDirFor(rel);
    wx.downloadFile({
      url: ASSET_BASE + rel,
      filePath: localFile(rel),
      success: () => resolve({ rel, ok: true }),
      fail: (err) => resolve({ rel, ok: false, err }),
    });
  });
}

const CONCURRENCY = 4;

// onProgress(done, total, failedCount)
async function downloadAll(manifest, onProgress) {
  const todo = manifest.filter((rel) => !exists(rel));
  const total = manifest.length;
  let done = total - todo.length;
  let failed = 0;
  onProgress && onProgress(done, total, failed);
  let i = 0;
  async function worker() {
    while (i < todo.length) {
      const rel = todo[i++];
      const r = await downloadOne(rel);
      if (!r.ok) failed++;
      done++;
      onProgress && onProgress(done, total, failed);
    }
  }
  const workers = [];
  for (let w = 0; w < CONCURRENCY; w++) workers.push(worker());
  await Promise.all(workers);
  return { total, failed };
}

module.exports = { ASSET_BASE, buildManifest, resolveSrc, downloadAll, exists, relPath };
