<script>
  import { createEventDispatcher } from 'svelte';
  import Logo from './Logo.svelte';
  import { CARDS, RATGEBER, VERGLEICHE, BRAND_NAME } from '../lib/data.js';

  const dispatch = createEventDispatcher();
  const base = import.meta.env.BASE_URL;
</script>

<footer class="foot">
  <div>
    <button class="brand mb-[14px]" on:click={() => dispatch('navigate', 'hub')}>
      <Logo /> {BRAND_NAME}
    </button>
    <p>Financial clarity for expats building a life in Germany.</p>
    <p class="text-[13px] mt-2">Niall Bradfield<br/>Independent Financial Advisor, Stuttgart</p>
    <div class="mt-3 text-[11px] text-fg4 font-mono">© 2026 {BRAND_NAME}</div>
  </div>

  <div>
    <h5>Calculators</h5>
    {#each CARDS as c}
      <a on:click={() => dispatch('navigate', c.id)}>{c.title}</a>
    {/each}
  </div>

  <div>
    <h5>Guides</h5>
    {#each RATGEBER as r}
      <a href="{base}{r.href}">{r.label}</a>
    {/each}
  </div>

  <div>
    <h5>Comparisons & More</h5>
    {#each VERGLEICHE as v}
      <a href="{base}{v.href}">{v.label}</a>
    {/each}
    <a href="{import.meta.env.BASE_URL}ueber-uns/">About</a>
    <a href="{import.meta.env.BASE_URL}kontakt/">Contact</a>
    <a class="mt-2 block" href="{import.meta.env.BASE_URL}impressum/">Impressum</a>
    <a href="{import.meta.env.BASE_URL}impressum/#datenschutz">Privacy Policy</a>
  </div>
</footer>
