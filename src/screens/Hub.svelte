<script>
  import { createEventDispatcher } from 'svelte';
  import Logo from '../components/Logo.svelte';
  import Search from '../components/Search.svelte';

  const dispatch = createEventDispatcher();
  const go = (name) => dispatch('navigate', name);
  const book = () => window.open('https://tidycal.com/niallbradfield/kostenfreies-beratungsgesprach', '_blank');

  let showPersonaModal = false;
  let selectedPersona = null;

  const personas = [
    {
      id: 'beamter',
      icon: '🏛',
      title: 'Beamter/in',
      sub: 'Pension · PKV · Beihilfe',
      hint: 'Lehrkraft, Richter, Polizei, Verwaltung',
      calcs: ['pension', 'depot', 'ruerup', 'versicherung'],
    },
    {
      id: 'angestellter',
      icon: '💼',
      title: 'Angestellte/r',
      sub: 'Gesetzliche Rente · Depot · Budget',
      hint: 'Sozialversicherungspflichtig beschäftigt',
      calcs: ['rente', 'depot', 'ruerup', 'cashflow'],
    },
    {
      id: 'selbstaendiger',
      icon: '⚡',
      title: 'Selbständige/r',
      sub: 'Rürup · Depot · Versicherungen',
      hint: 'Freiberufler, Unternehmer, Freelancer',
      calcs: ['ruerup', 'depot', 'cashflow', 'versicherung'],
    },
    {
      id: 'vorrente',
      icon: '🌅',
      title: 'Kurz vor Rente',
      sub: 'Versorgung · Entnahme · Cashflow',
      hint: 'Weniger als 5 Jahre bis zum Ruhestand',
      calcs: ['pension', 'rente', 'depot', 'cashflow'],
    },
  ];

  function selectPersona(p) {
    selectedPersona = p;
    showPersonaModal = false;
    setTimeout(() => {
      document.getElementById('rechner')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 120);
  }

  $: recCards = selectedPersona ? cards.filter(c => selectedPersona.calcs.includes(c.id)) : [];
  $: otherCards = selectedPersona ? cards.filter(c => !selectedPersona.calcs.includes(c.id)) : cards;

  const cards = [
    { id: 'pension',      faq: 'pensionsrechner30.html',  num: '01', badge: 'Beamte',             title: 'Pensionsrechner',    desc: 'Nettopension nach § 14 BeamtVG — Ruhegehaltssatz, Mindestversorgung, Steuer und KV-Beihilfe.', tags: ['§ 14 BeamtVG', '17 Bundesländer', 'PKV/GKV'] },
    { id: 'rente',        faq: 'rentenrechner.html',       num: '02', badge: 'Angestellte',         title: 'Rentenrechner',      desc: 'Gesetzliche Rente nach § 64 SGB VI. Entgeltpunkte, Rentenwert 2025 · 40,79 €, Besteuerungsanteil.', tags: ['§ 64 SGB VI', 'Rentenwert 40,79 €', 'Rentenlücke'] },
    { id: 'depot',        faq: 'av-depot-rechner30.html',  num: '03', badge: 'ETF · Altersvorsorge', title: 'AV-Depot-Rechner',  desc: 'Zinseszins-Depot, reale Rendite nach Inflation, 4 %-Entnahmerate und Sparrate zum Ziel.', tags: ['Zinseszins', '4 %-Regel', 'Realrendite'] },
    { id: 'ruerup',       faq: 'ruerup-rechner.html',      num: '04', badge: 'Steueroptimierung',   title: 'Rürup-Rechner',      desc: 'Steuervorteil der Basisrente nach § 10 EStG. 100 % absetzbar 2025. Netto-Kosten & Rentenprognose.', tags: ['§ 10 EStG', '100 % absetzbar', 'ETF-Rürup'] },
    { id: 'cashflow',     faq: 'cashflow-rechner.html',    num: '05', badge: 'Finanzplanung',       title: 'Cashflow-Rechner',   desc: 'Monatlichen Cashflow analysieren: Ist vs. 50/15/15-Empfehlung, Notgroschen und AV-Sparquote.', tags: ['50/15/15-Regel', 'Notgroschen', 'Sparquote'] },
    { id: 'versicherung', faq: 'versicherungscheck.html',  num: '06', badge: 'Marktvergleich',      title: 'Versicherungscheck', desc: 'Deine Versicherungskosten vs. GDV-Marktdurchschnitt 2025. Über- und Unterversicherung.', tags: ['GDV-Daten 2025', '8 Kategorien', 'Einsparpotenzial'] },
  ];

  const ratgeber = [
    { href: 'lehrerpension-nrw/',     label: 'Lehrerpension NRW' },
    { href: 'lehrerpension-bw/',      label: 'Lehrerpension BW' },
    { href: 'lehrerpension-bayern/',  label: 'Lehrerpension Bayern' },
    { href: 'a13-gehalt-pension/',    label: 'Pension A13' },
    { href: 'teilzeit-pension-lehrer/', label: 'Teilzeit & Pension' },
    { href: 'referendariat-pension/', label: 'Referendariat' },
    { href: 'altersvorsorgedepot-2027/', label: 'AV-Depot 2027' },
    { href: 'ruerup-lehrer/',         label: 'Rürup für Lehrer' },
    { href: 'pkv-beamte-ruhestand/',  label: 'PKV im Ruhestand' },
    { href: 'riester-nachfolger/',        label: 'Riester Nachfolger' },
    { href: 'fruehstartrente-kinder/',    label: 'Frühstartrente Kinder' },
    { href: 'altersvorsorgedepot-beamte/', label: 'AV-Depot Beamte' },
    { href: 'altersvorsorgedepot-foerderung/', label: 'AV-Depot Förderung' },
    { href: 'rentenluecke-2026/',         label: 'Rentenlücke 2026' },
    { href: 'gesetzliche-rente-reicht-nicht/', label: 'GRV reicht nicht' },
    { href: 'rente-mit-63-lehrer/',       label: 'Rente mit 63 Lehrer' },
    { href: 'aktivrente-2026/',           label: 'Aktivrente 2026' },
    { href: 'muetterrente-2027/',         label: 'Mütterrente 2027' },
    { href: 'versorgungsluecke-beamte-berechnen/', label: 'Versorgungslücke Beamte' },
    { href: 'pensionsluecke-lehrer/',     label: 'Pensionslücke Lehrer' },
    { href: 'pension-lehrer-prozent/',    label: 'Pension Lehrer Prozent' },
    { href: 'beamtenversorgung-teilzeit-elternzeit/', label: 'Teilzeit Elternzeit Pension' },
    { href: 'private-altersvorsorge-beamte/', label: 'Private AV Beamte' },
  ];

  const vergleiche = [
    { href: 'pension-vs-rente/',              label: 'Pension vs. Rente' },
    { href: 'pension-vs-rente-lehrer/',       label: 'Pension vs. Rente Lehrer' },
    { href: 'ruerup-vs-altersvorsorgedepot/', label: 'Rürup vs. AV-Depot' },
    { href: 'pkv-vs-gkv-beamte-ruhestand/',  label: 'PKV vs. GKV Beamte' },
    { href: 'teilzeit-vs-vollzeit-pension/',  label: 'Teilzeit vs. Vollzeit' },
  ];

  const stats = [
    { val: '71,75 %',   label: 'Max. Ruhegehaltssatz',  sub: '§ 14 BeamtVG · 40 Dienstjahre' },
    { val: '40,79 €',   label: 'Rentenwert 2025',        sub: 'DRV · pro Entgeltpunkt · ab Juli' },
    { val: '938 €/Mo.', label: 'Ø Versorgungslücke',     sub: 'Lehrkräfte · inflationsbereinigt' },
    { val: '540 €',     label: 'AV-Depot Grundzulage',   sub: 'ab 01.01.2027 · pro Jahr' },
  ];
</script>

<div>
  <!-- Update banner -->
  <div class="update-bar">
    <span class="update-dot"></span>
    <span class="update-label">Neu</span>
    <span class="update-entries">
      <span class="update-entry">AV-Depot 2027 — Grundzulage bestätigt: 540 €/Jahr · Stand 29.05.2026</span>
      <span class="update-sep">·</span>
      <span class="update-entry">Rentenwert 2026: 42,52 € · DRV · ab 1. Juli 2026</span>
      <span class="update-sep">·</span>
      <span class="update-entry">Rürup-Höchstbetrag 2026: 30.826 € · § 10 EStG</span>
    </span>
  </div>

  <!-- Nav -->
  <nav class="nav">
    <button class="brand" on:click={() => go('hub')}><Logo /> Pensora</button>

    <!-- Center nav -->
    <div class="nav-center">
      <!-- Rechner dropdown -->
      <div class="ddwrap">
        <button class="nav-link ddtrig">
          Rechner
          <svg width="9" height="5" viewBox="0 0 10 6" fill="currentColor"><path d="M0 0l5 6 5-6z"/></svg>
        </button>
        <div class="ddmenu dd-wide">
          <div class="dd-grid">
            {#each cards as c}
              <button class="dditem" on:click={() => go(c.id)}>
                <span class="dd-num">{c.num}</span>
                <span class="dd-text">
                  <span class="dd-title">{c.title}</span>
                  <span class="dd-badge">{c.badge}</span>
                </span>
              </button>
            {/each}
          </div>
        </div>
      </div>

      <!-- Ratgeber dropdown -->
      <div class="ddwrap">
        <button class="nav-link ddtrig">
          Ratgeber
          <svg width="9" height="5" viewBox="0 0 10 6" fill="currentColor"><path d="M0 0l5 6 5-6z"/></svg>
        </button>
        <div class="ddmenu dd-wide">
          <div class="dd-section-label">Bundesland & Thema</div>
          <div class="dd-grid dd-grid-3">
            {#each ratgeber as r}
              <a class="dditem" href={r.href}>
                <span class="dd-title">{r.label}</span>
              </a>
            {/each}
          </div>
          <div class="dd-divider"></div>
          <div class="dd-section-label">Vergleiche für KI-Zitierungen</div>
          <div class="dd-grid dd-grid-3">
            {#each vergleiche as v}
              <a class="dditem" href={v.href}>
                <span class="dd-title">{v.label}</span>
              </a>
            {/each}
          </div>
        </div>
      </div>

      <!-- Direct link -->
      <a class="nav-link" href="wie-wird-berechnet/">Wie berechnet?</a>
      <a class="nav-link" href="ueber-uns/">Über uns</a>
    </div>

    <!-- Right side -->
    <div class="row g8">
      <a class="nav-link" href="kontakt/" style="margin-right:4px">Kontakt</a>
      <button class="btn btnp" style="height:36px;padding:0 18px;font-size:13px;border-radius:8px" on:click={book}>Termin buchen</button>
    </div>
  </nav>

  <!-- Persona modal -->
  {#if showPersonaModal}
    <div class="persona-backdrop" on:click|self={() => showPersonaModal = false}>
      <div class="persona-modal">
        <button class="persona-close" on:click={() => showPersonaModal = false}>✕</button>
        <div class="ey" style="margin-bottom:8px">Personalisiert starten</div>
        <h2 style="font-size:26px;font-weight:700;letter-spacing:-.03em;color:var(--fg);margin-bottom:6px">Wer bist du?</h2>
        <p style="font-size:13px;color:var(--fg3);margin-bottom:24px;line-height:1.5">Wir zeigen dir die passenden Rechner und Artikel — kostenlos und anonym.</p>
        <div class="persona-grid">
          {#each personas as p}
            <button class="persona-card" on:click={() => selectPersona(p)}>
              <span class="persona-icon">{p.icon}</span>
              <span class="persona-title">{p.title}</span>
              <span class="persona-sub">{p.sub}</span>
              <span class="persona-hint">{p.hint}</span>
            </button>
          {/each}
        </div>
        <p style="font-size:11px;color:var(--fg4);text-align:center;margin-top:20px">Keine Anmeldung · Keine Daten gespeichert</p>
      </div>
    </div>
  {/if}

  <!-- Scrollable page -->
  <div class="vscr">

    <!-- ── HERO ── -->
    <section class="hero">
      <div class="hero-content">
        <div class="ey" style="margin-bottom:16px">Pension · Rente · Altersvorsorge · 2026</div>
        <h1 class="hero-title">
          Deine Finanzen.<br/><span class="hero-muted">Klartext.</span>
        </h1>
        <p class="hero-lead">
          Sechs präzise Rechner für Pension, Rente, Depot, Rürup, Cashflow und Versicherungen.
        </p>
        <p class="hero-trust">Kostenlos, anonym, keine Verpflichtung. Reine Information — damit du weißt, wo du stehst.</p>
        <div class="hero-search">
          <Search on:navigate={e => go(e.detail)} />
        </div>
        <div class="row g12 hero-btns">
          <button class="btn btnp btnlg" on:click={() => showPersonaModal = true}>Start → Was passt zu mir?</button>
          <button class="btn btno btnlg" on:click={book}>Kostenloses Gespräch</button>
        </div>
      </div>
      <div class="hero-visual">
        <img
          src="{import.meta.env.BASE_URL}assets/hero-person.png"
          alt="Pensora Nutzer plant Altersvorsorge"
          class="hero-person"
        />
      </div>
    </section>

    <!-- ── STATS TICKER ── -->
    <div class="ticker">
      {#each stats as s}
        <div class="ti">
          <div class="tl">{s.label}</div>
          <div class="tv">{s.val}</div>
          <div class="td">{s.sub}</div>
        </div>
      {/each}
    </div>

    <!-- ── CALCULATOR CARDS ── -->
    <section class="cards-section" id="rechner">
      <div class="section-header">
        <h2 class="section-title">{selectedPersona ? `Für dich — ${selectedPersona.title}` : 'Alle Rechner'}</h2>
        <div style="display:flex;align-items:center;gap:12px">
          {#if selectedPersona}
            <button class="persona-reset" on:click={() => selectedPersona = null}>× Alle anzeigen</button>
          {:else}
            <span class="section-sub">Geprüfte gesetzliche Formeln · Keine Anmeldung</span>
          {/if}
          <button class="btn btng" style="font-size:12px;height:32px;padding:0 14px" on:click={() => showPersonaModal = true}>
            {selectedPersona ? '↺ Persona ändern' : '→ Für mich filtern'}
          </button>
        </div>
      </div>

      {#if selectedPersona && recCards.length > 0}
        <div class="persona-label">Empfohlen für {selectedPersona.title}</div>
        <div class="cards-grid" style="margin-bottom:24px">
          {#each recCards as c}
            <button class="calc-card calc-card-rec" on:click={() => go(c.id)}>
              <div class="card-head">
                <span class="card-num">{c.num}</span>
                <span class="badge badge-rec">{c.badge}</span>
              </div>
              <h3 class="card-title">{c.title}</h3>
              <p class="card-desc">{c.desc}</p>
              <div class="card-tags">
                {#each c.tags as tag}<span class="card-tag">{tag}</span>{/each}
              </div>
              <div class="card-cta-row">
                <span>Rechner starten</span>
                <svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg>
              </div>
            </button>
          {/each}
        </div>
        {#if otherCards.length > 0}
          <div class="persona-label" style="color:var(--fg4)">Weitere Rechner</div>
        {/if}
      {/if}

      <div class="cards-grid">
        {#each otherCards as c}
          <button class="calc-card" on:click={() => go(c.id)}>
            <div class="card-head">
              <span class="card-num">{c.num}</span>
              <span class="badge">{c.badge}</span>
            </div>
            <h3 class="card-title">{c.title}</h3>
            <p class="card-desc">{c.desc}</p>
            <div class="card-tags">
              {#each c.tags as tag}<span class="card-tag">{tag}</span>{/each}
            </div>
            <div class="card-cta-row">
              <span>Rechner starten</span>
              <svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg>
            </div>
          </button>
        {/each}
      </div>
    </section>

    <!-- ── TRUST SECTION ── -->
    <section class="trust-section">
      <div class="trust-inner">
        <div class="ey" style="margin-bottom:16px">Warum Pensora</div>
        <div class="trust-grid">
          <div class="trust-item">
            <div class="trust-num">100 %</div>
            <div class="trust-label">Lokal im Browser</div>
            <div class="trust-sub">Keine Daten verlassen dein Gerät</div>
          </div>
          <div class="trust-item">
            <div class="trust-num">0</div>
            <div class="trust-label">Login nötig</div>
            <div class="trust-sub">Kein Konto, kein Formular, keine Wartezeit</div>
          </div>
          <div class="trust-item">
            <div class="trust-num">100+</div>
            <div class="trust-label">Lehrer beraten</div>
            <div class="trust-sub">Niall Bradfield, Stuttgart</div>
          </div>
          <div class="trust-item">
            <div class="trust-num">6</div>
            <div class="trust-label">Rechner</div>
            <div class="trust-sub">Alle nach geprüften gesetzlichen Formeln</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── CTA STRIP ── -->
    <section class="cta-strip">
      <div class="cta-inner">
        <h2 class="cta-title">Zahlen allein reichen nicht.</h2>
        <p class="cta-sub">30 Minuten, kostenlos — Niall Bradfield bespricht deine persönliche Situation und was deine Zahlen bedeuten.</p>
        <div class="row g12" style="justify-content:center;margin-top:32px">
          <button class="btn btnp btnlg" on:click={book}>Kostenloses Erstgespräch buchen →</button>
          <a class="btn btno btnlg" href="ueber-uns/">Über Pensora</a>
        </div>
      </div>
    </section>

    <!-- ── FOOTER ── -->
    <footer class="foot">
      <div>
        <button class="brand" style="margin-bottom:14px" on:click={() => go('hub')}><Logo /> Pensora</button>
        <p>Klare Zahlen. Unabhängige Beratung.</p>
        <p style="font-size:13px;margin-top:8px">Niall Bradfield<br/>unabhängiger Finanzberater, Stuttgart</p>
        <div style="margin-top:12px;font-size:11px;color:var(--fg4);font-family:var(--mono)">© 2026 Pensora</div>
      </div>
      <div>
        <h5>Rechner</h5>
        {#each cards as c}<a on:click={() => go(c.id)}>{c.title}</a>{/each}
      </div>
      <div>
        <h5>Ratgeber</h5>
        {#each ratgeber as r}<a href={r.href}>{r.label}</a>{/each}
      </div>
      <div>
        <h5>Vergleiche & Mehr</h5>
        {#each vergleiche as v}<a href={v.href}>{v.label}</a>{/each}
        <a href="wie-wird-berechnet/">Wie wird berechnet?</a>
        <a href="ueber-uns/">Über uns</a>
        <a href="kontakt/">Kontakt</a>
        <a style="margin-top:8px;display:block">Impressum</a>
        <a>Datenschutz</a>
      </div>
    </footer>
  </div>
</div>

<style>
  /* ── Update banner ── */
  .update-bar {
    display:flex; align-items:center; gap:10px;
    padding:8px 52px;
    background:rgba(251,191,36,.05); border-bottom:1px solid rgba(251,191,36,.12);
    font-size:12px; overflow:hidden; white-space:nowrap;
  }
  .update-dot {
    width:6px; height:6px; border-radius:50%; background:#fbbf24;
    flex-shrink:0; animation:pulse 2.5s ease-in-out infinite;
  }
  .update-label {
    font-size:10px; font-weight:700; letter-spacing:.12em; text-transform:uppercase;
    color:#fbbf24; flex-shrink:0;
  }
  .update-entries { color:var(--fg3); overflow:hidden; text-overflow:ellipsis; }
  .update-entry { color:var(--fg2); }
  .update-sep { margin:0 10px; color:var(--fg4); }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.35} }

  /* ── Nav ── */
  .nav-center {
    display:flex; align-items:center; gap:4px;
    position:absolute; left:50%; transform:translateX(-50%);
  }
  .nav-link {
    font-size:13px; font-weight:500; color:var(--fg2);
    cursor:pointer; transition:color .15s; text-decoration:none;
    padding:6px 10px; border-radius:6px; background:none; border:none;
    font-family:inherit;
  }
  .nav-link:hover { color:var(--fg); background:rgba(0,0,0,.05); }

  /* Dropdown overrides for nav */
  .ddtrig {
    font-size:13px; color:var(--fg2);
    display:flex; align-items:center; gap:4px;
    cursor:pointer; user-select:none;
    background:none; border:none; padding:6px 10px;
    font-family:inherit; font-weight:500;
    border-radius:6px;
    transition:color .15s, background .15s;
  }
  .ddtrig:hover { color:var(--fg); background:rgba(0,0,0,.05); }
  .ddtrig svg { transition:transform .2s var(--ease); margin-top:1px; }
  .ddwrap { position:relative; }
  .ddwrap:hover .ddtrig { color:var(--fg); }
  .ddwrap:hover .ddtrig svg { transform:rotate(180deg); }

  .ddmenu {
    position:absolute; top:calc(100% + 8px); left:50%;
    transform:translateX(-50%) translateY(-4px);
    background:rgba(250,250,250,.98); border:1px solid rgba(0,0,0,.09);
    border-radius:14px; padding:8px;
    min-width:200px;
    opacity:0; visibility:hidden;
    transition:opacity .18s var(--ease), visibility .18s, transform .18s var(--ease);
    box-shadow:0 20px 60px rgba(0,0,0,.14), 0 0 0 1px rgba(0,0,0,.04);
    z-index:200;
    backdrop-filter:blur(20px);
  }
  .ddwrap:hover .ddmenu {
    opacity:1; visibility:visible;
    transform:translateX(-50%) translateY(0);
  }
  .dd-wide { min-width:480px; left:0; transform:translateX(-10px) translateY(-4px); }
  .ddwrap:hover .dd-wide { transform:translateX(-10px) translateY(0); }

  .dd-grid { display:grid; grid-template-columns:1fr 1fr; gap:2px; }
  .dd-grid-3 { grid-template-columns:1fr 1fr 1fr; }
  .dd-section-label {
    font-size:10px; font-weight:600; letter-spacing:.1em; text-transform:uppercase;
    color:var(--fg4); padding:8px 10px 4px;
  }
  .dd-divider { height:1px; background:rgba(0,0,0,.08); margin:8px 4px; }

  .dditem {
    display:flex; align-items:center; gap:10px;
    padding:8px 10px; font-size:13px; color:var(--fg2);
    border-radius:8px; width:100%; text-align:left; background:none; border:none;
    font-family:inherit; cursor:pointer;
    transition:background .1s, color .1s;
    text-decoration:none;
  }
  .dditem:hover { background:rgba(0,0,0,.05); color:var(--fg); }
  .dd-num { font-family:var(--mono); color:var(--fg4); font-size:10px; flex-shrink:0; width:18px; }
  .dd-text { display:flex; flex-direction:column; gap:1px; }
  .dd-title { font-size:13px; font-weight:500; color:var(--fg2); transition:color .1s; }
  .dditem:hover .dd-title { color:var(--fg); }
  .dd-badge { font-size:10px; color:var(--fg4); font-family:var(--mono); }

  /* ── Hero ── */
  .hero {
    display:grid;
    grid-template-columns:1fr 1fr;
    align-items:center;
    gap:0;
    padding:80px 52px 80px 52px;
    border-bottom:1px solid var(--line);
    min-height:580px;
  }
  .hero-content {
    max-width:520px;
  }
  .hero-title {
    font-size:54px; font-weight:700; line-height:1.08;
    letter-spacing:-.025em;
    margin-bottom:20px;
    color:var(--fg);
  }
  .hero-muted { color:rgba(10,10,10,.35); }
  .hero-lead {
    font-size:17px; color:var(--fg2); line-height:1.65;
    margin-bottom:32px; max-width:46ch;
  }
  .hero-trust {
    font-size:13px; color:var(--fg4); margin-bottom:24px; letter-spacing:.01em;
  }
  .hero-search { margin-bottom:28px; }
  .hero-btns { flex-wrap:wrap; }
  .hero-visual {
    display:flex; align-items:center; justify-content:flex-end;
  }
  .hero-person {
    width:100%; max-width:460px; max-height:540px;
    object-fit:cover;
    border-radius:20px;
    display:block;
  }

  /* ── Stats ticker ── */
  /* uses global .ticker, .ti, .tl, .tv, .td */

  /* ── Calculator cards ── */
  .cards-section { padding:80px 52px; }
  .section-header {
    display:flex; align-items:baseline; justify-content:space-between; margin-bottom:36px;
  }
  .section-title { font-size:28px; font-weight:700; letter-spacing:-.03em; }
  .section-sub { font-size:12px; color:var(--fg4); font-family:var(--mono); }

  .cards-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; }

  .calc-card {
    background:var(--bg1); border:1px solid var(--line); border-radius:14px;
    padding:24px; cursor:pointer; text-align:left;
    font-family:var(--sans); color:var(--fg);
    position:relative; overflow:hidden;
    transition:border-color .22s var(--ease), transform .22s var(--ease), box-shadow .22s var(--ease), background .22s var(--ease);
    display:flex; flex-direction:column;
  }
  .calc-card:hover {
    border-color:var(--line3);
    transform:translateY(-3px);
    box-shadow:0 12px 40px rgba(0,0,0,.11), 0 0 0 1px rgba(0,0,0,.06);
    background:var(--bg2);
  }
  .calc-card:active { transform:translateY(-1px) scale(0.99); }
  .calc-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:1px;
    background:linear-gradient(90deg,transparent,rgba(0,0,0,.05),transparent);
    opacity:0; transition:opacity .22s;
  }
  .calc-card:hover::before { opacity:1; }

  .card-head { display:flex; align-items:center; justify-content:space-between; margin-bottom:18px; }
  .card-num { font-family:var(--mono); font-size:10px; color:var(--fg4); letter-spacing:.08em; }
  .card-title { font-size:18px; font-weight:700; letter-spacing:-.025em; margin-bottom:10px; line-height:1.25; }
  .card-desc { font-size:13px; color:var(--fg3); line-height:1.6; margin-bottom:18px; flex:1; }
  .card-tags { display:flex; gap:8px; flex-wrap:wrap; margin-bottom:18px; }
  .card-tag { font-size:10px; color:var(--fg4); font-family:var(--mono); letter-spacing:.03em; }
  .card-cta-row {
    display:flex; align-items:center; justify-content:space-between;
    padding-top:14px; border-top:1px solid var(--line);
    font-size:12px; color:var(--fg4);
    transition:color .15s;
  }
  .calc-card:hover .card-cta-row { color:var(--fg2); }

  /* ── Trust section ── */
  .trust-section {
    border-top:1px solid var(--line); border-bottom:1px solid var(--line);
    background:var(--bg1); padding:72px 52px;
  }
  .trust-inner { max-width:960px; margin:0 auto; }
  .trust-grid {
    display:grid; grid-template-columns:repeat(4,1fr); gap:0;
    border:1px solid var(--line); border-radius:14px; overflow:hidden;
    margin-top:32px;
  }
  .trust-item {
    padding:32px 28px; border-right:1px solid var(--line);
    transition:background .2s;
  }
  .trust-item:last-child { border-right:none; }
  .trust-item:hover { background:var(--bg2); }
  .trust-num { font-size:40px; font-weight:800; letter-spacing:-.05em; color:var(--fg); margin-bottom:6px; }
  .trust-label { font-size:14px; font-weight:600; color:var(--fg); margin-bottom:4px; }
  .trust-sub { font-size:12px; color:var(--fg4); line-height:1.5; }

  /* ── CTA strip ── */
  .cta-strip {
    padding:100px 52px; text-align:center;
    background:var(--bg);
    border-bottom:1px solid var(--line);
  }
  .cta-inner { max-width:700px; margin:0 auto; }
  .cta-title { font-size:48px; font-weight:800; letter-spacing:-.04em; margin-bottom:16px; }
  .cta-sub { font-size:18px; color:var(--fg2); line-height:1.65; }

  /* ── Persona modal ── */
  .persona-backdrop {
    position:fixed; inset:0; z-index:900;
    background:rgba(0,0,0,.45);
    backdrop-filter:blur(6px);
    display:flex; align-items:center; justify-content:center;
    padding:24px;
  }
  .persona-modal {
    background:#fff; border:1px solid rgba(0,0,0,.08);
    border-radius:20px; padding:36px;
    max-width:560px; width:100%;
    position:relative;
    box-shadow:0 24px 80px rgba(0,0,0,.18), 0 0 0 1px rgba(0,0,0,.04);
  }
  .persona-close {
    position:absolute; top:16px; right:16px;
    width:32px; height:32px; border-radius:50%;
    background:rgba(0,0,0,.06); border:none; cursor:pointer;
    font-size:13px; color:var(--fg3);
    display:flex; align-items:center; justify-content:center;
    transition:background .15s, color .15s;
  }
  .persona-close:hover { background:rgba(0,0,0,.1); color:var(--fg); }
  .persona-grid {
    display:grid; grid-template-columns:1fr 1fr; gap:10px;
  }
  .persona-card {
    display:flex; flex-direction:column; gap:4px;
    padding:18px 16px; border-radius:12px;
    border:1px solid rgba(0,0,0,.09); background:rgba(0,0,0,.02);
    cursor:pointer; text-align:left; font-family:inherit;
    transition:border-color .18s, background .18s, transform .18s, box-shadow .18s;
  }
  .persona-card:hover {
    border-color:var(--fg); background:#fff;
    transform:translateY(-2px);
    box-shadow:0 8px 24px rgba(0,0,0,.1);
  }
  .persona-icon { font-size:28px; margin-bottom:4px; }
  .persona-title { font-size:16px; font-weight:700; color:var(--fg); letter-spacing:-.02em; }
  .persona-sub { font-size:12px; font-weight:500; color:var(--fg3); font-family:var(--mono); }
  .persona-hint { font-size:11px; color:var(--fg4); margin-top:2px; }

  /* ── Persona banner in cards ── */
  .persona-reset {
    font-size:11px; color:var(--fg3); background:none; border:none;
    cursor:pointer; font-family:var(--mono); padding:4px 8px;
    border-radius:6px; transition:color .15s, background .15s;
  }
  .persona-reset:hover { color:var(--fg); background:rgba(0,0,0,.05); }
  .persona-label {
    font-size:10px; font-weight:700; letter-spacing:.1em;
    text-transform:uppercase; color:var(--fg3);
    font-family:var(--mono); margin-bottom:14px;
  }
  .calc-card-rec {
    border-color:rgba(0,0,0,.2);
    background:var(--bg);
  }
  .calc-card-rec:hover { border-color:var(--fg); }
  .badge-rec {
    background:rgba(0,0,0,.08) !important;
    color:var(--fg2) !important;
  }

  /* ── Mobile ── */
  @media (max-width:760px) {
    .update-bar { padding:8px 20px; }
    .nav-center { display:none; }
    .hero { grid-template-columns:1fr; padding:48px 24px; min-height:auto; }
    .hero-title { font-size:36px; }
    .hero-visual { display:none; }
    .cards-section { padding:48px 20px; }
    .cards-grid { grid-template-columns:1fr; }
    .trust-grid { grid-template-columns:1fr 1fr; }
    .trust-section { padding:48px 20px; }
    .cta-strip { padding:64px 24px; }
    .cta-title { font-size:32px; }
    :global(.foot) { grid-template-columns:1fr 1fr; padding:40px 24px; gap:24px; }
    .persona-grid { grid-template-columns:1fr 1fr; gap:8px; }
    .persona-modal { padding:24px 20px; }
    .persona-title { font-size:14px; }
    .section-header { flex-direction:column; align-items:flex-start; gap:10px; }
  }
</style>
