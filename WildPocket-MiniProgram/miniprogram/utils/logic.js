// Ported 1:1 from work/safari/dist/app.js so the ranking and rarity math match the web app exactly.

const encounterBase = {lion:25,leopard:10,cheetah:14,hyena:38,elephant:72,buffalo:70,rhino:8,hippo:32,giraffe:56,zebra:82,wildebeest:86,impala:88,thomson:76,grant:62,topi:45,eland:30,warthog:50,baboon:54,ostrich:42,crocodile:22,waterbuck:34,hartebeest:28,dikdik:18,jackal:30,serval:8,bateared:12,crane:18,secretary:11,bustard:20};
const nightLift = {lion:1.15,leopard:1.65,cheetah:.7,hyena:1.45,elephant:1.05,buffalo:1.2,rhino:.75,hippo:1.35,giraffe:.55,zebra:.65,wildebeest:.7,impala:.8,thomson:.7,grant:.7,topi:.7,eland:.7,warthog:1.05,baboon:.55,ostrich:.45,crocodile:.8,waterbuck:.95,hartebeest:.65,dikdik:1.15,jackal:1.4,serval:1.75,bateared:1.8,crane:.5,secretary:.45,bustard:.5};
const birds = new Set(['ostrich','crane','secretary','bustard']);
const reptiles = new Set(['crocodile']);
const RARITY_GROUPS = [{id:'common',name:'常见',min:55},{id:'uncommon',name:'少见',min:20},{id:'rare',name:'稀有',min:0}];

function kindOf(a) {
  return birds.has(a.id) ? '鸟类' : reptiles.has(a.id) ? '爬行动物' : '哺乳动物';
}

function encounterScore(a, period) {
  const raw = encounterBase[a.id] || 20;
  const periodFactor = period === 'night' ? (nightLift[a.id] || 1) : 1;
  return Math.max(1, Math.min(95, Math.round(raw * periodFactor)));
}

function encounterLabel(a, period) {
  return `约 ${encounterScore(a, period)}%`;
}

function rarityOf(a) {
  const score = encounterBase[a.id] || 20;
  return score >= 55 ? 'common' : score >= 20 ? 'uncommon' : 'rare';
}

module.exports = { encounterBase, nightLift, kindOf, encounterScore, encounterLabel, rarityOf, RARITY_GROUPS };
