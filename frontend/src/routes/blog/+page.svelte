<div class="min-h-screen p-8 max-w-2xl mx-auto">

  <div class="flex justify-between items-center navbar bg-base-100 h-20">
    <h1 class="text-4xl font-black">Development Blog</h1>
    <a href="/" class="text-lg hover:underline">Back to Polywatcher</a>
  </div>

  <div class="divider mb-6"></div>

  <div class="flex flex-col gap-6">

    <div class="py-2">
      <p class="text-sm leading-relaxed mb-4">
        Polywatcher was started because I wanted to learn about APIs, Python and data. Since Prof. <strong>[redacted]</strong> has forbidden the heresy of app development for my Goldsmiths final project, I decided to build it for Sandbox and save my D3 for summertime.
      </p>
      <p class="text-sm leading-relaxed">
        My fascination with prediction markets began in November last year. I learned via X—quite by accident—that some members of <a class="underline" href="https://finance.yahoo.com/news/nigel-farage-adviser-reportedly-whale-130215468.html?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAAeQHReo_asYbCF1H19jWGJmS3rbe-MVMdI-y873CuQXpNcKyzlDKQxTIUkG1jeBMKONaKLAQb4aJfe_wRF4yk90DmUVPm5js5aIDY5R8xBhSJZpRwA5eM5vZsLzx4_EcEEcr6Ms2JXNAcm10ymJCa_aJkcSjVlwxw8SDcndXIyN"> Nigel Farage's inner circle </a> had allegedly made a lot of money betting on USA political outcomes. The shock of discovering that Reform UK were not incorruptible paragons of financial virtue made me fall to my knees in the Sainsbury's biscuit aisle. It was truly disgusting; the way they misuse the funds entrusted to them by hardworking taxpayers in <a class="underline" href="https://bylinetimes.com/2025/12/16/nigel-farages-9m-donor-profits-from-putin-propaganda-platform-while-holding-mod-stake/" target="_blank" rel="noopener noreferrer">Russia</a> and the <a class="underline" href="https://www.theguardian.com/politics/2026/jan/29/nigel-farage-dubai-united-arab-emirates-reform-uk" target="_blank" rel="noopener noreferrer">UAE</a>.
      </p>
    </div>

    <div class="divider"></div>

    <article>
      <h2 class="text-xl font-black mb-4">Phase 1: Learning, v1, FastAPI</h2>
      <p class="text-sm leading-relaxed mb-4">
        To kick off this journey, I learned basic Python from a YouTuber named <a class="underline" href="https://www.youtube.com/@BroCodez" target="_blank" rel="noopener noreferrer">Brocode</a> because his videos are simple and I am rather dumb. <a class="underline" href="https://www.youtube.com/watch?v=0sOvCWFmrtA" target="_blank" rel="noopener noreferrer">Corey Schafer's FastAPI tutorials</a> was chosen over Next.js for the same reason—so I could practice my Python. All in all, I managed about 60 hours of grinding problems in Feb before I had to stop and catch up with schoolwork:
      </p>
      <figure class="my-6">
        <a href="/vscode.png" target="_blank" rel="noopener noreferrer"><img src="/vscode.png" alt="VSCode with Python exercises" class="block w-full rounded" /></a>
        <figcaption class="text-xs text-gray-400 mt-1">Sadly, I might have forgotten a lot of JS in the process.</figcaption>
      </figure>
      <p class="text-sm leading-relaxed mb-4">
        The toughest part of this phase was bridging the gap between the tutorial world and the real world. Looping over a [apple, orange, banana, monkey] is vastly less complicated than unpacking a nested JSON object where the numbers are "strings", the strings are Booleans, and the API documentation doesn't tell you whether asc=false until you scroll halfway to South Africa.
      </p>
      <figure class="my-6">
        <a href="/restfox.png" target="_blank" rel="noopener noreferrer"><img src="/restfox.png" alt="Restfox API testing" class="block w-full rounded" /></a>
        <figcaption class="text-xs text-gray-400 mt-1">Figuring out what data gets returned and how it might be useful.</figcaption>
      </figure>
      <p class="text-sm leading-relaxed mb-4">
        Polymarket's blockchain jargon added another layer of difficulty. What on earth was 'contractAddress'? What's the difference between 'endDate' and 'timestamp' on the closed-positions API endpoint? What is the difference between an event and a market? The learning curve was steep but I eventually figured out how to decipher the wall-of-text, filter by "side" or "eventId", int the relevant var, and return the relevant total by +=.
      </p>
      <p class="text-sm leading-relaxed mb-4">
        The first prototype was made using just FastAPI + Jinja. It examined the age of a wallet, the amount of activity in the first 48 hours, and which markets the wallet was trading in. All simple stuff, but it was such a relief to see data being returned on the page, even if it looked like Craigslist.
      </p>
      <figure class="my-6">
        <a href="/polymarketv1.png" target="_blank" rel="noopener noreferrer"><img src="/polymarketv1.png" alt="Polywatcher v1" class="block w-full rounded" /></a>
        <figcaption class="text-xs text-gray-400 mt-1">Polywatcher v1, running on Jinja2Templates, with just one source of data and no UI. Circa-2002 War on Terror aesthetics entirely accidental.</figcaption>
      </figure>
       <p class="text-sm leading-relaxed mb-4">
      I wish I could do more in-depth research into how insider tradiing detection on Polymarket but the entire field is relatively new. There were no well-worn grooves to follow, or established best practices to consult, even though I did consult with the founder of <a class="underline" href="https://www.chainargos.com" target="_blank" rel="noopener noreferrer">Chain Argos</a>. As inspiration, I studied other formative Polymarket apps like <a class="underline" href="https://hashdive.com" target="_blank" rel="noopener noreferrer">Hashdive</a> and <a class="underline" href="https://github.com/pselamy/polymarket-insider-tracker" target="_blank" rel="noopener noreferrer">Insider-tracker</a>, but I'll be the first to admit: This is a work in progress, not a finished product. Whatever you see here is the result of my thinking, rather than a well-established methodology.
      </p>
    </article>

    <div class="divider"></div>

    <article>
      <h2 class="text-xl font-black mb-4">Phase 2: Airwars, Tailwind, DaisyUI, GitHub, Railway Deployment</h2>
      <p class="text-sm leading-relaxed mb-4">
        My original plan was to slowly refine my Python analysis code till April, then build a beautiful frontend using <a class="underline" href="https://carbondesignsystem.com" target="_blank" rel="noopener noreferrer">IBM Carbon</a>. Unfortunately, this leisurely plan was derailed by me securing an interview with <a class="underline" href="https://airwars.org" target="_blank" rel="noopener noreferrer">Airwars</a>. Not wanting to show up at my meeting with fizzbuzz.py or a Temu AOL website, I started panic-coding a presentable skin over the Python skeleton.
      </p>
      <p class="text-sm leading-relaxed mb-4">
        Svelte was chosen because GitHub informed me that it was Airwars' preferred JS framework. It was a decision I would come to regret because the learning curve was steep. Much steeper than Python and completely at odds with how I thought JS worked.
      </p>
      <figure class="my-6">
        <a href="/airwars.png" target="_blank" rel="noopener noreferrer"><img src="/airwars.png" alt="Airwars website" class="block w-full rounded" /></a>
        <figcaption class="text-xs text-gray-400 mt-1">Probably the wrong kind of OSINT investigation, but who can resist in this economy.</figcaption>
      </figure>
      <p class="text-sm leading-relaxed mb-4">
        The {`{if}`} {`{else}`} blocks were at least somewhat familiar. The most confusing part was the file structure, which made zero sense. I do not understand why tailwindcss was loaded via vite.config.js while the data was loaded through page.server.js. Neither do I fully get the need for app.html as a separate file, while other bits of html sat individually under /routes.
      </p>
      <p class="text-sm leading-relaxed mb-4">
        As a result, a heavy dose of Claude was needed. Individual components like &lt;let activeTab= $state(1)&gt; were coded by me. The overall structure was helped along by AI. Luckily, the visual elements like Tailwind and DaisyUI were not too different from UIkit so I could make actual design decisions instead of surrendering all agency to AI.
      </p>
      <p class="text-sm leading-relaxed mb-4">
        For the most part, I opted for a minimal look since Polywatcher is an internal tool for investigators and journalists. Something that sits on a Slack channel in the newsroom. The analysis was colour-coded to make it easier to assess risk at a glance, but the raw JSON output is also available for those who would rather do their own analysis. An info section was added so users could easily understand what each metric meant and how it was calculated.
      </p>
      <figure class="my-6">
        <a href="/github.png" target="_blank" rel="noopener noreferrer"><img src="/github.png" alt="GitHub commits" class="block w-full rounded" /></a>
        <figcaption class="text-xs text-gray-400 mt-1">Reddit informs me that this is what programmers have instead of rap battles.</figcaption>
      </figure>
      <p class="text-sm leading-relaxed">
        The project was committed to GitHub and deployed to <a class="underline" href="https://railway.app" target="_blank" rel="noopener noreferrer">Railway</a> on advice from Andy. After the app was deployed, I had to take a break because my multimedia projects and CSMP was way overdue.
      </p>
    </article>

    <div class="divider"></div>

    <article>
      <h2 class="text-xl font-black mb-4">Phase 3: Postgres, SQLAlchemy, Async, Pandas, NetworkX and Vibe-coding</h2>
      <p class="text-sm leading-relaxed mb-4">
        For April, my ambition was to create a graph network analysis using the <a class="underline" href="https://polygonscan.com" target="_blank" rel="noopener noreferrer">Polygonscan</a> blockchain API. It would reveal if multiple wallets are coordinating trades on the same market, and if they are funnelling the proceeds towards the same ultimate beneficiary. In fact, I even attended a <a class="underline" href="https://www.gold.ac.uk/calendar/?id=15825" target="_blank" rel="noopener noreferrer">Goldsmiths blockchain seminar</a> to understand more about the nitty-gritty of web3.
      </p>
      <p class="text-sm leading-relaxed mb-4">
        Unfortunately, I'll have to leave this one to <a class="underline" href="https://investors.palantir.com/news-details/2026/Polymarket-Partners-With-Palantir-and-TWG-AI-to-Build-Next-generation-Sports-Integrity-Platform/" target="_blank" rel="noopener noreferrer">Palantir</a> because the sheer amount of data necessary will break Polywatcher and reduce me to tears. To return a list of wallets linked to the profile is perfectly possible. However, to check every wallet our profile has touched against every market our suspected insider is trading in would result in thousands of synchronous API calls in a rate-limited environment. A real software engineer could find a way, but I was too cowardly to return 100 JSON objects at the same time, analyse their links and visualize the whole hairball with NetworkX.
      </p>
      <figure class="my-6">
        <a href="/orange.jpg" target="_blank" rel="noopener noreferrer"><img src="/orange.jpg" alt="Network graph" class="block w-full rounded" /></a>
        <figcaption class="text-xs text-gray-400 mt-1">Knowledge gained -100%, Vitamin C +60%.</figcaption>
      </figure>
      <p class="text-sm leading-relaxed mb-4">To console myself, I added three new modest features:</p>
      <ul class="flex flex-col gap-4 mb-4">
        <li class="text-sm leading-relaxed">
          <span class="font-bold">Creation/Volume + Proximity Analysis:</span> These metrics chain together multiple sequential API calls for a more advanced analysis. Creation/Volume, for example, uses the <a class="underline" href="https://polygonscan.com" target="_blank" rel="noopener noreferrer">Polygonscan</a> API to find the wallet's first known activity. This start-date extracted from the Polygon blockchain is then used to fetch and sum 'BUY' activity for the first 48 hours of the wallet. The aim is to detect 'fresh wallets' that are trading aggressively in their infancy.
        </li>
        <li class="text-sm leading-relaxed">
          <span class="font-bold">SQL Database/Leaderboard:</span> Daily Leaderboard uses the <a class="underline" href="https://polymarket.com" target="_blank" rel="noopener noreferrer">Polymarket</a> Leaderboard API to return the top-performing wallets every day—sorted by PnL. These wallets are stored in my Postgres database and analysed sequentially for the risk of insider trading. I was reluctant to add SQL but it felt like the only sensible solution at this stage. The amount of data generated was increasing at a rapid rate. If I wanted to add new features which were data-intensive, I needed a way to store and query it without crashing the app.
        </li>
      </ul>
      <figure class="my-6">
        <a href="/railway.png" target="_blank" rel="noopener noreferrer"><img src="/railway.png" alt="Railway deployment dashboard" class="block w-full rounded" /></a>
          <figcaption class="text-xs text-gray-400 mt-1">I tried to avoid it for as long as I could but someone at Journocoders told me that the world secretly runs on SQL.</figcaption>
      </figure>
      <ul class="flex flex-col gap-4 mb-4">
        <li class="text-sm leading-relaxed">
          <span class="font-bold">AI Similarity Score:</span> No modern software project is complete without a pointless AI feature. This 100% vibe-coded AI Similarity Score is my take. It extracts the event-slugs returned via the activity API, and sends them to the <a class="underline" href="https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L6-v2" target="_blank" rel="noopener noreferrer">Hugging Face MiniLM sentence-transformer</a>, which then evaluates how similar or divergent the event-slugs are. 0 means totally different and 1 means they're exactly the same. The principles of how it works… are a complete mystery to me, but I am happy to report that Polywatcher's share price has increased by 600% since integrating Agentic AI into our workflow.
        </li>
      </ul>
      <p class="text-sm leading-relaxed">
        In all seriousness: The numbers do not tell you a great deal. The only use case for AI Similarity Score (ASS) is to find bitcoin trading bots, which usually return a value between 0.9–0.99.
      </p>
    </article>

    <div class="divider"></div>

    <article>
      <h2 class="text-xl font-black mb-4">Reflections</h2>
      <p class="text-sm leading-relaxed mb-4">
        Will Polywatcher help you find a ton of insiders, make headlines and secure your promotion at the FBI?
      </p>
      <p class="text-sm leading-relaxed mb-4">
        The short answer is probably not. There's a lot of noise on the prediction markets and Polywatcher is at best a blunt instrument. It gives you a snapshot of how certain wallets behaved on the market. It cannot—as yet—give you a fine-grained proof of an insider making it away with the big bucks and retiring in the Cayman Islands.
      </p>
      <p class="text-sm leading-relaxed mb-4">
        Some traders appear on the leaderboard because they got lucky betting on Arsenal v. Man City. Their huge wins are the result of reckless confidence, not uncanny clairvoyance. On the flipside, real insiders like the infamous <a class="underline" href="https://www.forbes.com/sites/digital-assets/2026/04/24/burdensome-mix-unmasked-soldier-charged-in-first-polymarket-case/" target="_blank" rel="noopener noreferrer">Maduro Whale</a> often do not trigger any of my metrics. Apart from a suspicious 95% similarity on market spread, his wallet looked like a completely normal chump account.
      </p>
      <p class="text-sm leading-relaxed mb-4">
        Ultimately, it depends on your end goal. If you just want a headline like 'Some Dude made $150,000 betting on Keir Starmer calling Badenoch a cunt in Parliament', Polymarket can get you there. If you want a more thorough investigation into sustained insider trading, scams targeting gullible under-21s or frontrunning by HFTs, then it's at best a starting point. My mathematics isn't good enough. I cannot write the algorithms to catch the charlatans in action.
      </p>
      <p class="text-sm leading-relaxed">
        That being said, I don't think it's been a wasted journey because of what I've learned and gained in the process. Returning from Polywatcher to my Jupyter Notebook investigations feels like doing the Stairmaster after a half-Marathon. Whatever might come of this Sandbox project, at least it has served its purpose in expanding my brain. Happy investigating.
      </p>
    </article>

  </div>

  <div class="divider mt-10"></div>
  <p class="text-xs text-gray-400 pb-8">Developed by PJ / Goldsmiths. Contact: pjie001@gold.ac.uk</p>

</div>
