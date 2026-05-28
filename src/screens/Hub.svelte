<script>
  import { createEventDispatcher } from 'svelte';
  import Logo from '../components/Logo.svelte';

  const dispatch = createEventDispatcher();
  const go = (name) => dispatch('navigate', name);
  const book = () => window.open('https://tidycal.com/niallbradfield/kostenfreies-beratungsgesprach', '_blank');

  const cards = [
    { id: 'pension',      num: '01', badge: 'Beamte',             title: 'Pensionsrechner',    desc: 'Nettopension nach § 14 BeamtVG — mit Ruhegehaltssatz, Mindestversorgung, Steuer und KV-Beihilfe.', tags: ['§ 14 BeamtVG', '17 Bundesländer', 'PKV/GKV'] },
    { id: 'rente',        num: '02', badge: 'Angestellte',         title: 'Rentenrechner',      desc: 'Gesetzliche Rente nach § 64 SGB VI. Entgeltpunkte, Rentenwert 2025 · 40,79 €, Besteuerungsanteil.', tags: ['§ 64 SGB VI', 'Rentenwert 40,79 €', 'Rentenlücke'] },
    { id: 'depot',        num: '03', badge: 'ETF · Altersvorsorge', title: 'AV-Depot-Rechner',  desc: 'Zinseszins-Depot, reale Rendite nach Inflation, 4 %-Entnahmerate und Sparrate zum Ziel.', tags: ['Zinseszins', '4 %-Regel', 'Realrendite'] },
    { id: 'ruerup',       num: '04', badge: 'Steueroptimierung',   title: 'Rürup-Rechner',      desc: 'Steuervorteil der Basisrente nach § 10 EStG. 100 % absetzbar 2025. Netto-Kosten & Rentenprognose.', tags: ['§ 10 EStG', '100 % absetzbar', 'ETF-Rürup'] },
    { id: 'cashflow',     num: '05', badge: 'Finanzplanung',       title: 'Cashflow-Rechner',   desc: 'Monatlichen Cashflow analysieren: Ist vs. 50/15/15-Empfehlung, Notgroschen und AV-Sparquote.', tags: ['50/15/15-Regel', 'Notgroschen', 'Sparquote'] },
    { id: 'versicherung', num: '06', badge: 'Marktvergleich',      title: 'Versicherungscheck', desc: 'Deine Versicherungskosten vs. GDV-Marktdurchschnitt 2025. Über- und Unterversicherung auf einen Blick.', tags: ['GDV-Daten 2025', '8 Kategorien', 'Einsparpotenzial'] },
  ];

  const tickers = [
    { label: 'Rentenwert 2025 · DRV', value: '40,79 €',  sub: 'pro Entgeltpunkt · ab Juli' },
    { label: 'Rürup-Höchstbetrag',    value: '29.344 €', sub: '§ 10 EStG · Single · 100 % absetzbar' },
    { label: 'Ruhegehaltssatz-Max',   value: '71,75 %',  sub: '§ 14 BeamtVG · 40 Dienstjahre' },
    { label: 'Ø Versorgungslücke',    value: '938 €/Mo.', sub: 'Lehrkräfte · inflationsbereinigt' },
  ];
</script>

<div>
  <!-- Nav -->
  <nav class="nav">
    <button class="brand"><Logo /> Pensora</button>
    <div class="row g32">
      <a class="nav-link">Über uns</a>
      <a class="nav-link">Kontakt</a>
      <div class="ddwrap">
        <button class="ddtrig">
          FAQ
          <svg width="9" height="6" viewBox="0 0 10 6" fill="currentColor"><path d="M0 0l5 6 5-6z"/></svg>
        </button>
        <div class="ddmenu">
          {#each cards as c}
            <button class="dditem" on:click={() => go(c.id)}>
              <span style="font-family:var(--mono);color:var(--fg4);font-size:10px;margin-right:8px">{c.num}</span>
              {c.title}
            </button>
          {/each}
        </div>
      </div>
    </div>
    <button class="btn btnp" on:click={book}>Beratung buchen</button>
  </nav>

  <!-- Scrollable content -->
  <div class="vscr">

    <!-- Hero -->
    <section class="hero-section">
      <div class="hero-inner">
        <div class="ey" style="margin-bottom:18px;animation:fadeUp .5s var(--ease) both">Finanzrechner · 2025 · Geprüfte Formeln</div>
        <h1 class="h1" style="margin-bottom:22px;animation:fadeUp .5s .07s var(--ease) both">
          Deine Finanzen.<br/><span style="color:var(--fg3)">Klartext.</span>
        </h1>
        <p class="lead" style="max-width:52ch;margin-bottom:36px;animation:fadeUp .5s .14s var(--ease) both">
          Sechs präzise Rechner für Pension, Rente, Depot, Rürup, Cashflow und Versicherungscheck. Keine Anmeldung. Daten bleiben lokal.
        </p>
        <div class="row g12" style="animation:fadeUp .5s .20s var(--ease) both">
          <button class="btn btnp btnlg" on:click={() => go('pension')}>Jetzt starten →</button>
          <button class="btn btng btnlg" on:click={book}>Kostenloses Gespräch</button>
        </div>
      </div>
    </section>

    <!-- Ticker -->
    <div class="ticker">
      {#each tickers as t}
        <div class="ti">
          <div class="tl">{t.label}</div>
          <div class="tv">{t.value}</div>
          <div class="td">{t.sub}</div>
        </div>
      {/each}
    </div>

    <!-- Calculator cards -->
    <section style="padding:64px 52px 80px">
      <div class="cards-header">
        <h2 style="font-size:26px;font-weight:600;letter-spacing:-.025em">Alle Rechner</h2>
        <span style="font-size:11px;color:var(--fg3);font-family:var(--mono)">{cards.length} Tools</span>
      </div>
      <div class="cards-grid">
        {#each cards as c}
          <button class="calc-card" on:click={() => go(c.id)}>
            <div class="card-head">
              <span class="card-num">{c.num}</span>
              <span class="badge">{c.badge}</span>
            </div>
            <h3 class="card-title">{c.title}</h3>
            <p class="card-desc">{c.desc}</p>
            <div class="card-tags">
              {#each c.tags as tag}
                <span class="card-tag">{tag}</span>
              {/each}
            </div>
            <div class="card-cta-row">
              <span>Rechner starten</span>
              <svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg>
            </div>
          </button>
        {/each}
      </div>
    </section>

    <!-- CTA strip -->
    <div class="cta-strip">
      <div>
        <h2 style="font-size:30px;font-weight:600;letter-spacing:-.025em;margin-bottom:10px">Zahlen allein reichen nicht.</h2>
        <p style="font-size:15px;color:var(--fg2);max-width:48ch;line-height:1.65">Unabhängige Finanzberatung ohne Provision. 30 Minuten, kostenlos — wir besprechen deine persönliche Situation.</p>
      </div>
      <button class="btn btnp btnlg" on:click={book} style="white-space:nowrap;flex-shrink:0">Kostenloses Gespräch buchen →</button>
    </div>

    <!-- Footer -->
    <footer class="foot">
      <div>
        <button class="brand" style="margin-bottom:14px"><Logo /> Pensora</button>
        <p>Unabhängige Finanzplanung.<br/>Keine Provisionen. Nur Klarheit.</p>
        <div style="margin-top:16px;font-size:11px;color:var(--fg4);font-family:var(--mono)">© 2025 Pensora</div>
      </div>
      <div>
        <h5>Rechner</h5>
        {#each cards.slice(0,4) as c}<a on:click={() => go(c.id)}>{c.title}</a>{/each}
      </div>
      <div>
        <h5>Tools</h5>
        {#each cards.slice(4) as c}<a on:click={() => go(c.id)}>{c.title}</a>{/each}
      </div>
      <div>
        <h5>Rechtliches</h5>
        <a>Impressum</a>
        <a>Datenschutz</a>
        <a>BaFin-Hinweis</a>
      </div>
    </footer>
  </div>
</div>

<style>
  .nav-link { font-size:13px; color:var(--fg3); cursor:pointer; transition:color .15s; text-decoration:none; }
  .nav-link:hover { color:var(--fg); }

  .hero-section {
    padding: 96px 52px 72px;
    position: relative; overflow: hidden;
  }
  .hero-section::before {
    content:''; position:absolute; inset:0;
    background: radial-gradient(ellipse 80% 55% at 50% -5%, rgba(250,250,250,.04) 0%, transparent 60%);
    pointer-events:none;
  }
  .hero-inner { max-width:860px; position:relative; }

  .cards-header {
    display:flex; align-items:baseline; justify-content:space-between; margin-bottom:28px;
  }
  .cards-grid {
    display:grid; grid-template-columns:repeat(3,1fr); gap:12px;
  }

  .calc-card {
    background: var(--bg1); border: 1px solid var(--line); border-radius: var(--rlg);
    padding: 22px; cursor: pointer; text-align: left;
    font-family: var(--sans); color: var(--fg);
    position:relative; overflow:hidden;
    transition: border-color .22s var(--ease), transform .22s var(--ease), box-shadow .22s var(--ease), background .22s var(--ease);
    display:flex; flex-direction:column;
  }
  .calc-card:hover {
    border-color: var(--line3);
    transform: translateY(-3px);
    box-shadow: 0 8px 32px rgba(0,0,0,.7), 0 0 0 1px rgba(255,255,255,.05);
    background: var(--bg2);
  }
  .calc-card:active { transform: translateY(-1px) scale(0.99); }
  .calc-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:1px;
    background: linear-gradient(90deg, transparent, rgba(250,250,250,.08), transparent);
    opacity:0; transition:opacity .22s;
  }
  .calc-card:hover::before { opacity:1; }

  .card-head { display:flex; align-items:center; justify-content:space-between; margin-bottom:16px; }
  .card-num { font-family:var(--mono); font-size:10px; color:var(--fg4); letter-spacing:.08em; }
  .card-title { font-size:19px; font-weight:600; letter-spacing:-.02em; margin-bottom:9px; line-height:1.2; }
  .card-desc { font-size:13px; color:var(--fg2); line-height:1.6; margin-bottom:16px; flex:1; }
  .card-tags { display:flex; gap:10px; flex-wrap:wrap; margin-bottom:16px; }
  .card-tag { font-size:10px; color:var(--fg4); font-family:var(--mono); letter-spacing:.03em; }
  .card-cta-row {
    display:flex; align-items:center; justify-content:space-between;
    padding-top:12px; border-top:1px solid var(--line);
    font-size:12px; color:var(--fg3);
    transition: color .15s;
  }
  .calc-card:hover .card-cta-row { color:var(--fg2); }

  .cta-strip {
    display:flex; align-items:center; justify-content:space-between; gap:40px;
    padding:52px; border-top:1px solid var(--line); border-bottom:1px solid var(--line);
    background:var(--bg1);
  }
</style>
