<script>
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  export let step = 0;
  export let labels = [];
  export let calcLabel = 'Berechnen →';
  export let withStepName = false;

  $: isFirst = step === 0;
  $: isLast  = step === labels.length - 1;
  $: nextLabel = isLast
    ? calcLabel
    : withStepName && labels[step + 1]
      ? `Weiter zu ${labels[step + 1].label} →`
      : 'Weiter →';
</script>

<div class="flex items-center justify-between mt-9 pt-5 border-t border-line">
  <button
    class="btn btnlg"
    class:opacity-30={isFirst}
    class:pointer-events-none={isFirst}
    on:click={() => dispatch('back')}
  >← Zurück</button>
  <div class="flex items-center gap-3">
    <button class="btn btng" on:click={() => dispatch('next')}>Überspringen</button>
    <button class="btn btnp btnlg" on:click={() => dispatch('next')}>{nextLabel}</button>
  </div>
</div>
