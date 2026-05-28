<script>
  import { createEventDispatcher } from 'svelte';
  import Logo from '../components/Logo.svelte';
  import Stepper from '../components/Stepper.svelte';
  import DepotResult from './DepotResult.svelte';
  import { defaultD, calcD, DS_LABELS } from '../lib/calcs.js';
  import { fmtE, de0 } from '../lib/utils.js';

  const dispatch = createEventDispatcher();
  let D = defaultD();
  let step = 0;
  let showResult = false;

  $: result = (() => { try { return calcD(D); } catch(e) { return null; } })();
  $: s = DS_LABELS[step];
  $: pct = Math.round(step / DS_LABELS.length * 100);

  function next() {
    if (step < DS_LABELS.length - 1) { step++; window.scrollTo(0,0); }
    else { showResult = true; window.scrollTo(0,0); }
  }
  function back() { if (step > 0) { step--; window.scrollTo(0,0); } }
</script>

{#if showResult}
  <DepotResult {D} {result}
    on:back={() => { showResult = false; step = 0; D = defaultD(); dispatch('back'); }}
    on:recalc={() => { showResult = false; step = 0; }}
    on:navigate={e => dispatch('navigate', e.detail)}
  />
{:else}
<div>
  <nav class="nav">
    <div class="row g16">
      <button class="brand" on:click={() => dispatch('back')}><Logo /> Pensora</button>
      <span style="color:var(--line2);font-size:16px">/</span>
      <span style="color:var(--fg2);font-size:14px">AV-Depot-Rechner</span>
    </div>
    <div class="row g8"><button class="btn btng" on:click={() => dispatch('back')}>← Hub</button></div>
  </nav>

  <div class="calc-stepper">
    <div class="row" style="justify-content:space-between;margin-bottom:10px">
      <div class="row g12">
        <span style="font-family:var(--mono);font-size:12px;color:var(--fg3);letter-spacing:.08em;text-transform:uppercase">Schritt {String(step+1).padStart(2,'0')} · {String(DS_LABELS.length).padStart(2,'0')}</span>
        <span style="font-size:15px;font-weight:500">{s.label}</span>
      </div>
      <span style="font-family:var(--mono);font-size:13px">{pct} %</span>
    </div>
    <Stepper total={DS_LABELS.length} current={step} />
  </div>

  <div class="fbody">
    <div class="calc-layout">
      <div class="calc-form">
        <div class="ey">{s.ey}</div>
        <h2 style="font-size:36px;font-weight:500;letter-spacing:-.03em;max-width:700px;margin-top:12px;line-height:1.1">{s.title}</h2>
        <p style="font-size:15px;color:var(--fg2);margin-top:12px;max-width:600px">{s.desc}</p>
        <div style="margin-top:28px">

          {#if step === 0}
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:16px">
              <div class="col g8">
                <label class="lbl">Monatliche Sparrate</label>
                <div class="sfx"><input type="number" step="25" bind:value={D.spar} /><span class="sfxt">€/Mo.</span></div>
              </div>
              <div class="col g8">
                <label class="lbl">Startkapital (optional)</label>
                <div class="sfx"><input type="number" step="1000" bind:value={D.startK} /><span class="sfxt">€</span></div>
              </div>
            </div>
            <div class="col g8">
              <label class="lbl">Anspardauer</label>
              <input class="inp" type="number" min="1" max="50" bind:value={D.lz} />
            </div>

          {:else if step === 1}
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:16px">
              <div class="col g8">
                <label class="lbl">Erwartete Rendite p.a. (ETF)</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={D.rendite} /><span class="sfxt">% p.a.</span></div>
                <span class="hint">MSCI World Ø: 7–9 % nominal</span>
              </div>
              <div class="col g8">
                <label class="lbl">Inflation p.a.</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={D.inf} /><span class="sfxt">% p.a.</span></div>
                <span class="hint">Aktuell: ~2,1 %</span>
              </div>
            </div>
            {#if result}
              <div class="card" style="background:var(--bg2)">
                <div class="ey" style="margin-bottom:10px">AV-Depot-Hochrechnung</div>
                <div class="stat" style="font-size:48px">{de0.format(Math.round(result.fvG))} €</div>
                <div style="font-size:12px;color:var(--fg3);font-family:var(--mono);margin-top:8px">ETF-Depot nach Ansparphase</div>
              </div>
            {/if}

          {:else if step === 2}
            <div class="col g8">
              <label class="lbl">Gewünschte Entnahmedauer</label>
              <input class="inp" type="number" min="5" max="40" bind:value={D.entDauer} />
            </div>
            <div class="card mt20">
              <div class="ey" style="margin-bottom:10px">4-%-Regel (William Bengen, 1994)</div>
              <p style="font-size:14px;color:var(--fg2);line-height:1.6">Jährlich 4 % des Depotwertes entnehmen — das Depot sollte dabei 30+ Jahre halten. Empirisch getestet an US-Aktienmarktdaten 1926–1994.</p>
            </div>

          {:else if step === 3}
            <div class="col g20">
              <div class="col g8">
                <label class="lbl">Monatliche Wunsch-Entnahme aus dem AV-Depot</label>
                <div class="sfx" style="font-size:20px">
                  <input type="number" step="50" bind:value={D.zielEur} style="font-size:20px;font-weight:500" />
                  <span class="sfxt" style="font-size:15px">€ / Monat</span>
                </div>
              </div>
              {#if result}
                <div class="card" style="border-color:rgba(255,107,107,.25)">
                  <div class="ey" style="color:var(--loss);margin-bottom:10px">Vorschau</div>
                  <div class="stat" style="font-size:48px;color:{result.e4 >= D.zielEur ? 'var(--fg)' : 'var(--loss)'}">{fmtE(result.e4)}/Mo.</div>
                  <div style="font-size:12px;color:var(--fg3);font-family:var(--mono);margin-top:8px">
                    ETF-Depot: {de0.format(Math.round(result.fvG))} € · Sparbuch: {de0.format(Math.round(result.fvSparB))} €
                  </div>
                  <div style="font-size:12px;margin-top:6px;color:{result.luecke > 0 ? 'var(--loss)' : 'var(--fg)'}">
                    {result.luecke > 0 ? 'Sparrate für Ziel: ' + fmtE(result.sparZ) + '/Mo.' : '✓ Ziel erreichbar'}
                  </div>
                </div>
              {/if}
            </div>
          {/if}
        </div>

        <div class="row" style="justify-content:space-between;margin-top:36px;padding-top:20px;border-top:1px solid var(--line)">
          <button class="btn btnlg" on:click={back} style="opacity:{step===0?0.3:1};pointer-events:{step===0?'none':'auto'}">← Zurück</button>
          <div class="row g12">
            <button class="btn btng" on:click={next}>Überspringen</button>
            <button class="btn btnp btnlg" on:click={next}>
              {step === DS_LABELS.length - 1 ? 'Ergebnis berechnen →' : 'Weiter →'}
            </button>
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <aside style="border-left:1px solid var(--line);padding:36px 28px;background:var(--bg1)">
        <div class="ey" style="margin-bottom:14px">Depot-Vorschau</div>
        <div class="stat" style="font-size:40px">{result ? de0.format(Math.round(result.fvG/1000)) + 'k €' : '–'}</div>
        <div style="color:var(--fg3);font-size:11px;font-family:var(--mono);margin-top:6px;text-transform:uppercase;letter-spacing:.08em">Depotgröße</div>
        {#if result}
          <div style="margin-top:16px;padding-top:16px;border-top:1px solid var(--line);font-size:13px">
            <div class="row" style="justify-content:space-between;padding:8px 0">
              <span style="color:var(--fg3)">4%-Entnahme</span>
              <span style="font-family:var(--mono)">{fmtE(result.e4)}/Mo.</span>
            </div>
          </div>
        {/if}
      </aside>
    </div>
  </div>
</div>
{/if}
