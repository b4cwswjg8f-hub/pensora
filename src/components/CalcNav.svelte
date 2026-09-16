<script>
  import { createEventDispatcher } from 'svelte';
  import Logo from './Logo.svelte';
  import { BRAND_NAME } from '../lib/data.js';

  const dispatch = createEventDispatcher();
  export let title = '';
</script>

<nav class="nav">
  <div class="flex items-center gap-4">
    <button class="brand" on:click={() => dispatch('back')}><Logo /> {BRAND_NAME}</button>
    <span class="text-line2 text-base" aria-hidden="true">/</span>
    <span class="text-fg2 text-[14px]">{title}</span>
  </div>
  <div class="flex items-center gap-2">
    <button class="btn btng" on:click={() => dispatch('back')}>← Home</button>
  </div>
</nav>
