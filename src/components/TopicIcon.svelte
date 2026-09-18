<script>
  export let icon = 'pension';
  export let accent = 'green';

  const PATHS = {
    pension: 'M12 21v-6M12 15a5 5 0 100-10 5 5 0 000 10zM7.5 9.5L4 7m16 0l-3.5 2.5M12 21c-3 0-5.5-.9-7-2.2M12 21c3 0 5.5-.9 7-2.2',
    etf:      'M4 19V9m5.5 10V5m5.5 14v-7m5-7 0 14M3 19h18',
    tax:      'M7 3h7l4 4v14a1 1 0 01-1 1H7a1 1 0 01-1-1V4a1 1 0 011-1zM14 3v4h4M9.5 16.5l5-5m0 5l-5-5',
    cashflow: 'M4 7h11a3 3 0 010 6H9a3 3 0 000 6h11M15 4l4 3-4 3M9 14l-4 3 4 3',
    insurance:'M12 3l7 3v6c0 4.5-3 8-7 9-4-1-7-4.5-7-9V6l7-3zM9 12l2 2 4-4',
  };
</script>

<div class="topic-diamond" style="--accent: var(--color-{accent})">
  <svg class="topic-diamond-bg" viewBox="0 0 120 120" aria-hidden="true">
    <rect x="20" y="20" width="80" height="80" rx="18" transform="rotate(45 60 60)" />
  </svg>
  <svg class="topic-diamond-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <path d={PATHS[icon]} />
  </svg>
</div>
