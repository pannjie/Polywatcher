<script>
  let { data } = $props();
  const wallets = data.wallets;

  const colours = [
    "rgba(59, 109, 17, 0.7)",
    "rgba(59, 109, 17, 0.4)",
    "rgba(239, 199, 39, 0.7)",
    "rgba(239, 159, 39, 0.7)",
    "rgba(163, 45, 45, 0.5)",
    "rgba(163, 45, 45, 0.8)"
  ];

  function getColour(risk) {
    if (risk == 'minimal risk') return colours[0];
    if (risk == 'low risk') return colours[1];
    if (risk == 'medium risk') return colours[2];
    if (risk == 'high risk') return colours[3];
    if (risk == 'very high risk') return colours[4];
    if (risk == 'extreme risk') return colours[5];
    return 'transparent';
  }

  function spreadRisk(v) {
    if (v == null) return null;
    if (v < 50) return 'minimal risk';
    if (v < 60) return 'low risk';
    if (v < 70) return 'medium risk';
    if (v < 80) return 'high risk';
    if (v < 90) return 'very high risk';
    return 'extreme risk';
  }

  function successRisk(v) {
    if (v == null) return null;
    if (v > 60) return 'extreme risk';
    if (v > 50) return 'very high risk';
    if (v > 40) return 'high risk';
    if (v > 30) return 'medium risk';
    if (v > 20) return 'low risk';
    return 'minimal risk';
  }

  function creationVolumeRisk(v) {
    if (v == null) return null;
    if (v > 100000) return 'extreme risk';
    if (v > 75000) return 'very high risk';
    if (v > 50000) return 'high risk';
    if (v > 25000) return 'medium risk';
    if (v > 10000) return 'low risk';
    return 'minimal risk';
  }

  function deposits24hRisk(v) {
    if (v == null) return null;
    if (v > 50000) return 'extreme risk';
    if (v > 25000) return 'very high risk';
    if (v > 12500) return 'high risk';
    if (v > 6250) return 'medium risk';
    if (v > 3125) return 'low risk';
    return 'minimal risk';
  }

  function similarityRisk(v) {
    if (v == null) return null;
    if (v > 0.8) return 'extreme risk';
    if (v > 0.7) return 'very high risk';
    if (v > 0.6) return 'high risk';
    if (v > 0.5) return 'medium risk';
    if (v > 0.4) return 'low risk';
    return 'minimal risk';
  }

  function cashoutRisk(v) {
    if (v == null) return null;
    if (v <= 5) return 'extreme risk';
    if (v <= 10) return 'very high risk';
    if (v <= 15) return 'high risk';
    if (v <= 25) return 'medium risk';
    if (v <= 30) return 'low risk';
    return 'minimal risk';
  }
</script>

<div class="min-h-screen p-8">

  <div class="flex justify-between navbar bg-base-100 h-20">
    <h1 class="text-4xl font-black mb-8">Leaderboard</h1>
    <a href="/" class="text-2xl font-bold hover:underline">Back to Polywatcher</a>
  </div>

  <div class="overflow-x-auto">
    <table class="table table-zebra w-full">
      <thead>
        <tr>
          <th>Rank</th>
          <th>Username</th>
          <th>PNL</th>
          <th>Market Spread</th>
          <th>Success Rate</th>
          <th>Creation/Volume</th>
          <th>24h Deposits</th>
          <th>AI Similarity</th>
          <th>Cashout Gap</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {#each wallets as wallet}
          <tr>
            <td>{wallet.rank}</td>
            <td>
              <div>{wallet.username ?? '-'}</div>
              <div class="text-xs text-gray-400 font-mono">{wallet.proxywallet?.slice(0, 10)}...</div>
            </td>
            <td>{wallet.pnl != null ? '$' + wallet.pnl.toLocaleString() : '-'}</td>
            <td style="background-color: {getColour(spreadRisk(wallet.market_spread))}">{wallet.market_spread ?? '-'}</td>
            <td style="background-color: {getColour(successRisk(wallet.success_rate))}">{wallet.success_rate != null ? wallet.success_rate + '%' : '-'}</td>
            <td style="background-color: {getColour(creationVolumeRisk(wallet.creation_volume))}">{wallet.creation_volume != null ? '$' + wallet.creation_volume.toLocaleString() : '-'}</td>
            <td style="background-color: {getColour(deposits24hRisk(wallet.deposits_24h))}">{wallet.deposits_24h != null ? '$' + wallet.deposits_24h.toLocaleString() : '-'}</td>
            <td style="background-color: {getColour(similarityRisk(wallet.ai_similarity))}">{wallet.ai_similarity ?? '-'}</td>
            <td style="background-color: {getColour(cashoutRisk(wallet.cashout_gap))}">{wallet.cashout_gap != null ? wallet.cashout_gap + ' days' : '-'}</td>
            <td>
              <a class="btn btn-xs btn-outline" href="/profile/{wallet.proxywallet}">View</a>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</div>
