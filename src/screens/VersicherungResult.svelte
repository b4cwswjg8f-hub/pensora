<script>
  import { createEventDispatcher } from 'svelte';
  import Logo from '../components/Logo.svelte';
  import PdfGate from '../components/PdfGate.svelte';
  import PdfFinanzplan from '../components/PdfFinanzplan.svelte';
  import { fmtE, de0 } from '../lib/utils.js';
  import { VBENCH } from '../lib/calcs.js';
  import { BOOK_URL, BRAND_NAME } from '../lib/data.js';

  export let V;
  export let total;

  const dispatch = createEventDispatcher();
  const book = () => window.open(BOOK_URL, '_blank');
  let showPdfGate = false;
  let showFinanzplan = false;

  $: vKeys = Object.keys(VBENCH);
  $: avgTotal = vKeys.reduce((s, k) => s + VBENCH[k].avg, 0);
  $: diff = total - avgTotal;
  $: overKeys = vKeys.filter(k => V[k] > VBENCH[k].avg * 1.3);
  $: underKeys = vKeys.filter(k => V[k] < VBENCH[k].avg * 0.7);

  $: chartSvg = (() => {
    const w = 800, h = 260, pad = 40;
    const n = vKeys.length;
    const maxV = Math.max(...vKeys.flatMap(k => [V[k], VBENCH[k].avg])) * 1.2;
    const bw = 20, gap = (w - pad * 2 - n * bw * 2) / (n - 1);
    const ys = v => h - pad - Math.max(0, Math.min(v / maxV, 1)) * (h - pad * 2);
    const yh = v => Math.max(0, Math.min(v / maxV, 1)) * (h - pad * 2);
    let svg = `<svg viewBox="0 0 ${w} ${h}" width="100%" height="${h}" style="display:block">`;
    [0, 0.25, 0.5, 0.75, 1].forEach(f => {
      const y = ys(f * maxV);
      svg += `<line x1="${pad}" x2="${w - pad}" y1="${y.toFixed(1)}" y2="${y.toFixed(1)}" stroke="rgba(36,30,25,.14)" stroke-width="1" ${f > 0 ? 'stroke-dasharray="2 3"' : ''}/>`;
      svg += `<text x="${pad - 6}" y="${(y + 3).toFixed(1)}" fill="#8a7f74" font-size="9" font-family="'Geist Mono',ui-monospace" text-anchor="end">${de0.format(Math.round(f * maxV))}€</text>`;
    });
    vKeys.forEach((k, i) => {
      const x = pad + i * (bw * 2 + gap);
      const ist = Number(V[k]) || 0, avg = VBENCH[k].avg;
      const color = ist > avg * 1.3 ? '#FF6B6B' : ist < avg * 0.7 ? '#6fcf97' : '#e5e5e5';
      svg += `<rect x="${x}" y="${ys(ist).toFixed(1)}" width="${bw}" height="${yh(ist).toFixed(1)}" fill="${color}" opacity=".9" rx="2"/>`;
      svg += `<rect x="${x + bw + 2}" y="${ys(avg).toFixed(1)}" width="${bw - 2}" height="${yh(avg).toFixed(1)}" fill="#e5e5e5" opacity=".2" rx="2" stroke="#e5e5e5" stroke-width="1" stroke-dasharray="2 2"/>`;
      // Short label
      const short = k.split(' ')[0].replace(/[()]/g, '').substring(0, 8);
      svg += `<text x="${(x + bw).toFixed(1)}" y="${(h - pad + 16).toFixed(1)}" fill="#8a7f74" font-size="8" font-family="'Geist Mono',ui-monospace" text-anchor="middle">${short}</text>`;
    });
    svg += `</svg>`;
    return svg;
  })();
</script>

<nav class="nav">
  <div class="row g16">
    <button class="brand" on:click={() => dispatch('back')}><Logo /> {BRAND_NAME}</button>
    <span style="color:var(--line2);font-size:16px">/</span>
    <span style="color:var(--fg2);font-size:14px">Result · Insurance</span>
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
      <PdfFinanzplan mode="versicherung" {V} {total} />
    </div>
  </div>
{/if}

<div class="vscr">
  <div class="calc-result-pad">
    <div class="ey" style="margin-bottom:12px">Insurance Analysis · Actual vs. 2025 GDV Market Average</div>
    <h1 style="font-size:48px;font-weight:600;letter-spacing:-.04em;margin-bottom:28px">
      Total Cost: <span style="color:{diff > 20 ? 'var(--loss)' : diff < -20 ? '#6fcf97' : 'var(--fg)'}">{fmtE(total)}/mo.</span>
    </h1>

    <!-- KPI strip -->
    <div style="display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line);border-radius:var(--rlg);overflow:hidden;background:var(--bg1);margin-bottom:20px">
      {#each [
        ['Your Costs',fmtE(total)+'/mo.',de0.format(Math.round(total*12))+' €/year'],
        ['Market Average',fmtE(avgTotal)+'/mo.','GDV avg. 2025'],
        ['Difference',(diff>=0?'+':'')+fmtE(diff)+'/mo.',diff>20?'Above market':diff<-20?'Below market':'In line'],
        ['Extra/Year',diff>0?de0.format(Math.round(diff*12))+' €':'–',diff>0?'possible savings potential':'no extra cost'],
      ] as [l,v,sub], i}
        <div style="padding:24px;border-right:{i<3?'1px solid var(--line)':'0'}">
          <div class="ey" style="margin-bottom:10px">{l}</div>
          <div class="stat" style="font-size:28px;color:{i===2&&diff>20?'var(--loss)':i===2&&diff<-20?'#6fcf97':'var(--fg)'}">{v}</div>
          <div style="font-size:11px;color:var(--fg3);font-family:var(--mono);margin-top:6px">{sub}</div>
        </div>
      {/each}
    </div>

    <div style="display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:16px">
      <div class="col g16">
        <div class="cardf" style="padding:28px">
          <div class="ey" style="margin-bottom:12px">Your Premiums vs. Market Average · Monthly</div>
          {@html chartSvg}
          <div style="display:flex;gap:20px;flex-wrap:wrap;margin-top:12px;font-size:11px;font-family:var(--mono);color:var(--fg3)">
            <span style="display:flex;align-items:center;gap:6px"><span style="width:10px;height:10px;background:var(--fg);border-radius:2px;display:inline-block"></span>Your Premium</span>
            <span style="display:flex;align-items:center;gap:6px"><span style="width:10px;height:10px;background:var(--fg);opacity:.25;border-radius:2px;display:inline-block;border:1px dashed var(--fg)"></span>GDV Market Average</span>
            <span style="display:flex;align-items:center;gap:6px"><span style="width:10px;height:10px;background:#FF6B6B;border-radius:2px;display:inline-block"></span>Above Avg. (&gt;130%)</span>
            <span style="display:flex;align-items:center;gap:6px"><span style="width:10px;height:10px;background:#6fcf97;border-radius:2px;display:inline-block"></span>Below Avg. (&lt;70%)</span>
          </div>
        </div>

        <!-- Detail table -->
        <div class="cardf" style="padding:28px">
          <div class="ey" style="margin-bottom:16px">Detailed Comparison</div>
          <div style="display:grid;grid-template-columns:1fr auto auto auto;gap:0;border-top:1px solid var(--line)">
            {#each ['Insurance','Your Premium','GDV Avg.','Difference'] as h, i}
              <div style="padding:8px {i>0?'8px':'0'};font-size:10px;color:var(--fg3);font-family:var(--mono);text-transform:uppercase;letter-spacing:.08em;text-align:{i>0?'right':'left'}">{h}</div>
            {/each}
            {#each vKeys as k}
              {@const ist = Number(V[k]) || 0}
              {@const avg = VBENCH[k].avg}
              {@const d = ist - avg}
              {@const c = d > avg * 0.3 ? 'var(--loss)' : d < -avg * 0.3 ? '#6fcf97' : 'var(--fg)'}
              <div style="padding:10px 0;border-top:1px solid var(--line);font-size:13px;color:var(--fg2)">{k}</div>
              <div style="padding:10px 8px;border-top:1px solid var(--line);font-family:var(--mono);font-size:13px;text-align:right;color:{c}">{fmtE(ist)}</div>
              <div style="padding:10px 8px;border-top:1px solid var(--line);font-family:var(--mono);font-size:12px;text-align:right;color:var(--fg3)">{fmtE(avg)}</div>
              <div style="padding:10px 0;border-top:1px solid var(--line);font-family:var(--mono);font-size:12px;text-align:right;color:{c}">{d >= 0 ? '+' : ''}{fmtE(d)}</div>
            {/each}
            <div style="padding:10px 0;border-top:2px solid var(--fg);font-size:13px;font-weight:600">Total</div>
            <div style="padding:10px 8px;border-top:2px solid var(--fg);font-family:var(--mono);font-size:13px;text-align:right;font-weight:600">{fmtE(total)}</div>
            <div style="padding:10px 8px;border-top:2px solid var(--fg);font-family:var(--mono);font-size:12px;text-align:right;color:var(--fg3)">{fmtE(avgTotal)}</div>
            <div style="padding:10px 0;border-top:2px solid var(--fg);font-family:var(--mono);font-size:12px;text-align:right;color:{diff>20?'var(--loss)':diff<-20?'#6fcf97':'var(--fg)'}">{diff>=0?'+':''}{fmtE(diff)}</div>
          </div>
        </div>

        <!-- Flags -->
        {#if overKeys.length > 0 || underKeys.length > 0}
          <div class="card" style="padding:28px">
            <div class="ey" style="margin-bottom:14px">Optimization Notes</div>
            {#if overKeys.length > 0}
              <div style="margin-bottom:16px">
                <div style="font-size:12px;color:var(--loss);font-family:var(--mono);text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px">Above Market Average (&gt;130%)</div>
                {#each overKeys as k}
                  <div style="padding:10px 14px;background:rgba(255,107,107,.06);border:1px solid rgba(255,107,107,.2);border-radius:var(--rmd);margin-bottom:8px;font-size:13px">
                    <span style="font-weight:500">{k}</span>
                    <span style="color:var(--fg3);margin-left:8px;font-family:var(--mono)">{fmtE(V[k])}/mo. vs. avg. {fmtE(VBENCH[k].avg)}/mo.</span>
                    <div style="font-size:11px;color:var(--fg3);margin-top:4px">{VBENCH[k].hint} — worth comparing offers.</div>
                  </div>
                {/each}
              </div>
            {/if}
            {#if underKeys.length > 0}
              <div>
                <div style="font-size:12px;color:#6fcf97;font-family:var(--mono);text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px">Below Market Average (&lt;70%) — check for underinsurance</div>
                {#each underKeys as k}
                  <div style="padding:10px 14px;background:rgba(111,207,151,.06);border:1px solid rgba(111,207,151,.2);border-radius:var(--rmd);margin-bottom:8px;font-size:13px">
                    <span style="font-weight:500">{k}</span>
                    <span style="color:var(--fg3);margin-left:8px;font-family:var(--mono)">{fmtE(V[k])}/mo. vs. avg. {fmtE(VBENCH[k].avg)}/mo.</span>
                    <div style="font-size:11px;color:var(--fg3);margin-top:4px">{VBENCH[k].hint}</div>
                  </div>
                {/each}
              </div>
            {/if}
          </div>
        {/if}
      </div>

      <aside style="position:sticky;top:88px">
        <div class="card" style="margin-bottom:12px;padding:20px">
          <div class="ey" style="margin-bottom:8px">Save Your Result</div>
          <button class="btn" style="width:100%;height:48px;background:rgba(36,30,25,.05);border:1px solid rgba(36,30,25,.18);border-radius:8px;font-size:14px;font-weight:600;gap:8px" on:click={() => showFinanzplan = true}>
            ⬇ Save as PDF
          </button>
          <p style="font-size:11px;color:var(--fg4);margin-top:8px;text-align:center;line-height:1.4">Enter your email · ready to print instantly</p>
        </div>
        <div class="card" style="border-color:var(--fg);position:relative;overflow:hidden">
          <div style="position:absolute;top:0;left:0;right:0;height:3px;background:var(--fg)"></div>
          <h3 style="font-size:22px;font-weight:500;margin-bottom:10px">Optimize your insurance.</h3>
          <p style="font-size:13px;color:var(--fg2);line-height:1.55">Over-insurance, gaps, or the best provider — an independent check is worth it. 30 min., free.</p>
          <button class="btn btnp btnlg" style="width:100%;margin-top:16px" on:click={book}>Book a Free Call →</button>
          <button class="btn btng" style="width:100%;margin-top:8px" on:click={() => dispatch('recalc')}>← Recalculate</button>
          <div style="margin-top:20px;padding-top:16px;border-top:1px solid var(--line)">
            <div class="ey" style="margin-bottom:10px">Related Calculators</div>
            {#each [['cashflow','Cashflow Calculator'],['depot','ETF Savings Plan Calculator'],['ruerup','Rürup Calculator']] as [k,l]}
              <button class="btn" style="width:100%;margin-bottom:8px;justify-content:flex-start" on:click={() => dispatch('navigate', k)}>{l} →</button>
            {/each}
          </div>
        </div>
      </aside>
    </div>
  </div>
</div>
