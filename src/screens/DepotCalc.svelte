<script>
  import { createEventDispatcher } from 'svelte';
  import CalcNav from '../components/CalcNav.svelte';
  import CalcStepperBar from '../components/CalcStepperBar.svelte';
  import CalcStepHeader from '../components/CalcStepHeader.svelte';
  import CalcNavButtons from '../components/CalcNavButtons.svelte';
  import DepotResult from './DepotResult.svelte';
  import { defaultD, calcD, DS_LABELS } from '../lib/calcs.js';
  import { fmtE, de0 } from '../lib/utils.js';

  const dispatch = createEventDispatcher();
  let D = defaultD();
  let step = 0;
  let showResult = false;

  $: result = (() => { try { return calcD(D); } catch(e) { return null; } })();
  $: s = DS_LABELS[step];

  function next() {
    if (step < DS_LABELS.length - 1) { step++; window.scrollTo(0, 0); }
    else { showResult = true; window.scrollTo(0, 0); }
  }
  function back() { if (step > 0) { step--; window.scrollTo(0, 0); } }
</script>

{#if showResult}
  <DepotResult {D} {result}
    on:back={() => { showResult = false; step = 0; D = defaultD(); dispatch('back'); }}
    on:recalc={() => { showResult = false; step = 0; }}
    on:navigate={e => dispatch('navigate', e.detail)}
  />
{:else}
<div>
  <CalcNav title="AV-Depot-Rechner" on:back={() => dispatch('back')} />
  <CalcStepperBar labels={DS_LABELS} {step} />

  <div class="fbody">
    <div class="calc-layout">
      <div class="calc-form">
        <CalcStepHeader {s} />

        <div class="mt-7">
          {#if step === 0}
            <div class="grid grid-cols-2 gap-5 mb-4">
              <div class="flex flex-col gap-2">
                <label class="lbl">Monatliche Sparrate</label>
                <div class="sfx"><input type="number" step="25" bind:value={D.spar} /><span class="sfxt">€/Mo.</span></div>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Startkapital (optional)</label>
                <div class="sfx"><input type="number" step="1000" bind:value={D.startK} /><span class="sfxt">€</span></div>
              </div>
            </div>
            <div class="flex flex-col gap-2">
              <label class="lbl">Anspardauer</label>
              <input class="inp" type="number" min="1" max="50" bind:value={D.lz} />
            </div>

          {:else if step === 1}
            <div class="grid grid-cols-2 gap-5 mb-4">
              <div class="flex flex-col gap-2">
                <label class="lbl">Erwartete Rendite p.a. (ETF)</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={D.rendite} /><span class="sfxt">% p.a.</span></div>
                <span class="hint">MSCI World Ø: 7–9 % nominal</span>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Inflation p.a.</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={D.inf} /><span class="sfxt">% p.a.</span></div>
                <span class="hint">Aktuell: ~2,1 %</span>
              </div>
            </div>
            {#if result}
              <div class="card" style="background:var(--bg2)">
                <div class="ey mb-[10px]">AV-Depot-Hochrechnung</div>
                <div class="stat text-[48px]">{de0.format(Math.round(result.fvG))} €</div>
                <div class="text-xs text-fg3 font-mono mt-2">ETF-Depot nach Ansparphase</div>
              </div>
            {/if}

          {:else if step === 2}
            <div class="flex flex-col gap-2">
              <label class="lbl">Gewünschte Entnahmedauer</label>
              <input class="inp" type="number" min="5" max="40" bind:value={D.entDauer} />
            </div>
            <div class="card mt-5">
              <div class="ey mb-[10px]">4-%-Regel (William Bengen, 1994)</div>
              <p class="text-[14px] text-fg2 leading-[1.6]">Jährlich 4 % des Depotwertes entnehmen — das Depot sollte dabei 30+ Jahre halten. Empirisch getestet an US-Aktienmarktdaten 1926–1994.</p>
            </div>

          {:else if step === 3}
            <div class="flex flex-col gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Monatliche Wunsch-Entnahme aus dem AV-Depot</label>
                <div class="sfx text-xl">
                  <input type="number" step="50" bind:value={D.zielEur} class="text-xl font-medium" />
                  <span class="sfxt text-[15px]">€ / Monat</span>
                </div>
              </div>
              {#if result}
                <div class="card" style="border-color:rgba(255,107,107,.25)">
                  <div class="ey mb-[10px]" style="color:var(--loss)">Vorschau</div>
                  <div class="stat text-[48px]" style="color:{result.e4 >= D.zielEur ? 'var(--fg)' : 'var(--loss)'}">
                    {fmtE(result.e4)}/Mo.
                  </div>
                  <div class="text-xs text-fg3 font-mono mt-2">
                    ETF-Depot: {de0.format(Math.round(result.fvG))} € · Sparbuch: {de0.format(Math.round(result.fvSparB))} €
                  </div>
                  <div class="text-xs mt-[6px]" style="color:{result.luecke > 0 ? 'var(--loss)' : 'var(--fg)'}">
                    {result.luecke > 0 ? 'Sparrate für Ziel: ' + fmtE(result.sparZ) + '/Mo.' : '✓ Ziel erreichbar'}
                  </div>
                </div>
              {/if}
            </div>
          {/if}
        </div>

        <CalcNavButtons
          {step} labels={DS_LABELS} calcLabel="Ergebnis berechnen →"
          on:back={back} on:next={next}
        />
      </div>

      <!-- Sidebar -->
      <aside class="calc-sidebar">
        <div class="ey mb-[14px]">Depot-Vorschau</div>
        <div class="stat text-[40px]">{result ? de0.format(Math.round(result.fvG / 1000)) + 'k €' : '–'}</div>
        <div class="text-fg3 text-[11px] font-mono mt-[6px] uppercase tracking-[.08em]">Depotgröße</div>
        {#if result}
          <div class="mt-4 pt-4 text-[13px]" style="border-top:1px solid var(--line)">
            <div class="flex items-center justify-between py-2 text-[13px]">
              <span class="text-fg3">4%-Entnahme</span>
              <span class="font-mono">{fmtE(result.e4)}/Mo.</span>
            </div>
          </div>
        {/if}
      </aside>
    </div>
  </div>
</div>
{/if}
