<script>
  let address = '';

  function search() {
    if (address.trim()) {
      window.location.href = `/profile/${address.trim()}`;
    }
  }
</script>

<div class="min-h-screen flex flex-col items-center justify-center">
<fieldset class="fieldset">
  <legend class="fieldset-legend font-black text-5xl">Polywatcher v.2.1</legend>
  <input type="text" class="input h-12 w-100 border-2 border-black " placeholder="Type here" bind:value={address} onkeydown={e => e.key === 'Enter' && search()}/>
  <p class="label">Developed by PJ/Goldsmiths</p>
</fieldset>

<div class="flex flex-col items-center gap-2 mt-16">
  <div class="flex gap-2">
    <a class="btn btn-outline btn-sm" href="https://polywatcherfrontend-production.up.railway.app/profile/0x44de2a52d8d2d3ddcf39d58e315a10df53ba9c08">Maduro Whale</a>
    <a class="btn btn-outline btn-sm" href="https://polywatcherfrontend-production.up.railway.app/profile/0x94a428cfa4f84b264e01f70d93d02bc96cb36356">George Cottrell</a>
    <a class="btn btn-outline btn-sm" href="https://polywatcherfrontend-production.up.railway.app/profile/0x4dfd481c16d9995b809780fd8a9808e8689f6e4a">Iran Whale #1</a>
  </div>
  <div class="flex gap-2">
    <a class="btn btn-outline btn-sm" href="https://polywatcherfrontend-production.up.railway.app/profile/0x162f6fff88a52864f2ecc9833e58089d5254798d">Superbowl Insider</a>
    <a class="btn btn-outline btn-sm" href="https://polywatcherfrontend-production.up.railway.app/profile/0xbad457dc633bbb7b6cbe09dd5867a5e8e597acd7">Iran Whale #2</a>
  </div>
</div>
</div>

<style>
  
</style>