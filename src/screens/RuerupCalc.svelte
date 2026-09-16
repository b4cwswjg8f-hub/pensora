<script>
  import { createEventDispatcher } from 'svelte';
  import CalcNav from '../components/CalcNav.svelte';
  import CalcStepperBar from '../components/CalcStepperBar.svelte';
  import CalcStepHeader from '../components/CalcStepHeader.svelte';
  import CalcNavButtons from '../components/CalcNavButtons.svelte';
  import RuerupResult from './RuerupResult.svelte';
  import { defaultRu, calcRu, RUS_LABELS } from '../lib/calcs.js';
  import { fmtE, de0 } from '../lib/utils.js';

  const dispatch = createEventDispatcher();
  let Ru = defaultRu();
  let step = 0;
  let showResult = false;

  $: result = (() => { try { return calcRu(Ru); } catch(e) { return null; } })();
  $: s = RUS_LABELS[step];

  function next() {
    if (step < RUS_LABELS.length - 1) { step++; window.scrollTo(0, 0); }
    else { showResult = true; window.scrollTo(0, 0); }
  }
  function back() { if (step > 0) { step--; window.scrollTo(0, 0); } }
</script>

{#if showResult}
  <RuerupResult {Ru} {result}
    on:back={() => { showResult = false; step = 0; Ru = defaultRu(); dispatch('back'); }}
    on:recalc={() => { showResult = false; step = 0; }}
    on:navigate={e => dispatch('navigate', e.detail)}
  />
{:else}
<div>
  <CalcNav title="Rürup Pension Calculator" on:back={() => dispatch('back')} />
  <CalcStepperBar labels={RUS_LABELS} {step} />

  <div class="fbody">
    <div class="calc-layout">
      <div class="calc-form">
        <CalcStepHeader {s} />

        <div class="mt-7">
          {#if step === 0}
            <div class="flex flex-col gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Self-Employed?</label>
                <div class="seg segf">
                  {#each ['Ja','Nein'] as opt}
                    <button class:on={Ru.selbst === opt} on:click={() => Ru.selbst = opt}>{opt === 'Ja' ? 'Yes' : 'No'}</button>
                  {/each}
                </div>
                <span class="hint">Self-employed: full Rürup contribution room</span>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Gross Annual Salary</label>
                <div class="sfx"><input type="number" step="1000" bind:value={Ru.brutto} /><span class="sfxt">€/year</span></div>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Marginal Tax Rate</label>
                <div class="sfx"><input type="number" step="1" bind:value={Ru.grenzSt} /><span class="sfxt">%</span></div>
                <span class="hint">~30% at €60k · ~42% from €68k</span>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Subject to Church Tax?</label>
                <div class="seg segf">
                  {#each ['Ja','Nein'] as opt}
                    <button class:on={Ru.kirche === opt} on:click={() => Ru.kirche = opt}>{opt === 'Ja' ? 'Yes' : 'No'}</button>
                  {/each}
                </div>
              </div>
            </div>

          {:else if step === 1}
            <div class="flex flex-col gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Monthly Rürup Contribution</label>
                <div class="sfx text-xl">
                  <input type="number" step="25" bind:value={Ru.mb} class="text-xl font-medium" />
                  <span class="sfxt text-[15px]">€ / month</span>
                </div>
              </div>
              {#if result}
                <div class="card" style="background:var(--bg2)">
                  <div class="ey mb-[10px]">Tax Savings 2025</div>
                  <div class="stat text-[40px]">{fmtE(result.steJ)} / year</div>
                  <div class="text-xs text-fg3 font-mono mt-2">
                    Contribution room 2025: {de0.format(Math.round(result.sp))} € · Deductible: {de0.format(Math.round(result.absB))} €
                  </div>
                </div>
              {/if}
              {#if Ru.selbst === 'Nein'}
                <div class="flex flex-col gap-2">
                  <label class="lbl">Employee Share of Statutory Pension</label>
                  <div class="sfx"><input type="number" step="100" bind:value={Ru.grvAN} /><span class="sfxt">€/year</span></div>
                  <span class="hint">Your share is deducted from the Rürup contribution room</span>
                </div>
              {/if}
            </div>

          {:else if step === 2}
            <div class="grid grid-cols-2 gap-5 mb-4">
              <div class="flex flex-col gap-2">
                <label class="lbl">Return p.a. (after costs)</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={Ru.rendite} /><span class="sfxt">% p.a.</span></div>
                <span class="hint">ETF-Rürup avg.: 5–7%</span>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Annual Inflation</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={Ru.inf} /><span class="sfxt">% p.a.</span></div>
              </div>
            </div>
            <div class="flex flex-col gap-2">
              <label class="lbl">Savings Period (years until retirement)</label>
              <input class="inp" type="number" min="5" max="40" bind:value={Ru.lz} />
            </div>

          {:else if step === 3}
            <div class="grid grid-cols-2 gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Retirement Age</label>
                <input class="inp" type="number" min="62" max="70" bind:value={Ru.rentAlter} />
                <span class="hint">Earliest: age 62 (contracts from 2012)</span>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Life Expectancy</label>
                <input class="inp" type="number" min="70" max="100" bind:value={Ru.lebErw} />
              </div>
            </div>
          {/if}
        </div>

        <CalcNavButtons
          {step} labels={RUS_LABELS} calcLabel="Calculate Rürup →"
          on:back={back} on:next={next}
        />
      </div>

      <!-- Sidebar -->
      <aside class="calc-sidebar">
        <div class="ey mb-[14px]">Tax Benefit</div>
        <div class="stat text-[40px]">{result ? fmtE(result.steM) + '/mo.' : '–'}</div>
        <div class="text-fg3 text-[11px] font-mono mt-[6px] uppercase tracking-[.08em]">€ / month saved</div>
        {#if result}
          <div class="mt-4 pt-4 text-[13px]" style="border-top:1px solid var(--line)">
            <div class="flex items-center justify-between py-2 text-[13px]">
              <span class="text-fg3">Monthly Pension (net)</span>
              <span class="font-mono">{fmtE(result.nettoR)}/mo.</span>
            </div>
          </div>
        {/if}
      </aside>
    </div>
  </div>
</div>
{/if}
