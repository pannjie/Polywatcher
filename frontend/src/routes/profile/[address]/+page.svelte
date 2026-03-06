<script>
  let { data } = $props();
</script>

{#if data}
  <h1>{data.creator?.name ?? data.creator?.proxyWallet ?? 'Unknown'}</h1>
  <p><strong>Username:</strong> {data.creator?.pseudonym ?? ''}</p>
  <p><strong>Bio:</strong> {data.creator?.bio ?? ''}</p>
  <p><strong>Wallet:</strong> {data.creator?.proxyWallet ?? ''}</p>
  <p><strong>Joined:</strong> {(data.creator?.createdAt ?? '').slice(0, 10)}</p>
  <!-- add the following 1) twitter handle if there is one? 2) check if the user has been active in the last 24/48 hours -->
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
  <p>48hr input/output: {data.chain_gap} / ${data.chain_output} out</p>

  <h2>Activity</h2>
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
  {/if}
{/if}
