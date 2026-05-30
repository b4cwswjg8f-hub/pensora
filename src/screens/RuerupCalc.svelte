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
  <CalcNav title="Rürup-Rechner" on:back={() => dispatch('back')} />
  <CalcStepperBar labels={RUS_LABELS} {step} />

  <div class="fbody">
    <div class="calc-layout">
      <div class="calc-form">
        <CalcStepHeader {s} />

        <div class="mt-7">
          {#if step === 0}
            <div class="flex flex-col gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Selbstständig?</label>
                <div class="seg segf">
                  {#each ['Ja','Nein'] as opt}
                    <button class:on={Ru.selbst === opt} on:click={() => Ru.selbst = opt}>{opt}</button>
                  {/each}
                </div>
                <span class="hint">Selbstständige: voller Rürup-Spielraum</span>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Bruttojahresgehalt</label>
                <div class="sfx"><input type="number" step="1000" bind:value={Ru.brutto} /><span class="sfxt">€/Jahr</span></div>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Grenzsteuersatz</label>
                <div class="sfx"><input type="number" step="1" bind:value={Ru.grenzSt} /><span class="sfxt">%</span></div>
                <span class="hint">~30% bei 60k € · ~42% ab 68k €</span>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Kirchensteuerpflichtig?</label>
                <div class="seg segf">
                  {#each ['Ja','Nein'] as opt}
                    <button class:on={Ru.kirche === opt} on:click={() => Ru.kirche = opt}>{opt}</button>
                  {/each}
                </div>
              </div>
            </div>

          {:else if step === 1}
            <div class="flex flex-col gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Monatlicher Rürup-Beitrag</label>
                <div class="sfx text-xl">
                  <input type="number" step="25" bind:value={Ru.mb} class="text-xl font-medium" />
                  <span class="sfxt text-[15px]">€ / Monat</span>
                </div>
              </div>
              {#if result}
                <div class="card" style="background:var(--bg2)">
                  <div class="ey mb-[10px]">Steuerersparnis 2025</div>
                  <div class="stat text-[40px]">{fmtE(result.steJ)} / Jahr</div>
                  <div class="text-xs text-fg3 font-mono mt-2">
                    Spielraum 2025: {de0.format(Math.round(result.sp))} € · Absetzbar: {de0.format(Math.round(result.absB))} €
                  </div>
                </div>
              {/if}
              {#if Ru.selbst === 'Nein'}
                <div class="flex flex-col gap-2">
                  <label class="lbl">GRV-Arbeitnehmeranteil</label>
                  <div class="sfx"><input type="number" step="100" bind:value={Ru.grvAN} /><span class="sfxt">€/Jahr</span></div>
                  <span class="hint">AN-Anteil wird vom Rürup-Spielraum abgezogen</span>
                </div>
              {/if}
            </div>

          {:else if step === 2}
            <div class="grid grid-cols-2 gap-5 mb-4">
              <div class="flex flex-col gap-2">
                <label class="lbl">Rendite p.a. (nach Kosten)</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={Ru.rendite} /><span class="sfxt">% p.a.</span></div>
                <span class="hint">ETF-Rürup Ø: 5–7 %</span>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Inflation p.a.</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={Ru.inf} /><span class="sfxt">% p.a.</span></div>
              </div>
            </div>
            <div class="flex flex-col gap-2">
              <label class="lbl">Ansparzeit (Jahre bis Rente)</label>
              <input class="inp" type="number" min="5" max="40" bind:value={Ru.lz} />
            </div>

          {:else if step === 3}
            <div class="grid grid-cols-2 gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Renteneintrittsalter</label>
                <input class="inp" type="number" min="62" max="70" bind:value={Ru.rentAlter} />
                <span class="hint">Frühestens: 62 J. (Verträge ab 2012)</span>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Lebenserwartung</label>
                <input class="inp" type="number" min="70" max="100" bind:value={Ru.lebErw} />
              </div>
            </div>
          {/if}
        </div>

        <CalcNavButtons
          {step} labels={RUS_LABELS} calcLabel="Rürup berechnen →"
          on:back={back} on:next={next}
        />
      </div>

      <!-- Sidebar -->
      <aside class="calc-sidebar">
        <div class="ey mb-[14px]">Steuervorteil</div>
        <div class="stat text-[40px]">{result ? fmtE(result.steM) + '/Mo.' : '–'}</div>
        <div class="text-fg3 text-[11px] font-mono mt-[6px] uppercase tracking-[.08em]">€ / Monat gespart</div>
        {#if result}
          <div class="mt-4 pt-4 text-[13px]" style="border-top:1px solid var(--line)">
            <div class="flex items-center justify-between py-2 text-[13px]">
              <span class="text-fg3">Monatsrente (netto)</span>
              <span class="font-mono">{fmtE(result.nettoR)}/Mo.</span>
            </div>
          </div>
        {/if}
      </aside>
    </div>
  </div>
</div>
{/if}
