<script>
  import Tabs from './tabs.svelte';
  let { data } = $props();
  const colours = [
    "rgba(59, 109, 17, 0.7)",   // minimal 
    "rgba(59, 109, 17, 0.4)",   // low 
    "rgba(239, 199, 39, 0.7)",  // medium 
    "rgba(239, 159, 39, 0.7)",  // high 
    "rgba(163, 45, 45, 0.5)",   // very high 
    "rgba(163, 45, 45, 0.8)"    // extreme 
  ]

  function getColour(value) {
    if (value == 'minimal risk') return colours[0];
    if (value == 'low risk') return colours[1];
    if (value == 'medium risk') return colours[2];
    if (value == 'high risk') return colours[3];
    if (value == 'very high risk') return colours[4];
    if (value == 'extreme risk') return colours[5];
    else return '#FFFFFF';
  }

  let address = '';

  function search() {
    if (address.trim()) {
      window.location.href = `/profile/${address.trim()}`;
    }
  }


</script>

<div class="drawer drawer-end">
<input id="profile-drawer" type="checkbox" class="drawer-toggle" />
<div class="drawer-content">

<div class="flex justify-between navbar bg-base-100 h-20 shadow-sm">
  <a href="/" class="font-black text-xl p-8 no-underline text-inherit">Polywatcher</a>
  <input type="text" class="input h-10 w-100 border-2 border-black " placeholder="Enter Wallet Address" bind:value={address} onkeydown={e => e.key === 'Enter' && search()}/>
  <label for="profile-drawer" class="font-black text-xl p-8 cursor-pointer">Info</label>
</div>


<div class="flex gap-8 p-8">

  <div id="profile" class="w-1/3 bg-white">
          

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

          
  <div id="analysis" class="w-2/3 bg-white">
  
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
                  <th>Risk</th>
                </tr>
              </thead>
              <tbody>

                <tr><td>Market Spread</td><td style="background-color:{getColour(data.spread_risk)}">{data.spread_analysis}</td><td style="background-color:{getColour(data.spread_risk)}">{data.spread_risk}</td></tr>

                <tr><td>Creation/Cashout Gap</td><td style="background-color:{getColour(data.time_gap_risk)}">{data.time_gap}</td><td style="background-color:{getColour(data.time_gap_risk)}">{data.time_gap_risk}</td></tr>

                <tr><td>Volume/Redemption Ratio</td><td style="background-color:{getColour(data.volume_risk)}">${data.value_redemptions} across {data.num_positions} positions</td><td style="background-color:{getColour(data.volume_risk)}">{data.volume_risk}</td></tr>

                <tr><td>Profit/loss</td><td style="background-color:{getColour(data.profit_risk)}">${data.total_profit}</td><td style="background-color:{getColour(data.profit_risk)}">{data.profit_risk}</td></tr>

                <tr><td>Success rate</td><td style="background-color:{getColour(data.success_risk)}">{data.success_rate}% ({data.success_count}W / {data.failure_count}L)</td><td style="background-color:{getColour(data.success_risk)}">{data.success_risk}</td></tr>

                <tr><td>High-frequency trading</td><td>{data.high_frequency}</td><td></td></tr>

                <tr><td>Position size</td><td style="background-color:{getColour(data.size_deviation_risk)}">{data.size_deviation}σ (avg: {data.average_size})</td><td style="background-color:{getColour(data.size_deviation_risk)}">{data.size_deviation_risk}</td></tr>

                <tr><td>Initial Deposit</td><td style="background-color:{getColour(data.sum_input_risk)}">${data.sum_input}</td><td style="background-color:{getColour(data.sum_input_risk)}">{data.sum_input_risk}</td></tr>

                <tr><td>48hr Deposit</td><td style="background-color:{getColour(data.sum_input_48hr_risk)}">${data.sum_input_48hr}</td><td style="background-color:{getColour(data.sum_input_48hr_risk)}">{data.sum_input_48hr_risk}</td></tr>

                <tr><td>24hr Deposit</td><td style="background-color:{getColour(data.sum_input_24hr_risk)}">${data.sum_input_24hr}</td><td style="background-color:{getColour(data.sum_input_24hr_risk)}">{data.sum_input_24hr_risk}</td></tr>

                <tr><td>Deposit/Withdrawal</td><td style="background-color:{getColour(data.chain_gap)}">${data.sum_input_48hr} in / ${data.chain_output} out</td><td style="background-color:{getColour(data.chain_gap)}">{data.chain_gap}</td></tr>
              </tbody>
            </table>
          </div>

  </div>


</div>

<Tabs {data} />

</div>

<div class="drawer-side">
  <label for="profile-drawer" aria-label="close sidebar" class="drawer-overlay"></label>
  <div class="bg-base-100 min-h-full w-80 p-4">
  </div>
</div>

</div>
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


