<script>
  let address = '';

  function search() {
    if (address.trim()) {
      window.location.href = `/profile/${address.trim()}`;
    }
  }
</script>

<div class="min-h-screen flex items-center justify-center">
<fieldset class="fieldset">
  <legend class="fieldset-legend font-black text-5xl">Polywatcher v.2.1</legend>
  <input type="text" class="input h-12 w-100 border-2 border-black " placeholder="Type here" bind:value={address} onkeydown={e => e.key === 'Enter' && search()}/>
  <p class="label">Developed by PJ/Goldsmiths</p>
</fieldset>
</div>

<style>
  
</style>