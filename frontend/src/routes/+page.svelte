<script>
  let address = '';

  function search() {
    if (address.trim()) {
      window.location.href = `/profile/${address.trim()}`;
    }
  }
</script>

<div class="container">
  <h1>Polywatcher</h1>
  <div class="search-bar">
    <input bind:value={address} placeholder="Enter wallet address" onkeydown={e => e.key === 'Enter' && search()} />
  </div>
  <div class="button">
    <button onclick={search}>Search</button>
  </div>
</div>

<style>
  .container {
    text-align: center;
    color: black;
    font-family: "Source Code Pro";
    margin-top: 10em;
  }

  h1 {
    font-size: 3rem;
    margin-bottom: 0.75em;
  }

  .search-bar input {
    width: 40em;
    height: 2.5em;
    border-radius: 5px;
    text-align: center;
    font-family: "Source Code Pro";
    font-size: 1rem;
  }

  .button {
    margin-top: 1.25em;
  }

  button {
    font-family: "Source Code Pro";
    font-weight: bold;
    font-size: 1rem;
    width: 8em;
    height: 2.5em;
    border-radius: 5px;
    cursor: pointer;
  }

  :global(body) {
    background: white;
  }
</style>