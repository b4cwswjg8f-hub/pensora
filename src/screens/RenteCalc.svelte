<script>
  import { createEventDispatcher } from 'svelte';
  import Logo from '../components/Logo.svelte';
  import Stepper from '../components/Stepper.svelte';
  import RenteResult from './RenteResult.svelte';
  import { defaultR, calcR, RS_LABELS, GRV } from '../lib/calcs.js';
  import { fmtE, de0 } from '../lib/utils.js';

  const dispatch = createEventDispatcher();
  let R = defaultR();
  let step = 0;
  let showResult = false;

  $: result = (() => { try { return calcR(R); } catch(e) { return null; } })();
  $: s = RS_LABELS[step];
  $: pct = Math.round(step / RS_LABELS.length * 100);
  $: ep_preview = (Math.min(R.brutto, GRV.bbg) / GRV.de).toFixed(3).replace('.', ',') + ' EP/Jahr';

  function next() {
    if (step < RS_LABELS.length - 1) { step++; window.scrollTo(0,0); }
    else { showResult = true; window.scrollTo(0,0); }
  }
  function back() { if (step > 0) { step--; window.scrollTo(0,0); } }
</script>

{#if showResult}
  <RenteResult {R} {result}
    on:back={() => { showResult = false; step = 0; R = defaultR(); dispatch('back'); }}
    on:recalc={() => { showResult = false; step = 0; }}
    on:navigate={e => dispatch('navigate', e.detail)}
  />
{:else}
<div>
  <nav class="nav">
    <div class="row g16">
      <button class="brand" on:click={() => dispatch('back')}><Logo /> Pensora</button>
      <span style="color:var(--line2);font-size:16px">/</span>
      <span style="color:var(--fg2);font-size:14px">Rentenrechner</span>
    </div>
    <div class="row g8"><button class="btn btng" on:click={() => dispatch('back')}>← Hub</button></div>
  </nav>

  <div style="padding:16px 56px 10px;border-bottom:1px solid var(--line)">
    <div class="row" style="justify-content:space-between;margin-bottom:10px">
      <div class="row g12">
        <span style="font-family:var(--mono);font-size:12px;color:var(--fg3);letter-spacing:.08em;text-transform:uppercase">Schritt {String(step+1).padStart(2,'0')} · {String(RS_LABELS.length).padStart(2,'0')}</span>
        <span style="font-size:15px;font-weight:500">{s.label}</span>
      </div>
      <span style="font-family:var(--mono);font-size:13px">{pct} %</span>
    </div>
    <Stepper total={RS_LABELS.length} current={step} />
  </div>

  <div class="fbody">
    <div style="display:grid;grid-template-columns:1fr 320px">
      <div style="padding:36px 56px">
        <div class="ey">{s.ey}</div>
        <h2 style="font-size:36px;font-weight:500;letter-spacing:-.03em;max-width:700px;margin-top:12px;line-height:1.1">{s.title}</h2>
        <p style="font-size:15px;color:var(--fg2);margin-top:12px;max-width:600px">{s.desc}</p>
        <div style="margin-top:28px">

          {#if step === 0}
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px">
              <div class="col g8">
                <label class="lbl">Geburtsdatum</label>
                <input class="inp" type="text" bind:value={R.gebdat} placeholder="TT.MM.JJJJ" />
              </div>
              <div class="col g8">
                <label class="lbl">Renteneintrittsalter</label>
                <input class="inp" type="number" min="60" max="70" bind:value={R.rentAlter} />
                <span class="hint">Regelaltersgrenze: 67 J.</span>
              </div>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
              <div class="col g8">
                <label class="lbl">Erwerbsbeginn (Jahr)</label>
                <input class="inp" type="number" min="1970" max="2025" bind:value={R.djBeginn} />
                <span class="hint">Ab wann GRV-Beiträge?</span>
              </div>
              <div class="col g8">
                <label class="lbl">Kirchensteuerpflichtig?</label>
                <div class="seg segf">
                  {#each ['Ja','Nein'] as opt}
                    <button class:on={R.kirche === opt} on:click={() => R.kirche = opt}>{opt}</button>
                  {/each}
                </div>
              </div>
            </div>

          {:else if step === 1}
            <div class="col g20">
              <div class="col g8">
                <label class="lbl">Bruttojahresgehalt</label>
                <div class="sfx"><input type="number" step="1000" bind:value={R.brutto} /><span class="sfxt">€/Jahr</span></div>
                <span class="hint">Basis für Entgeltpunkte (§ 70 SGB VI) · BBG 2025: 96.600 €/J.</span>
              </div>
              <div class="col g8">
                <label class="lbl">Jährl. Gehaltswachstum</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={R.wachstum} /><span class="sfxt">% p.a.</span></div>
                <span class="hint">Vereinfachung: konstante Rate</span>
              </div>
              <div class="card" style="background:var(--bg2)">
                <div class="ey" style="margin-bottom:10px">Entgeltpunkte / Jahr (aktuell)</div>
                <div class="stat" style="font-size:40px">{ep_preview}</div>
                <div style="font-size:12px;color:var(--fg3);font-family:var(--mono);margin-top:8px">Rentenwert 2025: 40,79 € · DE 2025: 50.493 €/J.</div>
              </div>
            </div>

          {:else if step === 2}
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:16px">
              <div class="col g8">
                <label class="lbl">Rentenanpassung p.a.</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={R.ra} /><span class="sfxt">% p.a.</span></div>
                <span class="hint">Ø: ~1,8 % · 2026: +4,24 %</span>
              </div>
              <div class="col g8">
                <label class="lbl">Inflation p.a.</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={R.inf} /><span class="sfxt">% p.a.</span></div>
                <span class="hint">Aktuell: ~2,1 %</span>
              </div>
            </div>
            <div class="col g8">
              <label class="lbl">Lebenserwartung</label>
              <input class="inp" type="number" min="70" max="100" bind:value={R.lebErw} />
              <span class="hint">Statistisch: 84–88 Jahre</span>
            </div>

          {:else if step === 3}
            <div class="col g20">
              <div class="col g8">
                <label class="lbl">Gewünschtes Netto-Monatseinkommen im Ruhestand</label>
                <div class="sfx" style="font-size:20px">
                  <input type="number" step="50" bind:value={R.zielEur} style="font-size:20px;font-weight:500" />
                  <span class="sfxt" style="font-size:15px">€ / Monat netto</span>
                </div>
              </div>
              <div class="col g8">
                <label class="lbl">Bestehende Vorsorge (monatlich)</label>
                <div class="sfx"><input type="number" step="1" bind:value={R.vorsorge} /><span class="sfxt">€/Mo.</span></div>
                <span class="hint">Riester, bAV, ETF …</span>
              </div>
              {#if result}
                <div class="card" style="border-color:rgba(255,107,107,.25)">
                  <div class="ey" style="color:var(--loss);margin-bottom:10px">Rentenlücke Vorschau</div>
                  <div class="stat" style="font-size:48px;color:{result.luecke > 0 ? 'var(--loss)' : 'var(--fg)'}">
                    {result.luecke > 0 ? '−' + de0.format(Math.round(result.luecke)) + ' €/Mo.' : '✓ Gedeckt'}
                  </div>
                  <div style="font-size:12px;color:var(--fg3);font-family:var(--mono);margin-top:8px">
                    Brutto: {fmtE(result.brutto)} · Netto: {fmtE(result.netto)} · Ziel: {fmtE(R.zielEur)}
                  </div>
                </div>
              {/if}
            </div>
          {/if}
        </div>

        <div class="row" style="justify-content:space-between;margin-top:36px;padding-top:20px;border-top:1px solid var(--line)">
          <button class="btn btnlg" on:click={back} style="opacity:{step===0?0.3:1};pointer-events:{step===0?'none':'auto'}">← Zurück</button>
          <div class="row g12">
            <button class="btn btng" on:click={next}>Überspringen</button>
            <button class="btn btnp btnlg" on:click={next}>
              {step === RS_LABELS.length - 1 ? 'Rente berechnen →' : 'Weiter →'}
            </button>
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <aside style="border-left:1px solid var(--line);padding:36px 28px;background:var(--bg1)">
        <div class="ey" style="margin-bottom:14px">Rentenvorschau</div>
        <div class="row g8" style="align-items:baseline">
          <span class="stat" style="font-size:52px">{result ? de0.format(Math.round(result.netto)) : '–'}</span>
          <span style="color:var(--fg2)"> €</span>
        </div>
        <div style="color:var(--fg3);font-size:11px;font-family:var(--mono);margin-top:6px;text-transform:uppercase;letter-spacing:.08em">Nettorente / Monat</div>
        {#if result}
          <div style="margin-top:20px;padding-top:16px;border-top:1px solid var(--line);font-size:13px">
            <div class="row" style="justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--line)">
              <span style="color:var(--fg3)">Entgeltpunkte</span>
              <span style="font-family:var(--mono)">{result.gesEP.toFixed(1).replace('.', ',')} EP</span>
            </div>
            <div class="row" style="justify-content:space-between;padding:8px 0">
              <span style="color:var(--fg3)">Rentenlücke</span>
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
