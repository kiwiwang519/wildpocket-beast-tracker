const app = getApp();
const logic = require('../../utils/logic.js');

Page({
  data: {
    animal: null,
    images: [],
    current: 0,
    galleryHeight: 420,
    probLabel: '',
    call: null,
    playing: false,
    soundInfoOpen: false,
    story: null,
    similar: [],
    morePhotoLines: [],
    isSeen: false,
  },

  onLoad(options) {
    const sys = wx.getWindowInfo ? wx.getWindowInfo() : wx.getSystemInfoSync();
    const galleryHeight = Math.min(Math.round(sys.windowHeight * 0.56), 520);
    this.id = options.id;
    this.setData({ galleryHeight });
    this.load();
    this.unsubSeen = app.onSeenChange(() => this.refreshSeen());
  },

  onUnload() {
    this.audio && this.audio.destroy();
    this.unsubSeen && this.unsubSeen();
  },

  load() {
    const { animals, stories, calls, gallery } = app.globalData.data;
    const animal = animals.find((a) => a.id === this.id);
    if (!animal) return;

    const images = [app.resolveSrc(animal.image)];
    const story = stories[this.id] || null;
    if (story && story.photo && story.photo.image !== animal.image) images.push(app.resolveSrc(story.photo.image));
    const extra = gallery[this.id] || [];
    extra.forEach((p) => images.push(app.resolveSrc(p.file)));

    const morePhotoLines = extra.map((p, i) => {
      const n = (story && story.photo ? 3 : 2) + i;
      return `第 ${n} 张 ${p.author} · ${p.license}`;
    });

    const similar = (animal.similar || []).map((sid) => animals.find((a) => a.id === sid)).filter(Boolean)
      .map((a) => ({ id: a.id, name: a.name, hint: a.hint, src: app.resolveSrc(a.image) }));

    const call = calls[this.id] || null;
    if (this.audio) { this.audio.destroy(); this.audio = null; }
    if (call) {
      this.audio = wx.createInnerAudioContext();
      this.audio.src = app.resolveSrc(call.file);
      this.audio.onPlay(() => this.setData({ playing: true }));
      this.audio.onPause(() => this.setData({ playing: false }));
      this.audio.onStop(() => this.setData({ playing: false }));
      this.audio.onEnded(() => this.setData({ playing: false }));
    }

    this.setData({
      animal,
      images,
      current: 0,
      probLabel: logic.encounterLabel(animal, app.globalData.filters.period),
      call,
      story,
      similar,
      morePhotoLines,
    });
    this.refreshSeen();
  },

  refreshSeen() {
    this.setData({ isSeen: app.globalData.seen.includes(this.id) });
  },

  onSwiper(e) {
    this.setData({ current: e.detail.current });
  },

  onPlaySound() {
    if (!this.audio) return;
    if (this.data.playing) this.audio.pause(); else this.audio.play();
  },

  onToggleInfo() {
    this.setData({ soundInfoOpen: !this.data.soundInfoOpen });
  },

  onToggleSeen() {
    app.toggleSeen(this.id);
  },

  onOpenSimilar(e) {
    this.id = e.currentTarget.dataset.id;
    this.load();
    wx.pageScrollTo({ scrollTop: 0, duration: 0 });
  },
});
