<script>
  import { navigating } from '$app/state';
  import { goto } from '$app/navigation';
  let address = $state('');

  function search() {
    if (address.trim()) {
      goto(`/profile/${address.trim()}`);
    }
  }
</script>

<!-- outer drawer: About (left) -->
<div class="drawer">
<input id="about-drawer" type="checkbox" class="drawer-toggle" />
<div class="drawer-content">

  <!-- inner drawer: Extras (right) -->
  <div class="drawer drawer-end">
  <input id="extras-drawer" type="checkbox" class="drawer-toggle" />
  <div class="drawer-content">

    <div class="flex justify-between navbar bg-base-100 h-20">
      <label for="about-drawer" class="font-black text-xl p-8 cursor-pointer">About</label>
      <label for="extras-drawer" class="font-black text-xl p-8 cursor-pointer">Extras</label>
    </div>

    <div class="min-h-screen flex flex-col items-center justify-center">
      <fieldset class="fieldset">
        <legend class="fieldset-legend font-black text-5xl">Polywatcher v.2.2</legend>
        {#if navigating.to}
          <div class="flex justify-center w-100"><span class="loading loading-bars loading-xl"></span></div>
        {:else}
          <input type="text" class="input h-12 w-100 border-2 border-black" placeholder="Type here" bind:value={address} onkeydown={e => e.key === 'Enter' && search()}/>
        {/if}
        <p class="label">Developed by PJ/Goldsmiths</p>
      </fieldset>

      <div class="flex flex-col items-center gap-2 mt-16">
        <div class="flex gap-2">
          <a class="btn btn-outline btn-sm" href="/profile/0x44de2a52d8d2d3ddcf39d58e315a10df53ba9c08">Maduro Whale</a>
          <a class="btn btn-outline btn-sm" href="/profile/0x94a428cfa4f84b264e01f70d93d02bc96cb36356">George Cottrell</a>
          <a class="btn btn-outline btn-sm" href="/profile/0x4dfd481c16d9995b809780fd8a9808e8689f6e4a">Iran Whale #1</a>
        </div>
        <div class="flex gap-2">
          <a class="btn btn-outline btn-sm" href="/profile/0x162f6fff88a52864f2ecc9833e58089d5254798d">Superbowl Insider</a>
          <a class="btn btn-outline btn-sm" href="/profile/0xbad457dc633bbb7b6cbe09dd5867a5e8e597acd7">Iran Whale #2</a>
        </div>
      </div>
    </div>

  </div>

  <!-- Extras sidebar (right) -->
  <div class="drawer-side">
    <label for="extras-drawer" aria-label="close sidebar" class="drawer-overlay"></label>
    <div class="bg-base-100 min-h-full w-80 p-4">
      <p class="font-black text-xl mb-4">Extras</p>
      <div class="divider"></div>
      <p class="font-bold">Daily Leaderboard</p>
      <p class="text-sm mb-3">Today's top wallets, ranked by PNL.</p>
      <div class="divider"></div>
      <p class="font-bold">Bitcoin Scams</p>
      <p class="text-sm mb-3">Notable bitcoin promoted on X, Reddit and Discord</p>
      <div class="divider"></div>
      <p class="font-bold">Politics Grift</p>
      <p class="text-sm mb-3">Biggest earners in the Politics category</p>
      <div class="divider"></div>
    </div>
  </div>
  </div>

</div>

<!-- About sidebar (left) -->
<div class="drawer-side">
  <label for="about-drawer" aria-label="close sidebar" class="drawer-overlay"></label>
  <div class="bg-base-100 min-h-full w-80 p-4">
    <p class="font-black text-xl mb-4">About</p>
    <div class="divider"></div>
    <p class="text-sm">Polywatcher is a journalistic tool that analyses Polymarket for suspicious trading patterns. It uses Polymarket's native APIs, the Goldsky Graph API, and Etherscan for blockchain data. All of the code can be found on my <a href="https://github.com/pannjie/Polywatcher" class="underline">Github page.</a></p>
    <div class="divider"></div>
    <p class="text-sm">Developed by PJ. A Digital Journalist working out of Goldsmiths. Contact me at pjie001@gold.ac.uk or connect with me on <a href="https://linkedin.com/in/pan-jie-a70173b2" class="underline">LinkedIn</a></p>
  </div>
</div>
</div>

<style>

</style>
