import { taxDE, de0 } from './utils.js';

// ── PENSION ────────────────────────────────────────────────────────────────
export const MINDEST = {
  'Baden-Württemberg': 1936, 'Bayern': 1920, 'Berlin': 1810, 'Brandenburg': 1780,
  'Bremen': 1800, 'Hamburg': 1940, 'Hessen': 1880, 'Mecklenburg-Vorpommern': 1730,
  'Niedersachsen': 1800, 'Nordrhein-Westfalen': 1850, 'Rheinland-Pfalz': 1790,
  'Saarland': 1760, 'Sachsen': 1740, 'Sachsen-Anhalt': 1740,
  'Schleswig-Holstein': 1800, 'Thüringen': 1740, 'Bund (Bundesbeamte)': 1870
};
export const LAENDER = Object.keys(MINDEST);

export const BESO = {
  'A9':  [2720,2820,2930,3050,3150,3250,3350,3450,3550,3630,3700,3700],
  'A10': [2950,3060,3190,3330,3460,3590,3720,3850,3980,4110,4110,4110],
  'A11': [3260,3400,3560,3730,3900,4080,4250,4430,4620,4800,4980,4980],
  'A12': [3580,3730,3920,4110,4310,4510,4710,4920,5130,5340,5550,5750],
  'A13': [4150,4320,4510,4720,4940,5170,5400,5630,5860,5860,5860,5860],
  'A14': [4500,4700,4920,5160,5410,5660,5910,6160,6420,6420,6420,6420],
  'A15': [4980,5210,5460,5720,5990,6260,6540,6810,7090,7360,7360,7360],
  'A16': [5510,5780,6060,6360,6660,6960,7270,7550,7550,7550,7550,7550],
  'B3':  [6800,6800,6800,6800,6800,6800,6800,6800,6800,6800,6800,6800],
  'B4':  [7200,7200,7200,7200,7200,7200,7200,7200,7200,7200,7200,7200],
};
export const BESO_KEYS = Object.keys(BESO);

export function getBeso(gr, st) {
  const t = BESO[gr] || BESO['A13'];
  return t[Math.min(Math.max(parseInt(st) - 1, 0), 11)] || 4000;
}

export function defaultP() {
  return {
    gebdat: '14.08.1986', dienst: '01.09.2012', bund: 'Nordrhein-Westfalen', kirche: 'Nein',
    bGr: 'A13', bSt: '8', zusatz: 0, pGr: 'A14', pSt: '10', pZusatz: 120,
    eltern: false, elternJ: 2.5, beurl: false, beurlJ: 0,
    tz: false, tzJ: 6, tzPct: 75, pensAlter: 67, lebErw: 87,
    steigerung: 1.8, kv: 'GKV', kvB: 380, beihilfe: 70, zielEur: 3000, vorsorge: 0
  };
}

export function calcP(P) {
  const yr = new Date().getFullYear();
  const gb = parseInt((P.gebdat || '').split('.')[2]) || 1986;
  const ej = parseInt((P.dienst || '').split('.')[2]) || 2012;
  const alter = yr - gb, jbp = Math.max(P.pensAlter - alter, 0);
  let dj = Math.max(yr - ej, 0);
  if (P.beurl) dj = Math.max(dj - P.beurlJ, 0);
  let djK = dj;
  if (P.tz && P.tzJ > 0) {
    const vz = dj - P.tzJ;
    djK = Math.max(vz, 0) + P.tzJ * (P.tzPct / 100);
  }
  const gdj = djK + jbp, satz = Math.min(gdj * 0.0179375, 0.7175);
  const mindest = MINDEST[P.bund] || 1850;
  const aktB = getBeso(P.bGr, P.bSt) + (P.zusatz || 0);
  const pB = getBeso(P.pGr, P.pSt) + (P.pZusatz || 0);
  const eg = pB * Math.pow(1 + P.steigerung / 100, jbp);
  const brutto = Math.max(eg * satz, mindest);
  const jb = brutto * 12, vfb = Math.min(jb * 0.144, 1080);
  const zvE = Math.max(jb - vfb - 102, 0);
  const tax = taxDE(zvE, P.kirche === 'Ja');
  const stM = tax.tot / 12;
  let kv = P.kv === 'PKV' ? P.kvB * (1 - P.beihilfe / 100) : brutto * 0.083;
  const pv = brutto * 0.034, kvpv = kv + pv;
  const netto = brutto - stM - kvpv;
  const nettoR = netto / Math.pow(1.021, jbp);
  const luecke = Math.max(P.zielEur - netto, 0);
  const jruh = Math.max(P.lebErw - P.pensAlter, 0);
  const kum = netto * 12 * jruh, kapB = luecke * 12 * jruh;
  const r = 0.035 / 12, n = jbp * 12;
  const vwert = n > 0 ? (P.vorsorge || 0) * ((Math.pow(1 + r, n) - 1) / r) : 0;
  const restK = Math.max(kapB - vwert, 0);
  let spar = 0; if (restK > 0 && n > 0) spar = (r * restK) / (Math.pow(1 + r, n) - 1);
  return { alter, jbp, gdj: Math.round(gdj * 10) / 10, satz, eg, brutto, stM, kvpv, netto, nettoR, luecke, kum, kapB, restK, spar, pensJ: yr + jbp, jruh, aktB, mindest, vfb, zvE, tax };
}

export const PS_LABELS = [
  { label: 'Stammdaten', ey: 'Stammdaten', title: 'Wer bist du — und wann hast du angefangen?', desc: 'Geburtsdatum, Diensteintritt, Bundesland und Kirchensteuerpflicht legen das Fundament.' },
  { label: 'Akt. Besoldung', ey: 'Aktuelle Besoldung', title: 'Was verdienst du heute?', desc: 'Besoldungsgruppe und Erfahrungsstufe nach Besoldungsordnung A, B oder W (BW-Tabelle 2025).' },
  { label: 'Perspektive', ey: 'Perspektivische Besoldung', title: 'Wo siehst du dich am Ende deiner Laufbahn?', desc: 'Pensora rechnet die voraussichtliche Endbesoldung in den Ruhegehaltssatz ein.' },
  { label: 'Zeiterfassung', ey: 'Zeiterfassung', title: 'Hattest du Phasen mit reduzierter Dienstzeit?', desc: 'Elternzeit, Beurlaubung und Teilzeit wirken sich unterschiedlich aus (§ 6, § 9, § 12a BeamtVG).' },
  { label: 'Annahmen', ey: 'Annahmen', title: 'Wie stellst du dir deinen Ruhestand vor?', desc: 'Pensionseintrittsalter, Lebenserwartung und Besoldungssteigerung.' },
  { label: 'KV', ey: 'Krankenversicherung', title: 'GKV oder PKV im Ruhestand?', desc: 'Beamte haben Beihilfeanspruch im Ruhestand — das senkt den KV-Eigenanteil.' },
  { label: 'Ziel', ey: 'Versorgungsziel', title: 'Mit wie viel Geld möchtest du im Ruhestand leben?', desc: 'Gib deinen monatlichen Netto-Wunschbetrag an — Pensora berechnet die Versorgungslücke.' },
];

// ── RENTE ──────────────────────────────────────────────────────────────────
export const GRV = { rv: 40.79, rv2026: 42.52, de: 50493, bbg: 96600 };

export function defaultR() {
  return { gebdat: '01.01.1985', rentAlter: 67, djBeginn: 2010, brutto: 60000, wachstum: 2.0, kirche: 'Nein', ra: 1.8, inf: 2.1, lebErw: 87, vorsorge: 0, zielEur: 2500 };
}

export function calcR(R) {
  const yr = new Date().getFullYear();
  const gb = parseInt((R.gebdat || '').split('.')[2]) || 1985;
  const alter = yr - gb, jbr = Math.max(R.rentAlter - alter, 0);
  const arbJ = Math.max(yr - R.djBeginn, 0), gesJ = arbJ + jbr;
  const ep = Math.min(R.brutto, GRV.bbg) / GRV.de;
  const gesEP = Math.min(ep * gesJ, gesJ * 1.95);
  const rvNow = GRV.rv * Math.pow(1 + R.ra / 100, jbr);
  const brutto = gesEP * rvNow;
  const rentJ = yr + jbr;
  const bestAnt = Math.min(100, 83.5 + (rentJ - 2025) * 0.5) / 100;
  const zvE = Math.max(brutto * 12 * bestAnt - 1230, 0);
  const tax = taxDE(zvE, R.kirche === 'Ja');
  const stM = tax.tot / 12;
  const kv = brutto * 0.083, pv = brutto * 0.034, kvpv = kv + pv;
  const netto = Math.max(brutto - stM - kvpv, 0);
  const nettoR = netto / Math.pow(1 + R.inf / 100, jbr);
  const jruh = Math.max(R.lebErw - R.rentAlter, 0);
  const kum = netto * 12 * jruh, luecke = Math.max(R.zielEur - netto, 0);
  const kapB = luecke * 12 * jruh, r35 = 0.035 / 12, n = jbr * 12;
  const vwert = n > 0 ? (R.vorsorge || 0) * ((Math.pow(1 + r35, n) - 1) / r35) : 0;
  const restK = Math.max(kapB - vwert, 0);
  let spar = 0; if (restK > 0 && n > 0) spar = (r35 * restK) / (Math.pow(1 + r35, n) - 1);
  return { alter, jbr, arbJ, gesJ, ep, gesEP, brutto, stM, kvpv, netto, nettoR, luecke, kum, kapB, restK, spar, rentJ, jruh, bestAnt };
}

export const RS_LABELS = [
  { label: 'Person', ey: 'Persönliche Daten', title: 'Wer bist du?', desc: 'Alter und Renteneintrittsalter bestimmen deine Ansparzeit und Entgeltpunkte.' },
  { label: 'Einkommen', ey: 'Einkommensverlauf', title: 'Was verdienst du?', desc: 'Dein Bruttogehalt bestimmt die Entgeltpunkte pro Jahr (§ 70 SGB VI). Durchschnittsentgelt 2025: 50.493 €/J.' },
  { label: 'Annahmen', ey: 'Annahmen', title: 'Welche Annahmen sollen gelten?', desc: 'Rentenanpassung, Inflation und Lebenserwartung prägen das langfristige Bild. Rentenanpassung 2026: +4,24 %.' },
  { label: 'Ziel', ey: 'Versorgungsziel', title: 'Mit wie viel Geld möchtest du im Ruhestand leben?', desc: 'Netto-Wunschbetrag pro Monat — Pensora berechnet die Rentenlücke.' },
];

// ── DEPOT ──────────────────────────────────────────────────────────────────
export function defaultD() {
  return { startK: 0, spar: 300, lz: 30, rendite: 7.0, inf: 2.1, entDauer: 20, zielEur: 1000 };
}

export function calcD(D) {
  const r = D.rendite / 100 / 12, n = D.lz * 12;
  const fvS = n > 0 ? D.spar * ((Math.pow(1 + r, n) - 1) / r) * (1 + r) : 0;
  const fvK = D.startK * Math.pow(1 + r, n);
  const fvG = fvS + fvK;
  const eingez = D.startK + D.spar * n;
  const gewinn = fvG - eingez;
  const fvR = fvG / Math.pow(1 + D.inf / 100, D.lz);
  const e4 = fvG * 0.04 / 12;
  const rE = r, nE = D.entDauer * 12;
  const eEx = nE > 0 ? fvG * rE / (1 - Math.pow(1 + rE, -nE)) : 0;
  const rs = 0.005 / 12;
  const fvSparB = n > 0 ? D.spar * ((Math.pow(1 + rs, n) - 1) / rs) * (1 + rs) + D.startK * Math.pow(1 + rs, n) : D.startK;
  const e4Spar = fvSparB * 0.04 / 12;
  const kapZ = D.zielEur * 12 / 0.04;
  let sparZ = 0;
  if (n > 0) {
    const fvKonly = D.startK * Math.pow(1 + r, n);
    const restF = Math.max(kapZ - fvKonly, 0);
    if (restF > 0) sparZ = restF * r / ((Math.pow(1 + r, n) - 1) * (1 + r));
  }
  return { fvG, fvR, eingez, gewinn, e4, eEx, kapZ, sparZ, fvSparB, e4Spar, luecke: Math.max(D.zielEur - e4, 0), vorteilGgSparbuch: fvG - fvSparB };
}

export const DS_LABELS = [
  { label: 'Sparplan', ey: 'Sparplan', title: 'Wie viel sparst du monatlich?', desc: 'Regelmäßiges Investieren mit dem Zinseszinseffekt ist der Kern des Altersvorsorge-Depots.' },
  { label: 'Rendite', ey: 'Rendite & Laufzeit', title: 'Welche Rendite erwartest du?', desc: 'Ein breit gestreutes ETF-Portfolio (MSCI World) erzielte historisch 7–9 % p.a. nominal. Vergleich mit Sparbuch wird automatisch eingeblendet.' },
  { label: 'Entnahme', ey: 'Entnahmephase', title: 'Wie lange willst du entnehmen?', desc: 'Die 4%-Regel gilt als nachhaltige Entnahmerate: jährlich 4 % des Depotwertes über 30 Jahre.' },
  { label: 'Ziel', ey: 'Monatliches Altersvorsorge-Ziel', title: 'Wie viel AV-Depot-Rente möchtest du?', desc: 'Dein monatlicher Wunschbetrag aus dem Altersvorsorge-Depot — Pensora zeigt, ob deine Sparrate ausreicht.' },
];

// ── RÜRUP ──────────────────────────────────────────────────────────────────
export const RMAX = 29344, RMAX26 = 30826;

export function defaultRu() {
  return { selbst: 'Nein', brutto: 60000, grenzSt: 30, kirche: 'Nein', mb: 300, grvAN: 9430, rendite: 5.0, inf: 2.1, lz: 25, rentAlter: 67, lebErw: 87 };
}

export function calcRu(Ru) {
  const jB = Ru.mb * 12;
  const grvGes = Ru.selbst === 'Ja' ? 0 : Ru.grvAN * 2;
  const sp = Math.max(RMAX - grvGes, 0);
  const absB = Math.min(jB, sp);
  const steJ = absB * (Ru.grenzSt / 100), steM = steJ / 12, nettoK = Ru.mb - steM;
  const r = Ru.rendite / 100 / 12, n = Ru.lz * 12;
  const fv = n > 0 ? Ru.mb * ((Math.pow(1 + r, n) - 1) / r) * (1 + r) : 0;
  const rs = 0.005 / 12;
  const fvSparB = n > 0 ? Ru.mb * ((Math.pow(1 + rs, n) - 1) / rs) * (1 + rs) : 0;
  const verrF = 0.035 / 12, mRente = fv * verrF;
  const rentJ = new Date().getFullYear() + Ru.lz;
  const bestAnt = Math.min(100, 83.5 + (rentJ - 2025) * 0.5) / 100;
  const zvE = Math.max(mRente * 12 * bestAnt - 1230, 0);
  const tax = taxDE(zvE, Ru.kirche === 'Ja');
  const nettoR = mRente - tax.tot / 12;
  const gesSte = steJ * Ru.lz;
  return { jB, sp, absB, steJ, steM, nettoK, fv, fvSparB, mRente, nettoR, bestAnt, gesSte, rentJ, jruh: Math.max(Ru.lebErw - Ru.rentAlter, 0) };
}

export const RUS_LABELS = [
  { label: 'Situation', ey: 'Persönliche Situation', title: 'Wer bist du?', desc: 'Selbstständige profitieren oft am stärksten — kein AG-Anteil zur GRV bedeutet mehr Rürup-Spielraum.' },
  { label: 'Beitrag', ey: 'Beitrag & Steuervorteil', title: 'Wie viel möchtest du einzahlen?', desc: 'Seit 2023: 100 % der Rürup-Beiträge absetzbar (§ 10 EStG). Max 2025: 29.344 € (Single), 2026: 30.826 €.' },
  { label: 'Rendite', ey: 'Rendite & Laufzeit', title: 'Welche Rendite erwartest du?', desc: 'ETF-Rürup ermöglicht marktnahe Renditen bei vollem Steuervorteil. Ø nach Kosten: 5–7 %.' },
  { label: 'Rente', ey: 'Rentenphase', title: 'Ab wann willst du Rürup-Rente beziehen?', desc: 'Frühestens ab 62 Jahren (Verträge ab 2012). Lebenslange Auszahlung, nicht kapitalisierbar.' },
];

// ── CASHFLOW ───────────────────────────────────────────────────────────────
export function defaultC() {
  return { netto: 3500, miete: 900, nk: 200, lm: 400, transport: 200, komm: 60, versich: 150, av: 0, frei: 300, sonst: 200 };
}

export function calcC(C) {
  const fix = C.miete + C.nk + C.lm + C.transport + C.komm;
  const vers = C.versich, av = C.av, leb = C.frei + C.sonst;
  const out = fix + vers + av + leb, frei = Math.max(C.netto - out, 0);
  return {
    fix, vers, av, leb, out, frei,
    emp_fix: C.netto * 0.50, emp_vers: C.netto * 0.10, emp_av: C.netto * 0.15,
    emp_vm: C.netto * 0.10, emp_frei: C.netto * 0.15, notg: C.netto * 3
  };
}

export const CS_LABELS = [
  { label: 'Einkommen', ey: 'Monatliches Nettoeinkommen', title: 'Was kommt rein?', desc: 'Dein monatliches Nettoeinkommen ist die Basis aller Empfehlungen.' },
  { label: 'Ausgaben', ey: 'Monatliche Ausgaben', title: 'Was geht raus?', desc: 'Je genauer deine Angaben, desto präziser die Optimierungsempfehlung.' },
];

// ── VERSICHERUNG ───────────────────────────────────────────────────────────
export const VBENCH = {
  'Privathaftpflicht': { avg: 7, hint: 'GDV Ø 2025: ~85 €/Jahr' },
  'Hausratversicherung': { avg: 11, hint: 'GDV Ø: ~130 €/Jahr' },
  'KFZ-Versicherung': { avg: 40, hint: 'Ø Haftpflicht: ~350–500 €/Jahr' },
  'Berufsunfähigkeit (BU)': { avg: 90, hint: 'Ø 30–45 J.: 60–130 €/Mo. (sehr individuell)' },
  'Rechtsschutz': { avg: 22, hint: 'Ø: ~250 €/Jahr' },
  'Unfallversicherung': { avg: 8, hint: 'Ø: ~100 €/Jahr' },
  'Zahnzusatz': { avg: 25, hint: 'Ø: 20–35 €/Mo.' },
  'Risikoleben': { avg: 25, hint: 'Ø 40 J., 200k €: ~20–35 €/Mo.' },
};

export function defaultV() {
  return Object.fromEntries(Object.entries(VBENCH).map(([k, b]) => [k, b.avg]));
}
