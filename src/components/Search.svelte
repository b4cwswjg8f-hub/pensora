<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  // ─── Search index ──────────────────────────────────────────────
  const INDEX = [
    // Calculators (SPA navigate)
    { type:'calc', id:'depot',        title:'ETF Savings Plan Calculator', sub:'Compound interest, real return, the 4% rule', tags:['etf','depot','investing','compound interest','savings plan','4% rule'] },
    { type:'calc', id:'rente',        title:'German Pension Calculator',   sub:'Statutory pension § 64 SGB VI',                tags:['pension','rente','state pension','pension gap','entgeltpunkte'] },
    { type:'calc', id:'ruerup',       title:'Rürup Pension Calculator',    sub:'Basic pension § 10 EStG, tax advantage',       tags:['rürup','ruerup','tax','basic pension','deduction'] },
    { type:'calc', id:'cashflow',     title:'Cashflow Calculator',         sub:'Monthly budget vs. the 50/15/15 rule',         tags:['cashflow','budget','savings rate','emergency fund'] },
    { type:'calc', id:'versicherung', title:'Insurance Check',             sub:'Over- and under-insurance vs. market average', tags:['insurance','versicherung','pkv','gkv','disability'] },

    // Guide articles (static pages)
    { type:'article', href:'etf-investing-expats-germany/',    title:'ETF Investing for Expats in Germany',    sub:'Broker accounts, taxes, and getting started',   tags:['etf','stock market','investing','broker','depot','abgeltungssteuer'] },
    { type:'article', href:'buying-property-germany-expat/',   title:'Buying Property in Germany as a Foreigner', sub:'Mortgages, Grunderwerbsteuer, the Notar process', tags:['property','real estate','mortgage','baufinanzierung','grunderwerbsteuer'] },
    { type:'article', href:'inheritance-tax-germany-expats/',  title:'Inheritance Tax for Expats in Germany',  sub:'Erbschaftsteuer basics for cross-border estates', tags:['inheritance','erbschaftsteuer','estate','tax class'] },
    { type:'article', href:'investing-for-kids-germany/',      title:'Investment Accounts for Kids in Germany', sub:'Custodial accounts and junior depots',          tags:['kids','children','junior depot','custodial','family'] },
    { type:'article', href:'tax-residency-germany-expats/',    title:'German Tax Residency for Expats',        sub:'The 183-day rule and double-tax treaties',      tags:['tax residency','183 day rule','double tax treaty','tax optimization'] },
    { type:'article', href:'rsu-stock-options-tax-germany/',   title:'RSUs & Stock Options: Taxation in Germany', sub:'Equity compensation for tech employees',       tags:['rsu','stock options','equity','tech','it professional'] },
    { type:'article', href:'us-citizens-investing-germany-pfic/', title:'US Citizens in Germany: Avoiding the PFIC Trap', sub:'PFIC and FATCA basics for American expats', tags:['us citizen','pfic','fatca','american expat'] },
    { type:'article', href:'financial-planning-expats-germany/', title:'Holistic Financial Planning for Expats', sub:'Bringing it all together',                    tags:['financial planning','holistic','overview'] },
  ];

  // ─── State ─────────────────────────────────────────────────────
  let query = '';
  let open = false;
  let focused = -1;
  let inputEl;

  $: results = query.trim().length < 2 ? [] : (() => {
    const q = query.toLowerCase().trim();
    const scored = INDEX.map(item => {
      const titleMatch = item.title.toLowerCase().includes(q) ? 3 : 0;
      const subMatch   = item.sub.toLowerCase().includes(q)   ? 1 : 0;
      const tagMatch   = item.tags.some(t => t.includes(q))   ? 2 : 0;
      // Also check token overlap
      const qTokens = q.split(/\s+/);
      const tokenScore = qTokens.filter(tok => tok.length > 1 && item.tags.some(t => t.includes(tok))).length;
      const score = titleMatch + subMatch + tagMatch + tokenScore;
      return { ...item, score };
    }).filter(i => i.score > 0).sort((a,b) => b.score - a.score);
    return scored.slice(0, 8);
  })();

  $: open = results.length > 0 && query.trim().length >= 2;

  function select(item) {
    if (item.type === 'calc') {
      dispatch('navigate', item.id);
    } else {
      window.location.href = item.href;
    }
    query = '';
    focused = -1;
  }

  function onKey(e) {
    if (!open) return;
    if (e.key === 'ArrowDown') { e.preventDefault(); focused = Math.min(focused+1, results.length-1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); focused = Math.max(focused-1, 0); }
    else if (e.key === 'Enter' && focused >= 0) { e.preventDefault(); select(results[focused]); }
    else if (e.key === 'Escape') { query = ''; focused = -1; }
  }

  function clickOutside(node) {
    const handle = e => { if (!node.contains(e.target)) { query = ''; focused = -1; } };
    document.addEventListener('click', handle, true);
    return { destroy() { document.removeEventListener('click', handle, true); } };
  }
</script>

<div class="search-wrap" use:clickOutside>
  <div class="search-box" class:search-open={open}>
    <svg class="search-icon" width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round">
      <circle cx="6.5" cy="6.5" r="4.5"/><path d="M10.5 10.5l3 3"/>
    </svg>
    <input
      bind:this={inputEl}
      bind:value={query}
      on:keydown={onKey}
      placeholder="Search calculators, guides…"
      class="search-input"
      autocomplete="off"
      spellcheck="false"
    />
    {#if query}
      <button class="search-clear" on:click={() => { query=''; inputEl.focus(); }}>✕</button>
    {/if}
  </div>

  {#if open}
    <div class="search-dropdown">
      {#each results as item, i}
        <button
          class="search-item"
          class:search-item-focused={focused === i}
          on:click={() => select(item)}
          on:mouseenter={() => focused = i}
        >
          <span class="search-item-type">{item.type === 'calc' ? '⊞ Calculator' : '✦ Guide'}</span>
          <span class="search-item-body">
            <span class="search-item-title">{item.title}</span>
            <span class="search-item-sub">{item.sub}</span>
          </span>
          <svg class="search-item-arrow" width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg>
        </button>
      {/each}
    </div>
  {/if}
</div>
