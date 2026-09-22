const data = require('./data/data.json');
const offline = require('./utils/offline.js');

App({
  globalData: {
    data,
    seen: [],
    filters: { route: 'all', period: 'day' },
    download: { done: 0, total: 0, failed: 0, complete: false, running: false },
    listeners: [],
  },

  onLaunch() {
    try {
      const seen = wx.getStorageSync('safari-seen');
      if (Array.isArray(seen)) this.globalData.seen = seen.filter((id) => data.animals.some((a) => a.id === id));
    } catch (e) {}
    try {
      const filters = wx.getStorageSync('safari-filters');
      if (filters && data.locations.some((l) => l.id === filters.route)) this.globalData.filters.route = filters.route;
      if (filters && ['day', 'night'].includes(filters.period)) this.globalData.filters.period = filters.period;
    } catch (e) {}
    this.startOfflineDownload();
  },

  // Pages call this in onShow to get progress pushes without a full re-render loop.
  onDownloadChange(fn) {
    this.globalData.listeners.push(fn);
    return () => {
      this.globalData.listeners = this.globalData.listeners.filter((f) => f !== fn);
    };
  },

  notifyDownload() {
    this.globalData.listeners.forEach((fn) => {
      try { fn(this.globalData.download); } catch (e) {}
    });
  },

  startOfflineDownload() {
    if (this.globalData.download.running || this.globalData.download.complete) return;
    const manifest = offline.buildManifest(data);
    this.globalData.download.running = true;
    this.globalData.download.total = manifest.length;
    this.notifyDownload();
    offline.downloadAll(manifest, (done, total, failed) => {
      this.globalData.download.done = done;
      this.globalData.download.total = total;
      this.globalData.download.failed = failed;
      this.notifyDownload();
    }).then(({ total, failed }) => {
      this.globalData.download.running = false;
      this.globalData.download.complete = failed === 0;
      this.notifyDownload();
    });
  },

  retryDownload() {
    this.globalData.download.complete = false;
    this.startOfflineDownload();
  },

  toggleSeen(id) {
    const seen = new Set(this.globalData.seen);
    if (seen.has(id)) seen.delete(id); else seen.add(id);
    this.globalData.seen = [...seen];
    try { wx.setStorageSync('safari-seen', this.globalData.seen); } catch (e) {
      wx.showToast({ title: '本机未能保存记录', icon: 'none' });
    }
    this.notifySeenChange();
  },

  onSeenChange(fn) {
    this.seenListeners = this.seenListeners || [];
    this.seenListeners.push(fn);
    return () => { this.seenListeners = this.seenListeners.filter((f) => f !== fn); };
  },
  notifySeenChange() {
    (this.seenListeners || []).forEach((fn) => { try { fn(this.globalData.seen); } catch (e) {} });
  },

  persistFilters() {
    try { wx.setStorageSync('safari-filters', this.globalData.filters); } catch (e) {}
  },

  resolveSrc(path) {
    return offline.resolveSrc(path);
  },
});
