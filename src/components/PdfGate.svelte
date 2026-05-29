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
    email = localStorage.getItem('pensora_email') || '';
  }

  function validate() {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !re.test(email)) {
      error = 'Bitte eine gültige E-Mail-Adresse eingeben.';
      return false;
    }
    error = '';
    return true;
  }

  function submit() {
    if (!validate()) return;
    sending = true;
    localStorage.setItem('pensora_email', email);

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
    <div class="gate-modal" on:click|stopPropagation role="dialog" aria-modal="true" aria-label="PDF herunterladen">
      <div class="gate-icon">
        {#if done}
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#4ade80" stroke-width="2" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
        {:else}
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="11" x2="12" y2="17"/><polyline points="9 14 12 17 15 14"/></svg>
        {/if}
      </div>

      {#if done}
        <h2 class="gate-title" style="color:#4ade80">PDF wird erstellt…</h2>
        <p class="gate-sub">Dein Druckdialog öffnet sich gleich.</p>
      {:else}
        <h2 class="gate-title">Ergebnis als PDF speichern</h2>
        <p class="gate-sub">Gib deine E-Mail-Adresse ein — wir schicken dir wichtige Aktualisierungen zu Pensionswerten, Rentenwert und Förderungen. Einmal, selten, nur wenn es zählt.</p>

        <div class="gate-field">
          <input
            type="email"
            bind:value={email}
            placeholder="deine@email.de"
            class="gate-input"
            class:err={!!error}
            on:keydown={onKey}
            autocomplete="email"
          />
          {#if error}<p class="gate-error">{error}</p>{/if}
        </div>

        <button class="gate-btn" on:click={submit} disabled={sending}>
          {#if sending}
            <span class="gate-spinner"></span> Wird vorbereitet…
          {:else}
            PDF herunterladen →
          {/if}
        </button>
        <p class="gate-legal">Kein Spam. Abmeldung jederzeit. Daten werden nicht weitergegeben.</p>
      {/if}

      <button class="gate-close" on:click={close} aria-label="Schließen">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>
  </div>
{/if}

<style>
  .gate-backdrop {
    position: fixed; inset: 0; z-index: 1000;
    background: rgba(0,0,0,.75);
    backdrop-filter: blur(8px);
    display: flex; align-items: center; justify-content: center;
    padding: 24px;
    animation: fadeIn .18s ease both;
  }
  .gate-modal {
    position: relative;
    background: #0f0f0f;
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 20px;
    padding: 44px 40px 36px;
    max-width: 420px; width: 100%;
    box-shadow: 0 24px 80px rgba(0,0,0,.9);
    animation: slideUp .22s cubic-bezier(0.16,1,0.3,1) both;
  }
  .gate-icon {
    width: 56px; height: 56px; border-radius: 14px;
    background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.1);
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 20px; color: #fafafa;
  }
  .gate-title {
    font-size: 22px; font-weight: 700; letter-spacing: -.03em;
    color: #fafafa; margin-bottom: 10px;
  }
  .gate-sub {
    font-size: 14px; color: #6b6b6b; line-height: 1.6; margin-bottom: 24px;
  }
  .gate-field { margin-bottom: 14px; }
  .gate-input {
    width: 100%; height: 50px; padding: 0 16px;
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.14);
    border-radius: 10px;
    color: #fafafa; font-size: 16px; font-family: inherit;
    outline: none; transition: border-color .15s, background .15s;
    -webkit-text-fill-color: #fafafa;
  }
  .gate-input:focus { border-color: rgba(255,255,255,.4); background: rgba(255,255,255,.06); }
  .gate-input.err { border-color: #FF6B6B; }
  .gate-error { font-size: 12px; color: #FF6B6B; margin-top: 6px; }
  .gate-btn {
    width: 100%; height: 52px;
    background: #fafafa; color: #000;
    border: none; border-radius: 10px;
    font-size: 15px; font-weight: 700; font-family: inherit;
    cursor: pointer; letter-spacing: -.01em;
    display: flex; align-items: center; justify-content: center; gap: 8px;
    transition: background .15s, transform .1s;
  }
  .gate-btn:hover:not(:disabled) { background: #e8e8e8; }
  .gate-btn:active { transform: scale(0.98); }
  .gate-btn:disabled { opacity: .6; cursor: default; }
  .gate-spinner {
    width: 16px; height: 16px; border: 2px solid rgba(0,0,0,.2);
    border-top-color: #000; border-radius: 50%;
    animation: spin .7s linear infinite;
  }
  .gate-legal {
    font-size: 11px; color: #3d3d3d; text-align: center;
    margin-top: 12px; line-height: 1.5;
  }
  .gate-close {
    position: absolute; top: 16px; right: 16px;
    width: 32px; height: 32px; border-radius: 8px;
    border: none; background: rgba(255,255,255,.06);
    color: #6b6b6b; display: flex; align-items: center; justify-content: center;
    cursor: pointer; transition: background .15s, color .15s;
  }
  .gate-close:hover { background: rgba(255,255,255,.1); color: #fafafa; }

  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
  @keyframes slideUp {
    from { opacity: 0; transform: translateY(16px) scale(.97); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
  }
  @keyframes spin { to { transform: rotate(360deg); } }
</style>
