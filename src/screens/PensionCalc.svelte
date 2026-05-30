<script>
  import { createEventDispatcher } from 'svelte';
  import CalcNav from '../components/CalcNav.svelte';
  import CalcStepperBar from '../components/CalcStepperBar.svelte';
  import CalcStepHeader from '../components/CalcStepHeader.svelte';
  import CalcNavButtons from '../components/CalcNavButtons.svelte';
  import PensionResult from './PensionResult.svelte';
  import { defaultP, calcP, PS_LABELS, LAENDER, BESO, BESO_KEYS, getBeso } from '../lib/calcs.js';
  import { fmtE, fmtP, de0 } from '../lib/utils.js';

  const dispatch = createEventDispatcher();

  let P = defaultP();
  let step = 0;
  let showResult = false;

  $: result = (() => { try { return calcP(P); } catch(e) { return null; } })();
  $: s = PS_LABELS[step];
  $: aktB_preview = de0.format(getBeso(P.bGr, parseInt(P.bSt)) + (P.zusatz || 0)) + ' €';
  $: yr = new Date().getFullYear();
  $: alter_preview = yr - (parseInt((P.gebdat || '').split('.')[2]) || 1986);
  $: jbp_preview = Math.max(P.pensAlter - alter_preview, 0);

  function next() {
    if (step < PS_LABELS.length - 1) { step++; window.scrollTo(0, 0); }
    else { showResult = true; window.scrollTo(0, 0); }
  }
  function back() {
    if (step > 0) { step--; window.scrollTo(0, 0); }
  }
</script>

{#if showResult}
  <PensionResult
    {P} {result}
    on:back={() => { showResult = false; step = 0; P = defaultP(); dispatch('back'); }}
    on:recalc={() => { showResult = false; step = 0; }}
    on:navigate={e => dispatch('navigate', e.detail)}
  />
{:else}
<div>
  <CalcNav title="Pensionsrechner" on:back={() => dispatch('back')} />
  <CalcStepperBar labels={PS_LABELS} {step} />

  <div class="fbody">
    <div class="calc-layout">
      <div class="calc-form">
        <CalcStepHeader {s} />

        <div class="mt-7">
          <!-- STEP 0: Stammdaten -->
          {#if step === 0}
            <div class="grid grid-cols-2 gap-5 mb-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Geburtsdatum</label>
                <input class="inp" type="text" bind:value={P.gebdat} placeholder="TT.MM.JJJJ" />
                <span class="hint">TT.MM.JJJJ</span>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Diensteintritt</label>
                <input class="inp" type="text" bind:value={P.dienst} placeholder="TT.MM.JJJJ" />
                <span class="hint">TT.MM.JJJJ</span>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Bundesland</label>
                <div class="sw">
                  <select class="sel" bind:value={P.bund}>
                    {#each LAENDER as l}<option value={l}>{l}</option>{/each}
                  </select>
                </div>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Kirchensteuerpflichtig?</label>
                <div class="seg segf">
                  {#each ['Ja','Nein'] as opt}
                    <button class:on={P.kirche === opt} on:click={() => P.kirche = opt}>{opt}</button>
                  {/each}
                </div>
              </div>
            </div>

          <!-- STEP 1: Aktuelle Besoldung -->
          {:else if step === 1}
            <div class="grid grid-cols-3 gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Besoldungsgruppe</label>
                <div class="sw">
                  <select class="sel" bind:value={P.bGr}>
                    {#each BESO_KEYS as k}<option value={k}>{k}</option>{/each}
                  </select>
                </div>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Erfahrungsstufe</label>
                <div class="sw">
                  <select class="sel" bind:value={P.bSt}>
                    {#each [1,2,3,4,5,6,7,8,9,10,11,12] as n}
                      <option value={String(n)}>{n}</option>
                    {/each}
                  </select>
                </div>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Zus. Zulagen</label>
                <div class="sfx">
                  <input type="number" step="1" bind:value={P.zusatz} />
                  <span class="sfxt">€/Mo.</span>
                </div>
                <span class="hint">z.B. Funktionszulage</span>
              </div>
            </div>
            <div class="card mt-5" style="background:var(--bg2)">
              <div class="ey mb-[10px]">Bruttogehalt (Schätzung BW 2025)</div>
              <div class="stat text-[40px]">{aktB_preview}</div>
            </div>

          <!-- STEP 2: Perspektive -->
          {:else if step === 2}
            <div class="grid grid-cols-3 gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Besoldungsgruppe Ziel</label>
                <div class="sw">
                  <select class="sel" bind:value={P.pGr}>
                    {#each BESO_KEYS as k}<option value={k}>{k}</option>{/each}
                  </select>
                </div>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Erfahrungsstufe Ziel</label>
                <div class="sw">
                  <select class="sel" bind:value={P.pSt}>
                    {#each [1,2,3,4,5,6,7,8,9,10,11,12] as n}
                      <option value={String(n)}>{n}</option>
                    {/each}
                  </select>
                </div>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Zus. Zulagen Ziel</label>
                <div class="sfx">
                  <input type="number" step="1" bind:value={P.pZusatz} />
                  <span class="sfxt">€/Mo.</span>
                </div>
              </div>
            </div>

          <!-- STEP 3: Zeiterfassung -->
          {:else if step === 3}
            <div class="flex flex-col gap-4">
              <!-- Elternzeit -->
              <div class="card">
                <div class="flex items-start justify-between gap-6">
                  <div>
                    <h3 class="text-base font-semibold mb-[6px]">Elternzeit</h3>
                    <p class="text-[13px] text-fg2">Teilweise als Dienstzeit anerkannt (§ 12a BeamtVG).</p>
                  </div>
                  <div class="flex items-center gap-3">
                    <div class="tog" class:on={P.eltern} on:click={() => P.eltern = !P.eltern}></div>
                    <span class="text-[14px] text-fg2">{P.eltern ? 'Erfasst' : 'Nicht relevant'}</span>
                  </div>
                </div>
                {#if P.eltern}
                  <div class="grid grid-cols-2 gap-4 mt-4">
                    <div class="flex flex-col gap-2">
                      <label class="lbl">Gesamtdauer</label>
                      <div class="sfx"><input type="number" step="0.5" bind:value={P.elternJ} /><span class="sfxt">Jahre</span></div>
                    </div>
                    <div class="flex flex-col gap-2">
                      <label class="lbl">Zeitraum (ca.)</label>
                      <input class="inp" type="text" placeholder="z.B. 2014–2016" />
                    </div>
                  </div>
                {/if}
              </div>

              <!-- Beurlaubung -->
              <div class="card">
                <div class="flex items-start justify-between gap-6">
                  <div>
                    <h3 class="text-base font-semibold mb-[6px]">Beurlaubung</h3>
                    <p class="text-[13px] text-fg2">Zählt nicht als Dienstzeit (§ 9 BeamtVG).</p>
                  </div>
                  <div class="flex items-center gap-3">
                    <div class="tog" class:on={P.beurl} on:click={() => P.beurl = !P.beurl}></div>
                    <span class="text-[14px] text-fg2">{P.beurl ? 'Erfasst' : 'Nicht relevant'}</span>
                  </div>
                </div>
                {#if P.beurl}
                  <div class="mt-4">
                    <div class="sfx"><input type="number" step="0.5" bind:value={P.beurlJ} /><span class="sfxt">Jahre</span></div>
                  </div>
                {/if}
              </div>

              <!-- Teilzeit -->
              <div class="card">
                <div class="flex items-start justify-between gap-6">
                  <div>
                    <h3 class="text-base font-semibold mb-[6px]">Teilzeit</h3>
                    <p class="text-[13px] text-fg2">Reduziert Ruhegehaltssatz (§ 6 Abs. 1 BeamtVG).</p>
                  </div>
                  <div class="flex items-center gap-3">
                    <div class="tog" class:on={P.tz} on:click={() => P.tz = !P.tz}></div>
                    <span class="text-[14px] text-fg2">{P.tz ? 'Erfasst' : 'Nicht relevant'}</span>
                  </div>
                </div>
                {#if P.tz}
                  <div class="grid mt-4" style="grid-template-columns:1fr 2fr;gap:12px">
                    <div class="sfx"><input type="number" step="0.5" bind:value={P.tzJ} /><span class="sfxt">Jahre</span></div>
                    <div class="seg segf">
                      {#each [50,60,75,85,100] as p}
                        <button class:on={P.tzPct === p} on:click={() => P.tzPct = p}>{p} %</button>
                      {/each}
                    </div>
                  </div>
                {/if}
              </div>
            </div>

          <!-- STEP 4: Annahmen -->
          {:else if step === 4}
            <div class="grid grid-cols-3 gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Pensionseintrittsalter</label>
                <input class="inp" type="number" min="55" max="70" bind:value={P.pensAlter} />
                <span class="hint">Regelgrenze: 67 Jahre</span>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Lebenserwartung</label>
                <input class="inp" type="number" min="70" max="100" bind:value={P.lebErw} />
                <span class="hint">Statistisch: 84–88 Jahre</span>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Besoldungssteigerung p.a.</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={P.steigerung} /><span class="sfxt">% p.a.</span></div>
                <span class="hint">Ø: 1,5–2,0 %</span>
              </div>
            </div>
            <div class="card mt-5">
              <div class="ey mb-4">Auf dieser Basis</div>
              <div class="grid gap-5" style="grid-template-columns:repeat(4,1fr)">
                {#each [['Alter heute', alter_preview + ' J'], ['Bis Pension', jbp_preview + ' J'], ['Im Ruhestand', Math.max(P.lebErw - P.pensAlter, 0) + ' J'], ['Pensionsjahr', yr + jbp_preview]] as [l, v]}
                  <div>
                    <div class="ey mb-[6px]">{l}</div>
                    <div class="stat text-2xl">{v}</div>
                  </div>
                {/each}
              </div>
            </div>

          <!-- STEP 5: KV -->
          {:else if step === 5}
            <div class="flex flex-col gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Krankenversicherung im Ruhestand</label>
                <div class="seg segf">
                  {#each [['GKV','Gesetzlich (GKV)'],['PKV','Privat (PKV)']] as [val, lab]}
                    <button class:on={P.kv === val} on:click={() => P.kv = val}>{lab}</button>
                  {/each}
                </div>
              </div>
              {#if P.kv === 'PKV'}
                <div class="grid grid-cols-2 gap-5">
                  <div class="flex flex-col gap-2">
                    <label class="lbl">PKV-Beitrag</label>
                    <div class="sfx"><input type="number" step="1" bind:value={P.kvB} /><span class="sfxt">€/Mo.</span></div>
                  </div>
                  <div class="flex flex-col gap-2">
                    <label class="lbl">Beihilfesatz im Ruhestand</label>
                    <span class="hint mb-1">Beamte: typisch 70 %</span>
                    <div class="seg segf">
                      {#each [50,60,70,80] as p}
                        <button class:on={P.beihilfe === p} on:click={() => P.beihilfe = p}>{p} %</button>
                      {/each}
                    </div>
                  </div>
                </div>
              {:else}
                <div class="card" style="background:var(--bg2)">
                  <p class="text-[14px] text-fg2 leading-[1.6]">GKV-Rentner zahlen ~8,3 % der Bruttopension als KV-Beitrag + 3,4 % Pflegeversicherung.</p>
                </div>
              {/if}
            </div>

          <!-- STEP 6: Ziel -->
          {:else if step === 6}
            <div class="flex flex-col gap-5">
              <div class="flex flex-col gap-2">
                <label class="lbl">Mit wie viel Netto-Monatsbetrag kannst du deinen Lebensstil halten?</label>
                <div class="sfx text-xl">
                  <input type="number" step="50" bind:value={P.zielEur} class="text-xl font-medium" />
                  <span class="sfxt text-[15px]">€ / Monat netto</span>
                </div>
                <span class="hint">Tipp: Miete + Essen + Freizeit + Rücklagen monatlich</span>
              </div>
              <div class="flex flex-col gap-2">
                <label class="lbl">Bestehende monatliche Vorsorge</label>
                <div class="sfx"><input type="number" step="1" bind:value={P.vorsorge} /><span class="sfxt">€/Mo.</span></div>
                <span class="hint">Rürup, Riester, ETF-Sparplan …</span>
              </div>
              {#if result}
                <div class="card" style="border-color:rgba(255,107,107,.25)">
                  <div class="ey mb-[10px]" style="color:var(--loss)">Vorschau Versorgungslücke</div>
                  <div class="stat text-[52px]" style="color:{result.luecke > 0 ? 'var(--loss)' : 'var(--fg)'}">
                    {result.luecke > 0 ? '−' + de0.format(Math.round(result.luecke)) + ' €/Mo.' : '✓ Gedeckt'}
                  </div>
                  <div class="text-xs text-fg3 font-mono mt-2">
                    Ziel: {fmtE(P.zielEur)} · Netto: {result ? fmtE(result.netto) : '–'} · Brutto: {result ? fmtE(result.brutto) : '–'}
                  </div>
                </div>
              {/if}
            </div>
          {/if}
        </div>

        <CalcNavButtons
          {step} labels={PS_LABELS} calcLabel="Pension berechnen →" withStepName={true}
          on:back={back} on:next={next}
        />
      </div>

      <!-- Sidebar -->
      <aside class="calc-sidebar">
        <div class="ey mb-[14px]">Zwischenstand</div>
        <div class="flex items-baseline gap-2">
          <span class="stat text-[52px]">{result ? de0.format(Math.round(result.netto)) : '–'}</span>
          <span class="text-fg2"> €</span>
        </div>
        <div class="text-fg3 text-[11px] font-mono mt-[6px] uppercase tracking-[.08em]">Netto / Monat · vorläufig</div>
        {#if result}
          <div class="mt-4 h-[6px] rounded-full overflow-hidden" style="background:var(--bg3)">
            <div class="h-full rounded-full" style="background:var(--fg);width:{Math.min(result.brutto > 0 ? result.netto / result.brutto * 100 : 0, 100).toFixed(1)}%;transition:width .4s"></div>
          </div>
          <div class="flex justify-between mt-2 text-[11px] text-fg3 font-mono">
            <span>{(result.brutto > 0 ? result.netto / result.brutto * 100 : 0).toFixed(1).replace('.', ',')} % v. Brutto</span>
            <span>Ziel: 80 %</span>
          </div>
          <div class="mt-5 pt-4 text-[13px]" style="border-top:1px solid var(--line)">
            <div class="calc-sidebar-row">
              <span class="text-fg3">Versorgungsziel</span>
              <span class="font-mono">{fmtE(P.zielEur)}</span>
            </div>
            <div class="flex items-center justify-between py-2 text-[13px]">
              <span class="text-fg3">Lücke</span>
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
