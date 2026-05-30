<script>
  import { createEventDispatcher } from 'svelte';
  import HubNav from '../components/HubNav.svelte';
  import UpdateBanner from '../components/UpdateBanner.svelte';
  import CalcCard from '../components/CalcCard.svelte';
  import SiteFooter from '../components/SiteFooter.svelte';
  import Search from '../components/Search.svelte';
  import { CARDS, STATS, PERSONAS, BOOK_URL } from '../lib/data.js';

  const dispatch = createEventDispatcher();
  const go = (name) => dispatch('navigate', name);
  const book = () => window.open(BOOK_URL, '_blank');

  let showPersonaModal = false;
  let selectedPersona = null;

  function selectPersona(p) {
    selectedPersona = p;
    showPersonaModal = false;
    setTimeout(() => {
      document.getElementById('rechner')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 120);
  }

  $: recCards   = selectedPersona ? CARDS.filter(c =>  selectedPersona.calcs.includes(c.id)) : [];
  $: otherCards = selectedPersona ? CARDS.filter(c => !selectedPersona.calcs.includes(c.id)) : CARDS;
</script>

<div>
  <!-- Update banner -->
  <UpdateBanner>
    <span class="update-entry">AV-Depot 2027 — Grundzulage bestätigt: 540 €/Jahr · Stand 29.05.2026</span>
    <span class="update-sep">·</span>
    <span class="update-entry">Rentenwert 2026: 42,52 € · DRV · ab 1. Juli 2026</span>
    <span class="update-sep">·</span>
    <span class="update-entry">Rürup-Höchstbetrag 2026: 30.826 € · § 10 EStG</span>
  </UpdateBanner>

  <HubNav on:navigate={e => go(e.detail)} />

  <!-- Persona modal -->
  {#if showPersonaModal}
    <div class="persona-backdrop" on:click|self={() => showPersonaModal = false}>
      <div class="persona-modal">
        <button class="persona-close" on:click={() => showPersonaModal = false}>✕</button>
        <div class="ey mb-2">Personalisiert starten</div>
        <h2 class="text-[26px] font-bold tracking-[-0.03em] text-fg mb-[6px]">Wer bist du?</h2>
        <p class="text-[13px] text-fg3 mb-6 leading-[1.5]">Wir zeigen dir die passenden Rechner und Artikel — kostenlos und anonym.</p>
        <div class="persona-grid">
          {#each PERSONAS as p}
            <button class="persona-card" on:click={() => selectPersona(p)}>
              <span class="persona-icon">{p.icon}</span>
              <span class="persona-title">{p.title}</span>
              <span class="persona-sub">{p.sub}</span>
              <span class="persona-hint">{p.hint}</span>
            </button>
          {/each}
        </div>
        <p class="text-[11px] text-fg4 text-center mt-5">Keine Anmeldung · Keine Daten gespeichert</p>
      </div>
    </div>
  {/if}

  <!-- Scrollable page -->
  <div class="vscr">

    <!-- ── HERO ── -->
    <section class="hero">
      <div class="hero-content">
        <div class="ey mb-4">Pension · Rente · Altersvorsorge · 2026</div>
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
        <div class="flex flex-wrap items-center gap-3">
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
      {#each STATS as s}
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
        <div class="flex items-center gap-3">
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
        <div class="cards-grid mb-6">
          {#each recCards as c}
            <CalcCard card={c} recommended on:select={e => go(e.detail)} />
          {/each}
        </div>
        {#if otherCards.length > 0}
          <div class="persona-label text-fg4">Weitere Rechner</div>
        {/if}
      {/if}

      <div class="cards-grid">
        {#each otherCards as c}
          <CalcCard card={c} on:select={e => go(e.detail)} />
        {/each}
      </div>
    </section>

    <!-- ── TRUST ── -->
    <section class="trust-section">
      <div class="trust-inner">
        <div class="ey mb-4">Warum Pensora</div>
        <div class="trust-grid">
          {#each [
            { num: '100 %', label: 'Lokal im Browser',  sub: 'Keine Daten verlassen dein Gerät' },
            { num: '0',     label: 'Login nötig',        sub: 'Kein Konto, kein Formular, keine Wartezeit' },
            { num: '100+',  label: 'Lehrer beraten',     sub: 'Niall Bradfield, Stuttgart' },
            { num: '6',     label: 'Rechner',            sub: 'Alle nach geprüften gesetzlichen Formeln' },
          ] as item}
            <div class="trust-item">
              <div class="trust-num">{item.num}</div>
              <div class="trust-label">{item.label}</div>
              <div class="trust-sub">{item.sub}</div>
            </div>
          {/each}
        </div>
      </div>
    </section>

    <!-- ── CTA ── -->
    <section class="cta-strip">
      <div class="cta-inner">
        <h2 class="cta-title">Zahlen allein reichen nicht.</h2>
        <p class="cta-sub">30 Minuten, kostenlos — Niall Bradfield bespricht deine persönliche Situation und was deine Zahlen bedeuten.</p>
        <div class="flex items-center justify-center gap-3 mt-8">
          <button class="btn btnp btnlg" on:click={book}>Kostenloses Erstgespräch buchen →</button>
          <a class="btn btno btnlg" href="ueber-uns/">Über Pensora</a>
        </div>
      </div>
    </section>

    <SiteFooter on:navigate={e => go(e.detail)} />
  </div>
</div>
