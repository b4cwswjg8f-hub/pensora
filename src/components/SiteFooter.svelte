<script>
  import { createEventDispatcher } from 'svelte';
  import Logo from './Logo.svelte';
  import { CARDS, RATGEBER, VERGLEICHE } from '../lib/data.js';

  const dispatch = createEventDispatcher();
  const base = import.meta.env.BASE_URL;
</script>

<footer class="foot">
  <div>
    <button class="brand mb-[14px]" on:click={() => dispatch('navigate', 'hub')}>
      <Logo /> Pensora
    </button>
    <p>Klare Zahlen. Unabhängige Beratung.</p>
    <p class="text-[13px] mt-2">Niall Bradfield<br/>unabhängiger Finanzberater, Stuttgart</p>
    <div class="mt-3 text-[11px] text-fg4 font-mono">© 2026 Pensora</div>
  </div>

  <div>
    <h5>Rechner</h5>
    {#each CARDS as c}
      <a on:click={() => dispatch('navigate', c.id)}>{c.title}</a>
    {/each}
  </div>

  <div>
    <h5>Ratgeber</h5>
    {#each RATGEBER as r}
      <a href="{base}{r.href}">{r.label}</a>
    {/each}
  </div>

  <div>
    <h5>Vergleiche & Mehr</h5>
    {#each VERGLEICHE as v}
      <a href="{base}{v.href}">{v.label}</a>
    {/each}
    <a href="{import.meta.env.BASE_URL}wie-wird-berechnet/">Wie wird berechnet?</a>
    <a href="{import.meta.env.BASE_URL}ueber-uns/">Über uns</a>
    <a href="{import.meta.env.BASE_URL}kontakt/">Kontakt</a>
    <a class="mt-2 block">Impressum</a>
    <a>Datenschutz</a>
  </div>
</footer>
