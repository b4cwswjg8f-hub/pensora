<script>
  import Stepper from './Stepper.svelte';

  export let labels = [];
  export let step = 0;

  $: s = labels[step];
  $: pct = Math.round(step / labels.length * 100);
</script>

<div class="calc-stepper">
  <div class="flex items-center justify-between mb-[10px]">
    <div class="flex items-center gap-3">
      <span class="font-mono text-xs text-fg3 tracking-[.08em] uppercase">
        Schritt {String(step + 1).padStart(2, '0')} · {String(labels.length).padStart(2, '0')}
      </span>
      <span class="text-[15px] font-medium">{s?.label}</span>
    </div>
    <span class="font-mono text-[13px]">{pct} %</span>
  </div>
  <Stepper total={labels.length} current={step} />
</div>
