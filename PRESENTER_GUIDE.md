# NovaMart: Agentic Retail Intelligence Platform
## Live Demo Presenter Guide & LinkedIn Recording Script

> **DISCLAIMER:** "NovaMart" is a completely fictitious company name created solely for this educational demonstration. It has no affiliation with any real company. Any resemblance to an actual entity is purely coincidental. This code is for **educational and experimentation purposes only** and must not be deployed to production. All data is synthetic. See [DISCLAIMER.md](DISCLAIMER.md) for full details.

---

## Quick Reference: Snowflake Cortex Services (Native)

| Service | What It Does | Demo Moment |
|---------|-------------|-------------|
| **Cortex Search** | Semantic product discovery via vector embeddings | AI Thinking panel + search results |
| **Cortex Complete** | LLM inference for agent reasoning and recommendations | Personalized product cards |
| **Cortex Analyst** | Text-to-SQL analytics via semantic model | Analytics dashboard (if connected) |
| **MCP** | Model Context Protocol -- Snowflake's native AI transport layer | Active whenever any Cortex service is invoked |

## Quick Reference: Industry Commerce Protocols

| Protocol | Full Name | Role | Demo Moment |
|----------|-----------|------|-------------|
| **UCP** | Universal Commerce Protocol (Google) | Overarching orchestration | Entire flow from discovery to delivery |
| **A2A** | Agent-to-Agent (Google) | Inter-agent communication | Agent cascade panel -- 7 agents passing context |
| **AP2** | Agent Payment Protocol | Payment orchestration | Checkout with dynamic pricing + loyalty |
| **ACP** | Agent Commerce Protocol (OpenAI) | Commerce transaction | Cart to order confirmation flow |

---

## Running the Showcase App

```bash
cd retail_intelligence_platform
streamlit run app_showcase.py
```

The app defaults to **dark mode** for optimal presentation impact. Use the theme toggle (top bar) to switch between dark and light modes.

---

## Live Demo Script (2 minutes)

### STEP 1: Boot + Opening (0:00 - 0:15)

**What happens on screen:**
- Cinematic boot sequence: NovaMart logo fades in, agent initialization lines appear one by one, progress bar fills
- App loads with dark glassmorphism UI, protocol strip visible below header
- Snowflake Cortex pills (blue) and industry protocol pills (warm) visible in protocol strip
- Floating "Live on Snowflake Cortex" badge visible in bottom-right

**What to say:**
> "This is NovaMart -- a fully agentic retail intelligence platform running live on Snowflake. What you're seeing is 7 specialized AI agents, each powered by Snowflake Cortex, orchestrating the complete commerce experience. Notice the protocol strip at the top -- the blue pills are Snowflake Cortex services powering this natively, and the warm-toned pills on the right are the emerging industry commerce protocols the flow maps to. We're going to light up every single one in the next 90 seconds."

**Key message:** This is production-grade agentic commerce, not a chatbot demo.

---

### STEP 2: Conversational Discovery (0:15 - 0:45)

**What to click:** Type into the search bar: `Help me plan a birthday party for a 5 year old`

**What happens on screen:**
1. AI Thinking Panel appears (dark terminal-style card) -- shows the reasoning chain:
   - "Analyzing query intent..."
   - "Detected occasion: birthday"
   - "Age group identified: child 3-5"
   - "Filtering categories: Toys, Party Supplies, Games"
   - "Querying Cortex Search Service..."
2. Skeleton shimmer loading cards appear
3. Protocol strip: Snowflake pills (**Cortex Search**, **Cortex Complete**, **MCP**) and industry pills (**UCP**, **A2A**) light up
4. Agent panel: agents cascade to active/done states with progress counter
5. Products appear with star ratings, ribbons, personalized AI recommendations

**What to say:**
> "Watch what happens when I type a natural language query. This isn't keyword search -- Cortex Search understands the *intent*. It knows a 5-year-old's birthday party means toys, games, and party supplies. It's filtering *out* garden tools, adult products, and hardware -- things a traditional search would have returned."

> "On the right, you can see Agent-to-Agent in action -- that's an emerging industry protocol. The Demand Sensing agent passes trending data to the Customer Intelligence agent, which passes the customer's PLATINUM tier to the Pricing agent. Structured context flowing between autonomous agents."

> "And the blue pills? That's what Snowflake is powering natively. Cortex Search providing the semantic understanding, Cortex Complete generating those personalized recommendations, and MCP -- Snowflake's Model Context Protocol -- serving as the AI transport layer."

**Key message:** Snowflake Cortex powers the AI natively. Industry protocols describe the pattern. Both are visualized in the strip.

---

### STEP 3: Product Selection + Cart (0:45 - 1:05)

**What to click:** Click "Add to Cart" on 2-3 products, then click "Cart" button

**What happens on screen:**
- Toast notifications confirm items added
- Cart badge updates count
- Agent panel shows 4/7 agents complete
- Activity log streams real-time events

**What to say:**
> "Each product card shows live inventory from the nearest distribution center, dynamic pricing with the customer's loyalty discount applied in real-time, and an AI-generated recommendation specific to the birthday party context. That's the Universal Commerce Protocol -- UCP -- orchestrating demand, inventory, pricing, and customer intelligence into a unified experience."

**Key message:** UCP unifies the agent responses into a cohesive customer experience.

---

### STEP 4: Checkout (1:05 - 1:25)

**What to click:** In the cart dialog, click "Proceed to Checkout", then "Pay"

**What happens on screen:**
1. Cart dialog shows all items with agent-calculated prices
2. Checkout dialog: payment method, total with loyalty discount
3. Protocol strip: **AP2** and **ACP** industry pills light up (now all pills are active)
4. On confirmation: confetti burst, supply chain map animation, all 7 agents show green

**What to say:**
> "Now we enter the payment flow -- that's AP2, the Agent Payment Protocol. The Pricing Agent has calculated the optimal price, the Customer Intelligence Agent has applied the PLATINUM loyalty discount, and the payment is processed with full agent context preserved."

> "And look -- the Agent Commerce Protocol, ACP, wraps this entire transaction. From the moment they said 'Add to Cart' to right now, every step has been agent-mediated. The Fulfillment Orchestrator just selected the optimal distribution center, the Logistics Optimizer calculated the delivery route, and the Supplier Collaboration Agent triggered auto-replenishment."

**Key message:** AP2 and ACP handle the commerce transaction. All Snowflake services and industry protocols are now active.

---

### STEP 5: Order Complete (1:25 - 1:45)

**What happens on screen:**
- Animated supply chain map of Australia shows DC-to-store route
- All 7 agents show green checkmarks with specific completion messages
- Confetti celebration animation
- Order ID, tracking number, and auto-replenishment PO displayed

**What to say:**
> "Every agent has executed. The supply chain map shows the route from the Melbourne Distribution Centre to the Chadstone store. An auto-replenishment purchase order has been generated. And every single transaction is recorded in Snowflake -- queryable, auditable, real-time."

> "What you just saw is the complete agentic commerce loop: 4 Snowflake Cortex services including MCP, 4 industry commerce protocols, 7 AI agents -- from 'Help me plan a party' to 'Your order is confirmed' -- in under 60 seconds."

**Key message:** End-to-end agentic commerce on Snowflake. All Cortex services and industry protocols demonstrated.

---

### STEP 6: Close (1:45 - 2:00)

**What to point out:**
- Protocol strip: all Snowflake blue + industry warm pills illuminated
- Agent panel: 7/7 complete
- Floating badge: "Live on Snowflake Cortex"

**What to say:**
> "This is what agentic retail looks like. Not a chatbot. Not a copilot. A fully autonomous commerce system where AI agents coordinate across every function -- demand, inventory, pricing, fulfillment, logistics, and supplier management -- all powered by Snowflake Cortex."

---

## LinkedIn Recording: Silent Screen Recording (45 seconds)

Silent walkthrough -- no voiceover. The UI tells the story. Add text overlays in post-production (iMovie or CapCut) so viewers following on mute understand each step.

### How to Record on Mac (zero audio)

1. Press **Cmd + Shift + 5** (screenshot toolbar appears)
2. Choose **Record Selected Portion** (dashed rectangle with record dot)
3. Drag selection to fit your browser window
4. Click **Options** > under Microphone select **None**
5. Click **Record**, run through the shot list below, click **Stop** in menu bar
6. File saves to Desktop as `.mov` -- trim in QuickTime with **Cmd + T** if needed

Record at 1080p or higher. Use dark mode. Open in incognito window so boot sequence plays fresh.

### Shot List + Text Overlays

| Time | What to Do | Text Overlay to Add |
|------|-----------|---------------------|
| 0:00-0:03 | Let boot sequence play | **"7 AI Agents Initializing..."** |
| 0:03-0:05 | App loads, pause on UI | **"NovaMart: Agentic Retail on Snowflake Cortex"** |
| 0:05-0:12 | Type: "Help me plan a birthday party for a 5 year old" | **"Natural Language Intent -- Not Keyword Search"** |
| 0:12-0:18 | Let results load, protocols light up | **"Cortex Search Understands Context"** |
| 0:18-0:22 | Click Add to Cart on 2 items | **"Real-time Pricing + Inventory Across 5 DCs"** |
| 0:22-0:28 | Open Cart > Checkout > Pay | **"All Protocols Active -- End-to-End Agent Commerce"** |
| 0:28-0:38 | Order completes, supply chain map animates | **"Auto-Replenishment PO Generated"** |
| 0:38-0:42 | Slow mouse pan across protocol strip | **"Cortex Search / Complete / Analyst / MCP + UCP / A2A / AP2 / ACP"** |
| 0:42-0:45 | Hold on full app with Snowflake badge | **"Powered by Snowflake Cortex"** |

### LinkedIn Post Caption

> Retailers lose $1.75 trillion annually to supply chain inefficiencies. What if AI agents could fix that?
>
> I built NovaMart -- a fully agentic retail commerce platform on Snowflake Cortex. Here's what it does:
>
> A customer types "help me plan a birthday party for a 5 year old."
>
> 7 AI agents activate autonomously:
> - Cortex Search understands intent (not keywords) -- returns toys and party supplies, filters out garden tools
> - Customer Intelligence applies the PLATINUM loyalty discount in real-time
> - Inventory Optimizer checks stock across 5 distribution centers
> - Pricing Agent calculates the optimal price dynamically
> - Fulfillment Orchestrator selects the best DC to ship from
> - Logistics Optimizer plans the delivery route
> - Supplier Collaboration generates an auto-replenishment PO before stock runs out
>
> From discovery to payment to replenishment -- in under 60 seconds.
>
> This is agentic commerce: not a chatbot, not a copilot. Autonomous agents powered by Snowflake Cortex (Search, Complete, Analyst, MCP) and mapping to industry protocols (UCP, A2A, AP2, ACP) to close the gap between customer experience and supply chain execution.
>
> Why does this matter?
> - Customers get intent-driven discovery, not keyword matching
> - Supply chains shift from reactive (run out, reorder, wait) to predictive (sense demand, pre-position, auto-replenish)
> - Every decision is auditable in Snowflake -- real-time, queryable, governed
>
> Built on: Snowflake Cortex (Search + Complete + Analyst) | Streamlit | Python
>
> #AgenticAI #SnowflakeCortex #RetailTech #SupplyChain #AgenticCommerce

---

## Technical Architecture for Q&A

If someone asks "how does this actually work?":

- **Frontend:** Streamlit with custom glassmorphism CSS, dark/light mode
- **AI backbone:** Snowflake Cortex (Search, Complete, Analyst)
- **Data layer:** Snowflake NOVAMART_RETAIL database with Product 360, Customer 360, Supply Chain, and Agent schemas
- **Agent orchestration:** 7 specialized Python agents, each calling Cortex services with structured context passing
- **Real-time:** Live inventory queries, dynamic pricing calculations, and contextual recommendations per request
- **No external APIs:** Everything runs inside Snowflake's ecosystem

---

## Presenter Notes

- **Toggle dark/light mode** mid-demo if you want to show both -- the transition is smooth and impressive
- **Presenter Mode toggle** (bottom-left area) shows a built-in demo script panel with talking points for each step
- **The boot sequence** only plays once per session. To replay it, clear browser cache or open an incognito window
- **Best demo query:** "Help me plan a birthday party for a 5 year old" (triggers all intent detection, age filtering, and contextual recommendations)
- **Backup query:** "I need wireless headphones for my commute" (simpler flow, still shows Cortex Search)
- **If Snowflake is disconnected:** The app gracefully falls back to local sample data. The agent orchestration visualization still works
