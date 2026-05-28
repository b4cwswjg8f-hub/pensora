<script>
  import { createEventDispatcher } from 'svelte';
  import Logo from '../components/Logo.svelte';

  const dispatch = createEventDispatcher();
  const go = (name) => dispatch('navigate', name);

  const cards = [
    { id: 'pension', num: '01', badge: 'Beamte', title: 'Pensionsrechner', desc: 'Beamtenpension nach § 14 BeamtVG mit korrekter Ruhegehaltssatz-Formel, Mindestversorgung, Steuer und KV.', tags: ['§ 14 BeamtVG', '17 Bundesländer', 'PKV/GKV Beihilfe'] },
    { id: 'rente', num: '02', badge: 'Angestellte', title: 'Rentenrechner', desc: 'Gesetzliche Rente nach § 64 SGB VI. Entgeltpunkte, Rentenwert 2025, Besteuerungsanteil und Rentenlücke.', tags: ['§ 64 SGB VI', 'Rentenwert 40,79€', 'Besteuerungsanteil'] },
    { id: 'depot', num: '03', badge: 'ETF · Altersvorsorge', title: 'AV-Depot-Rechner', desc: 'ETF-Altersvorsorge: Zinseszins-Depot, reale Rendite, 4%-Entnahmerate und Sparrate zum Ziel.', tags: ['Zinseszins-Formel', '4%-Regel', 'Realrendite'] },
    { id: 'ruerup', num: '04', badge: 'Steueroptimierung', title: 'Rürup-Rechner', desc: 'Steuerlicher Vorteil der Basisrente nach § 10 EStG. 100% absetzbar 2025. Netto-Kosten und Rentenprognose.', tags: ['§ 10 EStG', '100% absetzbar', 'ETF-Rürup'] },
    { id: 'cashflow', num: '05', badge: 'Finanzplanung', title: 'Cashflow-Rechner', desc: 'Monatlichen Cashflow analysieren: empfohlene Aufteilung für AV, Vermögensaufbau und Liquidität.', tags: ['50/15/15 Regel', 'Notgroschen-Ziel', 'Direkt zu AV-Rechner'] },
    { id: 'versicherung', num: '06', badge: 'Marktvergleich', title: 'Versicherungscheck', desc: 'Vergleich deiner Versicherungskosten mit dem Marktdurchschnitt 2025. Einsparpotenzial konkret beziffern.', tags: ['GDV-Daten 2025', '8 Kategorien', 'Vertragscheck-CTA'] },
  ];
</script>

<div>
  <!-- Nav -->
  <nav class="nav">
    <button class="brand"><Logo /> Pensora</button>
    <div class="row g32">
      <a style="font-size:13px;color:var(--fg2)">Über uns</a>
      <a style="font-size:13px;color:var(--fg2)">Kontakt</a>
      <div class="ddwrap">
        <button class="ddtrig">
          FAQ
          <svg width="10" height="6" viewBox="0 0 10 6" fill="currentColor"><path d="M0 0l5 6 5-6z"/></svg>
        </button>
        <div class="ddmenu">
          {#each cards as c}
            <button class="dditem" on:click={() => go(c.id)}>{c.title}</button>
          {/each}
        </div>
      </div>
    </div>
    <button class="btn btnp" on:click={() => alert('Calendly-Link einfügen')}>Beratung buchen</button>
  </nav>

  <!-- Scrollable content -->
  <div class="vscr">
    <!-- Hero -->
    <section style="padding:88px 56px 72px">
      <div style="max-width:900px">
        <div class="ey" style="margin-bottom:20px">Finanzrechner · 2025 · Geprüfte Formeln</div>
        <h1 class="h1" style="margin-bottom:24px">Deine Finanzen.<br/><span style="color:var(--fg3)">Klartext.</span></h1>
        <p class="lead" style="max-width:56ch;margin-bottom:40px">Sechs präzise Rechner für Pension, Rente, Depot, Rürup, Cashflow und Versicherungscheck. Keine Anmeldung. Daten bleiben lokal.</p>
      </div>
    </section>

    <!-- Ticker -->
    <div class="ticker">
      <div class="ti"><div class="tl">Rentenwert 2025 (DRV)</div><div class="tv">40,79 €/EP</div><div class="td">ab 01.07.2025</div></div>
      <div class="ti"><div class="tl">Rürup-Max 2025 (§10 EStG)</div><div class="tv">29.344 €</div><div class="td">Single · 100% absetzbar</div></div>
      <div class="ti"><div class="tl">Ruhegehaltssatz-Max</div><div class="tv">71,75 %</div><div class="td">§ 14 BeamtVG</div></div>
      <div class="ti"><div class="tl">Ø Versorgungslücke</div><div class="tv">938 €/Mo.</div><div class="td">Lehrkräfte</div></div>
    </div>

    <!-- Calculator Cards -->
    <section style="padding:72px 56px 96px">
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px">
        {#each cards as c}
          <div
            class="card"
            style="cursor:pointer;transition:border-color .15s"
            on:mouseenter={e => e.currentTarget.style.borderColor = 'var(--fg2)'}
            on:mouseleave={e => e.currentTarget.style.borderColor = 'var(--line)'}
            on:click={() => go(c.id)}
            role="button"
            tabindex="0"
            on:keydown={e => e.key === 'Enter' && go(c.id)}
          >
            <div class="row" style="justify-content:space-between;margin-bottom:20px">
              <span style="font-size:11px;font-family:var(--mono);color:var(--fg3);letter-spacing:.08em;text-transform:uppercase">{c.num}</span>
              <span class="badge">{c.badge}</span>
            </div>
            <h3 style="font-size:22px;font-weight:600;letter-spacing:-.02em;margin-bottom:10px">{c.title}</h3>
            <p style="font-size:14px;color:var(--fg2);line-height:1.55;margin-bottom:20px">{c.desc}</p>
            <div class="row g8" style="flex-wrap:wrap">
              {#each c.tags as tag}
                <span style="font-size:11px;color:var(--fg4);font-family:var(--mono)">{tag}</span>
              {/each}
            </div>
            <div class="row" style="margin-top:20px;padding-top:16px;border-top:1px solid var(--line);justify-content:flex-end">
              <span style="font-size:13px;color:var(--fg2)">Starten →</span>
            </div>
          </div>
        {/each}
      </div>
    </section>

    <!-- Footer -->
    <footer class="foot">
      <div>
        <button class="brand" style="margin-bottom:16px"><Logo /> Pensora</button>
        <p>Unabhängige Finanzplanung.<br/>Keine Provisionen. Nur Klarheit.</p>
      </div>
      <div>
        <h5>Rechner</h5>
        {#each cards.slice(0,4) as c}
          <a on:click={() => go(c.id)}>{c.title}</a>
        {/each}
      </div>
      <div>
        <h5>Tools</h5>
        {#each cards.slice(4) as c}
          <a on:click={() => go(c.id)}>{c.title}</a>
        {/each}
      </div>
      <div>
        <h5>Rechtliches</h5>
        <a>Impressum</a>
        <a>Datenschutz</a>
        <a>BaFin-Hinweise</a>
      </div>
    </footer>
  </div>
</div>
