<script>
  // PDF Finanzplan — Design C (Dashboard-Grid, monochrom, Signal-Rot nur für Lücke)
  // Props: mode='pension'|'rente', P or R (inputs), result (calc result)
  export let mode = 'rente';   // 'pension' | 'rente'
  export let P = null;         // pension inputs
  export let R = null;         // rente inputs
  export let result = null;

  import { onMount } from 'svelte';
  import { de0, fmtE } from '../lib/utils.js';

  const inputs = mode === 'pension' ? P : R;
  $: r = result || {};
  $: goal = inputs?.zielEur || 2500;
  $: realGap = Math.max(goal - (r.nettoR || 0), 0);
  $: lifetimeGap = Math.round(realGap * 12 * (r.jruh || 20) / 1000) * 1000;
  $: realOk = (r.nettoR || 0) >= goal;
  $: nomNetto = r.netto || 0;
  $: brutto  = r.brutto || 0;
  $: nettoR  = r.nettoR || 0;
  $: inflation = inputs?.inf || 2.1;
  $: rentAlter = mode === 'pension' ? (inputs?.pensAlter || 67) : (inputs?.rentAlter || 67);
  $: today = new Date().toLocaleDateString('de-DE',{day:'2-digit',month:'2-digit',year:'numeric'});

  // Abzüge breakdown
  $: abzSteuer = Math.round((brutto - nomNetto) * 0.56);
  $: abzKV     = Math.round((brutto - nomNetto) * 0.44);

  // Gap band realPct
  $: gapPct = goal > 0 ? Math.min(nettoR / goal, 1) : 0;

  // Sparrate (from result or estimate)
  $: sparBasis = r.spar || Math.max(realGap * 0.3, 30);
  $: sparSteps = [
    { v: sparBasis,                           l: 'Heute' },
    { v: sparBasis * Math.pow(1.035, 5),      l: '+5 J.' },
    { v: sparBasis * Math.pow(1.035, 10),     l: '+10 J.' },
    { v: sparBasis * Math.pow(1.035, 15),     l: '+15 J.' },
  ];
  $: sparMax = Math.max(...sparSteps.map(s => s.v));

  // Budget
  const BUDGET = [
    { label:'Warmmiete',     value:960,  shade:'#0B0B0C' },
    { label:'Lebensmittel',  value:440,  shade:'#2C2C2E' },
    { label:'Transport',     value:210,  shade:'#48484C' },
    { label:'Energie',       value:160,  shade:'#646468' },
    { label:'Gesundheit',    value:110,  shade:'#828287' },
    { label:'Bekleidung',    value:80,   shade:'#A2A2A6' },
    { label:'Kommunikation', value:65,   shade:'#C4C4C7' },
  ];
  const BUDGET_TOT = 2025;
  $: budgetShort = Math.max(nettoR - BUDGET_TOT, 0);
  $: budgetOver  = Math.max(BUDGET_TOT - nettoR, 0);

  // Timeline SVG (Catmull-Rom smooth)
  $: timelineSvg = (() => {
    const W = 714, H = 180;
    const pad = { t:16, r:16, b:28, l:10 };
    const YMAX = Math.max(goal * 1.12, 3000);
    const yr0 = new Date().getFullYear();
    const yr1 = yr0 + 30;
    const years = [yr0, yr0+6, yr0+12, yr0+18, yr0+24, yr0+30];
    const nomArr  = years.map((_,i) => nomNetto * Math.pow(1.018, i * 5));
    const realArr = years.map((_,i) => nomNetto / Math.pow(1 + inflation/100, i * 5));
    const sbArr   = years.map((_,i) => nomNetto * Math.pow(1.003, i * 5));

    const X = yr => pad.l + (yr - yr0) / (yr1 - yr0) * (W - pad.l - pad.r);
    const Y = v  => pad.t + (1 - Math.min(v / YMAX, 1)) * (H - pad.t - pad.b);

    function smooth(pts) {
      if (!pts.length) return '';
      let d = `M ${pts[0][0].toFixed(1)} ${pts[0][1].toFixed(1)}`;
      for (let i = 0; i < pts.length - 1; i++) {
        const p0 = pts[Math.max(0, i-1)], p1 = pts[i], p2 = pts[i+1], p3 = pts[Math.min(pts.length-1, i+2)];
        const c1x = p1[0] + (p2[0]-p0[0])/6, c1y = p1[1] + (p2[1]-p0[1])/6;
        const c2x = p2[0] - (p3[0]-p1[0])/6, c2y = p2[1] - (p3[1]-p1[1])/6;
        d += ` C ${c1x.toFixed(1)} ${c1y.toFixed(1)} ${c2x.toFixed(1)} ${c2y.toFixed(1)} ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;
      }
      return d;
    }

    const pts = arr => years.map((yr, i) => [X(yr), Y(arr[i])]);
    const nomPts  = pts(nomArr);
    const realPts = pts(realArr);
    const sbPts   = pts(sbArr);
    const zielY   = Y(goal);

    // Gap band
    let band = `M ${realPts[0][0].toFixed(1)} ${zielY.toFixed(1)}`;
    band += ` L ${realPts[realPts.length-1][0].toFixed(1)} ${zielY.toFixed(1)}`;
    for (let i = realPts.length-1; i >= 0; i--) band += ` L ${realPts[i][0].toFixed(1)} ${realPts[i][1].toFixed(1)}`;
    band += ' Z';

    // Grid lines
    let s = '';
    [0, 1000, 2000, Math.round(YMAX/1000)*1000].forEach(v => {
      const gy = Y(v);
      s += `<line x1="${pad.l}" x2="${W-pad.r}" y1="${gy.toFixed(1)}" y2="${gy.toFixed(1)}" stroke="#E6E6E3" stroke-width="1"/>`;
      s += `<text x="${W-pad.r-2}" y="${(gy-4).toFixed(1)}" text-anchor="end" font-size="8" fill="#8B8B90" font-family="'Plus Jakarta Sans',system-ui,sans-serif">${v >= 1000 ? (v/1000)+'k' : v} €</text>`;
    });

    // Gap band
    s += `<path d="${band}" fill="rgba(229,37,27,0.09)" stroke="none"/>`;

    // Ziel line
    s += `<line x1="${pad.l}" x2="${W-pad.r}" y1="${zielY.toFixed(1)}" y2="${zielY.toFixed(1)}" stroke="#E5251B" stroke-width="1.2" stroke-dasharray="2 4" opacity="0.8"/>`;
    s += `<text x="${pad.l+4}" y="${(zielY-5).toFixed(1)}" font-size="8" fill="#E5251B" font-weight="600" font-family="'Plus Jakarta Sans',system-ui,sans-serif">Versorgungsziel ${de0.format(goal)} €</text>`;

    // Sparbuch
    s += `<path d="${smooth(sbPts)}" fill="none" stroke="#B6B6BA" stroke-width="1.2" stroke-dasharray="1 3" stroke-linecap="round"/>`;
    // Nominal
    s += `<path d="${smooth(nomPts)}" fill="none" stroke="#B6B6BA" stroke-width="1.4"/>`;
    // Real
    s += `<path d="${smooth(realPts)}" fill="none" stroke="#0B0B0C" stroke-width="2.2" stroke-linecap="round"/>`;

    // Endpoint dot
    const last = realPts[realPts.length-1];
    s += `<circle cx="${last[0].toFixed(1)}" cy="${last[1].toFixed(1)}" r="2.8" fill="#0B0B0C"/>`;

    // X labels
    years.forEach(yr => {
      s += `<text x="${X(yr).toFixed(1)}" y="${H-6}" text-anchor="middle" font-size="8" fill="#8B8B90" font-family="'Plus Jakarta Sans',system-ui,sans-serif">${yr}</text>`;
    });

    return `<svg viewBox="0 0 ${W} ${H}" width="100%" style="display:block">${s}</svg>`;
  })();

  // Recommendations from result or default
  $: recos = (() => {
    const list = [];
    const grenz = mode === 'rente'
      ? (R?.brutto > 70000 ? 42 : R?.brutto > 55000 ? 35 : 30)
      : 35;
    if (grenz >= 35 && realGap > 400)
      list.push({ tag:'STEUER', num:'01', title:'Rürup lohnt sich ab Grenzsteuer 35 %',
        body:`Bei Ihrem Einkommensniveau (ca. ${grenz} % Grenzsteuersatz) erzielen Sie mit Rürup-ETF 30–50 € Steuervorteil je 100 € Beitrag — die Lücke steuersubventioniert schließen.` });
    if (realGap > 150)
      list.push({ tag:'AUFBAU', num:'02', title:'AV-Depot-Sparkonto aufbauen',
        body:`Ab 2027: 540 €/Jahr Grundzulage + steuerfreie Anlage. Bei einer Lücke von ${de0.format(realGap)} €/Mo. lohnt früher Aufbau — je früher, desto größer der Zinseszins-Effekt.` });
    list.push({ tag:'CASHFLOW', num: list.length === 0 ? '01' : '0'+(list.length+1), title:'Cashflow analysieren',
      body:'Wenn die reale Rente knapp wird und die Ausgaben kaum Spielraum lassen, lohnt ein Budget-Check — oft lassen sich 100–300 €/Mo. ohne großen Verzicht freimachen.' });
    return list.slice(0, 3);
  })();

  onMount(() => {
    setTimeout(() => window.print(), 400);
  });
</script>

<div class="fp-wrap" id="finanzplan-print">
  <!-- Header -->
  <header class="fp-topbar">
    <div class="fp-wordmark">PENSORA</div>
    <div class="fp-topbar-right">
      <div class="fp-label-sm">Persönlicher Finanzplan</div>
      <div class="fp-muted-sm">Erstellt am {today}</div>
    </div>
  </header>
  <div class="fp-prog">{mode === 'pension' ? 'Pensionsprognose' : 'Rentenprognose'} · {rentAlter} J. · Rentenwert 40,79 € · DRV 2025</div>

  <div class="fp-grid">

    <!-- Hero Gap card (dark) -->
    <div class="fp-card fp-dark fp-s7 fp-gap-card">
      <div class="fp-gap-label">Reale {mode==='pension'?'Versorgungslücke':'Rentenlücke'} · inflationsbereinigt</div>
      <div class="fp-gap-big">{realOk ? '+' : '−'}{de0.format(realGap)}<span class="fp-gap-unit">€/Mo.</span></div>
      <p class="fp-gap-body">So viel fehlt monatlich gegenüber dem Versorgungsziel von {de0.format(goal)} € netto — gerechnet in heutiger Kaufkraft.</p>
      {#if realGap > 0}
        <span class="fp-pill">Über {r.jruh||20} Jahre Ruhestand: <b>−{de0.format(lifetimeGap)} €</b></span>
      {/if}
    </div>

    <!-- Kaufkraft card -->
    <div class="fp-card fp-s5 fp-real-card">
      <div class="fp-clabel">Reale Kaufkraft im Ruhestand</div>
      <div class="fp-real-big">{de0.format(nettoR)}<span class="fp-real-unit">€/Mo.</span></div>
      <p class="fp-real-body">Heutige Kaufkraft deiner {mode==='pension'?'Pension':'Rente'} bei {inflation} % Inflation p. a.</p>
      <div class="fp-mini">
        <div class="fp-mini-r"><span class="fp-mini-lab">Nominal netto</span><span class="fp-mini-v">{de0.format(nomNetto)} €/Mo.</span></div>
        <div class="fp-mini-r"><span class="fp-mini-lab">Inflationsverlust</span><span class="fp-mini-v fp-neg">−{de0.format(nomNetto - nettoR)} €/Mo.</span></div>
      </div>
    </div>

    <!-- KPI tiles -->
    <div class="fp-card fp-kpi fp-s3"><div class="fp-clabel">Nominal netto</div><div class="fp-kv">{de0.format(nomNetto)} <span class="fp-ku">€/Mo.</span></div><div class="fp-kn">ab {new Date().getFullYear() + (rentAlter - (inputs?.gebJ ? new Date().getFullYear() - inputs.gebJ : 35))}</div></div>
    <div class="fp-card fp-kpi fp-s3"><div class="fp-clabel">Brutto</div><div class="fp-kv">{de0.format(brutto)} <span class="fp-ku">€/Mo.</span></div><div class="fp-kn">vor Steuer & KV</div></div>
    <div class="fp-card fp-kpi fp-s3"><div class="fp-clabel">{mode==='pension'?'Ruhegehaltssatz':'Entgeltpunkte'}</div><div class="fp-kv">{mode==='pension'? (r.rs ? (r.rs*100).toFixed(2)+'%' : '—') : (r.ep ? r.ep.toFixed(1)+' EP' : '—')}</div><div class="fp-kn">{mode==='pension'?'§ 14 BeamtVG':'§ 64 SGB VI'}</div></div>
    <div class="fp-card fp-kpi fp-s3"><div class="fp-clabel">Reale Kaufkraft</div><div class="fp-kv">{de0.format(nettoR)} <span class="fp-ku">€</span></div><div class="fp-kn">in heutigen €</div></div>

    <!-- Timeline chart -->
    <div class="fp-card fp-s12">
      <div class="fp-chead">
        <span class="fp-clabel">{mode==='pension'?'Pensions':'Renten'}entwicklung im Zeitverlauf</span>
        <span class="fp-chead-m">{new Date().getFullYear()} – {new Date().getFullYear()+30} · real &amp; nominal</span>
      </div>
      {@html timelineSvg}
      <div class="fp-legend">
        <div class="fp-legend-item"><span class="fp-swatch fp-sw-real"></span>Real (Kaufkraft heute)</div>
        <div class="fp-legend-item"><span class="fp-swatch fp-sw-nom"></span>Nominal</div>
        <div class="fp-legend-item"><span class="fp-swatch fp-sw-sb"></span>Klassisches Sparbuch</div>
        <div class="fp-legend-item"><span class="fp-swatch fp-sw-ziel"></span>Versorgungsziel</div>
      </div>
    </div>

    <!-- Versorgungsanalyse + Sparrate -->
    <div class="fp-card fp-s8">
      <div class="fp-chead"><span class="fp-clabel">Versorgungsanalyse auf einen Blick</span><span class="fp-chead-m">Ziel · real · Lücke</span></div>
      <div class="fp-vbars">
        <div class="fp-vbar">
          <div class="fp-vbar-top"><span class="fp-vbar-name">Versorgungsziel</span><span class="fp-vbar-val">{de0.format(goal)} €/Mo.</span></div>
          <div class="fp-track fp-track-full"></div>
        </div>
        <div class="fp-vbar">
          <div class="fp-vbar-top">
            <span class="fp-vbar-name">Reale {mode==='pension'?'Pension':'Rente'}
              {#if realGap > 0}<span class="fp-vbar-gap"> + Lücke {de0.format(realGap)} €</span>{/if}
            </span>
            <span class="fp-vbar-val">{de0.format(nettoR)} €/Mo.</span>
          </div>
          <div class="fp-track">
            <div class="fp-seg-ink" style="width:{(gapPct*100).toFixed(1)}%"></div>
            {#if realGap > 0}<div class="fp-seg-gap" style="width:{((1-gapPct)*100).toFixed(1)}%"></div>{/if}
          </div>
        </div>
      </div>
    </div>

    <div class="fp-card fp-s4">
      <div class="fp-chead"><span class="fp-clabel">Sparrate</span><span class="fp-chead-m">3,5 % p. a. Dynamisierung</span></div>
      <div class="fp-spar">
        {#each sparSteps as st}
          <div class="fp-spar-bar">
            <span class="fp-spar-v">{Math.round(st.v)} €</span>
            <span class="fp-spar-fill" style="height:{(st.v/sparMax*100).toFixed(0)}%"></span>
            <span class="fp-spar-l">{st.l}</span>
          </div>
        {/each}
      </div>
      <p class="fp-spar-note">Tragbare Sparrate, jährlich dynamisiert.</p>
    </div>

    <!-- Budget + Warn -->
    <div class="fp-card fp-s8">
      <div class="fp-chead"><span class="fp-clabel">Reicht es für den Alltag?</span><span class="fp-chead-m">Ø 2-Personen-Haushalt · Destatis 2025</span></div>
      <div class="fp-budget-bar">
        {#each BUDGET as b}
          <div class="fp-budget-seg" style="width:{(b.value/BUDGET_TOT*100).toFixed(1)}%;background:{b.shade}"></div>
        {/each}
      </div>
      <div class="fp-budget-grid">
        {#each BUDGET as b}
          <div class="fp-bi">
            <span class="fp-bi-nm"><span class="fp-bi-dot" style="background:{b.shade}"></span>{b.label}</span>
            <span class="fp-bi-amt">{b.value} €</span>
          </div>
        {/each}
      </div>
      <div class="fp-budget-total"><span>Grundbedarf gesamt</span><span class="fp-budget-tot-amt">{de0.format(BUDGET_TOT)} €</span></div>
    </div>

    <div class="fp-card fp-warn-card fp-s4">
      <div class="fp-warn-big">{budgetOver > 0 ? '−' : '+'}{de0.format(budgetOver > 0 ? budgetOver : budgetShort)} €</div>
      <h3 class="fp-warn-h">{budgetOver > 0 ? `Für den Ø-Grundbedarf fehlen ${de0.format(budgetOver)} €/Mo.` : `${de0.format(budgetShort)} €/Mo. Spielraum über Grundbedarf`}</h3>
      <p class="fp-warn-body">Reale {mode==='pension'?'Pension':'Rente'}: {de0.format(nettoR)} €. Referenz: Destatis 2025 — Warmmiete variiert regional stark.</p>
    </div>

    <!-- Abzüge -->
    <div class="fp-card fp-s12">
      <div class="fp-chead"><span class="fp-clabel">Abzüge im Überblick</span><span class="fp-chead-m">§ 22 Nr. 1 EStG · SGB V</span></div>
      <div class="fp-ledger">
        <div class="fp-ln"><span class="fp-ln-lab">Brutto{mode==='pension'?'pension':'rente'}</span><span class="fp-ln-amt">{de0.format(brutto)} €</span></div>
        <div class="fp-ln"><span class="fp-ln-lab">Einkommensteuer<span class="fp-ln-sub">{mode==='pension'?'Versorgungsfreibetrag':'97 % steuerpflichtig'}</span></span><span class="fp-ln-amt fp-neg">−{de0.format(abzSteuer)} €</span></div>
        <div class="fp-ln"><span class="fp-ln-lab">KV + PV<span class="fp-ln-sub">gesetzlicher Abzug{mode==='pension' && P?.kv==='PKV'?' (PKV-Eigenanteil)':''}</span></span><span class="fp-ln-amt fp-neg">−{de0.format(abzKV)} €</span></div>
        <div class="fp-ln fp-ln-total"><span class="fp-ln-lab">Netto{mode==='pension'?'pension':'rente'}</span><span class="fp-ln-amt">{de0.format(nomNetto)} €</span></div>
      </div>
    </div>

    <!-- Empfehlungen -->
    {#each recos as rec}
      <div class="fp-card fp-rec fp-s4">
        <span class="fp-rec-badge">{rec.num}</span>
        <span class="fp-rec-tag">{rec.tag}</span>
        <h3 class="fp-rec-h">{rec.title}</h3>
        <p class="fp-rec-body">{rec.body}</p>
      </div>
    {/each}

  </div>

  <footer class="fp-foot">
    <div class="fp-disc"><span class="fp-disc-mark">▲</span><span>Kein Anlagehinweis. Diese Hinweise basieren auf Beobachtungen aus der Praxis — keine individuelle Empfehlung. Bitte prüfe mit einem unabhängigen Berater.</span></div>
    <div class="fp-src">Quelle: <strong>pensora.de</strong> — Niall Bradfield, unabhängiger Finanzberater, Stuttgart</div>
  </footer>
</div>

<style>
  /* ── Design tokens (light paper, monochrom + Signal-Rot) ── */
  .fp-wrap {
    --ink:     #0B0B0C;
    --ink2:    #3C3C40;
    --muted:   #8B8B90;
    --line:    #E6E6E3;
    --paper:   #FFFFFF;
    --paper2:  #F5F5F2;
    --paper3:  #ECECE8;
    --red:     #E5251B;
    --red-ink: #C21A12;
    --red-soft:#FBEAE8;
    --red-dark:#FF5247;
    --d-line:  #2A2A2C;
    --d-muted: #8A8A8F;
    --font: 'Plus Jakarta Sans', system-ui, sans-serif;

    font-family: var(--font);
    background: var(--paper2);
    color: var(--ink);
    padding: 0 40px 48px;
    max-width: 860px;
    margin: 0 auto;
    -webkit-font-smoothing: antialiased;
  }

  /* Header */
  .fp-topbar { display:flex; justify-content:space-between; align-items:center; padding:36px 4px 20px; }
  .fp-wordmark { font-size:18px; font-weight:700; letter-spacing:.28em; }
  .fp-topbar-right { text-align:right; }
  .fp-label-sm { font-size:10px; font-weight:600; letter-spacing:.16em; text-transform:uppercase; }
  .fp-muted-sm { font-size:10px; color:var(--muted); margin-top:3px; }
  .fp-prog { padding:0 4px 16px; font-size:10px; font-weight:600; letter-spacing:.14em; text-transform:uppercase; color:var(--muted); }

  /* Grid */
  .fp-grid { display:grid; grid-template-columns:repeat(12,1fr); gap:12px; }
  .fp-card {
    background:var(--paper); border:1px solid var(--line); border-radius:14px; padding:20px 22px;
    font-variant-numeric: tabular-nums lining-nums;
  }
  .fp-dark { background:var(--ink); border-color:var(--ink); color:#fff; }
  .fp-s3 { grid-column:span 3; } .fp-s4 { grid-column:span 4; }
  .fp-s5 { grid-column:span 5; } .fp-s7 { grid-column:span 7; }
  .fp-s8 { grid-column:span 8; } .fp-s12 { grid-column:span 12; }

  .fp-clabel { font-size:9.5px; font-weight:600; letter-spacing:.14em; text-transform:uppercase; color:var(--muted); }
  .fp-dark .fp-clabel { color:var(--d-muted); }
  .fp-chead { display:flex; justify-content:space-between; align-items:baseline; margin-bottom:14px; }
  .fp-chead-m { font-size:9.5px; color:var(--muted); }

  /* Gap card */
  .fp-gap-label { font-size:10px; font-weight:600; letter-spacing:.14em; text-transform:uppercase; color:var(--red-dark); }
  .fp-gap-big { font-size:68px; font-weight:700; line-height:.88; letter-spacing:-.03em; color:var(--red-dark); margin-top:12px; display:flex; align-items:baseline; }
  .fp-gap-unit { font-size:20px; font-weight:500; color:#fff; margin-left:8px; }
  .fp-gap-body { font-size:11.5px; line-height:1.5; color:#D2D2D5; margin:14px 0 0; }
  .fp-pill { display:inline-block; margin-top:14px; font-size:11px; font-weight:600; color:#fff; padding:6px 12px; border:1px solid var(--d-line); border-radius:999px; }
  .fp-pill b { color:var(--red-dark); }

  /* Kaufkraft card */
  .fp-real-big { font-size:50px; font-weight:700; letter-spacing:-.03em; line-height:.9; margin:10px 0; display:flex; align-items:baseline; }
  .fp-real-unit { font-size:16px; font-weight:500; color:var(--muted); margin-left:6px; }
  .fp-real-body { font-size:11px; color:var(--ink2); line-height:1.45; margin-bottom:12px; }
  .fp-mini { display:flex; flex-direction:column; }
  .fp-mini-r { display:flex; justify-content:space-between; font-size:11.5px; padding:8px 0; border-top:1px solid var(--line); }
  .fp-mini-lab { color:var(--muted); }
  .fp-mini-v { font-weight:600; }
  .fp-neg { color:var(--red-ink) !important; }

  /* KPI tiles */
  .fp-kpi .fp-clabel { margin-bottom:0; }
  .fp-kv { font-size:24px; font-weight:700; letter-spacing:-.02em; margin-top:10px; }
  .fp-ku { font-size:12px; font-weight:500; color:var(--muted); }
  .fp-kn { font-size:9.5px; color:var(--muted); margin-top:4px; }

  /* Timeline legend */
  .fp-legend { display:flex; flex-wrap:wrap; gap:16px; margin-top:12px; }
  .fp-legend-item { display:flex; align-items:center; gap:6px; font-size:10px; color:var(--ink2); }
  .fp-swatch { display:inline-block; width:18px; height:0; }
  .fp-sw-real { border-top:2.5px solid #0B0B0C; }
  .fp-sw-nom  { border-top:1.6px solid #B6B6BA; }
  .fp-sw-sb   { border-top:1.4px dotted #B6B6BA; }
  .fp-sw-ziel { border-top:1.4px dashed #E5251B; }

  /* Versorgungsanalyse */
  .fp-vbars { display:flex; flex-direction:column; gap:14px; }
  .fp-vbar-top { display:flex; justify-content:space-between; align-items:baseline; margin-bottom:6px; }
  .fp-vbar-name { font-size:11px; font-weight:600; }
  .fp-vbar-gap  { color:var(--red-ink); }
  .fp-vbar-val  { font-size:11.5px; font-weight:700; }
  .fp-track { height:24px; display:flex; overflow:hidden; background:var(--paper2); border-radius:5px; }
  .fp-track-full { background:var(--ink); }
  .fp-seg-ink { background:var(--ink); height:100%; }
  .fp-seg-gap { height:100%; background:repeating-linear-gradient(135deg,var(--red) 0 2px,transparent 2px 7px); border-left:1.5px solid var(--red); }

  /* Sparrate */
  .fp-spar { display:grid; grid-template-columns:repeat(4,1fr); gap:8px; align-items:end; height:120px; margin:4px 0; }
  .fp-spar-bar { display:flex; flex-direction:column; align-items:center; justify-content:flex-end; height:100%; }
  .fp-spar-fill { width:100%; background:var(--paper3); border-radius:4px 4px 0 0; }
  .fp-spar-bar:last-child .fp-spar-fill { background:var(--ink); }
  .fp-spar-v { font-size:13px; font-weight:700; margin-bottom:6px; }
  .fp-spar-l { font-size:9px; color:var(--muted); margin-top:6px; letter-spacing:.04em; text-transform:uppercase; }
  .fp-spar-note { font-size:10px; color:var(--muted); margin-top:12px; line-height:1.45; }

  /* Budget */
  .fp-budget-bar { height:26px; display:flex; overflow:hidden; margin-bottom:16px; border-radius:5px; }
  .fp-budget-seg { height:100%; }
  .fp-budget-grid { display:grid; grid-template-columns:1fr 1fr; column-gap:32px; }
  .fp-bi { display:flex; align-items:center; justify-content:space-between; padding:7px 0; border-bottom:1px solid var(--line); font-size:11.5px; }
  .fp-bi-nm { display:flex; align-items:center; gap:8px; color:var(--ink2); }
  .fp-bi-dot { width:7px; height:7px; border-radius:2px; }
  .fp-bi-amt { font-weight:600; }
  .fp-budget-total { display:flex; justify-content:space-between; align-items:baseline; border-top:1.5px solid var(--ink); margin-top:10px; padding-top:10px; font-size:11.5px; font-weight:700; }
  .fp-budget-tot-amt { font-size:18px; font-weight:700; }

  /* Warning card */
  .fp-warn-card { background:var(--red-soft) !important; border-color:#F3CFCB !important; display:flex; flex-direction:column; justify-content:center; }
  .fp-warn-big { font-size:42px; font-weight:700; color:var(--red-ink); letter-spacing:-.03em; line-height:.9; }
  .fp-warn-h { margin:12px 0 7px; font-size:12.5px; font-weight:700; color:var(--red-ink); }
  .fp-warn-body { margin:0; font-size:10.5px; color:var(--ink2); line-height:1.5; }

  /* Ledger */
  .fp-ledger { font-size:12px; }
  .fp-ln { display:flex; justify-content:space-between; align-items:baseline; padding:9px 0; border-bottom:1px solid var(--line); }
  .fp-ln-lab { color:var(--ink2); }
  .fp-ln-sub { display:block; font-size:9.5px; color:var(--muted); margin-top:2px; }
  .fp-ln-amt { font-weight:600; }
  .fp-ln-total { border-bottom:0; border-top:1.5px solid var(--ink); margin-top:2px; padding-top:10px; }
  .fp-ln-total .fp-ln-lab { color:var(--ink); font-weight:700; }
  .fp-ln-total .fp-ln-amt { font-size:18px; font-weight:700; }

  /* Recs */
  .fp-rec { position:relative; }
  .fp-rec-badge { position:absolute; top:20px; right:22px; width:24px; height:24px; border-radius:999px; border:1px solid var(--line); display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:700; color:var(--ink); }
  .fp-rec-tag { font-size:9px; font-weight:700; letter-spacing:.14em; color:var(--muted); display:block; }
  .fp-rec-h { font-size:13px; font-weight:700; margin:9px 0 8px; line-height:1.25; letter-spacing:-.01em; }
  .fp-rec-body { font-size:10.5px; line-height:1.5; color:var(--ink2); margin:0; }

  /* Footer */
  .fp-foot { margin-top:20px; padding:0 4px; }
  .fp-disc { display:flex; gap:9px; font-size:9.5px; color:var(--muted); line-height:1.5; max-width:90ch; }
  .fp-disc-mark { color:var(--red); font-weight:700; flex-shrink:0; }
  .fp-src { margin-top:9px; font-size:9.5px; color:var(--muted); }
  .fp-src strong { color:var(--ink2); font-weight:600; }

  /* Print */
  @media print {
    .fp-wrap { max-width:100%; padding:0 32px 40px; background:#fff; }
    .fp-card { break-inside:avoid; }
    * { -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  }
</style>
