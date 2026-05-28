<script>
  import { createEventDispatcher } from 'svelte';
  import Logo from '../components/Logo.svelte';
  import { fmtE, fmtP, de0 } from '../lib/utils.js';
  import { lineChart, barChart, legend } from '../lib/charts.js';

  export let P;
  export let result;

  const dispatch = createEventDispatcher();

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
    <button class="btn btng print-hide" on:click={() => window.print()} title="Als PDF speichern">⬇ PDF</button>
    <button class="btn btnp print-hide" on:click={() => window.open('https://tidycal.com/niallbradfield/kostenfreies-beratungsgesprach', '_blank')}>Beratung buchen →</button>
  </div>
</nav>

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
      </div>

      <!-- CTA sidebar -->
      <aside style="position:sticky;top:88px">
        <div class="card" style="border-color:var(--fg);position:relative;overflow:hidden">
          <div style="position:absolute;top:0;left:0;right:0;height:3px;background:var(--fg)"></div>
          <div class="ey" style="color:var(--loss)">Handlungsbedarf erkannt</div>
          <div style="margin-top:10px;font-family:var(--mono);font-size:28px;font-weight:600;color:var(--loss)">
            {realLuecke > 0 ? de0.format(Math.round(realLuecke * 12 * r.jruh / 1000) * 1000) + ' €' : '✓'}
          </div>
          <div style="font-size:11px;color:rgba(255,107,107,.6);font-family:var(--mono);margin-top:4px;margin-bottom:16px">weniger über den Ruhestand</div>
          <h3 style="font-size:20px;font-weight:500;line-height:1.2;color:var(--fg)">Jetzt gegensteuern — bevor die Lücke wächst.</h3>
          <p style="margin-top:10px;color:var(--fg2);font-size:13px;line-height:1.55">30 Min. kostenlos. Unabhängiger Finanzberater. Kein Verkauf.</p>
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
