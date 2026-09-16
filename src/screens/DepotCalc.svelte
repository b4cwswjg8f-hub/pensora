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
  <CalcNav title="ETF Savings Plan Calculator" on:back={() => dispatch('back')} />
  <CalcStepperBar labels={DS_LABELS} {step} />

  <div class="fbody">
    <div class="calc-layout">
      <div class="calc-form">
        <CalcStepHeader {s} />

        <div class="mt-7">
          {#if step === 0}
            <div class="grid grid-cols-2 gap-5 mb-4">
              <div class="flex flex-col gap-2">
                <label class="lbl">Monthly Savings Rate</label>
                <div class="sfx"><input type="number" step="25" bind:value={D.spar} /><span class="sfxt">€/mo.</span></div>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Starting Capital (optional)</label>
                <div class="sfx"><input type="number" step="1000" bind:value={D.startK} /><span class="sfxt">€</span></div>
              </div>
            </div>
            <div class="flex flex-col gap-2">
              <label class="lbl">Savings Duration</label>
              <input class="inp" type="number" min="1" max="50" bind:value={D.lz} />
            </div>

          {:else if step === 1}
            <div class="grid grid-cols-2 gap-5 mb-4">
              <div class="flex flex-col gap-2">
                <label class="lbl">Expected Return p.a. (ETF)</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={D.rendite} /><span class="sfxt">% p.a.</span></div>
                <span class="hint">MSCI World avg.: 7–9% nominal</span>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Annual Inflation</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={D.inf} /><span class="sfxt">% p.a.</span></div>
                <span class="hint">Current: ~2.1%</span>
              </div>
            </div>
            {#if result}
              <div class="card" style="background:var(--bg2)">
                <div class="ey mb-[10px]">ETF Savings Plan Projection</div>
                <div class="stat text-[48px]">{de0.format(Math.round(result.fvG))} €</div>
                <div class="text-xs text-fg3 font-mono mt-2">ETF portfolio after the savings phase</div>
              </div>
            {/if}

          {:else if step === 2}
            <div class="flex flex-col gap-2">
              <label class="lbl">Desired Withdrawal Duration</label>
              <input class="inp" type="number" min="5" max="40" bind:value={D.entDauer} />
            </div>
            <div class="card mt-5">
              <div class="ey mb-[10px]">The 4% Rule (William Bengen, 1994)</div>
              <p class="text-[14px] text-fg2 leading-[1.6]">Withdraw 4% of your portfolio value annually — the portfolio should last 30+ years. Empirically tested against US stock market data from 1926–1994.</p>
            </div>

          {:else if step === 3}
            <div class="flex flex-col gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Desired Monthly Withdrawal from Your ETF Portfolio</label>
                <div class="sfx text-xl">
                  <input type="number" step="50" bind:value={D.zielEur} class="text-xl font-medium" />
                  <span class="sfxt text-[15px]">€ / month</span>
                </div>
              </div>
              {#if result}
                <div class="card" style="border-color:rgba(255,107,107,.25)">
                  <div class="ey mb-[10px]" style="color:var(--loss)">Preview</div>
                  <div class="stat text-[48px]" style="color:{result.e4 >= D.zielEur ? 'var(--fg)' : 'var(--loss)'}">
                    {fmtE(result.e4)}/mo.
                  </div>
                  <div class="text-xs text-fg3 font-mono mt-2">
                    ETF portfolio: {de0.format(Math.round(result.fvG))} € · Savings account: {de0.format(Math.round(result.fvSparB))} €
                  </div>
                  <div class="text-xs mt-[6px]" style="color:{result.luecke > 0 ? 'var(--loss)' : 'var(--fg)'}">
                    {result.luecke > 0 ? 'Savings rate needed for goal: ' + fmtE(result.sparZ) + '/mo.' : '✓ Goal achievable'}
                  </div>
                </div>
              {/if}
            </div>
          {/if}
        </div>

        <CalcNavButtons
          {step} labels={DS_LABELS} calcLabel="Calculate Result →"
          on:back={back} on:next={next}
        />
      </div>

      <!-- Sidebar -->
      <aside class="calc-sidebar">
        <div class="ey mb-[14px]">Portfolio Preview</div>
        <div class="stat text-[40px]">{result ? de0.format(Math.round(result.fvG / 1000)) + 'k €' : '–'}</div>
        <div class="text-fg3 text-[11px] font-mono mt-[6px] uppercase tracking-[.08em]">Portfolio Size</div>
        {#if result}
          <div class="mt-4 pt-4 text-[13px]" style="border-top:1px solid var(--line)">
            <div class="flex items-center justify-between py-2 text-[13px]">
              <span class="text-fg3">4% Withdrawal</span>
              <span class="font-mono">{fmtE(result.e4)}/mo.</span>
            </div>
          </div>
        {/if}
      </aside>
    </div>
  </div>
</div>
{/if}
