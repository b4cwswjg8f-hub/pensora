<script>
  import { createEventDispatcher } from 'svelte';
  import Logo from '../components/Logo.svelte';
  import PdfGate from '../components/PdfGate.svelte';
  import PdfFinanzplan from '../components/PdfFinanzplan.svelte';
  import { fmtE, fmtP, de0 } from '../lib/utils.js';
  import { lineChart, legend } from '../lib/charts.js';
  import { BOOK_URL, BRAND_NAME } from '../lib/data.js';

  export let R;
  export let result;

  const dispatch = createEventDispatcher();
  const book = () => window.open(BOOK_URL, '_blank');
  let showPdfGate = false;
  let showFinanzplan = false;

  $: r = result;
  $: realLuecke = Math.max(R.zielEur - r.nettoR, 0);
  $: lifetimeLoss = Math.round(realLuecke * 12 * r.jruh / 1000) * 1000;
  $: realOk = r.nettoR >= R.zielEur;
  $: sl = [[r.spar,'Today'],[r.spar*Math.pow(1.035,5),'+5 yrs'],[r.spar*Math.pow(1.035,10),'+10 yrs'],[r.spar*Math.pow(1.035,15),'+15 yrs']];
  $: yr = new Date().getFullYear();

  $: chartSvg = (() => {
    const yrs = 30;
    const rente = Array.from({length:yrs+1},(_,i)=>r.netto*Math.pow(1+R.ra/100,i));
    const renteR = Array.from({length:yrs+1},(_,i)=>r.netto/Math.pow(1+R.inf/100,i));
    const sparbuch = Array.from({length:yrs+1},(_,i)=>r.netto*Math.pow(1.003,i));
    const ziel = Array.from({length:yrs+1},()=>R.zielEur);
    return lineChart([
      {data:rente,color:'#60a5fa',fill:true,width:2},
      {data:renteR,color:'#4ade80',dash:'3 3',width:1.5},
      {data:sparbuch,color:'#FF6B6B',dash:'4 2',width:1.5},
      {data:ziel,color:'#fbbf24',dash:'6 3',width:1},
    ], yrs);
  })();
  $: legendHtml = legend([['#60a5fa','Nominal pension'],['#4ade80','Real (today\'s purchasing power)','3 3'],['#FF6B6B','Classic savings account (0.3% real)','4 2'],['#fbbf24','Retirement goal','6 3']]);

  // Gap diagram: 2 bars — Goal | Pension(blue)+Gap(red) stacked
  $: gapSvg = (() => {
    const w = 600, h = 320, padL = 64, padB = 52, padT = 48, padR = 60;
    const plotH = h - padT - padB;
    const goal = R.zielEur;
    const actual = r.nettoR;
    const luecke = Math.max(goal - actual, 0);
    const maxVal = Math.max(goal, actual) * 1.08;
    const sc = v => Math.max(0, Math.min(v / maxVal, 1)) * plotH;
    const baseY = h - padB;
    const bw = 120;
    const innerW = w - padL - padR;
    const gapBetween = innerW - bw * 2;
    const x1 = padL + gapBetween * 0.3;
    const x2 = x1 + bw + gapBetween * 0.4;

    let s = `<svg viewBox="0 0 ${w} ${h}" width="100%" height="${h}" style="display:block">`;
    [0,.25,.5,.75,1].forEach(f => {
      const yg = baseY - sc(f * maxVal);
      s += `<line x1="${padL}" x2="${w-padR}" y1="${yg.toFixed(1)}" y2="${yg.toFixed(1)}" stroke="rgba(36,30,25,.14)" stroke-width="1" ${f>0?'stroke-dasharray="3 3"':''}/>`;
      s += `<text x="${padL-8}" y="${(yg+3).toFixed(1)}" fill="#8a7f74" font-size="10" font-family="'Geist Mono',monospace" text-anchor="end">${de0.format(Math.round(f*maxVal))}€</text>`;
    });
    const glY = baseY - sc(goal);
    s += `<line x1="${padL}" x2="${w-padR}" y1="${glY.toFixed(1)}" y2="${glY.toFixed(1)}" stroke="rgba(251,191,36,.4)" stroke-width="1" stroke-dasharray="6 4"/>`;

    const gbH = sc(goal), gbY = baseY - gbH;
    s += `<rect x="${x1}" y="${gbY.toFixed(1)}" width="${bw}" height="${gbH.toFixed(1)}" fill="rgba(251,191,36,.18)" stroke="rgba(251,191,36,.6)" stroke-width="1.5" rx="5"/>`;
    s += `<text x="${(x1+bw/2).toFixed(1)}" y="${(gbY+gbH/2+5).toFixed(1)}" fill="rgba(251,191,36,.95)" font-size="14" font-weight="700" text-anchor="middle" font-family="'Geist Mono',monospace">${fmtE(goal)}</text>`;

    const ph = sc(actual), py = baseY - ph;
    if (luecke > 0) {
      const lh = sc(luecke), ly = py - lh;
      s += `<rect x="${x2}" y="${ly.toFixed(1)}" width="${bw}" height="${lh.toFixed(1)}" fill="rgba(255,107,107,.22)" stroke="rgba(255,107,107,.65)" stroke-width="1.5" rx="5"/>`;
      if (lh > 28) s += `<text x="${(x2+bw/2).toFixed(1)}" y="${(ly+lh/2+5).toFixed(1)}" fill="#FF6B6B" font-size="13" font-weight="700" text-anchor="middle" font-family="'Geist Mono',monospace">−${fmtE(luecke)}</text>`;
      s += `<rect x="${x2}" y="${py.toFixed(1)}" width="${bw}" height="${ph.toFixed(1)}" fill="rgba(96,165,250,.25)" stroke="rgba(96,165,250,.7)" stroke-width="1.5" rx="5"/>`;
      if (ph > 28) s += `<text x="${(x2+bw/2).toFixed(1)}" y="${(py+ph/2+5).toFixed(1)}" fill="rgba(96,165,250,.95)" font-size="13" font-weight="700" text-anchor="middle" font-family="'Geist Mono',monospace">${fmtE(actual)}</text>`;
    } else {
      s += `<rect x="${x2}" y="${py.toFixed(1)}" width="${bw}" height="${ph.toFixed(1)}" fill="rgba(74,222,128,.25)" stroke="rgba(74,222,128,.65)" stroke-width="1.5" rx="5"/>`;
      if (ph > 28) s += `<text x="${(x2+bw/2).toFixed(1)}" y="${(py+ph/2+5).toFixed(1)}" fill="rgba(74,222,128,.95)" font-size="14" font-weight="700" text-anchor="middle" font-family="'Geist Mono',monospace">✓ ${fmtE(actual)}</text>`;
    }
    const lblY = baseY + 18;
    s += `<text x="${(x1+bw/2).toFixed(1)}" y="${lblY}" fill="#8a7f74" font-size="10" text-anchor="middle" font-family="'Geist Mono',monospace">Retirement Goal</text>`;
    s += `<text x="${(x2+bw/2).toFixed(1)}" y="${lblY}" fill="#8a7f74" font-size="10" text-anchor="middle" font-family="'Geist Mono',monospace">Real Pension${luecke>0?' + Gap':' ✓'}</text>`;
    s += `</svg>`;
    return s;
  })();

  // Living-costs story section
  const KOSTEN = [
    { label: 'Rent (incl. utilities)', val: 960, color: '#60a5fa' },
    { label: 'Groceries', val: 440, color: '#4ade80' },
    { label: 'Transport', val: 210, color: '#fbbf24' },
    { label: 'Energy', val: 160, color: '#a78bfa' },
    { label: 'Communication', val: 65, color: '#f97316' },
    { label: 'Clothing', val: 80, color: '#ec4899' },
    { label: 'Health', val: 110, color: '#14b8a6' },
  ];
  const KOSTEN_TOT = KOSTEN.reduce((s, k) => s + k.val, 0);
  $: spielraum = r.nettoR - KOSTEN_TOT;

  // Marginal tax rate estimate from gross income
  $: grenzSt = R.brutto > 70000 ? 42 : R.brutto > 55000 ? 35 : R.brutto > 35000 ? 30 : 25;

  // Recommendation engine
  $: recos = (() => {
    const list = [];
    if (grenzSt >= 35 && realLuecke > 500) {
      list.push({ icon: '🧮', title: 'A Rürup plan pays off above a 35% marginal tax rate', text: `At your income level (approx. ${grenzSt}% marginal tax rate), many employees with an ETF-based Rürup plan get €30–50 tax benefit per €100 contributed — closing the gap with tax-subsidized savings.`, nav: 'ruerup', cta: 'Rürup Calculator →' });
    }
    if (realLuecke > 200) {
      list.push({ icon: '📊', title: 'Build an ETF savings plan', text: `Given a gap of ${fmtE(realLuecke)}/mo., starting early pays off — the earlier you start, the bigger the compound-interest effect.`, nav: 'depot', cta: 'ETF Savings Calculator →' });
    }
    if (realLuecke > 100 && spielraum < 200) {
      list.push({ icon: '🔍', title: 'Analyze your cashflow', text: 'If your real pension is tight and your current expenses leave little room, a budget check is worth it — often €100–300/mo. can be freed up without major sacrifice.', nav: 'cashflow', cta: 'Cashflow Calculator →' });
    }
    return list;
  })();
</script>

<nav class="nav">
  <div class="row g16">
    <button class="brand" on:click={() => dispatch('back')}><Logo /> {BRAND_NAME}</button>
    <span style="color:var(--line2);font-size:16px">/</span>
    <span style="color:var(--fg2);font-size:14px">Result · Pension</span>
  </div>
  <div class="row g8">
    <button class="btn btng print-hide" on:click={() => dispatch('back')}>← Home</button>
    <button class="btn btng print-hide" on:click={() => dispatch('recalc')}>← Recalculate</button>
    <button class="btn btng print-hide" on:click={() => showFinanzplan = true} title="Save as PDF">⬇ PDF</button>
    <button class="btn btnp print-hide" on:click={book}>Book a Consultation →</button>
  </div>
</nav>

<PdfGate bind:show={showPdfGate} />

{#if showFinanzplan}
  <div class="fp-overlay" on:click|self={() => showFinanzplan = false}>
    <div class="fp-overlay-inner">
      <button class="fp-overlay-close" on:click={() => showFinanzplan = false}>✕ Close</button>
      <PdfFinanzplan mode="rente" {R} {result} />
    </div>
  </div>
{/if}

<div class="vscr">
  <div class="calc-result-pad">
    <div class="ey" style="margin-bottom:20px">Pension Forecast · Age {R.rentAlter} · Pension value €40.79 (DRV 2025)</div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px">
      <div style="padding:32px;border-radius:var(--rlg);background:{realOk?'rgba(36,30,25,.04)':'var(--loss-dim)'};border:2px solid {realOk?'var(--fg)':'var(--loss)'}">
        <div class="ey" style="color:{realOk?'var(--fg3)':'var(--loss)'};margin-bottom:16px">Your Real Purchasing Power in Retirement · {r.rentJ}</div>
        <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:8px">
          <span class="stat" style="font-size:80px;color:{realOk?'var(--fg)':'var(--loss)'}">{de0.format(Math.round(r.nettoR))}</span>
          <span style="font-size:22px;color:var(--fg2)">€/mo.</span>
        </div>
        <div style="font-size:13px;color:var(--fg3);margin-bottom:16px">= today's purchasing power of your pension in {r.jbr} years ({R.inf}% inflation)</div>
        <div style="padding:12px 16px;background:rgba(36,30,25,.05);border-radius:var(--rmd);font-size:12px;color:var(--fg3)">
          Nominal pension: <span style="font-family:var(--mono);color:var(--fg)">{fmtE(r.netto)}/mo.</span> ·
          Inflation loss: <span style="font-family:var(--mono);color:var(--loss)">−{fmtE(r.netto-r.nettoR)}/mo.</span>
        </div>
      </div>
      <div style="padding:32px;border-radius:var(--rlg);background:var(--loss-dim);border:2px solid var(--loss)">
        <div class="ey" style="color:var(--loss);margin-bottom:16px">Real Pension Gap (inflation-adjusted)</div>
        <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:8px">
          <span class="stat" style="font-size:80px;color:var(--loss)">{realLuecke>0?'−'+de0.format(Math.round(realLuecke)):'✓'}</span>
          <span style="font-size:22px;color:rgba(255,107,107,.6)">{realLuecke>0?'€/mo.':''}</span>
        </div>
        <div style="font-size:13px;color:rgba(255,107,107,.6);margin-bottom:16px">vs. retirement goal {fmtE(R.zielEur)}/mo. net</div>
        {#if realLuecke > 0}
          <div style="padding:12px 16px;background:rgba(36,30,25,.05);border-radius:var(--rmd);font-size:13px;color:var(--loss);font-weight:600">
            = {de0.format(lifetimeLoss)} € less over {r.jruh} years of retirement
          </div>
        {:else}
          <div style="font-size:13px;color:var(--fg2)">Your pension covers your retirement goal.</div>
        {/if}
      </div>
    </div>

    <!-- KPI strip -->
    <div style="display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line);border-radius:var(--rlg);overflow:hidden;background:var(--bg1);margin-bottom:20px">
      {#each [['Nominal net/mo.',fmtE(r.netto),'from '+r.rentJ],['Gross/mo.',fmtE(r.brutto),'before tax & health insurance'],['Earnings Points',r.gesEP.toFixed(1)+' pts',r.gesJ+' working years'],['Real Purchasing Power',fmtE(r.nettoR),'in today\'s €']] as [l,v,sub], i}
        <div style="padding:20px 24px;border-right:{i<3?'1px solid var(--line)':'0'}">
          <div class="ey" style="margin-bottom:8px">{l}</div>
          <div class="stat" style="font-size:28px;color:{i===3&&!realOk?'var(--loss)':'var(--fg)'}">{v}</div>
          <div style="font-size:11px;color:var(--fg3);font-family:var(--mono);margin-top:4px">{sub}</div>
        </div>
      {/each}
    </div>

    <div style="display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:16px">
      <div class="col g16">
        <div class="cardf" style="padding:28px">
          <div class="ey" style="margin-bottom:12px">Pension Growth Over Time</div>
          {@html chartSvg}
          {@html legendHtml}
        </div>
        {#if r.luecke > 0}
          <div class="card" style="padding:28px">
            <div class="ey" style="margin-bottom:14px">Required Savings Rate (3.5% p.a.)</div>
            <div style="display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid var(--line)">
              {#each sl as [v,k], i}
                <div style="padding:14px 0;border-right:{i<3?'1px solid var(--line)':'0'};padding-left:{i>0?'14px':'0'}">
                  <div style="font-size:10px;color:{i===0?'var(--fg)':'var(--fg3)'};font-family:var(--mono);text-transform:uppercase;letter-spacing:.08em">{k}</div>
                  <div style="margin-top:6px;font-family:var(--mono);font-size:20px;color:{i===0?'var(--fg)':'var(--fg2)'};font-weight:500">{fmtE(v)}</div>
                </div>
              {/each}
            </div>
          </div>
        {/if}
        <div class="cardf" style="padding:28px">
          <div class="ey" style="margin-bottom:14px">Deductions (§ 22 No.1 EStG + SGB V)</div>
          <table>
            {#each [['Gross pension',r.brutto,'var(--fg)',false],['Income tax ('+Math.round(r.bestAnt*100)+'%)',-r.stM,'var(--loss)',false],['Health & long-term care insurance',-r.kvpv,'var(--fg3)',false],['Net pension',r.netto,'var(--fg)',true]] as [l,v,c,bold]}
              <tr>
                <td style="color:{bold?'var(--fg)':'var(--fg2)'};font-weight:{bold?600:400}">
                  <span style="display:inline-block;width:8px;height:8px;background:{c};border-radius:2px;margin-right:8px"></span>{l}
                </td>
                <td style="text-align:right;font-family:var(--mono);color:{v<0?'var(--loss)':'var(--fg)'};font-weight:{bold?700:500};font-size:{bold?15:13}px">
                  {v<0?'−':''}{fmtE(Math.abs(v))}
                </td>
              </tr>
            {/each}
          </table>
        </div>

        <!-- Gap diagram: stacked -->
        <div class="cardf" style="padding:28px">
          <div class="ey" style="margin-bottom:6px">Retirement Provision at a Glance</div>
          <div style="font-size:13px;color:var(--fg3);margin-bottom:20px">Target pension · Real pension · {realLuecke > 0 ? 'gap stacked on top of pension' : 'retirement goal covered ✓'}</div>
          {@html gapSvg}
          <div style="display:flex;gap:20px;flex-wrap:wrap;margin-top:14px;font-size:11px;font-family:var(--mono);color:var(--fg3)">
            <span style="display:flex;align-items:center;gap:6px"><span style="width:10px;height:10px;background:rgba(251,191,36,.5);border:1px solid rgba(251,191,36,.7);border-radius:2px;display:inline-block"></span>Retirement Goal</span>
            <span style="display:flex;align-items:center;gap:6px"><span style="width:10px;height:10px;background:rgba(96,165,250,.4);border:1px solid rgba(96,165,250,.7);border-radius:2px;display:inline-block"></span>Real Pension</span>
            {#if realLuecke > 0}<span style="display:flex;align-items:center;gap:6px"><span style="width:10px;height:10px;background:rgba(255,107,107,.35);border:1px solid rgba(255,107,107,.65);border-radius:2px;display:inline-block"></span>Gap (stacked)</span>{/if}
          </div>
        </div>

        <!-- Story: Is it enough for the basics? -->
        <div class="cardf" style="padding:28px">
          <div class="ey" style="margin-bottom:6px">Is It Enough for Everyday Life?</div>
          <div style="font-size:13px;color:var(--fg3);margin-bottom:20px">Avg. 2-person household Germany 2025 · Destatis reference values</div>
          <div style="position:relative;height:48px;background:rgba(36,30,25,.06);border-radius:8px;overflow:hidden;margin-bottom:16px">
            {#each (() => { let x=0; return KOSTEN.map(k => { const pct = k.val / Math.max(r.nettoR, KOSTEN_TOT) * 100; const left = x; x+=pct; return {...k, pct, left}; }); })() as k}
              <div style="position:absolute;top:0;left:{k.left.toFixed(1)}%;width:{k.pct.toFixed(1)}%;height:100%;background:{k.color};opacity:.55"></div>
            {/each}
            {#if r.nettoR >= KOSTEN_TOT}
              <div style="position:absolute;top:0;left:{(KOSTEN_TOT/Math.max(r.nettoR,KOSTEN_TOT)*100).toFixed(1)}%;width:{((r.nettoR-KOSTEN_TOT)/Math.max(r.nettoR,KOSTEN_TOT)*100).toFixed(1)}%;height:100%;background:rgba(74,222,128,.3);border-left:2px solid rgba(74,222,128,.7)"></div>
            {/if}
            {#if r.nettoR < KOSTEN_TOT}
              <div style="position:absolute;top:0;left:{(r.nettoR/KOSTEN_TOT*100).toFixed(1)}%;width:2px;height:100%;background:rgba(255,107,107,.9)"></div>
            {/if}
          </div>
          <div style="display:grid;grid-template-columns:1fr auto auto;gap:0;border-top:1px solid var(--line);margin-bottom:12px">
            {#each KOSTEN as k}
              <div style="display:flex;align-items:center;gap:8px;padding:7px 0;border-bottom:1px solid var(--line);font-size:12px;color:var(--fg2)">
                <span style="width:8px;height:8px;background:{k.color};opacity:.8;border-radius:2px;flex-shrink:0;display:inline-block"></span>{k.label}
              </div>
              <div style="padding:7px 12px;border-bottom:1px solid var(--line);font-family:var(--mono);font-size:12px;text-align:right;color:var(--fg3)">avg.</div>
              <div style="padding:7px 0;border-bottom:1px solid var(--line);font-family:var(--mono);font-size:12px;text-align:right">{fmtE(k.val)}</div>
            {/each}
            <div style="padding:10px 0;font-size:13px;font-weight:600">Total Basic Needs</div>
            <div style="padding:10px 12px;font-family:var(--mono);font-size:13px;text-align:right;color:var(--fg3)">avg.</div>
            <div style="padding:10px 0;font-family:var(--mono);font-size:13px;text-align:right;font-weight:600">{fmtE(KOSTEN_TOT)}</div>
          </div>
          <div style="padding:14px 16px;border-radius:8px;background:{spielraum >= 0 ? 'rgba(74,222,128,.06)' : 'rgba(255,107,107,.06)'};border:1px solid {spielraum >= 0 ? 'rgba(74,222,128,.2)' : 'rgba(255,107,107,.2)'}">
            {#if spielraum >= 0}
              <div style="font-size:14px;font-weight:600;color:#4ade80">✓ Basic needs covered — {fmtE(spielraum)}/mo. left over</div>
              <div style="font-size:12px;color:var(--fg3);margin-top:4px">After average expenses, {fmtE(spielraum)}/mo. remains for leisure, travel and reserves.</div>
            {:else}
              <div style="font-size:14px;font-weight:600;color:var(--loss)">⚠ {fmtE(Math.abs(spielraum))}/mo. short of average basic needs</div>
              <div style="font-size:12px;color:var(--fg3);margin-top:4px">Your real pension does not fully cover average basic expenses.</div>
            {/if}
          </div>
          <div style="font-size:10px;color:var(--fg4);margin-top:10px;font-family:var(--mono)">Reference: Destatis 2025 · 2-person household Germany · Rent varies significantly by region</div>
        </div>

        <!-- Recommendations -->
        {#if recos.length > 0}
          <div class="card" style="padding:28px">
            <div class="ey" style="margin-bottom:14px">What Others in Your Situation Have Chosen</div>
            {#each recos as rec}
              <div style="padding:16px;background:rgba(36,30,25,.03);border:1px solid var(--line2);border-radius:10px;margin-bottom:10px">
                <div style="font-size:14px;font-weight:600;margin-bottom:6px">{rec.icon} {rec.title}</div>
                <div style="font-size:13px;color:var(--fg2);line-height:1.6;margin-bottom:10px">{rec.text}</div>
                <button class="btn btng" style="height:34px;font-size:12px" on:click={() => dispatch('navigate', rec.nav)}>{rec.cta}</button>
              </div>
            {/each}
            <div style="font-size:10px;color:var(--fg4);margin-top:12px;line-height:1.5;font-family:var(--mono)">
              ⚠ Not investment advice. These pointers are based on practical observations — not an individual recommendation. Please verify with an independent advisor.
            </div>
          </div>
        {/if}
      </div>
      <aside style="position:sticky;top:88px">
        <div class="card" style="margin-bottom:12px;padding:20px">
          <div class="ey" style="margin-bottom:8px">Save Your Result</div>
          <button class="btn" style="width:100%;height:48px;background:rgba(36,30,25,.05);border:1px solid rgba(36,30,25,.18);border-radius:8px;font-size:14px;font-weight:600;gap:8px" on:click={() => showFinanzplan = true}>
            ⬇ Financial Plan as PDF
          </button>
          <p style="font-size:11px;color:var(--fg4);margin-top:8px;text-align:center;line-height:1.4">Enter your email · ready to print instantly</p>
        </div>
        <div class="card" style="border-color:var(--fg);position:relative;overflow:hidden">
          <div style="position:absolute;top:0;left:0;right:0;height:3px;background:var(--fg)"></div>
          <h3 style="font-size:22px;font-weight:500;margin-bottom:10px">Plan against the pension gap.</h3>
          <p style="font-size:13px;color:var(--fg2);line-height:1.55;margin-bottom:0">30 min., free. Independent financial advisor.</p>
          <button class="btn btnp btnlg" style="width:100%;margin-top:16px" on:click={book}>Book a Free Call →</button>
          <button class="btn btng" style="width:100%;margin-top:8px" on:click={() => dispatch('recalc')}>← Recalculate</button>
          <div style="margin-top:20px;padding-top:16px;border-top:1px solid var(--line)">
            <div class="ey" style="margin-bottom:10px">Related Calculators</div>
            {#each [['depot','ETF Savings Plan Calculator'],['ruerup','Rürup Calculator']] as [k,l]}
              <button class="btn" style="width:100%;margin-bottom:8px;justify-content:flex-start" on:click={() => dispatch('navigate', k)}>{l} →</button>
            {/each}
          </div>
        </div>
      </aside>
    </div>
  </div>
</div>
