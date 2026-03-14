<script>
  import Tabs from './tabs.svelte';
  let { data } = $props();
  const colours = [
    "#3B6D11", "#97C459", "#EF9F27",
    "#EF9F27", "#E24B4A", "#A32D2D"
  ]

  function getColour(value) {
    if (parseFloat(value) <= 10) return colours[0];
    if (parseFloat(value) <= 25) return colours[1];
    if (parseFloat(value) <= 50) return colours[2];
    if (parseFloat(value) <= 75) return colours[3];
    if (parseFloat(value) <= 90) return colours[4];
    if (parseFloat(value) <= 100) return colours[5];
    else return '000000';
  }

  let address = '';

  function search() {
    if (address.trim()) {
      window.location.href = `/profile/${address.trim()}`;
    }
  }


</script>

<div class="flex justify-between navbar bg-base-100 h-20 shadow-sm">
  <p class="font-black text-xl p-8">Polywatcher</p>
  <input type="text" class="input h-10 w-100 border-2 border-black " placeholder="Enter Wallet Address" bind:value={address} onkeydown={e => e.key === 'Enter' && search()}/>
  <p class="font-black text-xl p-8" >v.2.1</p>
</div>


<div class="flex gap-8 p-8">

  <div id="profile" class="w-1/2 bg-white">
          

          <div class="overflow-x-auto">
            <table class="table">
              <thead>
                <tr>
                  <th class='font-bold text-black'>Profile</th>
                </tr>
              </thead>
              <tbody>
                {#if data.creator?.profileImage}
                <tr><td>Photo</td><td><img src={data.creator.profileImage} width="100" height="100" class='rounded-full' alt="Profile" /></td></tr>
                {/if}
                <tr><td>Name</td><td>{data.creator?.name ?? data.creator?.proxyWallet ?? 'Unknown'}</td></tr>
                <tr><td>Username</td><td>{data.creator?.pseudonym ?? ''}</td></tr>
                <tr><td>Bio</td><td>{data.creator?.bio ?? ''}</td></tr>
                <tr><td>Wallet</td><td>{data.creator?.proxyWallet ?? ''}</td></tr>
                <tr><td>Joined</td><td>{(data.creator?.createdAt ?? '').slice(0, 10)}</td></tr>
              

              </tbody>
            </table>
          </div>
         </div> 

          
  <div id="analysis" class="w-1/2 bg-white">
  
          <div class="overflow-x-auto">
            <table class="table">
                <thead>
                <tr>
                  <th class='font-bold text-black'>Analysis</th>
                </tr>
              </thead>

              <thead>
                <tr>
                  <th>Param</th>
                  <th>Result</th>
                </tr>
              </thead>
              <tbody>
                
                <tr><td>Market Spread</td><td style="background-color:{getColour(data.spread_analysis)}">{data.spread_analysis}</td></tr>
            

                <tr><td>Creation/cashout gap</td><td>{data.time_gap}</td></tr>
                <tr><td>Volume/redemption</td><td>{data.volume_analysis} — ${data.value_redemptions} across {data.num_positions} positions</td></tr>
                <tr><td>Profit/loss ratio</td><td>{data.profit_analysis}</td></tr>
                <tr><td>Success rate</td><td>{data.success_rate} ({data.success_count}W / {data.failure_count}L)</td></tr>
                <tr><td>High-frequency trading</td><td>{data.high_frequency}</td></tr>
                <tr><td>Position size</td><td>{data.profit_size} (avg: {data.average_size})</td></tr>
                <tr><td>Initial deposit</td><td>{data.chain_analysis} / ${data.chain_total}</td></tr>
                <tr><td>24/48hr deposit</td><td>{data.chain_analysis_2} / {data.chain_analysis_3}</td></tr>
                <tr><td>48hr input/output</td><td>{data.chain_gap} / ${data.chain_output} out</td></tr>
              </tbody>
            </table>
          </div>

  </div>


</div>

<Tabs {data} />


<!-- {#if data}
  <h1>{data.creator?.name ?? data.creator?.proxyWallet ?? 'Unknown'}</h1>
  <p><strong>Username:</strong> {data.creator?.pseudonym ?? ''}</p>
  <p><strong>Bio:</strong> {data.creator?.bio ?? ''}</p>
  <p><strong>Wallet:</strong> {data.creator?.proxyWallet ?? ''}</p>
  <p><strong>Joined:</strong> {(data.creator?.createdAt ?? '').slice(0, 10)}</p>

  {#if data.creator?.profileImage}
    <img src={data.creator.profileImage} width="100" height="100" alt="Profile" />
  {/if}

  <p><a href="/">Back to search</a></p>

  <h2>Analysis</h2>
  <p>Market Spread: {data.spread_analysis}</p>
  <p>Creation/cashout gap: {data.time_gap}</p>
  <p>Volume/redemption: {data.volume_analysis} // ${data.value_redemptions} across {data.num_positions} positions</p>
  <p>Profit/loss ratio: {data.profit_analysis}</p>
  <p>Success rate: {data.success_rate} ({data.success_count}W / {data.failure_count}L)</p>
  <p>High-frequency trading: {data.high_frequency}</p>
  <p>Position size: {data.profit_size} (avg: {data.average_size})</p>
  <p>Initial deposit: {data.chain_analysis} / ${data.chain_total}</p>
  <p>24/48hr deposit: {data.chain_analysis_2} / {data.chain_analysis_3}</p>
  <p>48hr input/output: {data.chain_gap} / ${data.chain_output} out</p> -->

  <!-- <h2>Activity</h2>
  {#if data.activity?.length}
    <table border="1" cellpadding="5" cellspacing="0">
      <thead>
        <tr><th>Market</th><th>Type</th><th>Timestamp</th><th>Side</th><th>Outcome</th><th>Size</th><th>Cost</th><th>Price</th></tr>
      </thead>
      <tbody>
        {#each data.activity as trade}
          <tr>
            <td>{trade.title}</td><td>{trade.type}</td><td>{trade.timestamp}</td>
            <td>{trade.side}</td><td>{trade.outcome}</td><td>{trade.size}</td>
            <td>{trade.cost}</td><td>{trade.price}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  {:else}
    <p>No activity.</p>
  {/if}

  <h2>Positions</h2>
  {#if data.positions?.length}
    <table border="1" cellpadding="5" cellspacing="0">
      <thead>
        <tr><th>Market</th><th>Outcome</th><th>Size</th><th>Avg Price</th><th>Current Value</th></tr>
      </thead>
      <tbody>
        {#each data.positions as pos}
          <tr>
            <td>{pos.title ?? ''}</td><td>{pos.outcome ?? ''}</td><td>{pos.size ?? ''}</td>
            <td>{pos.avgPrice ?? ''}</td><td>{pos.currentValue ?? ''}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  {:else}
    <p>No positions.</p>
  {/if} -->
<!-- {/if} -->


