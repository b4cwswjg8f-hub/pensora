<script>
  import { createEventDispatcher } from 'svelte';
  import Logo from './Logo.svelte';
  import { CARDS, RATGEBER, VERGLEICHE, UPDATES, BOOK_URL } from '../lib/data.js';

  const dispatch = createEventDispatcher();
  const go = (id) => dispatch('navigate', id);
  const book = () => window.open(BOOK_URL, '_blank');
  const base = import.meta.env.BASE_URL;
</script>

<nav class="nav">
  <button class="brand" on:click={() => go('hub')}><Logo /> Pensora</button>

  <div class="nav-center">
    <!-- Rechner -->
    <div class="ddwrap">
      <button class="nav-link ddtrig">
        Rechner
        <svg width="9" height="5" viewBox="0 0 10 6" fill="currentColor"><path d="M0 0l5 6 5-6z"/></svg>
      </button>
      <div class="ddmenu dd-wide">
        <div class="dd-grid">
          {#each CARDS as c}
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

    <!-- Ratgeber -->
    <div class="ddwrap">
      <button class="nav-link ddtrig">
        Ratgeber
        <svg width="9" height="5" viewBox="0 0 10 6" fill="currentColor"><path d="M0 0l5 6 5-6z"/></svg>
      </button>
      <div class="ddmenu dd-wide">
        <div class="dd-section-label">Bundesland & Thema</div>
        <div class="dd-grid dd-grid-3">
          {#each RATGEBER as r}
            <a class="dditem" href="{base}{r.href}"><span class="dd-title">{r.label}</span></a>
          {/each}
        </div>
      </div>
    </div>

    <!-- Vergleiche -->
    <div class="ddwrap">
      <button class="nav-link ddtrig">
        Vergleiche
        <svg width="9" height="5" viewBox="0 0 10 6" fill="currentColor"><path d="M0 0l5 6 5-6z"/></svg>
      </button>
      <div class="ddmenu" style="min-width:260px">
        {#each VERGLEICHE as v}
          <a class="dditem" href="{base}{v.href}"><span class="dd-title">{v.label}</span></a>
        {/each}
      </div>
    </div>

    <!-- Updates -->
    <div class="ddwrap">
      <button class="nav-link ddtrig dd-updates-trig">
        Updates
        <span class="dd-updates-dot"></span>
        <svg width="9" height="5" viewBox="0 0 10 6" fill="currentColor"><path d="M0 0l5 6 5-6z"/></svg>
      </button>
      <div class="ddmenu" style="min-width:340px">
        <div class="dd-section-label">Aktuelle Meldungen · 2026</div>
        {#each UPDATES as u}
          <a class="dditem" href="{base}{u.href}">
            <span class="dd-text">
              <span class="dd-title flex items-center gap-[6px]">
                {#if u.dot}<span class="dd-updates-dot"></span>{/if}
                {u.label}
              </span>
              <span class="dd-badge">{u.sub}</span>
            </span>
          </a>
        {/each}
      </div>
    </div>

    <a class="nav-link" href="{import.meta.env.BASE_URL}ueber-uns/">Über uns</a>
  </div>

  <div class="flex items-center gap-2">
    <a class="nav-link mr-1" href="{import.meta.env.BASE_URL}kontakt/">Kontakt</a>
    <button
      class="btn btnp"
      style="height:36px;padding:0 18px;font-size:13px;border-radius:8px"
      on:click={book}
    >Termin buchen</button>
  </div>
</nav>
