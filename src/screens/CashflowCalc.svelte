<script>
  import { createEventDispatcher } from 'svelte';
  import CalcNav from '../components/CalcNav.svelte';
  import CalcStepperBar from '../components/CalcStepperBar.svelte';
  import CalcStepHeader from '../components/CalcStepHeader.svelte';
  import CalcNavButtons from '../components/CalcNavButtons.svelte';
  import CashflowResult from './CashflowResult.svelte';
  import { defaultC, calcC, CS_LABELS } from '../lib/calcs.js';
  import { fmtE, de0 } from '../lib/utils.js';

  const dispatch = createEventDispatcher();
  let C = defaultC();
  let step = 0;
  let showResult = false;

  $: result = (() => { try { return calcC(C); } catch(e) { return null; } })();
  $: s = CS_LABELS[step];

  function next() {
    if (step < CS_LABELS.length - 1) { step++; window.scrollTo(0, 0); }
    else { showResult = true; window.scrollTo(0, 0); }
  }
  function back() { if (step > 0) { step--; window.scrollTo(0, 0); } }
</script>

{#if showResult}
  <CashflowResult {C} {result}
    on:back={() => { showResult = false; step = 0; C = defaultC(); dispatch('back'); }}
    on:recalc={() => { showResult = false; step = 0; }}
    on:navigate={e => dispatch('navigate', e.detail)}
  />
{:else}
<div>
  <CalcNav title="Cashflow-Rechner" on:back={() => dispatch('back')} />
  <CalcStepperBar labels={CS_LABELS} {step} />

  <div class="fbody">
    <div class="calc-layout">
      <div class="calc-form">
        <CalcStepHeader {s} />

        <div class="mt-7">
          {#if step === 0}
            <div class="flex flex-col gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Monatliches Nettoeinkommen</label>
                <div class="sfx text-xl">
                  <input type="number" step="50" bind:value={C.netto} class="text-xl font-medium" />
                  <span class="sfxt text-[15px]">€ / Monat</span>
                </div>
              </div>
              {#if result}
                <div class="card" style="background:var(--bg2)">
                  <div class="ey mb-[10px]">50/15/15-Faustregel (Richtwerte)</div>
                  <div class="grid gap-3 mt-2" style="grid-template-columns:repeat(3,1fr)">
                    {#each [['Fixkosten (50 %)',result.emp_fix],['Vorsorge (15 %)',result.emp_av],['Freizeit (15 %)',result.emp_frei]] as [l, v]}
                      <div>
                        <div class="text-[10px] text-fg3 font-mono uppercase tracking-[.06em]">{l}</div>
                        <div class="text-xl font-medium font-mono mt-1">{fmtE(v)}</div>
                      </div>
                    {/each}
                  </div>
                </div>
              {/if}
            </div>

          {:else if step === 1}
            <div class="grid grid-cols-2 gap-4">
              <div>
                <div class="text-[11px] text-fg3 font-mono uppercase tracking-[.08em] mb-3">Fixkosten</div>
                <div class="flex flex-col gap-3">
                  {#each [
                    ['Warmmiete / Grundmiete','miete','€/Mo.',50],
                    ['Nebenkosten / Strom / Gas','nk','€/Mo.',10],
                    ['Lebensmittel','lm','€/Mo.',25],
                    ['Transport (ÖPNV / Tanken)','transport','€/Mo.',10],
                    ['Kommunikation (Handy, Internet)','komm','€/Mo.',5],
                  ] as [l, k, sfx, stp]}
                    <div class="flex flex-col gap-2">
                      <label class="lbl text-[11px]">{l}</label>
                      <div class="sfx"><input type="number" step={stp} bind:value={C[k]} /><span class="sfxt">{sfx}</span></div>
                    </div>
                  {/each}
                </div>
              </div>
              <div>
                <div class="text-[11px] text-fg3 font-mono uppercase tracking-[.08em] mb-3">Variable Kosten</div>
                <div class="flex flex-col gap-3">
                  {#each [
                    ['Versicherungen gesamt','versich','€/Mo.',10],
                    ['Altersvorsorge (Sparen/ETF)','av','€/Mo.',25],
                    ['Freizeit & Hobbys','frei','€/Mo.',25],
                    ['Sonstiges','sonst','€/Mo.',10],
                  ] as [l, k, sfx, stp]}
                    <div class="flex flex-col gap-2">
                      <label class="lbl text-[11px]">{l}</label>
                      <div class="sfx"><input type="number" step={stp} bind:value={C[k]} /><span class="sfxt">{sfx}</span></div>
                    </div>
                  {/each}
                </div>
                {#if result}
                  <div class="card mt-5" style="background:var(--bg2)">
                    <div class="ey mb-[6px]">Frei verfügbar</div>
                    <div class="stat text-[32px]" style="color:{result.frei > 0 ? 'var(--fg)' : 'var(--loss)'}">
                      {fmtE(result.frei)}/Mo.
                    </div>
                    <div class="text-[11px] text-fg3 font-mono mt-[6px]">
                      Ausgaben: {fmtE(result.out)} von {fmtE(C.netto)}
                    </div>
                  </div>
                {/if}
              </div>
            </div>
          {/if}
        </div>

        <CalcNavButtons
          {step} labels={CS_LABELS} calcLabel="Cashflow analysieren →"
          on:back={back} on:next={next}
        />
      </div>

      <!-- Sidebar -->
      <aside class="calc-sidebar">
        <div class="ey mb-[14px]">Frei verfügbar</div>
        <div class="stat text-[40px]" style="color:{result && result.frei > 0 ? 'var(--fg)' : 'var(--loss)'}">
          {result ? fmtE(result.frei) + '/Mo.' : '–'}
        </div>
        <div class="text-fg3 text-[11px] font-mono mt-[6px] uppercase tracking-[.08em]">nach allen Ausgaben</div>
        {#if result}
          <div class="mt-4 pt-4 text-[13px]" style="border-top:1px solid var(--line)">
            <div class="calc-sidebar-row">
              <span class="text-fg3">Notgroschen (3 Mo.)</span>
              <span class="font-mono">{fmtE(result.notg)}</span>
            </div>
            <div class="flex items-center justify-between py-2 text-[13px]">
              <span class="text-fg3">Ausgaben gesamt</span>
              <span class="font-mono">{fmtE(result.out)}</span>
            </div>
          </div>
        {/if}
      </aside>
    </div>
  </div>
</div>
{/if}
