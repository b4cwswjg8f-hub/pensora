<script>
  import { createEventDispatcher } from 'svelte';
  import CalcNav from '../components/CalcNav.svelte';
  import CalcStepperBar from '../components/CalcStepperBar.svelte';
  import CalcStepHeader from '../components/CalcStepHeader.svelte';
  import CalcNavButtons from '../components/CalcNavButtons.svelte';
  import RenteResult from './RenteResult.svelte';
  import { defaultR, calcR, RS_LABELS, GRV } from '../lib/calcs.js';
  import { fmtE, de0 } from '../lib/utils.js';

  const dispatch = createEventDispatcher();
  let R = defaultR();
  let step = 0;
  let showResult = false;

  $: result = (() => { try { return calcR(R); } catch(e) { return null; } })();
  $: s = RS_LABELS[step];
  $: ep_preview = (Math.min(R.brutto, GRV.bbg) / GRV.de).toFixed(3) + ' points/year';

  function next() {
    if (step < RS_LABELS.length - 1) { step++; window.scrollTo(0, 0); }
    else { showResult = true; window.scrollTo(0, 0); }
  }
  function back() { if (step > 0) { step--; window.scrollTo(0, 0); } }
</script>

{#if showResult}
  <RenteResult {R} {result}
    on:back={() => { showResult = false; step = 0; R = defaultR(); dispatch('back'); }}
    on:recalc={() => { showResult = false; step = 0; }}
    on:navigate={e => dispatch('navigate', e.detail)}
  />
{:else}
<div>
  <CalcNav title="German Pension Calculator" on:back={() => dispatch('back')} />
  <CalcStepperBar labels={RS_LABELS} {step} />

  <div class="fbody">
    <div class="calc-layout">
      <div class="calc-form">
        <CalcStepHeader {s} />

        <div class="mt-7">
          {#if step === 0}
            <div class="grid grid-cols-2 gap-5 mb-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Date of Birth</label>
                <input class="inp" type="text" bind:value={R.gebdat} placeholder="DD.MM.YYYY" />
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Retirement Age</label>
                <input class="inp" type="number" min="60" max="70" bind:value={R.rentAlter} />
                <span class="hint">Standard retirement age: 67</span>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Started Working in Germany (Year)</label>
                <input class="inp" type="number" min="1970" max="2025" bind:value={R.djBeginn} />
                <span class="hint">When did you start paying into statutory pension insurance?</span>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Subject to Church Tax?</label>
                <div class="seg segf">
                  {#each ['Ja','Nein'] as opt}
                    <button class:on={R.kirche === opt} on:click={() => R.kirche = opt}>{opt === 'Ja' ? 'Yes' : 'No'}</button>
                  {/each}
                </div>
              </div>
            </div>

          {:else if step === 1}
            <div class="flex flex-col gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Gross Annual Salary</label>
                <div class="sfx"><input type="number" step="1000" bind:value={R.brutto} /><span class="sfxt">€/year</span></div>
                <span class="hint">Basis for earnings points (§ 70 SGB VI) · Contribution ceiling 2025: €96,600/yr</span>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Annual Salary Growth</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={R.wachstum} /><span class="sfxt">% p.a.</span></div>
                <span class="hint">Simplification: constant rate</span>
              </div>
              <div class="card" style="background:var(--bg2)">
                <div class="ey mb-[10px]">Earnings Points / Year (current)</div>
                <div class="stat text-[40px]">{ep_preview}</div>
                <div class="text-xs text-fg3 font-mono mt-2">Pension value 2025: €40.79 · Average income 2025: €50,493/yr</div>
              </div>
            </div>

          {:else if step === 2}
            <div class="grid grid-cols-2 gap-5 mb-4">
              <div class="flex flex-col gap-2">
                <label class="lbl">Annual Pension Adjustment</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={R.ra} /><span class="sfxt">% p.a.</span></div>
                <span class="hint">Avg.: ~1.8% · 2026: +4.24%</span>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Annual Inflation</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={R.inf} /><span class="sfxt">% p.a.</span></div>
                <span class="hint">Current: ~2.1%</span>
              </div>
            </div>
            <div class="flex flex-col gap-2">
              <label class="lbl">Life Expectancy</label>
              <input class="inp" type="number" min="70" max="100" bind:value={R.lebErw} />
              <span class="hint">Statistically: 84–88 years</span>
            </div>

          {:else if step === 3}
            <div class="flex flex-col gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Desired Net Monthly Income in Retirement</label>
                <div class="sfx text-xl">
                  <input type="number" step="50" bind:value={R.zielEur} class="text-xl font-medium" />
                  <span class="sfxt text-[15px]">€ / month net</span>
                </div>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Existing Provisions (monthly)</label>
                <div class="sfx"><input type="number" step="1" bind:value={R.vorsorge} /><span class="sfxt">€/mo.</span></div>
                <span class="hint">Employer pension, ETF savings plan, etc.</span>
              </div>
              {#if result}
                <div class="card" style="border-color:rgba(255,107,107,.25)">
                  <div class="ey mb-[10px]" style="color:var(--loss)">Pension Gap Preview</div>
                  <div class="stat text-[48px]" style="color:{result.luecke > 0 ? 'var(--loss)' : 'var(--fg)'}">
                    {result.luecke > 0 ? '−' + de0.format(Math.round(result.luecke)) + ' €/mo.' : '✓ Covered'}
                  </div>
                  <div class="text-xs text-fg3 font-mono mt-2">
                    Gross: {fmtE(result.brutto)} · Net: {fmtE(result.netto)} · Goal: {fmtE(R.zielEur)}
                  </div>
                </div>
              {/if}
            </div>
          {/if}
        </div>

        <CalcNavButtons
          {step} labels={RS_LABELS} calcLabel="Calculate Pension →"
          on:back={back} on:next={next}
        />
      </div>

      <!-- Sidebar -->
      <aside class="calc-sidebar">
        <div class="ey mb-[14px]">Pension Preview</div>
        <div class="flex items-baseline gap-2">
          <span class="stat text-[52px]">{result ? de0.format(Math.round(result.netto)) : '–'}</span>
          <span class="text-fg2"> €</span>
        </div>
        <div class="text-fg3 text-[11px] font-mono mt-[6px] uppercase tracking-[.08em]">Net Pension / Month</div>
        {#if result}
          <div class="mt-5 pt-4 text-[13px]" style="border-top:1px solid var(--line)">
            <div class="calc-sidebar-row">
              <span class="text-fg3">Earnings Points</span>
              <span class="font-mono">{result.gesEP.toFixed(1)} pts</span>
            </div>
            <div class="flex items-center justify-between py-2 text-[13px]">
              <span class="text-fg3">Pension Gap</span>
              <span class="font-mono" style="color:{result.luecke > 0 ? 'var(--loss)' : 'var(--fg)'}">
                {result.luecke > 0 ? '−' + fmtE(result.luecke) + '/mo.' : '✓ Covered'}
              </span>
            </div>
          </div>
        {/if}
      </aside>
    </div>
  </div>
</div>
{/if}
