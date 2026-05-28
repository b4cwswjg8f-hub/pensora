<script>
  import { createEventDispatcher } from 'svelte';
  import Logo from '../components/Logo.svelte';
  import Stepper from '../components/Stepper.svelte';
  import RuerupResult from './RuerupResult.svelte';
  import { defaultRu, calcRu, RUS_LABELS } from '../lib/calcs.js';
  import { fmtE, de0 } from '../lib/utils.js';

  const dispatch = createEventDispatcher();
  let Ru = defaultRu();
  let step = 0;
  let showResult = false;

  $: result = (() => { try { return calcRu(Ru); } catch(e) { return null; } })();
  $: s = RUS_LABELS[step];
  $: pct = Math.round(step / RUS_LABELS.length * 100);

  function next() {
    if (step < RUS_LABELS.length - 1) { step++; window.scrollTo(0,0); }
    else { showResult = true; window.scrollTo(0,0); }
  }
  function back() { if (step > 0) { step--; window.scrollTo(0,0); } }
</script>

{#if showResult}
  <RuerupResult {Ru} {result}
    on:back={() => { showResult = false; step = 0; Ru = defaultRu(); dispatch('back'); }}
    on:recalc={() => { showResult = false; step = 0; }}
    on:navigate={e => dispatch('navigate', e.detail)}
  />
{:else}
<div>
  <nav class="nav">
    <div class="row g16">
      <button class="brand" on:click={() => dispatch('back')}><Logo /> Pensora</button>
      <span style="color:var(--line2);font-size:16px">/</span>
      <span style="color:var(--fg2);font-size:14px">Rürup-Rechner</span>
    </div>
    <div class="row g8"><button class="btn btng" on:click={() => dispatch('back')}>← Hub</button></div>
  </nav>

  <div style="padding:16px 56px 10px;border-bottom:1px solid var(--line)">
    <div class="row" style="justify-content:space-between;margin-bottom:10px">
      <div class="row g12">
        <span style="font-family:var(--mono);font-size:12px;color:var(--fg3);letter-spacing:.08em;text-transform:uppercase">Schritt {String(step+1).padStart(2,'0')} · {String(RUS_LABELS.length).padStart(2,'0')}</span>
        <span style="font-size:15px;font-weight:500">{s.label}</span>
      </div>
      <span style="font-family:var(--mono);font-size:13px">{pct} %</span>
    </div>
    <Stepper total={RUS_LABELS.length} current={step} />
  </div>

  <div class="fbody">
    <div style="display:grid;grid-template-columns:1fr 320px">
      <div style="padding:36px 56px">
        <div class="ey">{s.ey}</div>
        <h2 style="font-size:36px;font-weight:500;letter-spacing:-.03em;max-width:700px;margin-top:12px;line-height:1.1">{s.title}</h2>
        <p style="font-size:15px;color:var(--fg2);margin-top:12px;max-width:600px">{s.desc}</p>
        <div style="margin-top:28px">

          {#if step === 0}
            <div class="col g20">
              <div class="col g8">
                <label class="lbl">Selbstständig?</label>
                <div class="seg segf">
                  {#each ['Ja','Nein'] as opt}
                    <button class:on={Ru.selbst === opt} on:click={() => Ru.selbst = opt}>{opt}</button>
                  {/each}
                </div>
                <span class="hint">Selbstständige: voller Rürup-Spielraum</span>
              </div>
              <div class="col g8">
                <label class="lbl">Bruttojahresgehalt</label>
                <div class="sfx"><input type="number" step="1000" bind:value={Ru.brutto} /><span class="sfxt">€/Jahr</span></div>
              </div>
              <div class="col g8">
                <label class="lbl">Grenzsteuersatz</label>
                <div class="sfx"><input type="number" step="1" bind:value={Ru.grenzSt} /><span class="sfxt">%</span></div>
                <span class="hint">~30% bei 60k € · ~42% ab 68k €</span>
              </div>
              <div class="col g8">
                <label class="lbl">Kirchensteuerpflichtig?</label>
                <div class="seg segf">
                  {#each ['Ja','Nein'] as opt}
                    <button class:on={Ru.kirche === opt} on:click={() => Ru.kirche = opt}>{opt}</button>
                  {/each}
                </div>
              </div>
            </div>

          {:else if step === 1}
            <div class="col g20">
              <div class="col g8">
                <label class="lbl">Monatlicher Rürup-Beitrag</label>
                <div class="sfx" style="font-size:20px">
                  <input type="number" step="25" bind:value={Ru.mb} style="font-size:20px;font-weight:500" />
                  <span class="sfxt" style="font-size:15px">€ / Monat</span>
                </div>
              </div>
              {#if result}
                <div class="card" style="background:var(--bg2)">
                  <div class="ey" style="margin-bottom:10px">Steuerersparnis 2025</div>
                  <div class="stat" style="font-size:40px">{fmtE(result.steJ)} / Jahr</div>
                  <div style="font-size:12px;color:var(--fg3);font-family:var(--mono);margin-top:8px">
                    Spielraum 2025: {de0.format(Math.round(result.sp))} € · Absetzbar: {de0.format(Math.round(result.absB))} €
                  </div>
                </div>
              {/if}
              {#if Ru.selbst === 'Nein'}
                <div class="col g8">
                  <label class="lbl">GRV-Arbeitnehmeranteil</label>
                  <div class="sfx"><input type="number" step="100" bind:value={Ru.grvAN} /><span class="sfxt">€/Jahr</span></div>
                  <span class="hint">AN-Anteil wird vom Rürup-Spielraum abgezogen</span>
                </div>
              {/if}
            </div>

          {:else if step === 2}
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:16px">
              <div class="col g8">
                <label class="lbl">Rendite p.a. (nach Kosten)</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={Ru.rendite} /><span class="sfxt">% p.a.</span></div>
                <span class="hint">ETF-Rürup Ø: 5–7 %</span>
              </div>
              <div class="col g8">
                <label class="lbl">Inflation p.a.</label>
                <div class="sfx"><input type="number" step="0.1" bind:value={Ru.inf} /><span class="sfxt">% p.a.</span></div>
              </div>
            </div>
            <div class="col g8">
              <label class="lbl">Ansparzeit (Jahre bis Rente)</label>
              <input class="inp" type="number" min="5" max="40" bind:value={Ru.lz} />
            </div>

          {:else if step === 3}
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
              <div class="col g8">
                <label class="lbl">Renteneintrittsalter</label>
                <input class="inp" type="number" min="62" max="70" bind:value={Ru.rentAlter} />
                <span class="hint">Frühestens: 62 J. (Verträge ab 2012)</span>
              </div>
              <div class="col g8">
                <label class="lbl">Lebenserwartung</label>
                <input class="inp" type="number" min="70" max="100" bind:value={Ru.lebErw} />
              </div>
            </div>
          {/if}
        </div>

        <div class="row" style="justify-content:space-between;margin-top:36px;padding-top:20px;border-top:1px solid var(--line)">
          <button class="btn btnlg" on:click={back} style="opacity:{step===0?0.3:1};pointer-events:{step===0?'none':'auto'}">← Zurück</button>
          <div class="row g12">
            <button class="btn btng" on:click={next}>Überspringen</button>
            <button class="btn btnp btnlg" on:click={next}>
              {step === RUS_LABELS.length - 1 ? 'Rürup berechnen →' : 'Weiter →'}
            </button>
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <aside style="border-left:1px solid var(--line);padding:36px 28px;background:var(--bg1)">
        <div class="ey" style="margin-bottom:14px">Steuervorteil</div>
        <div class="stat" style="font-size:40px">{result ? fmtE(result.steM) + '/Mo.' : '–'}</div>
        <div style="color:var(--fg3);font-size:11px;font-family:var(--mono);margin-top:6px;text-transform:uppercase;letter-spacing:.08em">€ / Monat gespart</div>
        {#if result}
          <div style="margin-top:16px;padding-top:16px;border-top:1px solid var(--line);font-size:13px">
            <div class="row" style="justify-content:space-between;padding:8px 0">
              <span style="color:var(--fg3)">Monatsrente (netto)</span>
              <span style="font-family:var(--mono)">{fmtE(result.nettoR)}/Mo.</span>
            </div>
          </div>
        {/if}
      </aside>
    </div>
  </div>
</div>
{/if}
