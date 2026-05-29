<script>
  import { createEventDispatcher } from 'svelte';
  import Logo from '../components/Logo.svelte';
  import PdfGate from '../components/PdfGate.svelte';
  import PdfFinanzplan from '../components/PdfFinanzplan.svelte';
  import { fmtE, fmtP, de0 } from '../lib/utils.js';
  import { lineChart, barChart, legend } from '../lib/charts.js';

  export let P;
  export let result;

  const dispatch = createEventDispatcher();
  let showPdfGate = false;
  let showFinanzplan = false;

  $: r = result;
  $: realLuecke = Math.max(P.zielEur - r.nettoR, 0);
  $: lifetimeLoss = Math.round(realLuecke * 12 * r.jruh / 1000) * 1000;
  $: realOk = r.nettoR >= P.zielEur;
  $: sl = [[r.spar,'Heute starten'],[r.spar*Math.pow(1.035,5),'+5 Jahre'],[r.spar*Math.pow(1.035,10),'+10 Jahre'],[r.spar*Math.pow(1.035,15),'+15 Jahre']];
  $: yr = new Date().getFullYear();

  $: chartSvg = (() => {
    const yrs = 30;
    const pension = Array.from({length:yrs+1},(_,i)=>r.netto*Math.pow(1.018,i));
    const pensionR = Array.from({length:yrs+1},(_,i)=>r.netto/Math.pow(1.021,i));
    const sparbuch = Array.from({length:yrs+1},(_,i)=>r.netto*Math.pow(1.003,i));
    const ziel = Array.from({length:yrs+1},()=>P.zielEur);
    return lineChart([
      {data:pension,color:'#60a5fa',fill:true,width:2},
      {data:pensionR,color:'#4ade80',dash:'3 3',width:1.5},
      {data:sparbuch,color:'#FF6B6B',dash:'4 2',width:1.5},
      {data:ziel,color:'#fbbf24',dash:'6 3',width:1},
    ], yrs);
  })();

  $: barSvg = barChart([
    {label:'Brutto-\npension',val:r.brutto,color:'#3b82f6'},
    {label:'Netto-\npension',val:r.netto,color:'#60a5fa'},
    {label:'Real\n(Kaufkraft)',val:r.nettoR,color:'#4ade80'},
    {label:'Versorgungs-\nziel',val:P.zielEur,color:'#fbbf24'},
    {label:'Lücke',val:r.luecke,color:'#FF6B6B'},
  ]);

  $: legendHtml = legend([['#60a5fa','Pension nominal'],['#4ade80','Real (Kaufkraft heute)','3 3'],['#FF6B6B','Klassisches Sparbuch','4 2'],['#fbbf24','Versorgungsziel','6 3']]);

  // Gap diagram: 2 bars — Ziel | Pension(blue)+Lücke(red) stacked
  $: gapSvg = (() => {
    const w = 600, h = 320, padL = 64, padB = 52, padT = 48, padR = 60;
    const plotH = h - padT - padB;
    const goal = P.zielEur;
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
    // Grid
    [0,.25,.5,.75,1].forEach(f => {
      const yg = baseY - sc(f * maxVal);
      s += `<line x1="${padL}" x2="${w-padR}" y1="${yg.toFixed(1)}" y2="${yg.toFixed(1)}" stroke="#1c1c1c" stroke-width="1" ${f>0?'stroke-dasharray="3 3"':''}/>`;
      s += `<text x="${padL-8}" y="${(yg+3).toFixed(1)}" fill="#6b6b6b" font-size="10" font-family="'Geist Mono',monospace" text-anchor="end">${de0.format(Math.round(f*maxVal))}€</text>`;
    });
    // Goal dashed line
    const glY = baseY - sc(goal);
    s += `<line x1="${padL}" x2="${w-padR}" y1="${glY.toFixed(1)}" y2="${glY.toFixed(1)}" stroke="rgba(251,191,36,.4)" stroke-width="1" stroke-dasharray="6 4"/>`;

    // Bar 1: Versorgungsziel (amber)
    const gbH = sc(goal), gbY = baseY - gbH;
    s += `<rect x="${x1}" y="${gbY.toFixed(1)}" width="${bw}" height="${gbH.toFixed(1)}" fill="rgba(251,191,36,.18)" stroke="rgba(251,191,36,.6)" stroke-width="1.5" rx="5"/>`;
    s += `<text x="${(x1+bw/2).toFixed(1)}" y="${(gbY+gbH/2+5).toFixed(1)}" fill="rgba(251,191,36,.95)" font-size="14" font-weight="700" text-anchor="middle" font-family="'Geist Mono',monospace">${fmtE(goal)}</text>`;

    // Bar 2: Stacked — pension (blue, bottom) + Lücke (red, top)
    const ph = sc(actual), py = baseY - ph;
    if (luecke > 0) {
      const lh = sc(luecke), ly = py - lh;
      // Red gap on top
      s += `<rect x="${x2}" y="${ly.toFixed(1)}" width="${bw}" height="${lh.toFixed(1)}" fill="rgba(255,107,107,.22)" stroke="rgba(255,107,107,.65)" stroke-width="1.5" rx="5"/>`;
      if (lh > 28) s += `<text x="${(x2+bw/2).toFixed(1)}" y="${(ly+lh/2+5).toFixed(1)}" fill="#FF6B6B" font-size="13" font-weight="700" text-anchor="middle" font-family="'Geist Mono',monospace">−${fmtE(luecke)}</text>`;
      // Blue pension on bottom
      s += `<rect x="${x2}" y="${py.toFixed(1)}" width="${bw}" height="${ph.toFixed(1)}" fill="rgba(96,165,250,.25)" stroke="rgba(96,165,250,.7)" stroke-width="1.5" rx="5"/>`;
      if (ph > 28) s += `<text x="${(x2+bw/2).toFixed(1)}" y="${(py+ph/2+5).toFixed(1)}" fill="rgba(96,165,250,.95)" font-size="13" font-weight="700" text-anchor="middle" font-family="'Geist Mono',monospace">${fmtE(actual)}</text>`;
    } else {
      s += `<rect x="${x2}" y="${py.toFixed(1)}" width="${bw}" height="${ph.toFixed(1)}" fill="rgba(74,222,128,.25)" stroke="rgba(74,222,128,.65)" stroke-width="1.5" rx="5"/>`;
      if (ph > 28) s += `<text x="${(x2+bw/2).toFixed(1)}" y="${(py+ph/2+5).toFixed(1)}" fill="rgba(74,222,128,.95)" font-size="14" font-weight="700" text-anchor="middle" font-family="'Geist Mono',monospace">✓ ${fmtE(actual)}</text>`;
    }
    const lblY = baseY + 18;
    s += `<text x="${(x1+bw/2).toFixed(1)}" y="${lblY}" fill="#6b6b6b" font-size="10" text-anchor="middle" font-family="'Geist Mono',monospace">Versorgungsziel</text>`;
    s += `<text x="${(x2+bw/2).toFixed(1)}" y="${lblY}" fill="#6b6b6b" font-size="10" text-anchor="middle" font-family="'Geist Mono',monospace">Pension real${luecke>0?' + Lücke':' ✓'}</text>`;
    s += `</svg>`;
    return s;
  })();

  // Living-costs story section
  const KOSTEN = [
    { label: 'Warmmiete', val: 960, color: '#60a5fa' },
    { label: 'Lebensmittel', val: 440, color: '#4ade80' },
    { label: 'Transport', val: 210, color: '#fbbf24' },
    { label: 'Energie', val: 160, color: '#a78bfa' },
    { label: 'Kommunikation', val: 65, color: '#f97316' },
    { label: 'Bekleidung', val: 80, color: '#ec4899' },
    { label: 'Gesundheit', val: 110, color: '#14b8a6' },
  ];
  const KOSTEN_TOT = KOSTEN.reduce((s, k) => s + k.val, 0); // 2.025 €
  $: spielraum = r.nettoR - KOSTEN_TOT;

  // Recommendation engine
  $: recos = (() => {
    const list = [];
    if (P.kv === 'GKV') {
      list.push({ icon: '💊', title: 'PKV-Wechsel prüfen', text: 'Beamte mit 70 % Beihilfe zahlen in der GKV oft 200–300 €/Mo. mehr als nötig. Ein gezielter PKV-Tarif-Vergleich zeigt das Potenzial — ohne Lückenrisiko.', nav: 'versicherung', cta: 'Versicherungscheck →' });
    }
    if (realLuecke > 500) {
      list.push({ icon: '📈', title: 'Rürup + AV-Depot kombinieren', text: `Bei einer realen Lücke von ${fmtE(realLuecke)}/Mo. kombinieren viele Beamte den Rürup-ETF (Steuervorteil bis 42 %) mit dem AV-Depot-Sparkonto (540 €/Jahr Grundzulage ab 2027).`, nav: 'ruerup', cta: 'Rürup-Rechner →' });
    } else if (realLuecke > 150) {
      list.push({ icon: '🏦', title: 'AV-Depot-Sparkonto aufbauen', text: `Ab 2027: 540 €/Jahr Grundzulage + steuerfreie Anlage bis 3.000 €. Für eine Lücke von ${fmtE(realLuecke)}/Mo. kann das den Unterschied machen.`, nav: 'depot', cta: 'AV-Depot-Rechner →' });
    }
    if (P.eltern && realLuecke > 0) {
      list.push({ icon: '👨‍👩‍👧', title: 'Kinderzulage: 300 €/Jahr je Kind', text: 'Das neue AV-Depot-Sparkonto bringt ab 2027 zusätzlich 300 €/Jahr je kindergeldberechtigtem Kind — kombinierbar mit der Grundzulage.', nav: 'depot', cta: 'Mehr erfahren →' });
    }
    return list;
  })();
</script>

<nav class="nav">
  <div class="row g16">
    <button class="brand" on:click={() => dispatch('back')}><Logo /> Pensora</button>
    <span style="color:var(--line2);font-size:16px">/</span>
    <span style="color:var(--fg2);font-size:14px">Ergebnis · Pension</span>
  </div>
  <div class="row g8">
    <button class="btn btng print-hide" on:click={() => dispatch('back')}>← Hub</button>
    <button class="btn btng print-hide" on:click={() => dispatch('recalc')}>← Neu berechnen</button>
    <button class="btn btng print-hide" on:click={() => showFinanzplan = true} title="Als PDF speichern">⬇ PDF</button>
    <button class="btn btnp print-hide" on:click={() => window.open('https://tidycal.com/niallbradfield/kostenfreies-beratungsgesprach', '_blank')}>Beratung buchen →</button>
  </div>
</nav>

<PdfGate bind:show={showPdfGate} />

{#if showFinanzplan}
  <div class="fp-overlay" on:click|self={() => showFinanzplan = false}>
    <div class="fp-overlay-inner">
      <button class="fp-overlay-close" on:click={() => showFinanzplan = false}>✕ Schließen</button>
      <PdfFinanzplan mode="pension" {P} {result} />
    </div>
  </div>
{/if}

<div class="vscr">
  <div class="calc-result-pad">
    <div class="ey" style="margin-bottom:20px">Pensionsanalyse · {P.bGr} · St.{P.bSt} · {P.bund.split('-')[0]} · {yr}</div>

    <!-- Hero grid -->
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px">
      <div style="padding:32px;border-radius:var(--rlg);background:{realOk ? 'rgba(250,250,250,0.04)' : 'var(--loss-dim)'};border:2px solid {realOk ? 'var(--fg)' : 'var(--loss)'}">
        <div class="ey" style="color:{realOk ? 'var(--fg3)' : 'var(--loss)'};margin-bottom:16px">Deine reale Kaufkraft im Ruhestand · {r.pensJ}</div>
        <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:8px">
          <span class="stat" style="font-size:80px;color:{realOk ? 'var(--fg)' : 'var(--loss)'}">{de0.format(Math.round(r.nettoR))}</span>
          <span style="font-size:22px;color:var(--fg2)">€/Mo.</span>
        </div>
        <div style="font-size:13px;color:var(--fg3);margin-bottom:16px">= heutige Kaufkraft deiner Pension in {r.jbp} Jahren (2,1 % Inflation)</div>
        <div style="padding:12px 16px;background:rgba(0,0,0,.3);border-radius:var(--rmd);font-size:12px;color:var(--fg3)">
          Nominale Pension: <span style="font-family:var(--mono);color:var(--fg)">{fmtE(r.netto)}/Mo.</span> ·
          Inflationsverlust: <span style="font-family:var(--mono);color:var(--loss)">−{fmtE(r.netto - r.nettoR)}/Mo.</span>
        </div>
      </div>
      <div style="padding:32px;border-radius:var(--rlg);background:var(--loss-dim);border:2px solid var(--loss)">
        <div class="ey" style="color:var(--loss);margin-bottom:16px">Reale Versorgungslücke (inflationsbereinigt)</div>
        <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:8px">
          <span class="stat" style="font-size:80px;color:var(--loss)">{realLuecke > 0 ? '−' + de0.format(Math.round(realLuecke)) : '✓'}</span>
          <span style="font-size:22px;color:rgba(255,107,107,.6)">{realLuecke > 0 ? '€/Mo.' : ''}</span>
        </div>
        <div style="font-size:13px;color:rgba(255,107,107,.6);margin-bottom:16px">vs. Versorgungsziel {fmtE(P.zielEur)}/Mo. netto</div>
        {#if realLuecke > 0}
          <div style="padding:12px 16px;background:rgba(0,0,0,.3);border-radius:var(--rmd);font-size:13px;color:var(--loss);font-weight:600">
            = {de0.format(lifetimeLoss)} € weniger über {r.jruh} Jahre Ruhestand
          </div>
        {:else}
          <div style="font-size:13px;color:var(--fg2)">Deine Pension deckt dein Versorgungsziel.</div>
        {/if}
      </div>
    </div>

    <!-- KPI strip -->
    <div style="display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line);border-radius:var(--rlg);overflow:hidden;background:var(--bg1);margin-bottom:20px">
      {#each [['Nominal netto/Mo.',fmtE(r.netto),'ab '+r.pensJ],['Brutto/Mo.',fmtE(r.brutto),'vor Steuer & KV'],['Ruhegehaltssatz',fmtP(r.satz),r.gdj+' Dienstjahre'],['Reale Kaufkraft',fmtE(r.nettoR),'in heutigen €']] as [l,v,sub], i}
        <div style="padding:20px 24px;border-right:{i<3?'1px solid var(--line)':'0'}">
          <div class="ey" style="margin-bottom:8px">{l}</div>
          <div class="stat" style="font-size:28px;color:{i===3&&!realOk?'var(--loss)':'var(--fg)'}">{v}</div>
          <div style="font-size:11px;color:var(--fg3);font-family:var(--mono);margin-top:4px">{sub}</div>
        </div>
      {/each}
    </div>

    <div style="display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:16px">
      <div class="col g16">
        <!-- Chart -->
        <div class="cardf" style="padding:28px">
          <div class="row" style="justify-content:space-between;align-items:flex-end;margin-bottom:16px">
            <div>
              <div class="ey">Entwicklung deiner Pension im Zeitverlauf</div>
              <div style="font-size:13px;color:var(--fg3);margin-top:4px">Nominal vs. real vs. Sparbuch vs. Versorgungsziel</div>
            </div>
          </div>
          {@html chartSvg}
          {@html legendHtml}
        </div>

        <!-- Bar chart -->
        <div class="cardf" style="padding:28px">
          <div class="ey" style="margin-bottom:16px">Vergleich Monatsbeträge</div>
          {@html barSvg}
        </div>

        <!-- Details -->
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
          <div class="cardf" style="padding:28px">
            <div class="ey" style="margin-bottom:14px">Abzüge (§ 19 EStG)</div>
            <table>
              {#each [['Bruttopension',r.brutto,'var(--fg)',false],['VersorgungsFB',-(r.vfb/12),'var(--fg3)',false],['Einkommensteuer',-r.stM,'var(--loss)',false],['KV + PV',-r.kvpv,'var(--fg3)',false],['Nettopension',r.netto,'var(--fg)',true]] as [l,v,c,bold]}
                <tr>
                  <td style="color:{bold?'var(--fg)':'var(--fg2)'};font-weight:{bold?600:400}">
                    <span style="display:inline-block;width:8px;height:8px;background:{c};border-radius:2px;margin-right:8px"></span>{l}
                  </td>
                  <td style="text-align:right;font-family:var(--mono);color:{v<0?'var(--loss)':'var(--fg)'};font-weight:{bold?700:500};font-size:{bold?15:13}px">
                    {v < 0 ? '−' : ''}{fmtE(Math.abs(v))}
                  </td>
                </tr>
              {/each}
            </table>
          </div>
          <div class="cardf" style="padding:28px">
            <div class="ey" style="margin-bottom:14px">§ 14 BeamtVG Berechnung</div>
            {#each [['Anrechenb. Dienstj.',r.gdj+' J'],['Ruhegehaltssatz',fmtP(r.satz)],['Max. 71,75 %','40 Dienstjahre'],['Mindestversorgung',fmtE(r.mindest)+'/Mo.']] as [l,v]}
              <div class="row" style="justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--line);font-size:13px">
                <span style="color:var(--fg2)">{l}</span>
                <span style="font-family:var(--mono)">{v}</span>
              </div>
            {/each}
            <div style="margin-top:12px">
              <div class="bart"><div class="barf" style="width:{(r.satz/0.7175*100).toFixed(1)}%"></div></div>
              <div class="row" style="font-size:10px;color:var(--fg4);margin-top:4px">
                <span>0%</span><span class="grow" style="text-align:center">{fmtP(r.satz)}</span><span>71,75%</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Sparrate -->
        {#if r.luecke > 0}
          <div class="card" style="padding:28px">
            <div class="ey" style="margin-bottom:14px">Sparrate zum Schließen der Lücke (3,5 % p.a.)</div>
            <div style="display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid var(--line)">
              {#each sl as [v,k], i}
                <div style="padding:16px 0;border-right:{i<3?'1px solid var(--line)':'0'};padding-left:{i>0?'16px':'0'}">
                  <div style="font-size:10px;color:{i===0?'var(--fg)':'var(--fg3)'};font-family:var(--mono);text-transform:uppercase;letter-spacing:.08em">{k}</div>
                  <div style="margin-top:8px;font-family:var(--mono);font-size:22px;color:{i===0?'var(--fg)':'var(--fg2)'};font-weight:500">{fmtE(v)}</div>
                </div>
              {/each}
            </div>
          </div>
        {/if}

        <!-- Gap diagram: stacked -->
        <div class="cardf" style="padding:28px">
          <div class="ey" style="margin-bottom:6px">Versorgungsanalyse auf einen Blick</div>
          <div style="font-size:13px;color:var(--fg3);margin-bottom:20px">Wunschrente · Pension real · {realLuecke > 0 ? 'Versorgungslücke auf Pension gestapelt' : 'Versorgungsziel gedeckt ✓'}</div>
          {@html gapSvg}
          <div style="display:flex;gap:20px;flex-wrap:wrap;margin-top:14px;font-size:11px;font-family:var(--mono);color:var(--fg3)">
            <span style="display:flex;align-items:center;gap:6px"><span style="width:10px;height:10px;background:rgba(251,191,36,.5);border:1px solid rgba(251,191,36,.7);border-radius:2px;display:inline-block"></span>Versorgungsziel</span>
            <span style="display:flex;align-items:center;gap:6px"><span style="width:10px;height:10px;background:rgba(96,165,250,.4);border:1px solid rgba(96,165,250,.7);border-radius:2px;display:inline-block"></span>Pension real</span>
            {#if realLuecke > 0}<span style="display:flex;align-items:center;gap:6px"><span style="width:10px;height:10px;background:rgba(255,107,107,.35);border:1px solid rgba(255,107,107,.65);border-radius:2px;display:inline-block"></span>Lücke (gestapelt)</span>{/if}
          </div>
        </div>

        <!-- Story: Reicht es für die Basics? -->
        <div class="cardf" style="padding:28px">
          <div class="ey" style="margin-bottom:6px">Reicht es für den Alltag?</div>
          <div style="font-size:13px;color:var(--fg3);margin-bottom:20px">Ø 2-Personen-Haushalt Deutschland 2025 · Destatis-Referenzwerte</div>
          <!-- Horizontal bar: pension vs. costs -->
          <div style="position:relative;height:48px;background:rgba(255,255,255,.04);border-radius:8px;overflow:hidden;margin-bottom:16px">
            {#each (() => { let x=0; return KOSTEN.map(k => { const pct = k.val / Math.max(r.nettoR, KOSTEN_TOT) * 100; const left = x; x+=pct; return {...k, pct, left}; }); })() as k}
              <div style="position:absolute;top:0;left:{k.left.toFixed(1)}%;width:{k.pct.toFixed(1)}%;height:100%;background:{k.color};opacity:.55"></div>
            {/each}
            {#if r.nettoR >= KOSTEN_TOT}
              <div style="position:absolute;top:0;left:{(KOSTEN_TOT/Math.max(r.nettoR,KOSTEN_TOT)*100).toFixed(1)}%;width:{((r.nettoR-KOSTEN_TOT)/Math.max(r.nettoR,KOSTEN_TOT)*100).toFixed(1)}%;height:100%;background:rgba(74,222,128,.3);border-left:2px solid rgba(74,222,128,.7)"></div>
            {/if}
            <!-- Pension marker line -->
            {#if r.nettoR < KOSTEN_TOT}
              <div style="position:absolute;top:0;left:{(r.nettoR/KOSTEN_TOT*100).toFixed(1)}%;width:2px;height:100%;background:rgba(255,107,107,.9)"></div>
            {/if}
          </div>
          <!-- Category table -->
          <div style="display:grid;grid-template-columns:1fr auto auto;gap:0;border-top:1px solid var(--line);margin-bottom:12px">
            {#each KOSTEN as k}
              <div style="display:flex;align-items:center;gap:8px;padding:7px 0;border-bottom:1px solid var(--line);font-size:12px;color:var(--fg2)">
                <span style="width:8px;height:8px;background:{k.color};opacity:.8;border-radius:2px;flex-shrink:0;display:inline-block"></span>
                {k.label}
              </div>
              <div style="padding:7px 12px;border-bottom:1px solid var(--line);font-family:var(--mono);font-size:12px;text-align:right;color:var(--fg3)">Ø</div>
              <div style="padding:7px 0;border-bottom:1px solid var(--line);font-family:var(--mono);font-size:12px;text-align:right">{fmtE(k.val)}</div>
            {/each}
            <div style="padding:10px 0;font-size:13px;font-weight:600">Grundbedarf gesamt</div>
            <div style="padding:10px 12px;font-family:var(--mono);font-size:13px;text-align:right;color:var(--fg3)">Ø</div>
            <div style="padding:10px 0;font-family:var(--mono);font-size:13px;text-align:right;font-weight:600">{fmtE(KOSTEN_TOT)}</div>
          </div>
          <div style="padding:14px 16px;border-radius:8px;background:{spielraum >= 0 ? 'rgba(74,222,128,.06)' : 'rgba(255,107,107,.06)'};border:1px solid {spielraum >= 0 ? 'rgba(74,222,128,.2)' : 'rgba(255,107,107,.2)'}">
            {#if spielraum >= 0}
              <div style="font-size:14px;font-weight:600;color:#4ade80">✓ Grundbedarf gedeckt — {fmtE(spielraum)}/Mo. Spielraum</div>
              <div style="font-size:12px;color:var(--fg3);margin-top:4px">Nach Ø-Ausgaben verbleiben {fmtE(spielraum)}/Mo. für Freizeit, Urlaub und Rücklagen.</div>
            {:else}
              <div style="font-size:14px;font-weight:600;color:var(--loss)">⚠ Für Ø-Grundbedarf fehlen {fmtE(Math.abs(spielraum))}/Mo.</div>
              <div style="font-size:12px;color:var(--fg3);margin-top:4px">Die reale Pension deckt die durchschnittlichen Grundausgaben nicht vollständig ab.</div>
            {/if}
          </div>
          <div style="font-size:10px;color:var(--fg4);margin-top:10px;font-family:var(--mono)">Referenz: Destatis 2025 · 2-Personen-Haushalt Deutschland · Warmmiete regional variiert stark</div>
        </div>

        <!-- Recommendations -->
        {#if recos.length > 0}
          <div class="card" style="padding:28px">
            <div class="ey" style="margin-bottom:14px">Was andere in Ihrer Situation gewählt haben</div>
            {#each recos as rec}
              <div style="padding:16px;background:rgba(255,255,255,.03);border:1px solid var(--line2);border-radius:10px;margin-bottom:10px">
                <div style="font-size:14px;font-weight:600;margin-bottom:6px">{rec.icon} {rec.title}</div>
                <div style="font-size:13px;color:var(--fg2);line-height:1.6;margin-bottom:10px">{rec.text}</div>
                <button class="btn btng" style="height:34px;font-size:12px" on:click={() => dispatch('navigate', rec.nav)}>{rec.cta}</button>
              </div>
            {/each}
            <div style="font-size:10px;color:var(--fg4);margin-top:12px;line-height:1.5;font-family:var(--mono)">
              ⚠ Kein Anlagehinweis. Diese Hinweise basieren auf Beobachtungen aus der Praxis — keine individuelle Empfehlung. Bitte prüfe mit einem unabhängigen Berater.
            </div>
          </div>
        {/if}
      </div>

      <!-- CTA sidebar -->
      <aside style="position:sticky;top:88px">
        <!-- PDF save card -->
        <div class="card" style="margin-bottom:12px;padding:20px">
          <div class="ey" style="margin-bottom:8px">Ergebnis sichern</div>
          <button class="btn" style="width:100%;height:48px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.18);border-radius:8px;font-size:14px;font-weight:600;gap:8px" on:click={() => showFinanzplan = true}>
            ⬇ Finanzplan als PDF
          </button>
          <p style="font-size:11px;color:var(--fg4);margin-top:8px;text-align:center;line-height:1.4">Druckfertig · professionelles Layout</p>
        </div>
        <!-- Consultation card -->
        <div class="card" style="border-color:var(--fg);position:relative;overflow:hidden">
          <div style="position:absolute;top:0;left:0;right:0;height:3px;background:var(--fg)"></div>
          <div class="ey" style="color:var(--loss)">Handlungsbedarf erkannt</div>
          <div style="margin-top:10px;font-family:var(--mono);font-size:28px;font-weight:600;color:var(--loss)">
            {realLuecke > 0 ? de0.format(Math.round(realLuecke * 12 * r.jruh / 1000) * 1000) + ' €' : '✓'}
          </div>
          <div style="font-size:11px;color:rgba(255,107,107,.6);font-family:var(--mono);margin-top:4px;margin-bottom:16px">weniger über den Ruhestand</div>
          <h3 style="font-size:20px;font-weight:500;line-height:1.2;color:var(--fg)">Jetzt gegensteuern — bevor die Lücke wächst.</h3>
          <p style="margin-top:10px;color:var(--fg2);font-size:13px;line-height:1.55">30 Min. kostenlos. Unabhängiger Finanzberater.</p>
          <button class="btn btnp btnlg" style="width:100%;margin-top:16px" on:click={() => window.open('https://tidycal.com/niallbradfield/kostenfreies-beratungsgesprach', '_blank')}>Kostenloses Gespräch buchen →</button>
          <button class="btn btng" style="width:100%;margin-top:8px" on:click={() => dispatch('recalc')}>← Neu berechnen</button>
          <div style="margin-top:20px;padding-top:16px;border-top:1px solid var(--line)">
            <div class="ey" style="margin-bottom:10px">Weitere Rechner</div>
            {#each [['depot','AV-Depot-Rechner'],['ruerup','Rürup-Rechner'],['cashflow','Cashflow-Rechner']] as [k,l]}
              <button class="btn" style="width:100%;margin-bottom:8px;justify-content:flex-start" on:click={() => dispatch('navigate', k)}>{l} →</button>
            {/each}
          </div>
        </div>
      </aside>
    </div>
  </div>
</div>
