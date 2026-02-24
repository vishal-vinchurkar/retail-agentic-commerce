# NovaMart Slide Deck Talk Track

**Duration:** ~30 minutes total (slides + live demo + Q&A throughout)
**Audience:** Internal Snowflake panel (acting as Chief AI Officer)
**App:** Slide deck on localhost:8503, NovaMart demo on localhost:8501

---

## ZOOM SETUP (before you start)

- **Screen share:** localhost:8503 (slide deck) full screen
- **Second monitor / hidden window:** This talk track
- **Browser tab ready:** localhost:8501 (NovaMart demo) -- don't show yet
- **Browser tab ready:** localhost:8502 (interview app) -- for Prompt 2

---

## VERBAL BRIDGE (before Slide 1, ~15 seconds)

> "For this first prompt, I'm going to put us in a retail scenario. I've built an AI solution end to end in Streamlit and I'll walk you through the pitch and then demo it live. Let's get into it."

*[Slide 1 should already be on screen]*

---

## SLIDE 1: The Retail AI Challenge
**Time: ~3 minutes**

> "Thank you for your time. Today I'm going to walk you through an AI solution built for a retail use case, and then I'll demonstrate it live.
>
> Before the solution, let's set the scene. Retail isn't short on data. It's drowning in it, spread across supply chain, pricing, inventory, loyalty, and customer systems.
>
> According to industry research, retail inventory distortion continues to cost the global industry about **$1.73 trillion annually**. That's the combined cost of out-of-stocks and overstocks, and it persists despite recent investments in data and technology.
>
> By 2025, roughly **77% of e-commerce professionals report using AI daily**, and retailers that deploy AI broadly are seeing measurable revenue growth and cost reductions.
>
> But experience still lags. Nearly **45% of shoppers abandon digital experiences that fail to meet expectations**, especially when search, pricing, inventory, and loyalty systems fail to work together.
>
> We see a clear pattern: retailers want the promise of AI, many are adopting it, but **scaled operational execution remains uneven** as organizations struggle to turn experimentation into production outcomes.
>
> That gap between data, intent, and execution is what I set out to solve."

**What's true and citable:**
- **$1.73T:** IHL Group, September 2025 - inventory distortion cost including out-of-stocks and overstocks. Source: ihlservices.com/news/analyst-corner/2025/09/
- **77% use AI daily:** All About AI, 2025 analysis of e-commerce AI adoption. Source: allaboutai.com/resources/ai-statistics/ai-in-retail/
- **45% abandon:** ContentGrip / VML's 2025 Future Shopper Report - poor CX drives abandonment. Source: contentgrip.com/future-shopper-vml-report/
- **Maturity gap theme:** Widely supported. HKT Enterprise State of AI in Retail 2025. Source: hkt-enterprise.com/resources/Cases/retail-report-state-of-ai-report-2025.pdf
- The birthday party search example is a real, demonstrable problem in keyword-based retail search.

*[CLICK -> right arrow]*

---

## SLIDE 2: From Copilots to Autonomous Agents
**Time: ~2 minutes**

> "The industry has evolved through three AI generations.
>
> First were chatbots: rules-based, scripted, predictable.
>
> Second are copilots: LLMs assist humans, but humans still decide and act.
>
> Third is agentic AI: systems that sense context, make decisions, and take action -- not for novelty, but to deliver outcomes.
>
> At Snowflake, agentic AI means intelligence running on governed enterprise data. Cortex services execute on data where it lives, with security and governance inherited from Snowflake's platform.
>
> In our solution, we use three Cortex services: Search for semantic understanding, Complete for reasoning, and Analyst for analytics intelligence. Streamlit serves as the experience layer, all within Snowflake's compute boundary."

**What's true:** All three Cortex services (Search, Complete, Analyst) are genuinely used with real SQL/API calls in the app. Streamlit is the actual frontend. No external AI APIs are called. Cortex does run within Snowflake's compute on governed data.

*[CLICK -> right arrow]*

---

## SLIDE 3: NovaMart Solution Architecture
**Time: ~3 minutes**

> "This is NovaMart -- an agentic retail intelligence platform built to demonstrate what's possible with Snowflake.
>
> Layer 1 is the frontend. The entire experience you're seeing here, including this deck and the upcoming demo, runs in Streamlit.
>
> Layer 2 splits into two groups. On the left, Snowflake-native services: Cortex Search for semantic product discovery, Cortex Complete for reasoning and recommendations, and Cortex Analyst for analytics queries.
>
> On the right, we represent five protocol patterns. MCP is an emerging open specification for structured context sharing. The others -- orchestration, agent-to-agent coordination, payment flows, and transaction semantics -- are represented as architectural patterns the solution maps to and would be implemented via standard interfaces in production.
>
> Layer 3 is seven specialized agents: Demand Sensing, Customer Intelligence, Inventory Optimizer, Pricing Agent, Fulfilment Orchestrator, Logistics Optimizer, and Supplier Collaboration. They share structured context through the pattern we call agent-to-agent coordination.
>
> Below that, the Cortex services provide the compute and intelligence. The data layer is our NOVAMART_RETAIL database -- real tables for PRODUCT_360, CUSTOMER_360, and SUPPLY_CHAIN.
>
> Finally, the bottom layer represents five Australian distribution centres. The application queries inventory availability across these locations to drive decisions."

**What's true:** The architecture diagram accurately represents the app structure. Cortex Search, Complete, and Analyst are real with actual function calls. The NOVAMART_RETAIL database with PRODUCT_360, CUSTOMER_360, SUPPLY_CHAIN schemas is real in Snowflake. The 5 DCs are mapped in code. The 7 agents are represented as a logical orchestration layer -- they execute sequentially in the app flow, not as independent microservices. Industry protocols are architectural patterns the solution maps to, not protocol implementations.

*[CLICK -> right arrow]*

---

## SLIDE 4: Key Differentiation
**Time: ~3 minutes**

> "Why Snowflake? Let me be specific.
>
> First, there is zero unnecessary data movement. The product catalogue, customer profiles, inventory levels, pricing, and loyalty data already reside in Snowflake. Cortex executes directly on that governed data. There's no copying to an external ML platform, no separate governance layer to build.
>
> Second, Snowflake Intelligence and Cortex Code compress the path from insight to execution. Intelligence gives executives natural language access to governed data. Cortex Code accelerates build velocity for developers and pre-sales teams. Both operate within the same platform boundary.
>
> Third, governance is native. Every Cortex operation respects Snowflake's role-based access controls, masking, and auditing. You don't bolt on governance -- it's inherited.
>
> Fourth, Streamlit turns native AI output into an experience quickly, without external front-end frameworks or separate deployment pipelines.
>
> Finally, the economics are consumption-based. There are no GPU clusters to manage and no separate ML environment fees. The activation effort is significantly reduced because the data foundation is already in place."

**What's true:** Everything here is accurate. Cortex does operate on data within Snowflake. Snowflake Intelligence and Cortex Code are real, current Snowflake products. Governance is inherited from Snowflake's existing RBAC. Streamlit is genuinely part of the Snowflake platform. The app was built by one person. Consumption-based pricing is accurate.

*[CLICK -> right arrow]*

---

## SLIDE 5: Live Demo
**Time: Transition slide, ~30 seconds**

> "Let me show you the orchestrated agent flow live."
>
> *[Switch browser tab to NovaMart on localhost:8501]*

**Demo pacing (~12-14 min with Q&A):**
1. Boot sequence (~30s) - let it land, show the cinematic startup
2. Type the query "Help me plan a birthday party for a 5 year old" (~1 min)
3. Watch the agent cascade - Cortex Search finds semantically relevant products (~2 min, explain what's happening)
4. Show customer intelligence - loyalty tier, points, basket average (~1 min)
5. Show dynamic pricing based on loyalty tier (~1 min)
6. Add items to cart, proceed to checkout (~2 min)
7. Watch fulfilment routing and logistics optimization (~2 min)
8. Show supplier auto-PO trigger (~1 min)
9. Walk through the protocol strip and agent status (~1 min)
10. Interactive Q&A throughout

**During demo, add once:**

> "In this demo, the agents are orchestrated sequentially to make the flow visible. In production, these would run as independent services coordinating through structured APIs. The key point is that the intelligence runs on governed Snowflake data."

**What's true during demo:** Cortex Search is making real SEARCH_PREVIEW() calls against vector embeddings. Cortex Complete is making real LLM calls for recommendations. Customer data comes from a real Snowflake table query. Inventory queries hit real Snowflake tables across DC locations. Agent insights are generated based on real product/customer data but the agents themselves are orchestrated sequentially in the app flow (they're not independent autonomous services running in parallel). The auto-PO is a triggered event in the application logic, not an actual purchase order sent to a supplier system. Dynamic pricing applies tier-based loyalty discounts -- it's not a real-time market-driven pricing engine.

**If asked "are the agents truly autonomous?"** - Be honest: "The agents follow a defined orchestration pattern. Each agent is a logical function that calls Cortex services and queries Snowflake data. They pass context to each other through structured handoffs. In a production implementation, you'd deploy these as independent services with A2A protocol, but in this demo they're orchestrated sequentially to show the end-to-end flow. The key point is that every agent's intelligence comes from Cortex -- Search, Complete, or Analyst -- running on governed data."

*[Switch browser tab back to localhost:8503 slide deck]*
*[CLICK -> right arrow to Slide 6]*

---

## SLIDE 6: What You Just Saw
**Time: ~2 minutes**

> "Four Snowflake-native services executed: Cortex Search for semantic relevance, Cortex Complete for reasoning and recommendations, Cortex Analyst for analytics, and Streamlit for experience.
>
> All seven agents executed in the flow: Demand Sensing, Customer Intelligence, Inventory Optimizer, Pricing Agent, Fulfilment Orchestrator, Logistics Optimizer, and Supplier Collaboration.
>
> Nine components were active -- four Snowflake services and five protocol patterns representing orchestration and structured inter-agent coordination.
>
> From 'help me plan a birthday party' to order confirmation, routing, and auto-replenishment trigger -- one platform boundary, governed, auditable, extensible."

**What's true:** All claims match exactly what was demonstrated. The semantic search distinction (intent-based vs keyword) is real and demonstrable. Cortex Analyst is available in the app even if not shown in every demo flow. Agent execution follows the sequence described. Governance is inherited from Snowflake.

*[CLICK -> right arrow]*

---

## SLIDE 7: Why This Matters
**Time: ~2 minutes**

> "Three value pillars:
>
> 1. Customer experience: agents bridge disconnected functions -- search, pricing, inventory, loyalty -- into one context.
> 2. Supply chain velocity: event-driven decisions outperform weekly batch cycles.
> 3. Intelligence at scale: this architecture scales decisions that would overwhelm manual teams.
>
> The way to get started is a scoped validation sprint on one category and one customer segment. Define a couple of measurable metrics -- search success rate, conversion lift, stockout reduction. Execute a short sprint using Cortex Search and Complete. If the signal moves, expand. It's consumption-based, governed from day one, and expandable without re-architecting.
>
> I'd welcome your perspectives on where you would start inside your own organization."

**What's true:** The three pillars are genuine value propositions of agentic architecture. The POC framing is realistic -- Cortex Search + Complete POCs can indeed deliver results quickly. Consumption-based pricing is accurate. No specific timeline is promised.

---

## KEY THINGS NOT TO CLAIM

1. **Don't say the agents run autonomously in parallel.** They orchestrate sequentially in the demo. Say "orchestrated agent flow" or "agent cascade."
2. **Don't say MCP is implemented.** It's listed as an industry protocol the architecture maps to. If asked, say "the architecture is designed to align with MCP as a context protocol."
3. **Don't say UCP/A2A/AP2/ACP are implemented.** They are architectural patterns. Say "the solution maps to emerging industry commerce protocols."
4. **Don't say the auto-PO is a real purchase order.** It's a triggered event in the app. Say "the system detects the replenishment threshold and generates the PO event."
5. **Don't say dynamic pricing is market-driven.** It's loyalty-tier-based. Say "pricing factors in the customer's loyalty tier."
6. **Don't say this is production-ready.** It's a demo/showcase. Say "this demonstrates the art of the possible" or "this shows what a production architecture would look like."
7. **Don't claim specific ROI numbers.** You don't have production data to back them up.
8. **Don't say "database" when referring to Snowflake.** Use "platform" or "data cloud."

---

## TRANSITION TO PROMPT 2

*[When panel signals to move on, or after Q&A wraps]*

> "Happy to take more questions on the solution, but if we're ready to move to the territory plan, let me switch over."

*[Switch screen share to localhost:8502 -- interview prep app]*
*[Navigate to Executive Summary page]*
*[Switch to INTERVIEW_APP_TALK_TRACK.md on your second monitor]*
