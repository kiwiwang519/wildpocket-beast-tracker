const app = getApp();
const logic = require('../../utils/logic.js');

const CATEGORIES = ['全部', '有角的', '大型动物', '猫科', '其他哺乳类', '鸟类与爬行类'];

Page({
  data: {
    locations: [],
    routeIndex: 0,
    routeLabel: '',
    period: 'day',
    query: '',
    category: '全部',
    categories: CATEGORIES,
    sortAsc: false,
    onlyUnseen: false,
    list: [],
    seenCountText: '',
  },

  onLoad() {
    const { locations } = app.globalData.data;
    const { route, period } = app.globalData.filters;
    const routeIndex = Math.max(0, locations.findIndex((l) => l.id === route));
    this.setData({ locations, routeIndex, routeLabel: locations[routeIndex].label, period });
    this.unsubSeen = app.onSeenChange(() => this.render());
  },

  onShow() {
    this.render();
  },

  onUnload() {
    this.unsubSeen && this.unsubSeen();
  },

  onRouteChange(e) {
    const idx = Number(e.detail.value);
    const { locations } = app.globalData.data;
    app.globalData.filters.route = locations[idx].id;
    app.persistFilters();
    this.setData({ routeIndex: idx, routeLabel: locations[idx].label });
    this.render();
  },

  onPeriod(e) {
    const period = e.currentTarget.dataset.period;
    app.globalData.filters.period = period;
    app.persistFilters();
    this.setData({ period });
    this.render();
  },

  onSearch(e) {
    this.setData({ query: e.detail.value });
    this.render();
  },

  onCategory(e) {
    this.setData({ category: e.currentTarget.dataset.cat });
    this.render();
  },

  onSort() {
    this.setData({ sortAsc: !this.data.sortAsc });
    this.render();
  },

  onOnlyUnseen() {
    this.setData({ onlyUnseen: !this.data.onlyUnseen });
    this.render();
  },

  onToggleSeen(e) {
    const id = e.currentTarget.dataset.id;
    app.toggleSeen(id);
  },

  openDetail(e) {
    wx.navigateTo({ url: '/pages/detail/detail?id=' + e.currentTarget.dataset.id });
  },

  render() {
    const { animals } = app.globalData.data;
    const { route, period } = app.globalData.filters;
    const { query, category, sortAsc, onlyUnseen } = this.data;
    const seen = new Set(app.globalData.seen);
    const q = (query || '').trim().toLowerCase();

    const filtered = animals.filter((a) => {
      if (route !== 'all' && !a.locations.includes(route)) return false;
      if (!a.periods.includes(period)) return false;
      if (category !== '全部' && !a.groups.includes(category)) return false;
      if (onlyUnseen && seen.has(a.id)) return false;
      if (q) {
        const hay = [a.name, a.en, a.latin, a.hint, ...(a.traits || []), ...(a.tags || []), a.label].join(' ').toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });

    filtered.sort((a, b) => {
      const sa = logic.encounterScore(a, period), sb = logic.encounterScore(b, period);
      return (sortAsc ? sa - sb : sb - sa) || a.name.localeCompare(b.name, 'zh-CN');
    });

    const list = filtered.map((a) => ({
      id: a.id,
      name: a.name,
      en: a.en,
      label: a.label,
      probLabel: logic.encounterLabel(a, period),
      src: app.resolveSrc(a.image),
      isSeen: seen.has(a.id),
    }));

    this.setData({
      list,
      seenCountText: seen.size ? ` · 已见 ${seen.size} 种` : '',
    });
  },
});
