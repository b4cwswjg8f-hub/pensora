<script>
  import { createEventDispatcher } from 'svelte';
  import TopicIcon from './TopicIcon.svelte';
  import { BOOK_URL } from '../lib/data.js';

  export let topic;
  export let reverse = false;

  const dispatch = createEventDispatcher();
  const goCalc = () => dispatch('navigate', topic.calc);
  const book = () => window.open(BOOK_URL, '_blank');
</script>

<article class="topic-row" class:topic-row-rev={reverse} style="--accent: var(--color-{topic.accent})">
  <div class="topic-copy">
    <div class="ey-pill topic-eyebrow">{topic.eyebrow}</div>
    <h3 class="topic-title">{topic.title}</h3>
    {#each topic.paragraphs as p}
      <p class="topic-p">{p}</p>
    {/each}

    <div class="topic-cta-row">
      <button class="btn btnp btnlg topic-btn-primary" on:click={goCalc}>{topic.calcLabel} →</button>
      <button class="btn btno btnlg" on:click={book}>Need Help? Request Expert Opinion</button>
    </div>
  </div>

  <div class="topic-visual">
    <TopicIcon icon={topic.icon} accent={topic.accent} />
    <div class="topic-fact">
      <div class="topic-fact-value">{topic.fact.value}</div>
      <div class="topic-fact-label">{topic.fact.label}</div>
    </div>
  </div>
</article>
