# NovaMart: Demo Talk Track

> **DISCLAIMER:** "NovaMart" is a completely fictitious company name created solely for this educational demonstration. It has no affiliation with any real company. Any resemblance to an actual entity is purely coincidental. This code is for **educational and experimentation purposes only** and must not be deployed to production. All data is synthetic. See [DISCLAIMER.md](DISCLAIMER.md) for full details.

**Total time: ~12 minutes**
- Slides 1-2: 2 minutes (scene setting)
- Live demo: 7-8 minutes
- Closing slide: 2 minutes (architecture one-pager ties it back)

### Delivery Notes

This talk track uses **cadence markers** to guide pacing. Cadence is what separates a presentation from a performance.

- **`[pause]`** = full 1-2 second silence. Let the room absorb. Resist the urge to fill it.
- **`[beat]`** = half-second breath. Just enough to separate two ideas.
- **Short lines** on their own = deliver as standalone declarative sentences. Don't rush into the next one.
- **Parallel structure** ("This is not X. This is not Y. This is Z.") = deliver each at the same pace, same weight, with a beat between each.

The audience remembers rhythm, not information density.

---

## SLIDE 1: AI Assisted Enrichment (0:00 - 1:00)

*[Show the "Agentic AI for Retail Use Cases: AI Assisted Enrichment" slide]*

> "Retailers today are sitting on one of the most valuable datasets in any industry. [beat] Product catalogs. Customer behavior. Supply chain signals. Pricing history. [pause] And most of it lives in Snowflake.
>
> The question is not whether you have the data. [beat] The question is: what happens when you let AI agents *act* on that data? [beat] Not just query it. Act on it. [pause]
>
> That's what we're going to walk through today. Let me start with the foundation.
>
> [pause]
>
> On the left -- Product 360. The single source of truth for every product across every channel. Product data. Pricing. Inventory. Fulfillment. Social. Customer signals. [beat] All in one place.
>
> But here's the problem retailers face. [beat] This data is incomplete. It's inconsistent. It's stale. A listing might be missing attributes. Pricing might be outdated. Descriptions might be too thin to drive conversion. [pause] And humans cannot keep up. Not at scale.
>
> That's where Cortex AI comes in. [beat] At the bottom of this diagram. AI-powered enrichment. Generating descriptions. Filling missing attributes. Categorizing products. Ensuring data is complete, accurate, and fresh -- ready for Google's Enhanced Organic search standard.
>
> And in the middle -- governance. Every enrichment decision is governed. [beat] Auditable. [beat] Compliant. [beat] No black-box AI. Every change is traceable.
>
> Better data means better search. [beat] Better recommendations. [beat] Fewer returns. [pause] When your catalog is enriched by AI, customers find what they're actually looking for."

**Transition:** *[pause]* "So that's the data foundation. [beat] Now let me show you what happens when we add commerce on top."

---

## SLIDE 2: Agentic Commerce (1:00 - 2:00)

*[Show the "Agentic AI for Retail Use Cases: Agentic Commerce" slide]*

> "Everything from the previous slide is still here. The Product 360. The governance. The data agents. [beat] But now -- we add the commerce experience layer.
>
> Notice the connections in the middle. API. A2A. MCP. [beat] These are the protocols that let the data agents talk to the commerce experience. And on the right -- the AI-powered commerce layer. Search to Buy. Shopper Brings Own Agent. Kiosk Experience. [pause]
>
> Here's why this matters. [pause]
>
> Today's retail is fragmented. [beat] A customer searches on a website. [beat] Checks inventory on an app. [beat] Compares prices on Google. [beat] Then walks into a store. [pause] No single system coordinates that journey.
>
> With agentic commerce, AI agents handle the entire flow. [beat] From understanding intent. [beat] To pricing. [beat] Fulfillment. [beat] Delivery. [beat] And replenishment. [pause] Autonomously.
>
> The customer says 'I'm planning a birthday party for a 5-year-old.' [pause] And the system knows. [beat] That means toys. Party supplies. Games. [beat] Not garden tools. Not wine accessories. Not office supplies."

**Transition:** *[pause]* "Enough slides." *[beat]* "Let me show you this. Live."

---

## LIVE DEMO (2:00 - 9:30)

### Step 1: Boot + Opening (2:00 - 2:45)

**Action:** Launch the app (or switch to the already-running tab). The cinematic boot sequence plays.

**On screen:** NovaMart logo fades in, agent initialization lines appear one by one ("Initializing Demand Sensing Agent...", "Initializing Customer Intelligence Agent..."), progress bar fills to 100%.

*Let the boot sequence breathe. Don't talk over the first 2 seconds. Let the audience watch the agents initialize.*

> "This is NovaMart. [beat] Running live on Snowflake Cortex. [pause]
>
> Watch the boot sequence. Seven AI agents. Each one connecting to Snowflake. Loading its context. Standing ready.
>
> Notice the protocol strip at the top. [beat] Blue pills on the left -- those are Snowflake Cortex services. Warm pills on the right -- industry commerce protocols. [beat] UCP is already lit. As we move through the flow, you'll see the rest light up one by one.
>
> On the right -- the agent cascade panel. All seven standing by. [pause] By the time we're done, every single one will have executed.
>
> And at the bottom right: 'Live on Snowflake Cortex.' [beat] This is not a mockup. Every AI call you're about to see hits Snowflake in real-time."

---

### Step 2: Conversational Discovery (2:45 - 4:00)

**Action:** Click into the search bar and type: `Help me plan a birthday party for a 5 year old`

**On screen:** AI Thinking panel appears showing the reasoning chain. Skeleton shimmer loading. Products load. Cortex Search, Cortex Complete pills light up (Snowflake blue), plus UCP, A2A, and MCP pills (industry warm).

> "Now. [beat] I'm not going to search for a product name. [beat] I'm going to describe a situation. [pause]
>
> 'Help me plan a birthday party for a 5-year-old.'
>
> [pause -- let the search run, let the audience watch the AI Thinking panel]
>
> Watch the left panel. Cortex Search is analyzing intent. [beat] It's detected 'birthday' as the occasion. [beat] Age group: child, three to five. [beat] Categories: Toys. Party Supplies. Games. [pause]
>
> Now think about what a traditional search engine would do. [beat] It would return everything containing the word 'birthday.' Birthday cards for adults. Party supplies for office events. Maybe garden decorations. [pause]
>
> Cortex Search doesn't match keywords. [beat] It understands context. [beat] It knows a 5-year-old's birthday means age-appropriate toys. Fun games. Party decorations. [beat] And it's filtering *out* the things that don't belong. Power tools. Wine accessories. Office supplies. [pause]
>
> Look at the protocol strip. [beat] The Snowflake blue pills just lit up. Cortex Search providing the understanding. Cortex Complete generating recommendations. [beat] And on the industry side -- A2A is active. The Demand Sensing agent just passed trending data to Customer Intelligence, which recognized our customer as PLATINUM. MCP is active too -- structured context flowing between agents.
>
> Each product card shows three things the agents calculated in real-time. [beat] Live inventory from the nearest distribution center. [beat] A dynamically calculated price with the PLATINUM 15% discount already applied. [beat] And an AI-generated recommendation specific to the birthday party context. [pause]
>
> This is supply chain optimization at the discovery layer. [beat] We're not just showing products. We're showing products that are in stock. [beat] Priced correctly. [beat] And relevant. [pause] The customer never sees an item they can't actually buy."

---

### Step 3: Product Selection (4:00 - 4:45)

**Action:** Click on a product to see details. Point out the dynamic pricing, inventory levels, and AI recommendation. Then click "Add to Cart" on 2 items. Toast notifications appear.

> "Let me click into this product. [pause] Look at what the agents have assembled.
>
> The Pricing Agent calculated an optimal price. [beat] Not a fixed retail price. [beat] It factors in loyalty tier. Demand trends. Competitive positioning. Inventory levels. [beat] If this were the last 5 units, you'd see a different price than if we had 500.
>
> The Inventory Optimizer checked ATP -- available-to-promise -- across all 5 distribution centers. Melbourne DC: 47 units. Sydney: 23. [beat] Real-time supply chain visibility.
>
> And Cortex Complete generated a personalized recommendation. Not a generic description. [beat] A contextual recommendation for a 5-year-old's birthday party specifically. [pause]
>
> Now -- see UCP lighting up on the protocol strip? [beat] That's the Universal Commerce Protocol. What we're showing here is the exact pattern UCP is designed for -- a single orchestration layer that coordinates discovery, pricing, inventory, and customer context into one unified experience. [pause]
>
> Imagine this on your own website or app. [beat] A customer asks your chatbot 'I need running shoes for a marathon.' [beat] Today your search returns 400 results. [beat] With this pattern, your agents would understand the intent, check stock at the nearest warehouse, apply loyalty pricing, and surface only what's relevant -- in one coordinated response. [beat] That's what UCP enables. [beat] And the data layer powering it? Already in Snowflake.
>
> Let me add a couple of items. [beat] Watch the agent panel. 4 out of 7 agents complete. Demand Sensing. Customer Intelligence. Inventory Optimizer. Pricing Agent. [beat] All done. [beat] The final three activate at checkout.
>
> Real price. Real stock. Real recommendation. [beat] No surprises."

---

### Step 4: Cart Review (4:45 - 5:15)

**Action:** Click the Cart button. Review the items in the cart dialog.

> "Here's the cart. Every item shows the agent-calculated price with the PLATINUM discount applied.
>
> In a traditional system [beat] the pricing engine is separate from inventory. [beat] Which is separate from the loyalty system. [beat] Mismatches happen constantly. A customer gets a price that doesn't reflect their tier. Or buys an item that's actually out of stock. [pause]
>
> With agentic commerce, the agents coordinate in real-time. [beat] The price the customer sees is the price they pay. [beat] And the item they buy is the item that ships.
>
> [pause]
>
> This is where ACP -- the Agent Commerce Protocol -- becomes relevant. [beat] What you're seeing is the pattern ACP describes: an agent-mediated transaction where every step from 'Add to Cart' through to checkout preserves full context. [beat] The agent knows the customer's tier. It knows the intent. It knows the inventory position. [beat] Nothing is lost between steps. [pause]
>
> Think about how this applies to your ecosystem. [beat] Your mobile app. [beat] Your in-store kiosk. [beat] Your call centre. [beat] Even a customer's own AI assistant shopping on their behalf. [pause] ACP gives you a standard way for any of those touchpoints to carry a complete agent-mediated transaction -- not just a shopping cart, but the full context of *why* the customer is buying, *what* the agents decided, and *how* the price was calculated. [beat] That's the difference between a cart and an intelligent transaction."

---

### Step 5: Checkout + Payment (5:15 - 6:15)

**Action:** Click "Proceed to Checkout." The checkout dialog appears with payment method (VISA 4242), total with loyalty discount. Click "Pay."

> "Now we enter checkout. [beat] Watch the protocol strip. [pause]
>
> AP2 lights up. The Agent Payment Protocol. [beat] The Pricing Agent has finalized the calculation. The Customer Intelligence Agent has confirmed the PLATINUM discount. Payment processed with full agent context. [beat] This isn't just a payment gateway. The agent understands *why* this price was calculated -- and preserves that context for audit.
>
> I'll click Pay. [pause]
>
> And there. [beat] ACP. The Agent Commerce Protocol. [beat] Wrapping this entire transaction end-to-end. [pause]
>
> From the moment our customer typed 'birthday party' [beat] to this payment confirmation [beat] every step has been agent-mediated. [pause]
>
> All Snowflake services active. [beat] All industry protocols lit. [beat] That's the complete agentic commerce stack.
>
> No promo codes to hunt for. [beat] No manual discount application. [beat] No 'sorry, that price changed since you added it to cart.' [pause] The agents maintain consistency throughout."

---

### Step 6: Order Completion + Supply Chain (6:15 - 7:30)

**On screen:** Confetti celebration. Supply chain map of Australia animates showing DC-to-store route. All 7 agents show green checkmarks. Order ID, tracking number, and auto-replenishment PO displayed.

*Let the confetti play for a second. Don't talk immediately. Let the visual land.*

> "All seven agents. [beat] Green. [pause]
>
> But the real story is what just happened behind the scenes.
>
> [pause]
>
> The Fulfillment Orchestrator evaluated all 5 distribution centers. [beat] And selected Melbourne. [beat] Why? Highest stock levels. Closest to the delivery address. Throughput capacity available. [beat] That decision happened in milliseconds.
>
> The Logistics Optimizer calculated the route. Melbourne DC to Chadstone. [beat] Carrier availability. Transit time. Cost optimization. [beat] The tracking number you see -- generated in real-time.
>
> And then -- the Supplier Collaboration Agent. [pause] This is the supply chain piece. [beat] It detected that fulfilling this order dropped Melbourne's stock below the reorder threshold. [beat] So it generated a purchase order. Automatically. [beat] The PO number is right there. [beat] That goes to the supplier to replenish inventory *before* we run out.
>
> [pause]
>
> In traditional retail, replenishment happens on a schedule. [beat] Weekly. Sometimes monthly. [beat] By the time the PO is generated, you've already had stockouts. [pause]
>
> With agentic commerce, replenishment is event-driven. [beat] The moment inventory drops below threshold, the agent acts. [beat] Zero lag. [beat] Zero stockouts. [pause]
>
> The customer doesn't see any of this. [beat] They just get their package on time. [beat] But behind the scenes -- payment, fulfillment, routing, replenishment -- all executed autonomously."

---

### Step 7: Demo Wrap (7:30 - 8:00)

**Action:** Point at the protocol strip (all pills lit -- blue Snowflake + warm industry), the agent panel (7/7 green), and the floating "Live on Snowflake Cortex" badge.

> "So. [pause]
>
> All Snowflake Cortex services active. [beat] All industry protocols lit. [beat] Seven out of seven agents complete. [pause]
>
> From 'help me plan a birthday party' [beat] to order confirmed [beat] supply chain routed [beat] and auto-replenishment PO generated. [pause]
>
> All agent-mediated. [beat] All real-time. [beat] All on Snowflake Cortex. [pause]
>
> Let me switch back to the slides and tie this together."

**Transition:** *Switch from demo app back to presentation. Take a breath. The audience needs a moment to shift gears.*

---

## CLOSING SLIDE: NovaMart Architecture One-Pager (8:00 - 10:00)

*[Show the NovaMart architecture diagram -- the Snowflake slide PNG]*

*This is the most important cadence section of the entire presentation. You've shown the demo. Now you walk it back, layer by layer, with authority. Each layer gets the same rhythmic treatment. Slow down. Let each one land.*

> "Now that you've seen it live [beat] let me map what just happened back to the architecture. [pause] Layer by layer.
>
> [pause]
>
> **Layer 1. The frontend.** [beat] That was the UI you just interacted with. Dark mode. Cinematic boot sequence. Mobile responsive. [beat] The front door.
>
> **Layer 2. The protocol layer.** [beat] You watched two groups light up in real-time. Snowflake-native on the left -- Cortex Search, Complete, Analyst, Streamlit. [beat] Industry protocols on the right -- UCP, A2A, MCP, AP2, ACP. [beat] Pill by pill. That's exactly what you saw.
>
> **Layer 3. Seven AI agents.** [beat] Demand Sensing spotted the birthday party trend. [beat] Customer Intelligence recognized PLATINUM. [beat] Inventory Optimizer checked ATP across 5 DCs. [beat] Pricing Agent applied the discount. [beat] Fulfillment selected Melbourne. [beat] Logistics calculated the route. [beat] Supplier Collaboration fired the PO. [pause] Every single one executed.
>
> **Layer 4. Snowflake Cortex.** [beat] Cortex Search with vector embeddings. [beat] Cortex Complete with LLM inference. [beat] Cortex Analyst with the semantic model. [beat] The AI engine underneath everything you just saw.
>
> **Layer 5. The data platform.** [beat] NOVAMART_RETAIL. [beat] Product 360. Customer 360. Supply Chain. Agents. Semantic Models. [beat] Every transaction. Every agent decision. Every PO. [beat] Recorded. Queryable. Governed. In Snowflake.
>
> **Layer 6. Distribution infrastructure.** [beat] Sydney. Melbourne. Brisbane. Perth. Adelaide. [beat] You saw Melbourne selected, the route to Chadstone planned, right there on the supply chain map.
>
> [long pause]
>
> That is the one-pager. [beat] What you just experienced is this architecture. End-to-end. [beat] From the moment a customer typed a query [beat] to the moment a replenishment PO was generated. [beat] Every layer touched. [beat] Every agent active. [beat] Every decision AI-driven and recorded in Snowflake.
>
> [pause]
>
> So why does this matter? [pause]
>
> **First. The customer experience gap.** [beat] Today, search doesn't know about inventory. [beat] Pricing doesn't know about loyalty tier. [beat] Fulfillment doesn't know about demand trends. [pause] Agentic commerce closes that gap. Every agent shares context. The customer gets one seamless experience.
>
> **Second. Supply chain velocity.** [beat] Today's supply chains are reactive. You run out. [beat] You reorder. [beat] You wait. [pause] With agentic commerce, replenishment is event-driven. The Demand Sensing agent sees trends before they become stockouts. [beat] The Supplier agent generates POs before you run out. [beat] React and recover [beat] becomes predict and prevent.
>
> **Third. Scale.** [beat] A human merchandiser manages a few hundred products. [beat] AI agents manage thousands. [beat] With personalized pricing. [beat] Real-time inventory optimization. [beat] Contextual recommendations for every customer. [pause] That's not automation. [beat] That's intelligence at scale.
>
> [long pause]
>
> This is what agentic retail looks like. [pause]
>
> Not a chatbot. [beat] Not a copilot. [beat] A fully autonomous commerce system [beat] powered by Snowflake Cortex. [pause]
>
> The data is already in Snowflake. [beat] The AI is already in Cortex. [beat] The question isn't whether this is possible. [pause] The question is what you'd build first. [pause]
>
> I'd love to hear what resonated -- and where you see this applying."

---

## Quick Reference: Full Presentation Flow

| Time | Phase | Action |
|------|-------|--------|
| 0:00 | **SLIDE 1** | AI Assisted Enrichment -- scene setting |
| 1:00 | **SLIDE 2** | Agentic Commerce -- scene setting |
| 2:00 | **DEMO** | Switch to app, boot sequence plays |
| 2:45 | Demo | Search bar: "Help me plan a birthday party for a 5 year old" |
| 4:00 | Demo | Click product card, point out pricing/inventory/recommendation |
| 4:15 | Demo | "Add to Cart" on 2 products |
| 4:45 | Demo | Click Cart button in header |
| 5:15 | Demo | "Proceed to Checkout" |
| 5:30 | Demo | Click "Pay $XX.XX" |
| 6:15 | Demo | Observe confetti, supply chain map, 7/7 agents green |
| 7:30 | Demo | Point at protocol strip, agent panel, quick recap |
| 8:00 | **CLOSING SLIDE** | Switch back to presentation -- Architecture one-pager |
| 10:00 | Close | Layer-by-layer walkback, "why it matters", Q&A |

## Key Messages to Hit (from dry-run feedback)

1. **Benefits to customer at each step:**
   - Discovery: finds what they actually want (intent, not keywords)
   - Product details: real price, real stock, real recommendation
   - Checkout: no surprises, automatic loyalty discount
   - Delivery: fastest route from optimal DC

2. **Supply chain optimization:**
   - Real-time ATP across 5 DCs
   - Event-driven replenishment (not scheduled)
   - Predict and prevent vs. react and recover
   - Auto-PO generation on order fulfillment

3. **Why we need Agentic Commerce:**
   - Close the customer experience gap (disconnected systems today)
   - Supply chain velocity (reactive to predictive)
   - Intelligence at scale (thousands of products, every customer personalized)
