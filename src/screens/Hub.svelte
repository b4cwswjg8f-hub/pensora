<script>
  import { createEventDispatcher } from 'svelte';
  import HubNav from '../components/HubNav.svelte';
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
  <HubNav on:navigate={e => go(e.detail)} />

  <!-- Persona modal -->
  {#if showPersonaModal}
    <div class="persona-backdrop" on:click|self={() => showPersonaModal = false}>
      <div class="persona-modal">
        <button class="persona-close" on:click={() => showPersonaModal = false}>✕</button>
        <div class="ey mb-2">Start Personalized</div>
        <h2 class="text-[26px] font-bold tracking-[-0.03em] text-fg mb-[6px]">Who are you?</h2>
        <p class="text-[13px] text-fg3 mb-6 leading-[1.5]">We'll show you the right calculators and guides — free and anonymous.</p>
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
        <p class="text-[11px] text-fg4 text-center mt-5">No sign-up · No data stored</p>
      </div>
    </div>
  {/if}

  <!-- Scrollable page -->
  <div class="vscr">

    <!-- ── HERO ── -->
    <section class="hero">
      <div class="hero-content">
        <div class="ey mb-4">Investing · Tax · Real Estate · 2026</div>
        <h1 class="hero-title">
          Build wealth.<br/><span class="hero-muted">In your new home.</span>
        </h1>
        <p class="hero-lead">
          Five precise calculators for expats in Germany — pension, ETF investing, taxes, cashflow and insurance.
        </p>
        <p class="hero-trust">Free, anonymous, no obligation. Just clear numbers — so you know where you stand.</p>
        <div class="hero-search">
          <Search on:navigate={e => go(e.detail)} />
        </div>
        <div class="flex flex-wrap items-center gap-3">
          <button class="btn btnp btnlg" on:click={() => showPersonaModal = true}>Start → What fits me?</button>
          <button class="btn btno btnlg" on:click={book}>Free Consultation</button>
        </div>
      </div>
      <div class="hero-visual">
        <img
          src="{import.meta.env.BASE_URL}assets/hero-person.png"
          alt="Thrive Abroad user planning their financial future in Germany"
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
        <h2 class="section-title">{selectedPersona ? `For you — ${selectedPersona.title}` : 'All Calculators'}</h2>
        <div class="flex items-center gap-3">
          {#if selectedPersona}
            <button class="persona-reset" on:click={() => selectedPersona = null}>× Show all</button>
          {:else}
            <span class="section-sub">Verified formulas under German law · No sign-up</span>
          {/if}
          <button class="btn btng" style="font-size:12px;height:32px;padding:0 14px" on:click={() => showPersonaModal = true}>
            {selectedPersona ? '↺ Change persona' : '→ Filter for me'}
          </button>
        </div>
      </div>

      {#if selectedPersona && recCards.length > 0}
        <div class="persona-label">Recommended for {selectedPersona.title}</div>
        <div class="cards-grid mb-6">
          {#each recCards as c}
            <CalcCard card={c} recommended on:select={e => go(e.detail)} />
          {/each}
        </div>
        {#if otherCards.length > 0}
          <div class="persona-label text-fg4">More Calculators</div>
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
        <div class="ey mb-4">Why Thrive Abroad</div>
        <div class="trust-grid">
          {#each [
            { num: '100 %', label: 'Runs in Your Browser', sub: 'Your data never leaves your device' },
            { num: '0',     label: 'Login Required',       sub: 'No account, no forms, no waiting' },
            { num: 'DE',    label: 'German Tax Law',       sub: 'Built for the rules of your new home' },
            { num: '5',     label: 'Calculators',          sub: 'All built on verified legal formulas' },
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
        <h2 class="cta-title">Numbers alone aren't enough.</h2>
        <p class="cta-sub">30 minutes, free — Niall Bradfield walks through your personal situation and what your numbers actually mean.</p>
        <div class="flex items-center justify-center gap-3 mt-8">
          <button class="btn btnp btnlg" on:click={book}>Book a Free Consultation →</button>
          <a class="btn btno btnlg" href="ueber-uns/">About Thrive Abroad</a>
        </div>
      </div>
    </section>

    <SiteFooter on:navigate={e => go(e.detail)} />
  </div>
</div>
