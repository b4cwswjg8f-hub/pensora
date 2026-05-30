<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  export let card;
  export let recommended = false;
</script>

<button
  class="calc-card"
  class:calc-card-rec={recommended}
  on:click={() => dispatch('select', card.id)}
>
  <div class="card-head">
    <span class="card-num">{card.num}</span>
    <span class="badge" class:badge-rec={recommended}>{card.badge}</span>
  </div>
  <h3 class="card-title">{card.title}</h3>
  <p class="card-desc">{card.desc}</p>
  <div class="card-tags">
    {#each card.tags as tag}<span class="card-tag">{tag}</span>{/each}
  </div>
  <div class="card-cta-row">
    <span>Rechner starten</span>
    <svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <path d="M3 8h10M9 4l4 4-4 4"/>
    </svg>
  </div>
</button>
