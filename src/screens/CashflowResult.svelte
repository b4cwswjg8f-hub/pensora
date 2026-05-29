<script>
  import { createEventDispatcher } from 'svelte';
  import Logo from '../components/Logo.svelte';
  import PdfGate from '../components/PdfGate.svelte';
  import { fmtE, de0 } from '../lib/utils.js';

  export let C;
  export let result;

  const dispatch = createEventDispatcher();
  let showPdfGate = false;
  $: r = result;

  // Donut/bar-style cashflow breakdown chart
  $: chartSvg = (() => {
    const w = 800, h = 220, pad = 40;
    const cats = [
      { label: 'Fixkosten', ist: r.fix, emp: r.emp_fix, color: '#fafafa' },
      { label: 'Versicherungen', ist: r.vers, emp: r.emp_vers, color: '#a3a3a3' },
      { label: 'Vorsorge/Sparen', ist: r.av, emp: r.emp_av, color: '#6fcf97' },
      { label: 'Freizeit', ist: r.leb, emp: r.emp_frei, color: '#f2994a' },
      { label: 'Frei verfügbar', ist: r.frei, emp: r.emp_vm, color: '#4a90d9' },
    ];
    const maxV = Math.max(...cats.flatMap(c => [c.ist, c.emp]), 1) * 1.15;
    const bw = 28, gap = (w - pad * 2 - cats.length * bw * 2) / (cats.length - 1);
    const ys = v => h - pad - Math.max(0, Math.min(v / maxV, 1)) * (h - pad * 2);
    const yh = v => Math.max(0, Math.min(v / maxV, 1)) * (h - pad * 2);
    let svg = `<svg viewBox="0 0 ${w} ${h}" width="100%" height="${h}" style="display:block">`;
    // Grid lines
    [0, 0.25, 0.5, 0.75, 1].forEach(f => {
      const y = ys(f * maxV);
      svg += `<line x1="${pad}" x2="${w - pad}" y1="${y.toFixed(1)}" y2="${y.toFixed(1)}" stroke="#1f1f1f" stroke-width="1" ${f > 0 ? 'stroke-dasharray="2 3"' : ''}/>`;
      svg += `<text x="${pad - 6}" y="${(y + 3).toFixed(1)}" fill="#6b6b6b" font-size="9" font-family="'Geist Mono',ui-monospace" text-anchor="end">${de0.format(Math.round(f * maxV))}€</text>`;
    });
    cats.forEach((c, i) => {
      const x = pad + i * (bw * 2 + gap);
      const istH = yh(c.ist), empH = yh(c.emp);
      svg += `<rect x="${x}" y="${ys(c.ist).toFixed(1)}" width="${bw}" height="${istH.toFixed(1)}" fill="${c.color}" opacity=".9" rx="2"/>`;
      svg += `<rect x="${x + bw + 2}" y="${ys(c.emp).toFixed(1)}" width="${bw - 2}" height="${empH.toFixed(1)}" fill="${c.color}" opacity=".35" rx="2" stroke="${c.color}" stroke-width="1" stroke-dasharray="2 2"/>`;
      svg += `<text x="${(x + bw).toFixed(1)}" y="${(h - pad + 16).toFixed(1)}" fill="#6b6b6b" font-size="9" font-family="'Geist Mono',ui-monospace" text-anchor="middle">${c.label}</text>`;
    });
    svg += `</svg>`;
    return svg;
  })();

  $: legendHtml = `<div style="display:flex;gap:20px;flex-wrap:wrap;margin-top:12px;font-size:11px;font-family:var(--mono);color:var(--fg3)">
    <span style="display:flex;align-items:center;gap:6px"><span style="width:12px;height:12px;background:var(--fg);border-radius:2px;display:inline-block"></span>Ist-Wert</span>
    <span style="display:flex;align-items:center;gap:6px"><span style="width:12px;height:12px;background:var(--fg);opacity:.3;border-radius:2px;display:inline-block;border:1px dashed var(--fg)"></span>Empfehlung (50/10/15/15-Regel)</span>
  </div>`;
</script>

<nav class="nav">
  <div class="row g16">
    <button class="brand" on:click={() => dispatch('back')}><Logo /> Pensora</button>
    <span style="color:var(--line2);font-size:16px">/</span>
    <span style="color:var(--fg2);font-size:14px">Ergebnis · Cashflow</span>
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
    <div class="ey" style="margin-bottom:12px">Cashflow-Analyse · Monatliches Budget · Ist vs. Empfehlung</div>
    <h1 style="font-size:48px;font-weight:600;letter-spacing:-.04em;margin-bottom:28px">
      Frei verfügbar: <span style="color:{r.frei > 0 ? 'var(--fg)' : 'var(--loss)'}">{fmtE(r.frei)}/Mo.</span>
    </h1>

    <!-- KPI strip -->
    <div style="display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line);border-radius:var(--rlg);overflow:hidden;background:var(--bg1);margin-bottom:20px">
      {#each [['Fixkosten',fmtE(r.fix),'Empfehlung: '+fmtE(r.emp_fix)],['Vorsorge/Sparen',fmtE(r.av),'Empfehlung: '+fmtE(r.emp_av)],['Freizeit',fmtE(r.leb),'Empfehlung: '+fmtE(r.emp_frei)],['Notgroschen',fmtE(r.notg),'3 Nettogehälter']] as [l,v,sub], i}
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
          <div class="ey" style="margin-bottom:12px">Ist-Ausgaben vs. Empfehlung · Monatlich</div>
          {@html chartSvg}
          {@html legendHtml}
        </div>

        <!-- Detail comparison -->
        <div class="cardf" style="padding:28px">
          <div class="ey" style="margin-bottom:16px">Detailvergleich · Ist vs. Empfehlung</div>
          <div style="display:grid;grid-template-columns:1fr auto auto;gap:0;border-top:1px solid var(--line)">
            <div style="padding:8px 0;font-size:10px;color:var(--fg3);font-family:var(--mono);text-transform:uppercase;letter-spacing:.08em">Kategorie</div>
            <div style="padding:8px 12px;font-size:10px;color:var(--fg3);font-family:var(--mono);text-transform:uppercase;letter-spacing:.08em;text-align:right">Ist</div>
            <div style="padding:8px 0;font-size:10px;color:var(--fg3);font-family:var(--mono);text-transform:uppercase;letter-spacing:.08em;text-align:right">Empfehlung</div>
            {#each [
              ['Warmmiete',C.miete,''],['Nebenkosten',C.nk,''],['Lebensmittel',C.lm,''],['Transport',C.transport,''],['Kommunikation',C.komm,''],
              ['— Fixkosten gesamt',r.fix,r.emp_fix,true],
              ['Versicherungen',C.versich,r.emp_vers],
              ['Altersvorsorge / Sparen',C.av,r.emp_av],
              ['Freizeit & Sonstiges',r.leb,r.emp_frei],
              ['— Ausgaben gesamt',r.out,C.netto * 0.85,true],
              ['Frei verfügbar',r.frei,r.emp_vm,true],
            ] as [l,ist,emp,bold]}
              <div style="padding:8px 0;border-top:1px solid var(--line);font-size:{bold?'13':'12'}px;font-weight:{bold?600:400};color:{bold?'var(--fg)':'var(--fg2)'}">{l}</div>
              <div style="padding:8px 12px;border-top:1px solid var(--line);font-family:var(--mono);font-size:13px;text-align:right;color:{typeof emp==='number'&&ist>emp*1.1?'var(--loss)':'var(--fg)'}">{fmtE(ist)}</div>
              <div style="padding:8px 0;border-top:1px solid var(--line);font-family:var(--mono);font-size:12px;text-align:right;color:var(--fg3)">{typeof emp==='number'?fmtE(emp):'–'}</div>
            {/each}
          </div>
        </div>

        <!-- Notgroschen card -->
        <div class="card" style="padding:28px">
          <div class="ey" style="margin-bottom:12px">Notgroschen-Empfehlung</div>
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;border-top:1px solid var(--line);padding-top:16px">
            {#each [[3,r.notg,'Minimum'],[6,r.notg*2,'Standard'],[12,r.notg*4,'Komfort']] as [mo,val,l]}
              <div>
                <div style="font-size:10px;color:var(--fg3);font-family:var(--mono);text-transform:uppercase;letter-spacing:.08em">{l} ({mo} Mo.)</div>
                <div style="font-size:22px;font-weight:500;font-family:var(--mono);margin-top:6px">{de0.format(Math.round(val))} €</div>
              </div>
            {/each}
          </div>
          <p style="font-size:13px;color:var(--fg2);margin-top:16px;line-height:1.6">
            Ein Notgroschen von 3–6 Nettogehältern schützt vor unerwarteten Ausgaben (Autoreparatur, Zahnarzt, Jobverlust) ohne in Schulden zu geraten.
          </p>
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
          <h3 style="font-size:22px;font-weight:500;margin-bottom:10px">Cashflow optimieren.</h3>
          <p style="font-size:13px;color:var(--fg2);line-height:1.55">Budget strukturieren, Sparpotenziale aufdecken, Vorsorge aufbauen. 30 Min. kostenlos.</p>
          <button class="btn btnp btnlg" style="width:100%;margin-top:16px" on:click={() => window.open('https://tidycal.com/niallbradfield/kostenfreies-beratungsgesprach', '_blank')}>Kostenloses Gespräch buchen →</button>
          <button class="btn btng" style="width:100%;margin-top:8px" on:click={() => dispatch('recalc')}>← Neu berechnen</button>
          <div style="margin-top:20px;padding-top:16px;border-top:1px solid var(--line)">
            <div class="ey" style="margin-bottom:10px">Passende Rechner</div>
            {#each [['depot','AV-Depot-Rechner'],['ruerup','Rürup-Rechner'],['versicherung','Versicherungs-Check']] as [k,l]}
              <button class="btn" style="width:100%;margin-bottom:8px;justify-content:flex-start" on:click={() => dispatch('navigate', k)}>{l} →</button>
            {/each}
          </div>
        </div>
      </aside>
    </div>
  </div>
</div>
