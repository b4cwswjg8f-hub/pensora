<script>
  import { createEventDispatcher } from 'svelte';
  import Logo from '../components/Logo.svelte';
  import Stepper from '../components/Stepper.svelte';
  import PensionResult from './PensionResult.svelte';
  import { defaultP, calcP, PS_LABELS, LAENDER, BESO, BESO_KEYS, getBeso } from '../lib/calcs.js';
  import { fmtE, fmtP, de0 } from '../lib/utils.js';

  const dispatch = createEventDispatcher();

  let P = defaultP();
  let step = 0;
  let showResult = false;

  $: result = (() => { try { return calcP(P); } catch(e) { return null; } })();
  $: s = PS_LABELS[step];
  $: pct = Math.round(step / PS_LABELS.length * 100);
  $: aktB_preview = de0.format(getBeso(P.bGr, parseInt(P.bSt)) + (P.zusatz || 0)) + ' €';
  $: yr = new Date().getFullYear();
  $: alter_preview = yr - (parseInt((P.gebdat || '').split('.')[2]) || 1986);
  $: jbp_preview = Math.max(P.pensAlter - alter_preview, 0);

  function next() {
    if (step < PS_LABELS.length - 1) { step++; window.scrollTo(0,0); }
    else { showResult = true; window.scrollTo(0,0); }
  }
  function back() {
    if (step > 0) { step--; window.scrollTo(0,0); }
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
  <!-- Nav -->
  <nav class="nav">
    <div class="row g16">
      <button class="brand" on:click={() => dispatch('back')}><Logo /> Pensora</button>
      <span style="color:var(--line2);font-size:16px">/</span>
      <span style="color:var(--fg2);font-size:14px">Pensionsrechner</span>
    </div>
    <div class="row g8">
      <button class="btn btng" on:click={() => dispatch('back')}>← Hub</button>
    </div>
  </nav>

  <!-- Progress bar -->
  <div class="calc-stepper">
    <div class="row" style="justify-content:space-between;margin-bottom:10px">
      <div class="row g12">
        <span style="font-family:var(--mono);font-size:12px;color:var(--fg3);letter-spacing:.08em;text-transform:uppercase">
          Schritt {String(step + 1).padStart(2, '0')} · {String(PS_LABELS.length).padStart(2, '0')}
        </span>
        <span style="font-size:15px;font-weight:500">{s.label}</span>
      </div>
      <span style="font-family:var(--mono);font-size:13px">{pct} %</span>
    </div>
    <Stepper total={PS_LABELS.length} current={step} />
  </div>

  <!-- Body -->
  <div class="fbody">
    <div class="calc-layout">
      <!-- Main form -->
      <div class="calc-form">
        <div class="ey">{s.ey}</div>
        <h2 style="font-size:36px;font-weight:500;letter-spacing:-.03em;max-width:700px;margin-top:12px;line-height:1.1">{s.title}</h2>
        <p style="font-size:15px;color:var(--fg2);margin-top:12px;max-width:600px">{s.desc}</p>

        <div style="margin-top:28px">
          <!-- STEP 0: Stammdaten -->
          {#if step === 0}
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px">
              <div class="col g8">
                <label class="lbl">Geburtsdatum</label>
                <input class="inp" type="text" bind:value={P.gebdat} placeholder="TT.MM.JJJJ" />
                <span class="hint">TT.MM.JJJJ</span>
              </div>
              <div class="col g8">
                <label class="lbl">Diensteintritt</label>
                <input class="inp" type="text" bind:value={P.dienst} placeholder="TT.MM.JJJJ" />
                <span class="hint">TT.MM.JJJJ</span>
              </div>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
              <div class="col g8">
                <label class="lbl">Bundesland</label>
                <div class="sw">
                  <select class="sel" bind:value={P.bund}>
                    {#each LAENDER as l}<option value={l}>{l}</option>{/each}
                  </select>
                </div>
              </div>
              <div class="col g8">
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
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px">
              <div class="col g8">
                <label class="lbl">Besoldungsgruppe</label>
                <div class="sw">
                  <select class="sel" bind:value={P.bGr}>
                    {#each BESO_KEYS as k}<option value={k}>{k}</option>{/each}
                  </select>
                </div>
              </div>
              <div class="col g8">
                <label class="lbl">Erfahrungsstufe</label>
                <div class="sw">
                  <select class="sel" bind:value={P.bSt}>
                    {#each [1,2,3,4,5,6,7,8,9,10,11,12] as s}
                      <option value={String(s)}>{s}</option>
                    {/each}
                  </select>
                </div>
              </div>
              <div class="col g8">
                <label class="lbl">Zus. Zulagen</label>
                <div class="sfx">
                  <input type="number" step="1" bind:value={P.zusatz} />
                  <span class="sfxt">€/Mo.</span>
                </div>
                <span class="hint">z.B. Funktionszulage</span>
              </div>
            </div>
            <div class="card mt20" style="background:var(--bg2)">
              <div class="ey" style="margin-bottom:10px">Bruttogehalt (Schätzung BW 2025)</div>
              <div class="stat" style="font-size:40px">{aktB_preview}</div>
            </div>

          <!-- STEP 2: Perspektive -->
          {:else if step === 2}
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px">
              <div class="col g8">
                <label class="lbl">Besoldungsgruppe Ziel</label>
                <div class="sw">
                  <select class="sel" bind:value={P.pGr}>
                    {#each BESO_KEYS as k}<option value={k}>{k}</option>{/each}
                  </select>
                </div>
              </div>
              <div class="col g8">
                <label class="lbl">Erfahrungsstufe Ziel</label>
                <div class="sw">
                  <select class="sel" bind:value={P.pSt}>
                    {#each [1,2,3,4,5,6,7,8,9,10,11,12] as s}
                      <option value={String(s)}>{s}</option>
                    {/each}
                  </select>
                </div>
              </div>
              <div class="col g8">
                <label class="lbl">Zus. Zulagen Ziel</label>
                <div class="sfx">
                  <input type="number" step="1" bind:value={P.pZusatz} />
                  <span class="sfxt">€/Mo.</span>
                </div>
              </div>
            </div>

          <!-- STEP 3: Zeiterfassung -->
          {:else if step === 3}
            <div class="col g16">
              <!-- Elternzeit -->
              <div class="card">
                <div class="row" style="justify-content:space-between;align-items:flex-start;gap:24px">
                  <div>
                    <h3 style="font-size:16px;font-weight:600;margin-bottom:6px">Elternzeit</h3>
                    <p style="font-size:13px;color:var(--fg2)">Teilweise als Dienstzeit anerkannt (§ 12a BeamtVG).</p>
                  </div>
                  <div class="row g12">
                    <div class="tog" class:on={P.eltern} on:click={() => P.eltern = !P.eltern}></div>
                    <span style="font-size:14px;color:var(--fg2)">{P.eltern ? 'Erfasst' : 'Nicht relevant'}</span>
                  </div>
                </div>
                {#if P.eltern}
                  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px">
                    <div class="col g8">
                      <label class="lbl">Gesamtdauer</label>
                      <div class="sfx"><input type="number" step="0.5" bind:value={P.elternJ} /><span class="sfxt">Jahre</span></div>
                    </div>
                    <div class="col g8">
                      <label class="lbl">Zeitraum (ca.)</label>
                      <input class="inp" type="text" placeholder="z.B. 2014–2016" />
                    </div>
                  </div>
                {/if}
              </div>
              <!-- Beurlaubung -->
              <div class="card">
                <div class="row" style="justify-content:space-between;align-items:flex-start;gap:24px">
                  <div>
                    <h3 style="font-size:16px;font-weight:600;margin-bottom:6px">Beurlaubung</h3>
                    <p style="font-size:13px;color:var(--fg2)">Zählt nicht als Dienstzeit (§ 9 BeamtVG).</p>
                  </div>
                  <div class="row g12">
                    <div class="tog" class:on={P.beurl} on:click={() => P.beurl = !P.beurl}></div>
                    <span style="font-size:14px;color:var(--fg2)">{P.beurl ? 'Erfasst' : 'Nicht relevant'}</span>
                  </div>
                </div>
                {#if P.beurl}
                  <div style="margin-top:16px">
                    <div class="sfx"><input type="number" step="0.5" bind:value={P.beurlJ} /><span class="sfxt">Jahre</span></div>
                  </div>
                {/if}
              </div>
              <!-- Teilzeit -->
              <div class="card">
                <div class="row" style="justify-content:space-between;align-items:flex-start;gap:24px">
                  <div>
                    <h3 style="font-size:16px;font-weight:600;margin-bottom:6px">Teilzeit</h3>
                    <p style="font-size:13px;color:var(--fg2)">Reduziert Ruhegehaltssatz (§ 6 Abs. 1 BeamtVG).</p>
                  </div>
                  <div class="row g12">
                    <div class="tog" class:on={P.tz} on:click={() => P.tz = !P.tz}></div>
                    <span style="font-size:14px;color:var(--fg2)">{P.tz ? 'Erfasst' : 'Nicht relevant'}</span>
                  </div>
                </div>
                {#if P.tz}
                  <div style="display:grid;grid-template-columns:1fr 2fr;gap:12px;margin-top:16px">
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
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px">
              <div class="col g8">
                <label class="lbl">Pensionseintrittsalter</label>
                <input class="inp" type="number" min="55" max="70" bind:value={P.pensAlter} />
                <span class="hint">Regelgrenze: 67 Jahre</span>
              </div>
              <div class="col g8">
                <label class="lbl">Lebenserwartung</label>
                <input class="inp" type="number" min="70" max="100" bind:value={P.lebErw} />
                <span class="hint">Statistisch: 84–88 Jahre</span>
              </div>
              <div class="col g8">
                <label class="lbl">Besoldungssteigerung p.a.</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={P.steigerung} /><span class="sfxt">% p.a.</span></div>
                <span class="hint">Ø: 1,5–2,0 %</span>
              </div>
            </div>
            <div class="card mt20">
              <div class="ey" style="margin-bottom:16px">Auf dieser Basis</div>
              <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:20px">
                {#each [['Alter heute', alter_preview + ' J'], ['Bis Pension', jbp_preview + ' J'], ['Im Ruhestand', Math.max(P.lebErw - P.pensAlter, 0) + ' J'], ['Pensionsjahr', yr + jbp_preview]] as [l,v]}
                  <div>
                    <div class="ey" style="margin-bottom:6px">{l}</div>
                    <div class="stat" style="font-size:24px">{v}</div>
                  </div>
                {/each}
              </div>
            </div>

          <!-- STEP 5: KV -->
          {:else if step === 5}
            <div class="col g20">
              <div class="col g8">
                <label class="lbl">Krankenversicherung im Ruhestand</label>
                <div class="seg segf">
                  {#each [['GKV','Gesetzlich (GKV)'],['PKV','Privat (PKV)']] as [val,lab]}
                    <button class:on={P.kv === val} on:click={() => P.kv = val}>{lab}</button>
                  {/each}
                </div>
              </div>
              {#if P.kv === 'PKV'}
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
                  <div class="col g8">
                    <label class="lbl">PKV-Beitrag</label>
                    <div class="sfx"><input type="number" step="1" bind:value={P.kvB} /><span class="sfxt">€/Mo.</span></div>
                  </div>
                  <div class="col g8">
                    <label class="lbl">Beihilfesatz im Ruhestand</label>
                    <span class="hint" style="margin-bottom:4px">Beamte: typisch 70 %</span>
                    <div class="seg segf">
                      {#each [50,60,70,80] as p}
                        <button class:on={P.beihilfe === p} on:click={() => P.beihilfe = p}>{p} %</button>
                      {/each}
                    </div>
                  </div>
                </div>
              {:else}
                <div class="card" style="background:var(--bg2)">
                  <p style="font-size:14px;color:var(--fg2);line-height:1.6">GKV-Rentner zahlen ~8,3 % der Bruttopension als KV-Beitrag + 3,4 % Pflegeversicherung.</p>
                </div>
              {/if}
            </div>

          <!-- STEP 6: Ziel -->
          {:else if step === 6}
            <div class="col g20">
              <div class="col g8">
                <label class="lbl">Mit wie viel Netto-Monatsbetrag kannst du deinen Lebensstil halten?</label>
                <div class="sfx" style="font-size:20px">
                  <input type="number" step="50" bind:value={P.zielEur} style="font-size:20px;font-weight:500" />
                  <span class="sfxt" style="font-size:15px">€ / Monat netto</span>
                </div>
                <span class="hint">Tipp: Miete + Essen + Freizeit + Rücklagen monatlich</span>
              </div>
              <div class="col g8">
                <label class="lbl">Bestehende monatliche Vorsorge</label>
                <div class="sfx"><input type="number" step="1" bind:value={P.vorsorge} /><span class="sfxt">€/Mo.</span></div>
                <span class="hint">Rürup, Riester, ETF-Sparplan …</span>
              </div>
              {#if result}
                <div class="card" style="border-color:rgba(255,107,107,.25)">
                  <div class="ey" style="color:var(--loss);margin-bottom:10px">Vorschau Versorgungslücke</div>
                  <div class="stat" style="font-size:52px;color:{result.luecke > 0 ? 'var(--loss)' : 'var(--fg)'}">
                    {result.luecke > 0 ? '−' + de0.format(Math.round(result.luecke)) + ' €/Mo.' : '✓ Gedeckt'}
                  </div>
                  <div style="font-size:12px;color:var(--fg3);font-family:var(--mono);margin-top:8px">
                    Ziel: {fmtE(P.zielEur)} · Netto: {result ? fmtE(result.netto) : '–'} · Brutto: {result ? fmtE(result.brutto) : '–'}
                  </div>
                </div>
              {/if}
            </div>
          {/if}
        </div>

        <!-- Navigation buttons -->
        <div class="row" style="justify-content:space-between;margin-top:36px;padding-top:20px;border-top:1px solid var(--line)">
          <button class="btn btnlg" on:click={back} style="opacity:{step === 0 ? 0.3 : 1};pointer-events:{step === 0 ? 'none' : 'auto'}">← Zurück</button>
          <div class="row g12">
            <button class="btn btng" on:click={next}>Überspringen</button>
            <button class="btn btnp btnlg" on:click={next}>
              {step === PS_LABELS.length - 1 ? 'Pension berechnen →' : 'Weiter zu ' + PS_LABELS[Math.min(step + 1, PS_LABELS.length - 1)].label + ' →'}
            </button>
          </div>
        </div>
      </div>

      <!-- Sidebar preview -->
      <aside style="border-left:1px solid var(--line);padding:36px 28px;background:var(--bg1)">
        <div class="ey" style="margin-bottom:14px">Zwischenstand</div>
        <div class="row g8" style="align-items:baseline">
          <span class="stat" style="font-size:52px">{result ? de0.format(Math.round(result.netto)) : '–'}</span>
          <span style="color:var(--fg2)"> €</span>
        </div>
        <div style="color:var(--fg3);font-size:11px;font-family:var(--mono);margin-top:6px;text-transform:uppercase;letter-spacing:.08em">Netto / Monat · vorläufig</div>
        {#if result}
          <div style="margin-top:16px;height:6px;border-radius:999px;background:var(--bg3);overflow:hidden">
            <div style="height:100%;background:var(--fg);width:{Math.min(result.brutto > 0 ? result.netto / result.brutto * 100 : 0, 100).toFixed(1)}%;transition:width .4s"></div>
          </div>
          <div class="row" style="justify-content:space-between;margin-top:8px;font-size:11px;color:var(--fg3);font-family:var(--mono)">
            <span>{(result.brutto > 0 ? result.netto / result.brutto * 100 : 0).toFixed(1).replace('.', ',')} % v. Brutto</span>
            <span>Ziel: 80 %</span>
          </div>
          <div style="margin-top:20px;padding-top:16px;border-top:1px solid var(--line);font-size:13px">
            <div class="row" style="justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--line)">
              <span style="color:var(--fg3)">Versorgungsziel</span>
              <span style="font-family:var(--mono)">{fmtE(P.zielEur)}</span>
            </div>
            <div class="row" style="justify-content:space-between;padding:8px 0">
              <span style="color:var(--fg3)">Lücke</span>
              <span style="font-family:var(--mono);color:{result.luecke > 0 ? 'var(--loss)' : 'var(--fg)'}">
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
