<script>
  import { createEventDispatcher } from 'svelte';
  import CalcNav from '../components/CalcNav.svelte';
  import VersicherungResult from './VersicherungResult.svelte';
  import { defaultV, VBENCH } from '../lib/calcs.js';
  import { fmtE, de0 } from '../lib/utils.js';

  const dispatch = createEventDispatcher();
  let V = defaultV();
  let showResult = false;

  $: vKeys = Object.keys(VBENCH);
  $: total = vKeys.reduce((s, k) => s + (Number(V[k]) || 0), 0);
  $: totalJ = total * 12;
</script>

{#if showResult}
  <VersicherungResult {V} {total}
    on:back={() => { showResult = false; V = defaultV(); dispatch('back'); }}
    on:recalc={() => { showResult = false; V = defaultV(); }}
    on:navigate={e => dispatch('navigate', e.detail)}
  />
{:else}
<div>
  <CalcNav title="Versicherungs-Check" on:back={() => dispatch('back')} />

  <div class="fbody">
    <div class="calc-layout">
      <div class="calc-form">
        <div class="ey">Versicherungsanalyse</div>
        <h2 class="text-4xl font-medium tracking-[-0.03em] max-w-[700px] mt-3 leading-[1.1]">
          Was zahlst du für deine Versicherungen?
        </h2>
        <p class="text-[15px] text-fg2 mt-3 max-w-[600px]">
          Trage deine monatlichen Beiträge ein. Pensora vergleicht deine Ausgaben mit dem GDV-Marktdurchschnitt 2025.
        </p>

        <div class="grid grid-cols-2 gap-4 mt-7">
          {#each vKeys as k}
            <div class="cardf" style="padding:20px">
              <div class="ey mb-[6px] text-[10px]">{k}</div>
              <div class="sfx">
                <input type="number" step="1" bind:value={V[k]} style="font-size:18px;font-weight:500" />
                <span class="sfxt">€/Mo.</span>
              </div>
              <div class="mt-2 text-[11px] text-fg3 font-mono">{VBENCH[k].hint}</div>
              <div class="flex items-center gap-2 mt-[6px]">
                <div class="flex-1 h-[3px] rounded-sm overflow-hidden" style="background:var(--line)">
                  <div style="height:100%;width:{Math.min((V[k]/VBENCH[k].avg)*100,200)}%;background:{V[k]>VBENCH[k].avg*1.3?'var(--loss)':V[k]<VBENCH[k].avg*0.7?'#6fcf97':'var(--fg)'};border-radius:2px;transition:width .2s"></div>
                </div>
                <span class="text-[10px] font-mono" style="color:{V[k]>VBENCH[k].avg*1.3?'var(--loss)':V[k]<VBENCH[k].avg*0.7?'#6fcf97':'var(--fg3)'}">
                  Ø {VBENCH[k].avg} €
                </span>
              </div>
            </div>
          {/each}
        </div>

        <div class="flex justify-end mt-9 pt-5" style="border-top:1px solid var(--line)">
          <button class="btn btnp btnlg" on:click={() => { showResult = true; window.scrollTo(0, 0); }}>
            Versicherungen analysieren →
          </button>
        </div>
      </div>

      <!-- Sidebar -->
      <aside class="calc-sidebar">
        <div class="ey mb-[14px]">Gesamtkosten</div>
        <div class="stat text-[40px]">{fmtE(total)}/Mo.</div>
        <div class="text-fg3 text-[11px] font-mono mt-[6px] uppercase tracking-[.08em]">monatlich</div>
        <div class="mt-4 pt-4 text-[13px]" style="border-top:1px solid var(--line)">
          <div class="calc-sidebar-row">
            <span class="text-fg3">Pro Jahr</span>
            <span class="font-mono">{de0.format(Math.round(totalJ))} €</span>
          </div>
          <div class="flex items-center justify-between py-2 text-[13px]">
            <span class="text-fg3">Ø-Markt</span>
            <span class="font-mono">{fmtE(Object.values(VBENCH).reduce((s,b)=>s+b.avg,0))}/Mo.</span>
          </div>
        </div>
        <div class="mt-4">
          {#each vKeys as k}
            <div class="flex items-center justify-between py-[5px] text-[11px]" style="border-bottom:1px solid var(--line)">
              <span class="text-fg3 max-w-[140px] overflow-hidden text-ellipsis whitespace-nowrap">{k}</span>
              <span class="font-mono" style="color:{V[k]>VBENCH[k].avg*1.3?'var(--loss)':V[k]<VBENCH[k].avg*0.7?'#6fcf97':'var(--fg)'}">
                {fmtE(V[k])}
              </span>
            </div>
          {/each}
        </div>
      </aside>
    </div>
  </div>
</div>
{/if}
