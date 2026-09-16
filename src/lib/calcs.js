import { taxDE, de0 } from './utils.js';

// ── STATUTORY PENSION (RENTE) ───────────────────────────────────────────────
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
  { label: 'You', ey: 'Personal Details', title: 'Who are you?', desc: 'Your age and target retirement age determine your contribution period and earnings points.' },
  { label: 'Income', ey: 'Income History', title: 'What do you earn?', desc: 'Your gross salary determines earnings points per year (§ 70 SGB VI). Average income 2025: €50,493/yr.' },
  { label: 'Assumptions', ey: 'Assumptions', title: 'What assumptions should apply?', desc: 'Pension adjustments, inflation and life expectancy shape the long-term picture. Pension adjustment 2026: +4.24%.' },
  { label: 'Goal', ey: 'Retirement Goal', title: 'How much money do you want to live on in retirement?', desc: 'Enter your desired net monthly amount — we calculate your pension gap.' },
];

// ── ETF SAVINGS DEPOT ────────────────────────────────────────────────────────
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
  { label: 'Savings Plan', ey: 'Savings Plan', title: 'How much do you save each month?', desc: 'Regular investing and the power of compound interest are the core of an ETF savings plan.' },
  { label: 'Return', ey: 'Return & Time Horizon', title: 'What return do you expect?', desc: 'A broadly diversified ETF portfolio (MSCI World) has historically returned 7–9% p.a. nominal. A comparison against a savings account is shown automatically.' },
  { label: 'Withdrawal', ey: 'Withdrawal Phase', title: 'How long do you want to withdraw for?', desc: 'The 4% rule is considered a sustainable withdrawal rate: 4% of the portfolio value per year, over 30 years.' },
  { label: 'Goal', ey: 'Monthly Investing Goal', title: 'How much monthly income do you want from your ETF depot?', desc: 'Your desired monthly amount from your ETF savings plan — we show whether your savings rate is enough.' },
];

// ── RÜRUP PENSION ────────────────────────────────────────────────────────────
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
  { label: 'Situation', ey: 'Your Situation', title: 'Who are you?', desc: 'The self-employed often benefit most — no employer share into statutory pension insurance means more room for Rürup contributions.' },
  { label: 'Contribution', ey: 'Contribution & Tax Benefit', title: 'How much do you want to contribute?', desc: 'Since 2023: 100% of Rürup contributions are tax-deductible (§ 10 EStG). Max 2025: €29,344 (single), 2026: €30,826.' },
  { label: 'Return', ey: 'Return & Time Horizon', title: 'What return do you expect?', desc: 'An ETF-based Rürup plan allows near-market returns with the full tax benefit. Average net of costs: 5–7%.' },
  { label: 'Payout', ey: 'Payout Phase', title: 'From when do you want to draw your Rürup pension?', desc: 'Earliest from age 62 (contracts from 2012). Lifelong payout, cannot be taken as a lump sum.' },
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
  { label: 'Income', ey: 'Monthly Net Income', title: 'What comes in?', desc: 'Your monthly net income is the basis for every recommendation.' },
  { label: 'Expenses', ey: 'Monthly Expenses', title: 'What goes out?', desc: 'The more precise your figures, the more precise the optimization recommendation.' },
];

// ── INSURANCE CHECK ──────────────────────────────────────────────────────────
export const VBENCH = {
  'Personal Liability':       { avg: 7,  hint: 'GDV avg. 2025: ~€85/year' },
  'Home Contents':            { avg: 11, hint: 'GDV avg.: ~€130/year' },
  'Car Insurance':            { avg: 40, hint: 'Avg. liability: ~€350–500/year' },
  'Disability (BU)':          { avg: 90, hint: 'Avg. age 30–45: €60–130/mo. (highly individual)' },
  'Legal Protection':         { avg: 22, hint: 'Avg.: ~€250/year' },
  'Accident Insurance':       { avg: 8,  hint: 'Avg.: ~€100/year' },
  'Supplemental Dental':      { avg: 25, hint: 'Avg.: €20–35/mo.' },
  'Term Life Insurance':      { avg: 25, hint: 'Avg. age 40, €200k: ~€20–35/mo.' },
};

export function defaultV() {
  return Object.fromEntries(Object.entries(VBENCH).map(([k, b]) => [k, b.avg]));
}
