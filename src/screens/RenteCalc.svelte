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
  $: ep_preview = (Math.min(R.brutto, GRV.bbg) / GRV.de).toFixed(3).replace('.', ',') + ' EP/Jahr';

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
  <CalcNav title="Rentenrechner" on:back={() => dispatch('back')} />
  <CalcStepperBar labels={RS_LABELS} {step} />

  <div class="fbody">
    <div class="calc-layout">
      <div class="calc-form">
        <CalcStepHeader {s} />

        <div class="mt-7">
          {#if step === 0}
            <div class="grid grid-cols-2 gap-5 mb-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Geburtsdatum</label>
                <input class="inp" type="text" bind:value={R.gebdat} placeholder="TT.MM.JJJJ" />
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Renteneintrittsalter</label>
                <input class="inp" type="number" min="60" max="70" bind:value={R.rentAlter} />
                <span class="hint">Regelaltersgrenze: 67 J.</span>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Erwerbsbeginn (Jahr)</label>
                <input class="inp" type="number" min="1970" max="2025" bind:value={R.djBeginn} />
                <span class="hint">Ab wann GRV-Beiträge?</span>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Kirchensteuerpflichtig?</label>
                <div class="seg segf">
                  {#each ['Ja','Nein'] as opt}
                    <button class:on={R.kirche === opt} on:click={() => R.kirche = opt}>{opt}</button>
                  {/each}
                </div>
              </div>
            </div>

          {:else if step === 1}
            <div class="flex flex-col gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Bruttojahresgehalt</label>
                <div class="sfx"><input type="number" step="1000" bind:value={R.brutto} /><span class="sfxt">€/Jahr</span></div>
                <span class="hint">Basis für Entgeltpunkte (§ 70 SGB VI) · BBG 2025: 96.600 €/J.</span>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Jährl. Gehaltswachstum</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={R.wachstum} /><span class="sfxt">% p.a.</span></div>
                <span class="hint">Vereinfachung: konstante Rate</span>
              </div>
              <div class="card" style="background:var(--bg2)">
                <div class="ey mb-[10px]">Entgeltpunkte / Jahr (aktuell)</div>
                <div class="stat text-[40px]">{ep_preview}</div>
                <div class="text-xs text-fg3 font-mono mt-2">Rentenwert 2025: 40,79 € · DE 2025: 50.493 €/J.</div>
              </div>
            </div>

          {:else if step === 2}
            <div class="grid grid-cols-2 gap-5 mb-4">
              <div class="flex flex-col gap-2">
                <label class="lbl">Rentenanpassung p.a.</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={R.ra} /><span class="sfxt">% p.a.</span></div>
                <span class="hint">Ø: ~1,8 % · 2026: +4,24 %</span>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Inflation p.a.</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={R.inf} /><span class="sfxt">% p.a.</span></div>
                <span class="hint">Aktuell: ~2,1 %</span>
              </div>
            </div>
            <div class="flex flex-col gap-2">
              <label class="lbl">Lebenserwartung</label>
              <input class="inp" type="number" min="70" max="100" bind:value={R.lebErw} />
              <span class="hint">Statistisch: 84–88 Jahre</span>
            </div>

          {:else if step === 3}
            <div class="flex flex-col gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Gewünschtes Netto-Monatseinkommen im Ruhestand</label>
                <div class="sfx text-xl">
                  <input type="number" step="50" bind:value={R.zielEur} class="text-xl font-medium" />
                  <span class="sfxt text-[15px]">€ / Monat netto</span>
                </div>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Bestehende Vorsorge (monatlich)</label>
                <div class="sfx"><input type="number" step="1" bind:value={R.vorsorge} /><span class="sfxt">€/Mo.</span></div>
                <span class="hint">Riester, bAV, ETF …</span>
              </div>
              {#if result}
                <div class="card" style="border-color:rgba(255,107,107,.25)">
                  <div class="ey mb-[10px]" style="color:var(--loss)">Rentenlücke Vorschau</div>
                  <div class="stat text-[48px]" style="color:{result.luecke > 0 ? 'var(--loss)' : 'var(--fg)'}">
                    {result.luecke > 0 ? '−' + de0.format(Math.round(result.luecke)) + ' €/Mo.' : '✓ Gedeckt'}
                  </div>
                  <div class="text-xs text-fg3 font-mono mt-2">
                    Brutto: {fmtE(result.brutto)} · Netto: {fmtE(result.netto)} · Ziel: {fmtE(R.zielEur)}
                  </div>
                </div>
              {/if}
            </div>
          {/if}
        </div>

        <CalcNavButtons
          {step} labels={RS_LABELS} calcLabel="Rente berechnen →"
          on:back={back} on:next={next}
        />
      </div>

      <!-- Sidebar -->
      <aside class="calc-sidebar">
        <div class="ey mb-[14px]">Rentenvorschau</div>
        <div class="flex items-baseline gap-2">
          <span class="stat text-[52px]">{result ? de0.format(Math.round(result.netto)) : '–'}</span>
          <span class="text-fg2"> €</span>
        </div>
        <div class="text-fg3 text-[11px] font-mono mt-[6px] uppercase tracking-[.08em]">Nettorente / Monat</div>
        {#if result}
          <div class="mt-5 pt-4 text-[13px]" style="border-top:1px solid var(--line)">
            <div class="calc-sidebar-row">
              <span class="text-fg3">Entgeltpunkte</span>
              <span class="font-mono">{result.gesEP.toFixed(1).replace('.', ',')} EP</span>
            </div>
            <div class="flex items-center justify-between py-2 text-[13px]">
              <span class="text-fg3">Rentenlücke</span>
              <span class="font-mono" style="color:{result.luecke > 0 ? 'var(--loss)' : 'var(--fg)'}">
                {result.luecke > 0 ? '−' + fmtE(result.luecke) + '/Mo.' : '✓ Gedeckt'}
              </span>
            </div>
          </div>
        {/if}
      </aside>
    </div>
  </div>
</div>
{/if}
