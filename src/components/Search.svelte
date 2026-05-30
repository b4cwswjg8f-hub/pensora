<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  // ─── Search index ──────────────────────────────────────────────
  const INDEX = [
    // Rechner (SPA navigate)
    { type:'calc', id:'pension',      title:'Pensionsrechner',      sub:'Beamtenpension § 14 BeamtVG berechnen',    tags:['pension','beamte','ruhegehalt','dienstzeit','pension berechnen','beamtenpension','lehrer pension'] },
    { type:'calc', id:'rente',        title:'Rentenrechner',        sub:'Gesetzliche Rente § 64 SGB VI',            tags:['rente','rentenrechner','gesetzliche rente','entgeltpunkte','rentenlücke','rente berechnen'] },
    { type:'calc', id:'depot',        title:'AV-Depot-Rechner',     sub:'ETF-Altersvorsorgedepot, Zinseszins',      tags:['depot','etf','altersvorsorge','av depot','zinseszins','sparen','altersvorsorgedepot'] },
    { type:'calc', id:'ruerup',       title:'Rürup-Rechner',        sub:'Basisrente § 10 EStG, Steuervorteil',      tags:['rürup','ruerup','basisrente','steuer','steuervorteil','sonderausgaben'] },
    { type:'calc', id:'cashflow',     title:'Cashflow-Rechner',     sub:'Monatlichen Cashflow analysieren',          tags:['cashflow','ausgaben','budget','sparen','haushalt','sparquote'] },
    { type:'calc', id:'versicherung', title:'Versicherungscheck',   sub:'Über- und Unterversicherung prüfen',        tags:['versicherung','versicherungscheck','pkv','gkv','berufsunfähigkeit','bu'] },

    // Ratgeber-Artikel (static pages)
    { type:'article', href:'altersvorsorgedepot-2027/',         title:'Altersvorsorgedepot 2027',            sub:'Das neue geförderte ETF-Depot ab 2027',         tags:['altersvorsorgedepot','av depot','2027','riester nachfolger','grundzulage','etf depot','depot news','av news','förderung','zulage'] },
    { type:'article', href:'riester-nachfolger/',               title:'Riester Nachfolger 2027',             sub:'Was kommt nach Riester?',                       tags:['riester','riester nachfolger','av depot','2027','reform'] },
    { type:'article', href:'fruehstartrente-kinder/',           title:'Frühstartrente für Kinder',           sub:'Altersvorsorge ab Geburt — 10 €/Monat vom Staat', tags:['frühstartrente','kinder','altersvorsorge kinder','früh anfangen'] },
    { type:'article', href:'altersvorsorgedepot-beamte/',       title:'AV-Depot für Beamte',                 sub:'Lohnt sich das neue Depot für Beamte?',         tags:['beamte','altersvorsorgedepot','av depot beamte','förderung beamte'] },
    { type:'article', href:'altersvorsorgedepot-foerderung/',   title:'AV-Depot Förderung 2027',             sub:'Grundzulage 540 €, Kinderzulage 300 €',         tags:['förderung','grundzulage','kinderzulage','steuerbonus','av depot','förderung 2027'] },
    { type:'article', href:'rentenluecke-2026/',                title:'Rentenlücke 2026',                    sub:'Wie groß ist die Versorgungslücke wirklich?',    tags:['rentenlücke','versorgungslücke','rente reicht nicht','lücke','altersarmut','2026'] },
    { type:'article', href:'gesetzliche-rente-reicht-nicht/',   title:'Gesetzliche Rente reicht nicht',     sub:'Was tun wenn GRV nicht ausreicht?',              tags:['rente reicht nicht','gesetzliche rente','grv','rentenniveau','altersarmut','lücke'] },
    { type:'article', href:'rente-mit-63-lehrer/',              title:'Rente mit 63 für Lehrer',             sub:'Frühpensionierung, Abzüge, Nettopension',        tags:['rente mit 63','früh pension','lehrer','frühpensionierung','abzüge'] },
    { type:'article', href:'aktivrente-2026/',                  title:'Aktivrente 2026',                     sub:'Bis 2.000 € steuerfrei dazuverdienen',           tags:['aktivrente','dazuverdienen','steuerfrei','rente','2026','nebenerwerb'] },
    { type:'article', href:'muetterrente-2027/',                title:'Mütterrente 2027',                    sub:'Kindererziehungszeiten & Rentenerhöhung',        tags:['mütterrente','mutterrente','kindererziehung','rente','2027','frauen'] },
    { type:'article', href:'versorgungsluecke-beamte-berechnen/', title:'Versorgungslücke Beamte',          sub:'Lücke korrekt berechnen',                       tags:['versorgungslücke','beamte','lücke berechnen','ruhegehalt','pension'] },
    { type:'article', href:'pensionsluecke-lehrer/',            title:'Pensionslücke Lehrer',                sub:'Wie groß ist die Lücke bei Lehrern?',            tags:['pensionslücke','lehrer','pension','lücke','teilzeit','elternzeit'] },
    { type:'article', href:'pension-lehrer-prozent/',           title:'Pension Lehrer: wie viel Prozent?',   sub:'Ruhegehaltssatz, A12, A13, A14',                tags:['pension prozent','lehrer pension','ruhegehaltssatz','a13','a14','wie viel pension'] },
    { type:'article', href:'beamtenversorgung-teilzeit-elternzeit/', title:'Beamtenversorgung Teilzeit',    sub:'Was kostet Teilzeit & Elternzeit an Pension?',   tags:['teilzeit','elternzeit','pension','beamtenversorgung','verlust'] },
    { type:'article', href:'private-altersvorsorge-beamte/',    title:'Private Altersvorsorge Beamte',      sub:'Wann ist private Vorsorge sinnvoll?',            tags:['private altersvorsorge','beamte','rürup','etf','sinnvoll'] },
    { type:'article', href:'lehrerpension-nrw/',                title:'Lehrerpension NRW',                   sub:'Pension in Nordrhein-Westfalen',                 tags:['lehrer','nrw','pension','nordrhein-westfalen','lehrerpension nrw'] },
    { type:'article', href:'lehrerpension-bw/',                 title:'Lehrerpension BW',                    sub:'Pension in Baden-Württemberg',                  tags:['lehrer','bw','baden-württemberg','pension','lehrerpension bw'] },
    { type:'article', href:'lehrerpension-bayern/',             title:'Lehrerpension Bayern',                sub:'Pension in Bayern',                              tags:['lehrer','bayern','pension','lehrerpension'] },
    { type:'article', href:'a13-gehalt-pension/',               title:'A13 Gehalt und Pension',              sub:'Beamtenbesoldung A13, Ruhegehalt',               tags:['a13','gehalt','pension','besoldung','beamte','wie bekomme ich mit a13'] },
    { type:'article', href:'teilzeit-pension-lehrer/',          title:'Teilzeit und Pension Lehrer',         sub:'Pensionsverluste durch Teilzeit',                tags:['teilzeit','pension','lehrer','verlust'] },
    { type:'article', href:'referendariat-pension/',            title:'Referendariat & Pension',             sub:'Anrechnung des Referendariats',                  tags:['referendariat','pension','anrechnung','beamte'] },
    { type:'article', href:'ruerup-lehrer/',                    title:'Rürup für Lehrer',                    sub:'Steuervorteil der Basisrente für Lehrkräfte',    tags:['rürup','lehrer','basisrente','steuervorteil','pension'] },
    { type:'article', href:'pkv-beamte-ruhestand/',             title:'PKV Beamte im Ruhestand',             sub:'Beihilfe und PKV-Kosten',                       tags:['pkv','beamte','ruhestand','beihilfe','krankenversicherung'] },
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
      placeholder='Suche — z.B. „AV-Depot" oder „A13 Pension"'
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
          <span class="search-item-type">{item.type === 'calc' ? '⊞ Rechner' : '✦ Artikel'}</span>
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
