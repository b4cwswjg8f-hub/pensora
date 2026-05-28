<script>
  import { createEventDispatcher } from 'svelte';
  import Logo from '../components/Logo.svelte';
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
  <nav class="nav">
    <div class="row g16">
      <button class="brand" on:click={() => dispatch('back')}><Logo /> Pensora</button>
      <span style="color:var(--line2);font-size:16px">/</span>
      <span style="color:var(--fg2);font-size:14px">Versicherungs-Check</span>
    </div>
    <div class="row g8"><button class="btn btng" on:click={() => dispatch('back')}>← Hub</button></div>
  </nav>

  <div class="fbody">
    <div style="display:grid;grid-template-columns:1fr 320px">
      <div style="padding:36px 56px">
        <div class="ey">Versicherungsanalyse</div>
        <h2 style="font-size:36px;font-weight:500;letter-spacing:-.03em;max-width:700px;margin-top:12px;line-height:1.1">
          Was zahlst du für deine Versicherungen?
        </h2>
        <p style="font-size:15px;color:var(--fg2);margin-top:12px;max-width:600px">
          Trage deine monatlichen Beiträge ein. Pensora vergleicht deine Ausgaben mit dem GDV-Marktdurchschnitt 2025.
        </p>

        <div style="margin-top:28px;display:grid;grid-template-columns:1fr 1fr;gap:16px">
          {#each vKeys as k}
            <div class="cardf" style="padding:20px">
              <div class="ey" style="margin-bottom:6px;font-size:10px">{k}</div>
              <div class="sfx">
                <input type="number" step="1" bind:value={V[k]} style="font-size:18px;font-weight:500" />
                <span class="sfxt">€/Mo.</span>
              </div>
              <div style="margin-top:8px;font-size:11px;color:var(--fg3);font-family:var(--mono)">{VBENCH[k].hint}</div>
              <div style="margin-top:6px;display:flex;align-items:center;gap:8px">
                <div style="flex:1;height:3px;background:var(--line);border-radius:2px;overflow:hidden">
                  <div style="height:100%;width:{Math.min((V[k]/VBENCH[k].avg)*100,200)}%;background:{V[k]>VBENCH[k].avg*1.3?'var(--loss)':V[k]<VBENCH[k].avg*0.7?'#6fcf97':'var(--fg)'};border-radius:2px;transition:width .2s"></div>
                </div>
                <span style="font-size:10px;font-family:var(--mono);color:{V[k]>VBENCH[k].avg*1.3?'var(--loss)':V[k]<VBENCH[k].avg*0.7?'#6fcf97':'var(--fg3)'}">
                  Ø {VBENCH[k].avg} €
                </span>
              </div>
            </div>
          {/each}
        </div>

        <div class="row" style="justify-content:flex-end;margin-top:36px;padding-top:20px;border-top:1px solid var(--line)">
          <button class="btn btnp btnlg" on:click={() => { showResult = true; window.scrollTo(0,0); }}>
            Versicherungen analysieren →
          </button>
        </div>
      </div>

      <!-- Sidebar -->
      <aside style="border-left:1px solid var(--line);padding:36px 28px;background:var(--bg1)">
        <div class="ey" style="margin-bottom:14px">Gesamtkosten</div>
        <div class="stat" style="font-size:40px">{fmtE(total)}/Mo.</div>
        <div style="color:var(--fg3);font-size:11px;font-family:var(--mono);margin-top:6px;text-transform:uppercase;letter-spacing:.08em">monatlich</div>
        <div style="margin-top:16px;padding-top:16px;border-top:1px solid var(--line);font-size:13px">
          <div class="row" style="justify-content:space-between;padding:8px 0">
            <span style="color:var(--fg3)">Pro Jahr</span>
            <span style="font-family:var(--mono)">{de0.format(Math.round(totalJ))} €</span>
          </div>
          <div class="row" style="justify-content:space-between;padding:8px 0">
            <span style="color:var(--fg3)">Ø-Markt</span>
            <span style="font-family:var(--mono)">{fmtE(Object.values(VBENCH).reduce((s,b)=>s+b.avg,0))}/Mo.</span>
          </div>
        </div>
        <div style="margin-top:16px">
          {#each vKeys as k}
            <div class="row" style="justify-content:space-between;padding:5px 0;border-bottom:1px solid var(--line);font-size:11px">
              <span style="color:var(--fg3);max-width:140px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{k}</span>
              <span style="font-family:var(--mono);color:{V[k]>VBENCH[k].avg*1.3?'var(--loss)':V[k]<VBENCH[k].avg*0.7?'#6fcf97':'var(--fg)'}">{fmtE(V[k])}</span>
            </div>
          {/each}
        </div>
      </aside>
    </div>
  </div>
</div>
{/if}
