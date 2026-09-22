const app = getApp();
const logic = require('../../utils/logic.js');

Page({
  data: {
    seenCount: 0,
    total: 0,
    percent: 0,
    download: { done: 0, total: 0, failed: 0, complete: false, running: false },
    offlineStatusText: '检查中',
    downloadPercent: 0,
    rarityGroups: [],
    activeRarity: 'common',
    activeAnimals: [],
  },

  onLoad() {
    this.unsubSeen = app.onSeenChange(() => this.render());
    this.unsubDownload = app.onDownloadChange((d) => this.renderDownload(d));
  },

  onShow() {
    this.render();
    this.renderDownload(app.globalData.download);
  },

  onUnload() {
    this.unsubSeen && this.unsubSeen();
    this.unsubDownload && this.unsubDownload();
  },

  onRarity(e) {
    this.setData({ activeRarity: e.currentTarget.dataset.id });
    this.render();
  },

  onOpenAnimal(e) {
    wx.navigateTo({ url: '/pages/detail/detail?id=' + e.currentTarget.dataset.id });
  },

  onOfflineTap() {
    const d = app.globalData.download;
    if (d.running) {
      wx.showToast({ title: `正在下载 ${d.done}/${d.total}`, icon: 'none' });
    } else if (d.complete) {
      wx.showToast({ title: '离线资料已就绪', icon: 'none' });
    } else {
      wx.showModal({
        title: '离线资料未完成',
        content: `已保存 ${d.done}/${d.total} 个文件，是否重新尝试下载？`,
        confirmText: '重新下载',
        success: (r) => { if (r.confirm) app.retryDownload(); },
      });
    }
  },

  renderDownload(d) {
    const complete = d.complete;
    const running = d.running;
    const text = complete ? '已下载' : running ? `下载中 ${d.done}/${d.total}` : '未下载';
    this.setData({
      download: d,
      offlineStatusText: text,
      downloadPercent: d.total ? Math.round((d.done / d.total) * 100) : 0,
    });
  },

  render() {
    const { animals } = app.globalData.data;
    const seen = new Set(app.globalData.seen);
    const total = animals.length;
    const seenCount = seen.size;
    const percent = total ? Math.round((seenCount / total) * 100) : 0;

    const groups = logic.RARITY_GROUPS.map((g) => {
      const list = animals.filter((a) => logic.rarityOf(a) === g.id);
      const seenCountG = list.filter((a) => seen.has(a.id)).length;
      const ratio = list.length ? Math.round((seenCountG / list.length) * 100) : 0;
      return { ...g, animals: list, seenCount: seenCountG, ratio };
    });

    const active = groups.find((g) => g.id === this.data.activeRarity) || groups[0];
    const activeAnimals = active.animals
      .slice()
      .sort((a, b) => Number(seen.has(b.id)) - Number(seen.has(a.id)) || a.name.localeCompare(b.name, 'zh-CN'))
      .map((a) => ({ id: a.id, name: a.name, collected: seen.has(a.id), src: app.resolveSrc(a.image) }));

    this.setData({ seenCount, total, percent, rarityGroups: groups, activeAnimals });
  },
});
