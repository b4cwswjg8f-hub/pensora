<script>
  import Hub from './screens/Hub.svelte';
  import PensionCalc from './screens/PensionCalc.svelte';
  import RenteCalc from './screens/RenteCalc.svelte';
  import DepotCalc from './screens/DepotCalc.svelte';
  import RuerupCalc from './screens/RuerupCalc.svelte';
  import CashflowCalc from './screens/CashflowCalc.svelte';
  import VersicherungCalc from './screens/VersicherungCalc.svelte';

  // Valid screen names
  const SCREENS = ['hub', 'pension', 'rente', 'depot', 'ruerup', 'cashflow', 'versicherung'];

  function readHash() {
    const raw = window.location.hash.replace(/^#\/?/, '');
    return SCREENS.includes(raw) ? raw : 'hub';
  }

  let screen = readHash();

  function navigate(name) {
    screen = name;
    window.location.hash = name === 'hub' ? '' : name;
    window.scrollTo(0, 0);
  }

  // Keep screen in sync when user presses back/forward
  window.addEventListener('hashchange', () => { screen = readHash(); });
</script>

{#if screen === 'hub'}
  <Hub on:navigate={e => navigate(e.detail)} />
{:else if screen === 'pension'}
  <PensionCalc on:back={() => navigate('hub')} on:navigate={e => navigate(e.detail)} />
{:else if screen === 'rente'}
  <RenteCalc on:back={() => navigate('hub')} on:navigate={e => navigate(e.detail)} />
{:else if screen === 'depot'}
  <DepotCalc on:back={() => navigate('hub')} on:navigate={e => navigate(e.detail)} />
{:else if screen === 'ruerup'}
  <RuerupCalc on:back={() => navigate('hub')} on:navigate={e => navigate(e.detail)} />
{:else if screen === 'cashflow'}
  <CashflowCalc on:back={() => navigate('hub')} on:navigate={e => navigate(e.detail)} />
{:else if screen === 'versicherung'}
  <VersicherungCalc on:back={() => navigate('hub')} on:navigate={e => navigate(e.detail)} />
{/if}
