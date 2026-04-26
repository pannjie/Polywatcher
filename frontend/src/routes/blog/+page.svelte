<div class="min-h-screen p-8 max-w-2xl mx-auto">

  <div class="flex justify-between items-center navbar bg-base-100 h-20">
    <h1 class="text-4xl font-black">Development Diary</h1>
    <a href="/" class="text-lg hover:underline">Back to Polywatcher</a>
  </div>

  <div class="divider"></div>

  <p class="text-sm text-gray-500 mb-8">A running log of how Polywatcher was built — the decisions, dead ends, and discoveries along the way.</p>

  <div class="flex flex-col gap-10">

    <article>
      <p class="text-xs text-gray-400 font-mono mb-1">April 2026</p>
      <h2 class="text-xl font-black mb-2">v2.2 — Risk Scoring & the Leaderboard</h2>
      <p class="text-sm leading-relaxed">
        The leaderboard was the first time I tried to turn raw on-chain data into something a journalist could actually use. The idea was simple: rank today's top wallets by PNL, then flag anything suspicious alongside it. The hard part was deciding what "suspicious" even means. I landed on six signals — market spread, success rate, creation/volume ratio, 24h deposits, AI similarity, and cashout gap — each with their own colour-coded thresholds. Getting those thresholds right took a lot of trial and error.
      </p>
    </article>

    <div class="divider"></div>

    <article>
      <p class="text-xs text-gray-400 font-mono mb-1">March 2026</p>
      <h2 class="text-xl font-black mb-2">The Naughty List</h2>
      <p class="text-sm leading-relaxed">
        Before any of the automated scoring existed, I kept a plain text file of wallets I'd flagged by hand — the Maduro Whale, the Superbowl insider, a few Iran-linked accounts. It still lives in the repo as <span class="font-mono text-xs bg-base-200 px-1 rounded">naughty_list</span>. Eventually I want to pull it into the UI properly, but for now it's a reminder that the tool started as a notebook and some notes.
      </p>
    </article>

    <div class="divider"></div>

    <article>
      <p class="text-xs text-gray-400 font-mono mb-1">February 2026</p>
      <h2 class="text-xl font-black mb-2">Why Polymarket?</h2>
      <p class="text-sm leading-relaxed">
        Prediction markets are interesting to me journalistically because they sit at the intersection of money and information. When someone bets heavily on an outcome before it's public knowledge, that's a story. Polymarket is on-chain, which means the data is all there — you just have to know how to read it. That's the gap Polywatcher is trying to close: making on-chain prediction market data legible to journalists who aren't blockchain developers.
      </p>
    </article>

    <div class="divider"></div>

    <article>
      <p class="text-xs text-gray-400 font-mono mb-1">January 2026</p>
      <h2 class="text-xl font-black mb-2">Starting Out</h2>
      <p class="text-sm leading-relaxed">
        This started as a Jupyter notebook during my MA at Goldsmiths. I was pulling data from Polymarket's API and Goldsky's subgraph, mostly just to see what was possible. The first thing I built was a basic wallet profiler — paste in an address, get back a summary of what they'd traded. It was rough, but it worked well enough to find some genuinely interesting accounts.
      </p>
    </article>

  </div>

  <div class="divider mt-10"></div>
  <p class="text-xs text-gray-400 pb-8">Developed by PJ / Goldsmiths. Contact: pjie001@gold.ac.uk</p>

</div>
