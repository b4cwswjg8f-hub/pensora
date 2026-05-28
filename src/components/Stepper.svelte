<script>
  export let total = 1;
  export let current = 0; // 0-indexed
</script>

<div class="stepper">
  {#each Array(total) as _, i}
    <div class="step" class:done={i < current} class:active={i === current}></div>
  {/each}
</div>
