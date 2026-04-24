<script>
  let { data } = $props();
  const wallets = data.wallets;
</script>

<div class="min-h-screen p-8">
  <h1 class="text-4xl font-black mb-8">Leaderboard</h1>

  <div class="overflow-x-auto">
    <table class="table table-zebra w-full">
      <thead>
        <tr>
          <th>Rank</th>
          <th>Username</th>
          <th>Wallet</th>
          <th>PNL</th>
          <th>Volume</th>
          <th>Market Spread</th>
          <th>Success Rate</th>
          <th>AI Similarity</th>
          <th>Cashout Gap</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {#each wallets as wallet}
          <tr>
            <td>{wallet.rank}</td>
            <td>{wallet.username ?? '-'}</td>
            <td class="font-mono text-xs">{wallet.proxywallet?.slice(0, 10)}...</td>
            <td>{wallet.pnl != null ? '$' + wallet.pnl.toLocaleString() : '-'}</td>
            <td>{wallet.vol != null ? '$' + wallet.vol.toLocaleString() : '-'}</td>
            <td>{wallet.market_spread ?? '-'}</td>
            <td>{wallet.success_rate != null ? wallet.success_rate + '%' : '-'}</td>
            <td>{wallet.ai_similarity ?? '-'}</td>
            <td>{wallet.cashout_gap != null ? wallet.cashout_gap + ' days' : '-'}</td>
            <td>
              <a class="btn btn-xs btn-outline" href="/profile/{wallet.proxywallet}">View</a>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</div>
