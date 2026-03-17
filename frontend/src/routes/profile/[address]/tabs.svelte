<script>
  let { data } = $props();
  let activeTab = $state(1)
</script>


<div class="flex gap-8 p-8">
  <div role="tablist" class="tabs tabs-lift">
  <a onclick={()=> activeTab = 1} role="tab" class="tab font-black" class:tab-active={activeTab ==1}>Activity</a>
  <a onclick={()=> activeTab = 2} role="tab" class="tab font-black" class:tab-active={activeTab ==2}>Positions</a>
  <a onclick={()=> activeTab = 3} role="tab" class="tab font-black" class:tab-active={activeTab ==3}>Redemptions</a>
  <a onclick={()=> activeTab = 4} role="tab" class="tab font-black" class:tab-active={activeTab ==4}>PnL</a>
  <a onclick={()=> activeTab = 5} role="tab" class="tab font-black" class:tab-active={activeTab ==5}>Blockchain</a>
</div>
</div>

<div class="p-8 overflow-x-auto">
  {#if activeTab == 1}
    <table class="table">
      <thead><tr><th>Title</th><th>Market</th><th>Timestamp</th><th>Side</th><th>Outcome</th><th>Size</th><th>Cost</th><th>Price</th><th>Type</th></tr></thead>
      <tbody>
        {#each data.activity ?? [] as action}
          <tr>
            <td>{action.title}</td><td>{action.conditionId ? `${action.conditionId.slice(0,5)}...${action.conditionId.slice(-4)}` : ''}</td><td>{action.timestamp}</td><td>{action.side}</td>
            <td>{action.outcome}</td><td>{action.size}</td><td>{action.usdcSize}</td><td>{action.price}</td><td>{action.type}</td>
          </tr>
        {:else}
          <tr><td colspan="6">No Activity data.</td></tr>
        {/each}
      </tbody>
    </table>
  {/if}

  {#if activeTab == 2}
    <table class="table">
      <thead><tr><th>Title</th><th>Outcome</th><th>Size</th><th>Initial Value</th><th>Current Value</th><th> Cash Pnl</th><th>Percent% PnL</th></tr></thead>
      <tbody>
        {#each data.positions ?? [] as positions}
          <tr>
            <td>{positions.title}</td><td>{positions.outcome}</td><td>{positions.size}</td>
            <td>{positions.initialValue}</td><td>{positions.currentValue}</td><td>{positions.cashPnl}</td><td>{positions.percentPnl}</td>
          </tr>
        {:else}
          <tr><td colspan="6">No positions data.</td></tr>
        {/each}
      </tbody>
    </table>
  {/if}

  {#if activeTab == 3}
     <table class="table">
      <thead><tr><th>Title</th><th>Timestamp</th><th>Size</th><th>Condition Id</th></tr></thead>
      <tbody>
        {#each data.redemptions ?? [] as redemption}
          <tr>
            <td>{redemption.title}</td><td>{redemption.timestamp}</td><td>{redemption.size}</td>
            <td>{redemption.conditionId}</td>
          </tr>
        {:else}
          <tr><td colspan="6">No redemption data.</td></tr>
        {/each}
      </tbody>
    </table>
  {/if}

  {#if activeTab == 4}
    <table class="table">
      <thead><tr><th>Token Id</th><th>Amount</th><th>Avg Price</th><th>Realized Pnl</th><th>Total Bought</th></tr></thead>
      <tbody>
        {#each data.pnl ?? [] as pnl}
          <tr>
            <td>{pnl.tokenId}</td><td>{pnl.amount}</td><td>{pnl.avgPrice}</td>
            <td>{pnl.realizedPnl}</td><td>{pnl.totalBought}</td>
          </tr>
        {:else}
          <tr><td colspan="6">No PnL data.</td></tr>
        {/each}
      </tbody>
    </table>
  {/if}

  {#if activeTab == 5}
    <table class="table">
      <thead><tr><th>Timestamp</th><th>From</th><th>To</th><th>Value</th><th>Token</th><th>Hash</th></tr></thead>
      <tbody>
        {#each Array.isArray(data.chain_raw) ? data.chain_raw : [] as tx}
          <tr>
            <td>{tx.timeStamp}</td><td>{tx.from}</td><td>{tx.to}</td>
            <td>{tx.value}</td><td>{tx.tokenSymbol}</td><td>{tx.hash}</td>
          </tr>
        {:else}
          <tr><td colspan="6">No blockchain data.</td></tr>
        {/each}
      </tbody>
    </table>
  {/if}

</div>  

