<script>
  import { createEventDispatcher } from 'svelte';
  import Logo from '../components/Logo.svelte';
  import { fmtE, de0 } from '../lib/utils.js';
  import { legend } from '../lib/charts.js';
  import { RMAX, RMAX26 } from '../lib/calcs.js';

  export let Ru;
  export let result;

  const dispatch = createEventDispatcher();
  $: r = result;

  $: chartSvg = (() => {
    const lz=Ru.lz, w=800, h=260, pad=40, rate=Ru.rendite/100/12, rs=0.005/12;
    const etf=[], sparbuch=[], netEtf=[];
    let accE=0, accS=0, netE=0;
    const steM_mo = r.steM;
    for(let i=0;i<=lz*12;i++){
      etf.push(accE); sparbuch.push(accS); netEtf.push(netE);
      if(i<lz*12){
        accE=accE*(1+rate)+Ru.mb;
        accS=accS*(1+rs)+Ru.mb;
        netE=netE*(1+rate)+(Ru.mb-steM_mo);
      }
    }
    const maxY=Math.max(...etf)*1.05, pts=etf.length;
    const xs=i=>pad+(i/(pts-1))*(w-pad*2), ys=v=>h-pad-Math.max(0,Math.min(v/maxY,1))*(h-pad*2);
    const path=arr=>arr.map((v,i)=>`${i===0?'M':'L'}${xs(i).toFixed(1)},${ys(v).toFixed(1)}`).join(' ');
    return `<svg viewBox="0 0 ${w} ${h}" width="100%" height="${h}" style="display:block">
      <defs><linearGradient id="rg" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#fafafa" stop-opacity=".25"/><stop offset="100%" stop-color="#fafafa" stop-opacity="0"/></linearGradient></defs>
      ${[0,.25,.5,.75,1].map(f=>`<line x1="${pad}" x2="${w-pad}" y1="${ys(f*maxY).toFixed(1)}" y2="${ys(f*maxY).toFixed(1)}" stroke="#1f1f1f" stroke-width="1" ${f>0?'stroke-dasharray="2 3"':''}/>
        <text x="${pad-6}" y="${(ys(f*maxY)+3).toFixed(1)}" fill="#6b6b6b" font-size="10" font-family="'Geist Mono',ui-monospace" text-anchor="end">${de0.format(Math.round(f*maxY/1000))}k</text>`).join('')}
      ${[0,.25,.5,.75,1].map(f=>`<text x="${xs(Math.round(f*(pts-1))).toFixed(1)}" y="${h-pad+16}" fill="#6b6b6b" font-size="10" font-family="'Geist Mono',ui-monospace" text-anchor="middle">Jahr ${Math.round(f*lz)}</text>`).join('')}
      <path d="M${xs(0)},${h-pad} ${etf.map((v,i)=>`L${xs(i).toFixed(1)},${ys(v).toFixed(1)}`).join(' ')} L${xs(pts-1)},${h-pad} Z" fill="url(#rg)"/>
      <path d="${path(etf)}" stroke="#fafafa" stroke-width="2" fill="none"/>
      <path d="${path(netEtf)}" stroke="#a3a3a3" stroke-width="1.5" fill="none" stroke-dasharray="3 3"/>
      <path d="${path(sparbuch)}" stroke="#FF6B6B" stroke-width="2" fill="none"/>
    </svg>`;
  })();

  $: legendHtml = legend([['#fafafa','Rürup-ETF (brutto)'],['#a3a3a3','Rürup-ETF (netto nach Steuervorteil)','3 3'],['#FF6B6B','Klassisches Sparbuch (0,5 % p.a.)']]);
</script>

<nav class="nav">
  <div class="row g16">
    <button class="brand" on:click={() => dispatch('back')}><Logo /> Pensora</button>
    <span style="color:var(--line2);font-size:16px">/</span>
    <span style="color:var(--fg2);font-size:14px">Ergebnis · Rürup</span>
  </div>
  <div class="row g8">
    <button class="btn btng" on:click={() => dispatch('back')}>← Hub</button>
    <button class="btn btng" on:click={() => dispatch('recalc')}>← Neu berechnen</button>
    <button class="btn btnp" on:click={() => window.open('https://tidycal.com/niallbradfield/kostenfreies-beratungsgesprach', '_blank')}>Beratung buchen →</button>
  </div>
</nav>

<div class="vscr">
  <div class="calc-result-pad">
    <div class="ey" style="margin-bottom:12px">Rürup-Analyse · {Ru.lz} J. · § 10 EStG · 2025</div>
    <h1 style="font-size:48px;font-weight:600;letter-spacing:-.04em;margin-bottom:28px">
      Monatlicher Steuervorteil: <span>{fmtE(r.steM)}</span>
    </h1>

    <div style="display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line);border-radius:var(--rlg);overflow:hidden;background:var(--bg1);margin-bottom:20px">
      {#each [['Steuerersparnis/Jahr',fmtE(r.steJ),'Grenzst. '+Ru.grenzSt+' %'],['Nettokosten/Monat',fmtE(r.nettoK),'statt '+fmtE(Ru.mb)+' brutto'],['Depot bei Rente',de0.format(Math.round(r.fv))+' €','nach '+Ru.lz+' Jahren'],['Monatsrente (netto)',fmtE(r.nettoR),'ab '+r.rentJ]] as [l,v,sub], i}
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
          <div class="ey" style="margin-bottom:12px">Rürup-ETF vs. Sparbuch · Aufbaukurve</div>
          {@html chartSvg}
          {@html legendHtml}
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
          <div class="cardf" style="padding:24px">
            <div class="ey" style="margin-bottom:12px">Steuerliche Förderung § 10 EStG</div>
            {#each [['Höchstbetrag 2025','29.344 €'],['Höchstbetrag 2026',de0.format(RMAX26)+' €'],['GRV-Abzug',Ru.selbst==='Ja'?'0 € (Selbst.)':'−'+fmtE(Ru.grvAN*2)],['Spielraum',fmtE(r.sp)],['Jahresbeitrag',fmtE(r.jB)],['Absetzbar (100%)',fmtE(r.absB)],['Steuer-Vorteil/J.',fmtE(r.steJ)],['Gesamt '+Ru.lz+' J.',fmtE(r.gesSte)]] as [l,v]}
              <div class="row" style="justify-content:space-between;padding:7px 0;border-bottom:1px solid var(--line);font-size:12px">
                <span style="color:var(--fg2)">{l}</span>
                <span style="font-family:var(--mono)">{v}</span>
              </div>
            {/each}
          </div>
          <div class="cardf" style="padding:24px">
            <div class="ey" style="margin-bottom:12px">Rentenphase</div>
            {#each [['Depot bei Rente',de0.format(Math.round(r.fv))+' €'],['Sparbuch-Vergl.',de0.format(Math.round(r.fvSparB))+' €'],['Brutto-Monatsrente',fmtE(r.mRente)],['Besteuerungsanteil',Math.round(r.bestAnt*100)+' % (§ 22)'],['Netto-Monatsrente',fmtE(r.nettoR)],['Bezugsdauer',r.jruh+' Jahre'],['Kumuliert netto',de0.format(Math.round(r.nettoR*12*r.jruh))+' €']] as [l,v]}
              <div class="row" style="justify-content:space-between;padding:7px 0;border-bottom:1px solid var(--line);font-size:12px">
                <span style="color:var(--fg2)">{l}</span>
                <span style="font-family:var(--mono)">{v}</span>
              </div>
            {/each}
          </div>
        </div>
      </div>
      <aside style="position:sticky;top:88px">
        <div class="card" style="border-color:var(--fg);position:relative;overflow:hidden">
          <div style="position:absolute;top:0;left:0;right:0;height:3px;background:var(--fg)"></div>
          <h3 style="font-size:22px;font-weight:500;margin-bottom:10px">Rürup-Strategie optimieren.</h3>
          <button class="btn btnp btnlg" style="width:100%;margin-top:16px" on:click={() => window.open('https://tidycal.com/niallbradfield/kostenfreies-beratungsgesprach', '_blank')}>Beratung buchen →</button>
          <button class="btn btng" style="width:100%;margin-top:8px" on:click={() => dispatch('recalc')}>← Neu berechnen</button>
        </div>
      </aside>
    </div>
  </div>
</div>
