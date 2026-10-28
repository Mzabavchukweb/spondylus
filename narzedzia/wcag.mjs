// Audyt WCAG 2.2 AA (axe-core) wszystkich stron z dist/sitemap.xml + 404, na telefonie i komputerze.
// Wymaga podglądu: python3 -m http.server 8790 --directory dist. Użycie: npm run wcag [-- /adres/ ...]
import { readFileSync } from 'node:fs';
import { chromium } from 'playwright';

const BAZA = process.env.BAZA || 'http://localhost:8790';
const AXE = readFileSync(new URL('../node_modules/axe-core/axe.min.js', import.meta.url), 'utf8');
const mapa = readFileSync(new URL('../dist/sitemap.xml', import.meta.url), 'utf8');
const adresy = process.argv.slice(2).length ? process.argv.slice(2)
  : [...mapa.matchAll(/<loc>https:\/\/spondylus\.pl([^<]*)<\/loc>/g)].map(m => m[1]).concat(['/404.html', '/pakietysportowe/']);
const EKRANY = { telefon: { width: 390, height: 844 }, komputer: { width: 1366, height: 900 } };

const br = await chromium.launch({ channel: 'chrome' });
const zbior = new Map();
const sprawdz = async (ctx, ekran, url) => {
  const p = await ctx.newPage();
  try {
    await p.goto(BAZA + url, { waitUntil: 'domcontentloaded', timeout: 20000 });
    await p.addScriptTag({ content: AXE });
    const wynik = await p.evaluate(async () => (await axe.run(document, {
      runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'] },
    })).violations.map(v => ({ id: v.id, wplyw: v.impact, opis: v.help, wezly: v.nodes.map(n => n.target.join(' ')) })));
    for (const v of wynik) {
      const k = `${v.id} (${v.wplyw}): ${v.opis}`;
      if (!zbior.has(k)) zbior.set(k, new Set());
      v.wezly.slice(0, 3).forEach(w => zbior.get(k).add(`${ekran} ${url} ${w}`));
    }
  } catch (e) { console.log(`błąd ${ekran} ${url}: ${e.message.split('\n')[0]}`); }
  await p.close().catch(() => {});
};
for (const [ekran, vp] of Object.entries(EKRANY)) {
  const ctx = await br.newContext({ viewport: vp });
  await ctx.route(/googletagmanager|google-analytics|proassist/, r => r.abort());
  const kolejka = [...adresy];
  await Promise.all(Array.from({ length: 4 }, async () => { while (kolejka.length) await sprawdz(ctx, ekran, kolejka.shift()); }));
  console.log(`${ekran}: sprawdzono ${adresy.length} stron`);
  await ctx.close();
}
await br.close();
if (!zbior.size) { console.log(`WCAG: bez naruszeń (${adresy.length} stron × 2 ekrany)`); process.exit(0); }
for (const [k, w] of zbior) { console.log(k); [...w].slice(0, 6).forEach(x => console.log('   ', x)); if (w.size > 6) console.log(`    … i ${w.size - 6} więcej`); }
process.exit(1);
