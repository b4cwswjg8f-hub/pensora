<script>
  import { createEventDispatcher } from 'svelte';
  export let show = false;

  const dispatch = createEventDispatcher();

  let email = '';
  let error = '';
  let sending = false;
  let done = false;

  // Pre-fill from localStorage if user entered before
  if (typeof localStorage !== 'undefined') {
    email = localStorage.getItem('thrive_abroad_email') || '';
  }

  function validate() {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !re.test(email)) {
      error = 'Please enter a valid email address.';
      return false;
    }
    error = '';
    return true;
  }

  function submit() {
    if (!validate()) return;
    sending = true;
    localStorage.setItem('thrive_abroad_email', email);

    // Brief visual confirmation, then print
    setTimeout(() => {
      done = true;
      setTimeout(() => {
        window.print();
        close();
      }, 600);
    }, 500);
  }

  function close() {
    show = false;
    sending = false;
    done = false;
    error = '';
  }

  function onKey(e) {
    if (e.key === 'Escape') close();
    if (e.key === 'Enter') submit();
  }
</script>

{#if show}
  <!-- Backdrop -->
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <!-- svelte-ignore a11y-no-static-element-interactions -->
  <div class="gate-backdrop" on:click={close}>
    <!-- Modal -->
    <div class="gate-modal" on:click|stopPropagation role="dialog" aria-modal="true" aria-label="Download PDF">
      <div class="gate-icon">
        {#if done}
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#4ade80" stroke-width="2" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
        {:else}
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="11" x2="12" y2="17"/><polyline points="9 14 12 17 15 14"/></svg>
        {/if}
      </div>

      {#if done}
        <h2 class="gate-title" style="color:#4ade80">Preparing your PDF…</h2>
        <p class="gate-sub">Your print dialog will open shortly.</p>
      {:else}
        <h2 class="gate-title">Save Your Result as a PDF</h2>
        <p class="gate-sub">Enter your email — we'll send you occasional updates on investing, tax and financial planning for expats in Germany. Rarely, and only when it matters.</p>

        <div class="gate-field">
          <input
            type="email"
            bind:value={email}
            placeholder="you@email.com"
            class="gate-input"
            class:err={!!error}
            on:keydown={onKey}
            autocomplete="email"
          />
          {#if error}<p class="gate-error">{error}</p>{/if}
        </div>

        <button class="gate-btn" on:click={submit} disabled={sending}>
          {#if sending}
            <span class="gate-spinner"></span> Preparing…
          {:else}
            Download PDF →
          {/if}
        </button>
        <p class="gate-legal">No spam. Unsubscribe anytime. Your data is never shared.</p>
      {/if}

      <button class="gate-close" on:click={close} aria-label="Close">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>
  </div>
{/if}
