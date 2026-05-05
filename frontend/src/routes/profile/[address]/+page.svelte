<script>
  import Tabs from './tabs.svelte';
  import { navigating } from '$app/state';
  import { goto } from '$app/navigation';

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

  let address = $state('');

  function search() {
    if (address.trim()) {
      goto (`/profile/${address.trim()}`);
    }
  }


</script>

<div class="drawer drawer-end">
<input id="profile-drawer" type="checkbox" class="drawer-toggle" />
<div class="drawer-content">

<div class="flex justify-between navbar bg-base-100 h-20 shadow-sm">
  <a href="/" class="font-black text-xl p-8 no-underline text-inherit">Polywatcher</a>
  {#if navigating.to}
    <span class="loading loading-bars loading-xl"></span>
  {:else}
    <input type="text" class="input h-10 w-100 border-2 border-black " placeholder="Enter Wallet Address" bind:value={address} onkeydown={e => e.key === 'Enter' && search()}/>
  {/if}  
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
                <tr><td>High Frequency Trader</td><td>{data.high_frequency}</td></tr>
                <tr><td>AI Similiarity Index</td><td>{data.slug_similarity}</td></tr>

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

                <tr><td>Market Spread</td><td style="background-color:{getColour(data.spread_risk)}">{data.spread_analysis}%</td><td style="background-color:{getColour(data.spread_risk)}">{data.spread_risk}</td></tr>

                <tr><td>Creation/Cashout Gap</td><td style="background-color:{getColour(data.time_gap_risk)}">{data.time_gap} Days</td><td style="background-color:{getColour(data.time_gap_risk)}">{data.time_gap_risk}</td></tr>


                <tr><td>Creation/Volume</td><td style="background-color:{getColour(data.volume_48hr_risk)}">${data.volume_48hr}</td><td style="background-color:{getColour(data.volume_48hr_risk)}">{data.volume_48hr_risk}</td></tr>

                
                <tr><td>Volume/Redemption Ratio</td><td style="background-color:{getColour(data.volume_risk)}">${data.value_redemptions} across {data.num_positions} positions</td><td style="background-color:{getColour(data.volume_risk)}">{data.volume_risk}</td></tr>

                <tr><td>Profit/loss</td><td style="background-color:{getColour(data.profit_risk)}">${data.total_profit}</td><td style="background-color:{getColour(data.profit_risk)}">{data.profit_risk}</td></tr>

                <tr><td>Success rate</td><td style="background-color:{getColour(data.success_risk)}">{data.success_rate}% ({data.success_count}W / {data.failure_count}L)</td><td style="background-color:{getColour(data.success_risk)}">{data.success_risk}</td></tr>

                <tr>
                  <td rowspan="3">Proximity Analysis</td>
                  <td style="background-color:{getColour(data.activity_risk)}">{data.top_3_event_slug[0]}: ${data.top_activity_1}</td>
                  <td rowspan="3" style="background-color:{getColour(data.activity_risk)}">{data.activity_risk}</td>
                </tr>
                <tr>
                  <td style="background-color:{getColour(data.activity_risk)}">{data.top_3_event_slug[1]}: ${data.top_activity_2}</td>
                </tr>
                <tr>
                  <td style="background-color:{getColour(data.activity_risk)}">{data.top_3_event_slug[2]}: ${data.top_activity_3}</td>
                </tr>


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
    <p class="font-black text-xl mb-4">Analysis Guide</p>
    <div class="divider"></div>
    <p class="font-bold">High Frequency Trading</p>
    <p class="text-sm mb-3">Checks the time gap between each trade in the activity API endpoint. More than 10 trades less than 1s apart indicates high frequency trading.</p>
    <div class="divider"></div>
    
    <p class="font-bold">AI Similarity Index</p>
    <p class="text-sm mb-3">Analyses event slugs from the closed_positions API endpoint using HuggingFace sentence transformer. 1 = completely identical. 0 = completely unrelated</p>
    <div class="divider"></div>
   
    <p class="font-bold">Market Spread</p>
    <p class="text-sm mb-3">Checks what percentage of the user's open and closed positions are in the same market. A higher percentage indicates higher risk.</p>
    <div class="divider"></div>
    <p class="font-bold">Creation/Cashout Gap</p>
    <p class="text-sm mb-3">Days elapsed between account creation and a redemption of more than $10,000. The shorter the gap, the higher the risk.</p>
    <div class="divider"></div>
    <p class="font-bold">Creation/Volume</p>
    <p class="text-sm mb-3">Uses the Polygonscan API to find the wallet's first known on-chain activity, then sums all BUY trades placed within the first 48 hours of that date. A high volume of early trades suggests a fresh wallet trading aggressively from the outset.</p>
    <div class="divider"></div>
    <p class="font-bold">Volume/Redemption Ratio</p>
    <p class="text-sm mb-3">Compares the value of redemptions against the number of positions. A large volume of redemptions across few positions indicates higher risk.</p>
    <div class="divider"></div>
    <p class="font-bold">Profit/Loss</p>
    <p class="text-sm mb-3">Total realised trading profits. The higher the profits, the greater the risk.</p>
    <div class="divider"></div>
    <p class="font-bold">Success Rate</p>
    <p class="text-sm mb-3">Fewer than 30% of all Polymarket users make a profit. Compares wins and losses to gauge whether the user is unusually successful.</p>
    <div class="divider"></div>
    <p class="font-bold">Proximity Analysis</p>
    <p class="text-sm mb-3">Shows the three markets where the wallet has concentrated the most dollar activity. A high volume of trading just before the market closes reflects a higher risk.</p>
    <div class="divider"></div>
    <p class="font-bold">Position Size</p>
    <p class="text-sm mb-3">Checks whether the user has taken positions that are unusually large compared to their average position size.</p>
    <div class="divider"></div>
    <p class="font-bold">Blockchain — Initial Deposit</p>
    <p class="text-sm mb-3">Sums the total value of the user's first 20 transactions into their Polymarket account. The larger the initial stake, the higher the risk.</p>
    <div class="divider"></div>
    <p class="font-bold">Blockchain — 48hr Deposit</p>
    <p class="text-sm mb-3">Sums the total value of deposits within the first 48 hours. The larger the sum, the higher the risk.</p>
    <div class="divider"></div>
    <p class="font-bold">Blockchain — 24hr Deposit</p>
    <p class="text-sm mb-3">Sums the total value of deposits within the first 24 hours. The larger the sum, the higher the risk.</p>
    <div class="divider"></div>
    <p class="font-bold">Blockchain — Chain Gap</p>
    <p class="text-sm mb-3">Checks the first 48 hours of blockchain activity. If large sums are both deposited and withdrawn in quick succession, the user is flagged for potential insider trading.</p>
  </div>
</div>

</div>



