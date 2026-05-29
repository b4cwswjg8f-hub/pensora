<script>
  import { createEventDispatcher } from 'svelte';
  import Logo from '../components/Logo.svelte';
  import PdfGate from '../components/PdfGate.svelte';
  import { fmtE, fmtP, de0 } from '../lib/utils.js';
  import { lineChart, legend } from '../lib/charts.js';

  export let R;
  export let result;

  const dispatch = createEventDispatcher();
  let showPdfGate = false;

  $: r = result;
  $: realLuecke = Math.max(R.zielEur - r.nettoR, 0);
  $: lifetimeLoss = Math.round(realLuecke * 12 * r.jruh / 1000) * 1000;
  $: realOk = r.nettoR >= R.zielEur;
  $: sl = [[r.spar,'Heute'],[r.spar*Math.pow(1.035,5),'+5 J.'],[r.spar*Math.pow(1.035,10),'+10 J.'],[r.spar*Math.pow(1.035,15),'+15 J.']];
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
  $: legendHtml = legend([['#60a5fa','Rente nominal'],['#4ade80','Real (Kaufkraft heute)','3 3'],['#FF6B6B','Klassisches Sparbuch (0,3 % real)','4 2'],['#fbbf24','Versorgungsziel','6 3']]);
</script>

<nav class="nav">
  <div class="row g16">
    <button class="brand" on:click={() => dispatch('back')}><Logo /> Pensora</button>
    <span style="color:var(--line2);font-size:16px">/</span>
    <span style="color:var(--fg2);font-size:14px">Ergebnis · Rente</span>
  </div>
  <div class="row g8">
    <button class="btn btng print-hide" on:click={() => dispatch('back')}>← Hub</button>
    <button class="btn btng print-hide" on:click={() => dispatch('recalc')}>← Neu berechnen</button>
    <button class="btn btng print-hide" on:click={() => showPdfGate = true} title="Als PDF speichern">⬇ PDF</button>
    <button class="btn btnp print-hide" on:click={() => window.open('https://tidycal.com/niallbradfield/kostenfreies-beratungsgesprach', '_blank')}>Beratung buchen →</button>
  </div>
</nav>

<PdfGate bind:show={showPdfGate} />

<div class="vscr">
  <div class="calc-result-pad">
    <div class="ey" style="margin-bottom:20px">Rentenprognose · {R.rentAlter} J. · Rentenwert 40,79 € (DRV 2025)</div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px">
      <div style="padding:32px;border-radius:var(--rlg);background:{realOk?'rgba(250,250,250,0.04)':'var(--loss-dim)'};border:2px solid {realOk?'var(--fg)':'var(--loss)'}">
        <div class="ey" style="color:{realOk?'var(--fg3)':'var(--loss)'};margin-bottom:16px">Deine reale Kaufkraft im Ruhestand · {r.rentJ}</div>
        <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:8px">
          <span class="stat" style="font-size:80px;color:{realOk?'var(--fg)':'var(--loss)'}">{de0.format(Math.round(r.nettoR))}</span>
          <span style="font-size:22px;color:var(--fg2)">€/Mo.</span>
        </div>
        <div style="font-size:13px;color:var(--fg3);margin-bottom:16px">= heutige Kaufkraft deiner Rente in {r.jbr} Jahren ({R.inf} % Inflation)</div>
        <div style="padding:12px 16px;background:rgba(0,0,0,.3);border-radius:var(--rmd);font-size:12px;color:var(--fg3)">
          Nominale Rente: <span style="font-family:var(--mono);color:var(--fg)">{fmtE(r.netto)}/Mo.</span> ·
          Inflationsverlust: <span style="font-family:var(--mono);color:var(--loss)">−{fmtE(r.netto-r.nettoR)}/Mo.</span>
        </div>
      </div>
      <div style="padding:32px;border-radius:var(--rlg);background:var(--loss-dim);border:2px solid var(--loss)">
        <div class="ey" style="color:var(--loss);margin-bottom:16px">Reale Rentenlücke (inflationsbereinigt)</div>
        <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:8px">
          <span class="stat" style="font-size:80px;color:var(--loss)">{realLuecke>0?'−'+de0.format(Math.round(realLuecke)):'✓'}</span>
          <span style="font-size:22px;color:rgba(255,107,107,.6)">{realLuecke>0?'€/Mo.':''}</span>
        </div>
        <div style="font-size:13px;color:rgba(255,107,107,.6);margin-bottom:16px">vs. Versorgungsziel {fmtE(R.zielEur)}/Mo. netto</div>
        {#if realLuecke > 0}
          <div style="padding:12px 16px;background:rgba(0,0,0,.3);border-radius:var(--rmd);font-size:13px;color:var(--loss);font-weight:600">
            = {de0.format(lifetimeLoss)} € weniger über {r.jruh} Jahre Ruhestand
          </div>
        {:else}
          <div style="font-size:13px;color:var(--fg2)">Deine Rente deckt dein Versorgungsziel.</div>
        {/if}
      </div>
    </div>

    <!-- KPI strip -->
    <div style="display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line);border-radius:var(--rlg);overflow:hidden;background:var(--bg1);margin-bottom:20px">
      {#each [['Nominal netto/Mo.',fmtE(r.netto),'ab '+r.rentJ],['Brutto/Mo.',fmtE(r.brutto),'vor Steuer & KV'],['Entgeltpunkte',r.gesEP.toFixed(1).replace('.',',')+' EP',r.gesJ+' Arbeitsjahre'],['Reale Kaufkraft',fmtE(r.nettoR),'in heutigen €']] as [l,v,sub], i}
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
          <div class="ey" style="margin-bottom:12px">Rentenentwicklung im Zeitverlauf</div>
          {@html chartSvg}
          {@html legendHtml}
        </div>
        {#if r.luecke > 0}
          <div class="card" style="padding:28px">
            <div class="ey" style="margin-bottom:14px">Sparrate (3,5 % p.a.)</div>
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
          <div class="ey" style="margin-bottom:14px">Abzüge (§ 22 Nr.1 EStG + SGB V)</div>
          <table>
            {#each [['Bruttorente',r.brutto,'var(--fg)',false],['Einkommensteuer ('+Math.round(r.bestAnt*100)+' %)',-r.stM,'var(--loss)',false],['KV+PV Rentner',-r.kvpv,'var(--fg3)',false],['Nettorente',r.netto,'var(--fg)',true]] as [l,v,c,bold]}
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
      </div>
      <aside style="position:sticky;top:88px">
        <div class="card" style="margin-bottom:12px;padding:20px">
          <div class="ey" style="margin-bottom:8px">Ergebnis sichern</div>
          <button class="btn" style="width:100%;height:48px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.18);border-radius:8px;font-size:14px;font-weight:600;gap:8px" on:click={() => showPdfGate = true}>
            ⬇ Als PDF speichern
          </button>
          <p style="font-size:11px;color:var(--fg4);margin-top:8px;text-align:center;line-height:1.4">E-Mail eingeben · sofort druckfertig</p>
        </div>
        <div class="card" style="border-color:var(--fg);position:relative;overflow:hidden">
          <div style="position:absolute;top:0;left:0;right:0;height:3px;background:var(--fg)"></div>
          <h3 style="font-size:22px;font-weight:500;margin-bottom:10px">Plane gegen die Rentenlücke.</h3>
          <p style="font-size:13px;color:var(--fg2);line-height:1.55;margin-bottom:0">30 Min. kostenlos. Unabhängiger Finanzberater. Kein Verkauf.</p>
          <button class="btn btnp btnlg" style="width:100%;margin-top:16px" on:click={() => window.open('https://tidycal.com/niallbradfield/kostenfreies-beratungsgesprach', '_blank')}>Kostenloses Gespräch buchen →</button>
          <button class="btn btng" style="width:100%;margin-top:8px" on:click={() => dispatch('recalc')}>← Neu berechnen</button>
          <div style="margin-top:20px;padding-top:16px;border-top:1px solid var(--line)">
            <div class="ey" style="margin-bottom:10px">Passende Rechner</div>
            {#each [['depot','AV-Depot-Rechner'],['ruerup','Rürup-Rechner']] as [k,l]}
              <button class="btn" style="width:100%;margin-bottom:8px;justify-content:flex-start" on:click={() => dispatch('navigate', k)}>{l} →</button>
            {/each}
          </div>
        </div>
      </aside>
    </div>
  </div>
</div>
