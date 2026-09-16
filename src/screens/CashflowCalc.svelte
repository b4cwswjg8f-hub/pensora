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
  <CalcNav title="Cashflow Calculator" on:back={() => dispatch('back')} />
  <CalcStepperBar labels={CS_LABELS} {step} />

  <div class="fbody">
    <div class="calc-layout">
      <div class="calc-form">
        <CalcStepHeader {s} />

        <div class="mt-7">
          {#if step === 0}
            <div class="flex flex-col gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Monthly Net Income</label>
                <div class="sfx text-xl">
                  <input type="number" step="50" bind:value={C.netto} class="text-xl font-medium" />
                  <span class="sfxt text-[15px]">€ / month</span>
                </div>
              </div>
              {#if result}
                <div class="card" style="background:var(--bg2)">
                  <div class="ey mb-[10px]">The 50/15/15 Rule of Thumb (Guidelines)</div>
                  <div class="grid gap-3 mt-2" style="grid-template-columns:repeat(3,1fr)">
                    {#each [['Fixed Costs (50%)',result.emp_fix],['Savings (15%)',result.emp_av],['Leisure (15%)',result.emp_frei]] as [l, v]}
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
                <div class="text-[11px] text-fg3 font-mono uppercase tracking-[.08em] mb-3">Fixed Costs</div>
                <div class="flex flex-col gap-3">
                  {#each [
                    ['Rent (incl. utilities)','miete','€/mo.',50],
                    ['Additional Costs / Electricity / Gas','nk','€/mo.',10],
                    ['Groceries','lm','€/mo.',25],
                    ['Transport (public transit / fuel)','transport','€/mo.',10],
                    ['Communication (phone, internet)','komm','€/mo.',5],
                  ] as [l, k, sfx, stp]}
                    <div class="flex flex-col gap-2">
                      <label class="lbl text-[11px]">{l}</label>
                      <div class="sfx"><input type="number" step={stp} bind:value={C[k]} /><span class="sfxt">{sfx}</span></div>
                    </div>
                  {/each}
                </div>
              </div>
              <div>
                <div class="text-[11px] text-fg3 font-mono uppercase tracking-[.08em] mb-3">Variable Costs</div>
                <div class="flex flex-col gap-3">
                  {#each [
                    ['Total Insurance','versich','€/mo.',10],
                    ['Retirement Savings (ETF, etc.)','av','€/mo.',25],
                    ['Leisure & Hobbies','frei','€/mo.',25],
                    ['Other','sonst','€/mo.',10],
                  ] as [l, k, sfx, stp]}
                    <div class="flex flex-col gap-2">
                      <label class="lbl text-[11px]">{l}</label>
                      <div class="sfx"><input type="number" step={stp} bind:value={C[k]} /><span class="sfxt">{sfx}</span></div>
                    </div>
                  {/each}
                </div>
                {#if result}
                  <div class="card mt-5" style="background:var(--bg2)">
                    <div class="ey mb-[6px]">Available</div>
                    <div class="stat text-[32px]" style="color:{result.frei > 0 ? 'var(--fg)' : 'var(--loss)'}">
                      {fmtE(result.frei)}/mo.
                    </div>
                    <div class="text-[11px] text-fg3 font-mono mt-[6px]">
                      Expenses: {fmtE(result.out)} of {fmtE(C.netto)}
                    </div>
                  </div>
                {/if}
              </div>
            </div>
          {/if}
        </div>

        <CalcNavButtons
          {step} labels={CS_LABELS} calcLabel="Analyze Cashflow →"
          on:back={back} on:next={next}
        />
      </div>

      <!-- Sidebar -->
      <aside class="calc-sidebar">
        <div class="ey mb-[14px]">Available</div>
        <div class="stat text-[40px]" style="color:{result && result.frei > 0 ? 'var(--fg)' : 'var(--loss)'}">
          {result ? fmtE(result.frei) + '/mo.' : '–'}
        </div>
        <div class="text-fg3 text-[11px] font-mono mt-[6px] uppercase tracking-[.08em]">after all expenses</div>
        {#if result}
          <div class="mt-4 pt-4 text-[13px]" style="border-top:1px solid var(--line)">
            <div class="calc-sidebar-row">
              <span class="text-fg3">Emergency Fund (3 mo.)</span>
              <span class="font-mono">{fmtE(result.notg)}</span>
            </div>
            <div class="flex items-center justify-between py-2 text-[13px]">
              <span class="text-fg3">Total Expenses</span>
              <span class="font-mono">{fmtE(result.out)}</span>
            </div>
          </div>
        {/if}
      </aside>
    </div>
  </div>
</div>
{/if}
