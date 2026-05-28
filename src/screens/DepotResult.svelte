<script>
  import { createEventDispatcher } from 'svelte';
  import Logo from '../components/Logo.svelte';
  import { fmtE, de0 } from '../lib/utils.js';
  import { barChart, legend } from '../lib/charts.js';

  export let D;
  export let result;

  const dispatch = createEventDispatcher();
  $: r = result;

  // Custom depot growth chart (month-by-month)
  $: chartSvg = (() => {
    const lz=D.lz, w=800, h=280, pad=40, rate=D.rendite/100/12, rs=0.005/12, inf=D.inf/100;
    const etf=[], sparbuch=[], inputs=[], etfR=[];
    let accE=D.startK, accS=D.startK;
    for(let i=0;i<=lz*12;i++){
      etf.push(accE); etfR.push(accE/Math.pow(1+inf,i/12));
      sparbuch.push(accS); inputs.push(D.startK+D.spar*i);
      if(i<lz*12){ accE=accE*(1+rate)+D.spar; accS=accS*(1+rs)+D.spar; }
    }
    const maxY=Math.max(...etf)*1.05, pts=etf.length;
    const xs=i=>pad+(i/(pts-1))*(w-pad*2), ys=v=>h-pad-Math.max(0,Math.min(v/maxY,1))*(h-pad*2);
    const path=arr=>arr.map((v,i)=>`${i===0?'M':'L'}${xs(i).toFixed(1)},${ys(v).toFixed(1)}`).join(' ');
    return `<svg viewBox="0 0 ${w} ${h}" width="100%" height="${h}" style="display:block">
      <defs><linearGradient id="dg" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#60a5fa" stop-opacity=".3"/><stop offset="100%" stop-color="#60a5fa" stop-opacity="0"/></linearGradient></defs>
      ${[0,.25,.5,.75,1].map(f=>`<line x1="${pad}" x2="${w-pad}" y1="${ys(f*maxY).toFixed(1)}" y2="${ys(f*maxY).toFixed(1)}" stroke="#1f1f1f" stroke-width="1" ${f>0?'stroke-dasharray="2 3"':''}/>
        <text x="${pad-6}" y="${(ys(f*maxY)+3).toFixed(1)}" fill="#6b6b6b" font-size="10" font-family="'Geist Mono',ui-monospace" text-anchor="end">${de0.format(Math.round(f*maxY/1000))}k</text>`).join('')}
      ${[0,.25,.5,.75,1].map(f=>`<text x="${xs(Math.round(f*(pts-1))).toFixed(1)}" y="${h-pad+16}" fill="#6b6b6b" font-size="10" font-family="'Geist Mono',ui-monospace" text-anchor="middle">Jahr ${Math.round(f*lz)}</text>`).join('')}
      <path d="M${xs(0)},${h-pad} ${etf.map((v,i)=>`L${xs(i).toFixed(1)},${ys(v).toFixed(1)}`).join(' ')} L${xs(pts-1)},${h-pad} Z" fill="url(#dg)"/>
      <path d="${path(etf)}" stroke="#60a5fa" stroke-width="2" fill="none"/>
      <path d="${path(etfR)}" stroke="#4ade80" stroke-width="1.5" fill="none" stroke-dasharray="3 3"/>
      <path d="${path(sparbuch)}" stroke="#FF6B6B" stroke-width="2" fill="none"/>
      <path d="${path(inputs)}" stroke="#fbbf24" stroke-width="1.5" fill="none" stroke-dasharray="4 2"/>
    </svg>`;
  })();

  $: barSvg = barChart([
    {label:'ETF-Depot',val:r.fvG,color:'#60a5fa'},
    {label:'ETF real',val:r.fvR,color:'#4ade80'},
    {label:'Sparbuch',val:r.fvSparB,color:'#FF6B6B'},
    {label:'Eingezahlt',val:r.eingez,color:'#fbbf24'},
  ]);

  $: legendHtml = legend([['#60a5fa','ETF-AV-Depot (nominale Rendite)'],['#4ade80','ETF real (Kaufkraft heute)','3 3'],['#FF6B6B','Klassisches Sparbuch (0,5 % p.a.)'],['#fbbf24','Eingezahltes Kapital','4 2']]);
</script>

<nav class="nav">
  <div class="row g16">
    <button class="brand" on:click={() => dispatch('back')}><Logo /> Pensora</button>
    <span style="color:var(--line2);font-size:16px">/</span>
    <span style="color:var(--fg2);font-size:14px">Ergebnis · Depot</span>
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
    <div class="ey" style="margin-bottom:12px">AV-Depot-Analyse · {D.lz} J. Anspar + {D.entDauer} J. Entnahme · ETF vs. Sparbuch</div>
    <h1 style="font-size:48px;font-weight:600;letter-spacing:-.04em;margin-bottom:28px">
      ETF-Vorteil gegenüber Sparbuch: <span>{de0.format(Math.round(r.vorteilGgSparbuch))} €</span>
    </h1>

    <!-- KPI strip -->
    <div style="display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line);border-radius:var(--rlg);overflow:hidden;background:var(--bg1);margin-bottom:20px">
      {#each [['ETF-Depotgröße',de0.format(Math.round(r.fvG))+' €','nach '+D.lz+' Jahren'],['Sparbuch-Vergleich',de0.format(Math.round(r.fvSparB))+' €','0,5 % p.a. Negativszenario'],['4%-ETF-Entnahme',fmtE(r.e4)+'/Mo.','4%-Regel'],['Eingezahlt',de0.format(Math.round(r.eingez))+' €','Rendite: '+de0.format(Math.round(r.gewinn))+' €']] as [l,v,sub], i}
        <div style="padding:24px;border-right:{i<3?'1px solid var(--line)':'0'}">
          <div class="ey" style="margin-bottom:10px">{l}</div>
          <div class="stat" style="font-size:28px">{v}</div>
          <div style="font-size:11px;color:var(--fg3);font-family:var(--mono);margin-top:6px">{sub}</div>
        </div>
      {/each}
    </div>

    <div style="display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:16px">
      <div class="col g16">
        <div class="cardf" style="padding:28px">
          <div class="ey" style="margin-bottom:12px">ETF-Depot vs. Sparbuch · Wachstumskurve</div>
          {@html chartSvg}
          {@html legendHtml}
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px">
          {#each [['ETF-Depot',r.e4,r.fvG,'var(--fg)'],['Sparbuch (0,5 %)',r.e4Spar,r.fvSparB,'var(--loss)'],['Ziel',D.zielEur,r.kapZ,'var(--fg3)']] as [l,ent,dep,c]}
            <div class="cardf" style="padding:20px">
              <div class="ey" style="margin-bottom:8px">{l}</div>
              <div class="stat" style="font-size:28px;color:{c}">{fmtE(ent)}/Mo.</div>
              <div style="font-size:11px;color:var(--fg3);font-family:var(--mono);margin-top:6px">Depot: {de0.format(Math.round(dep))} €</div>
            </div>
          {/each}
        </div>
        <div class="cardf" style="padding:28px">
          <div class="ey" style="margin-bottom:12px">ETF vs. Sparbuch: direkter Vergleich nach {D.lz} Jahren</div>
          {@html barSvg}
        </div>
      </div>
      <aside style="position:sticky;top:88px">
        <div class="card" style="border-color:var(--fg);position:relative;overflow:hidden">
          <div style="position:absolute;top:0;left:0;right:0;height:3px;background:var(--fg)"></div>
          <h3 style="font-size:22px;font-weight:500;margin-bottom:10px">AV-Depot-Strategie besprechen.</h3>
          <p style="font-size:13px;color:var(--fg2);line-height:1.55">Welche ETFs, welcher Broker, welche steuerliche Optimierung.</p>
          <button class="btn btnp btnlg" style="width:100%;margin-top:16px" on:click={() => window.open('https://tidycal.com/niallbradfield/kostenfreies-beratungsgesprach', '_blank')}>Beratung buchen →</button>
          <button class="btn btng" style="width:100%;margin-top:8px" on:click={() => dispatch('recalc')}>← Neu berechnen</button>
          <div style="margin-top:20px;padding-top:16px;border-top:1px solid var(--line)">
            <div class="ey" style="margin-bottom:10px">Weitere Rechner</div>
            {#each [['ruerup','Rürup-Rechner'],['cashflow','Cashflow-Rechner']] as [k,l]}
              <button class="btn" style="width:100%;margin-bottom:8px;justify-content:flex-start" on:click={() => dispatch('navigate', k)}>{l} →</button>
            {/each}
          </div>
        </div>
      </aside>
    </div>
  </div>
</div>
