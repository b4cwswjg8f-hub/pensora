<script>
  import { createEventDispatcher } from 'svelte';
  import Logo from '../components/Logo.svelte';
  import Stepper from '../components/Stepper.svelte';
  import CashflowResult from './CashflowResult.svelte';
  import { defaultC, calcC, CS_LABELS } from '../lib/calcs.js';
  import { fmtE, de0 } from '../lib/utils.js';

  const dispatch = createEventDispatcher();
  let C = defaultC();
  let step = 0;
  let showResult = false;

  $: result = (() => { try { return calcC(C); } catch(e) { return null; } })();
  $: s = CS_LABELS[step];
  $: pct = Math.round(step / CS_LABELS.length * 100);

  function next() {
    if (step < CS_LABELS.length - 1) { step++; window.scrollTo(0,0); }
    else { showResult = true; window.scrollTo(0,0); }
  }
  function back() { if (step > 0) { step--; window.scrollTo(0,0); } }
</script>

{#if showResult}
  <CashflowResult {C} {result}
    on:back={() => { showResult = false; step = 0; C = defaultC(); dispatch('back'); }}
    on:recalc={() => { showResult = false; step = 0; }}
    on:navigate={e => dispatch('navigate', e.detail)}
  />
{:else}
<div>
  <nav class="nav">
    <div class="row g16">
      <button class="brand" on:click={() => dispatch('back')}><Logo /> Pensora</button>
      <span style="color:var(--line2);font-size:16px">/</span>
      <span style="color:var(--fg2);font-size:14px">Cashflow-Rechner</span>
    </div>
    <div class="row g8"><button class="btn btng" on:click={() => dispatch('back')}>← Hub</button></div>
  </nav>

  <div class="calc-stepper">
    <div class="row" style="justify-content:space-between;margin-bottom:10px">
      <div class="row g12">
        <span style="font-family:var(--mono);font-size:12px;color:var(--fg3);letter-spacing:.08em;text-transform:uppercase">Schritt {String(step+1).padStart(2,'0')} · {String(CS_LABELS.length).padStart(2,'0')}</span>
        <span style="font-size:15px;font-weight:500">{s.label}</span>
      </div>
      <span style="font-family:var(--mono);font-size:13px">{pct} %</span>
    </div>
    <Stepper total={CS_LABELS.length} current={step} />
  </div>

  <div class="fbody">
    <div class="calc-layout">
      <div class="calc-form">
        <div class="ey">{s.ey}</div>
        <h2 style="font-size:36px;font-weight:500;letter-spacing:-.03em;max-width:700px;margin-top:12px;line-height:1.1">{s.title}</h2>
        <p style="font-size:15px;color:var(--fg2);margin-top:12px;max-width:600px">{s.desc}</p>
        <div style="margin-top:28px">

          {#if step === 0}
            <div class="col g20">
              <div class="col g8">
                <label class="lbl">Monatliches Nettoeinkommen</label>
                <div class="sfx" style="font-size:20px">
                  <input type="number" step="50" bind:value={C.netto} style="font-size:20px;font-weight:500" />
                  <span class="sfxt" style="font-size:15px">€ / Monat</span>
                </div>
              </div>
              {#if result}
                <div class="card" style="background:var(--bg2)">
                  <div class="ey" style="margin-bottom:10px">50/15/15-Faustregel (Richtwerte)</div>
                  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:8px">
                    {#each [['Fixkosten (50 %)',result.emp_fix],['Vorsorge (15 %)',result.emp_av],['Freizeit (15 %)',result.emp_frei]] as [l,v]}
                      <div>
                        <div style="font-size:10px;color:var(--fg3);font-family:var(--mono);text-transform:uppercase;letter-spacing:.06em">{l}</div>
                        <div style="font-size:20px;font-weight:500;font-family:var(--mono);margin-top:4px">{fmtE(v)}</div>
                      </div>
                    {/each}
                  </div>
                </div>
              {/if}
            </div>

          {:else if step === 1}
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
              <div>
                <div style="font-size:11px;color:var(--fg3);font-family:var(--mono);text-transform:uppercase;letter-spacing:.08em;margin-bottom:12px">Fixkosten</div>
                <div class="col g12">
                  {#each [['Warmmiete / Grundmiete','miete','€/Mo.',50],['Nebenkosten / Strom / Gas','nk','€/Mo.',10],['Lebensmittel','lm','€/Mo.',25],['Transport (ÖPNV / Tanken)','transport','€/Mo.',10],['Kommunikation (Handy, Internet)','komm','€/Mo.',5]] as [l,k,sfx,stp]}
                    <div class="col g8">
                      <label class="lbl" style="font-size:11px">{l}</label>
                      <div class="sfx"><input type="number" step={stp} bind:value={C[k]} /><span class="sfxt">{sfx}</span></div>
                    </div>
                  {/each}
                </div>
              </div>
              <div>
                <div style="font-size:11px;color:var(--fg3);font-family:var(--mono);text-transform:uppercase;letter-spacing:.08em;margin-bottom:12px">Variable Kosten</div>
                <div class="col g12">
                  {#each [['Versicherungen gesamt','versich','€/Mo.',10],['Altersvorsorge (Sparen/ETF)','av','€/Mo.',25],['Freizeit & Hobbys','frei','€/Mo.',25],['Sonstiges','sonst','€/Mo.',10]] as [l,k,sfx,stp]}
                    <div class="col g8">
                      <label class="lbl" style="font-size:11px">{l}</label>
                      <div class="sfx"><input type="number" step={stp} bind:value={C[k]} /><span class="sfxt">{sfx}</span></div>
                    </div>
                  {/each}
                </div>
                {#if result}
                  <div class="card mt20" style="background:var(--bg2)">
                    <div class="ey" style="margin-bottom:6px">Frei verfügbar</div>
                    <div class="stat" style="font-size:32px;color:{result.frei > 0 ? 'var(--fg)' : 'var(--loss)'}">{fmtE(result.frei)}/Mo.</div>
                    <div style="font-size:11px;color:var(--fg3);font-family:var(--mono);margin-top:6px">
                      Ausgaben: {fmtE(result.out)} von {fmtE(C.netto)}
                    </div>
                  </div>
                {/if}
              </div>
            </div>
          {/if}
        </div>

        <div class="row" style="justify-content:space-between;margin-top:36px;padding-top:20px;border-top:1px solid var(--line)">
          <button class="btn btnlg" on:click={back} style="opacity:{step===0?0.3:1};pointer-events:{step===0?'none':'auto'}">← Zurück</button>
          <div class="row g12">
            <button class="btn btng" on:click={next}>Überspringen</button>
            <button class="btn btnp btnlg" on:click={next}>
              {step === CS_LABELS.length - 1 ? 'Cashflow analysieren →' : 'Weiter →'}
            </button>
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <aside style="border-left:1px solid var(--line);padding:36px 28px;background:var(--bg1)">
        <div class="ey" style="margin-bottom:14px">Frei verfügbar</div>
        <div class="stat" style="font-size:40px;color:{result && result.frei > 0 ? 'var(--fg)' : 'var(--loss)'}">
          {result ? fmtE(result.frei) + '/Mo.' : '–'}
        </div>
        <div style="color:var(--fg3);font-size:11px;font-family:var(--mono);margin-top:6px;text-transform:uppercase;letter-spacing:.08em">nach allen Ausgaben</div>
        {#if result}
          <div style="margin-top:16px;padding-top:16px;border-top:1px solid var(--line);font-size:13px">
            <div class="row" style="justify-content:space-between;padding:8px 0">
              <span style="color:var(--fg3)">Notgroschen (3 Mo.)</span>
              <span style="font-family:var(--mono)">{fmtE(result.notg)}</span>
            </div>
            <div class="row" style="justify-content:space-between;padding:8px 0">
              <span style="color:var(--fg3)">Ausgaben gesamt</span>
              <span style="font-family:var(--mono)">{fmtE(result.out)}</span>
            </div>
          </div>
        {/if}
      </aside>
    </div>
  </div>
</div>
{/if}
