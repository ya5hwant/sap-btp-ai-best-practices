# USE CASE 1: Post-Sales Chatbot (Automotive Services)

## Quick Summary
Conversational AI bot for automotive dealership customers—handles warranty status, service history, appointment scheduling. Uses LLM with tool orchestration (LangGraph) to maintain context and call multi-step APIs.

---

## Customer Pain Point

**What you'd hear:**
"Our customers call support for simple questions—'When was my last service?', 'What's my warranty status?', 'Can I schedule an appointment?'. These are repetitive, consume support staff, and frustrate customers. We want conversational AI to handle these self-service."

**Business Impact:**
- 30-40% of support calls are routine/repetitive
- Each call costs €5-10 in labor
- Customer satisfaction drops due to wait times
- Opportunity: Save €100k+/year with automation

---

## Discovery Questions (Show Strategic Thinking)

Ask these **before** jumping to architecture:

1. **"How many customer inquiries per day are we talking about?"** 
   - (Scope: 100s? 1000s? Affects infrastructure scale)
2. **"What are the top 5-10 customer questions we want the bot to handle?"**
   - (Not all questions—focus high-volume, low-complexity)
3. **"Do you have customer data in a central system or scattered across multiple systems?"**
   - (Affects data layer: HANA, API, CRM?)
4. **"What's your acceptable response time—real-time or is 2-3 seconds okay?"**
   - (Affects streaming, async design)
5. **"If the bot can't answer, what should happen?"**
   - (Escalation: Connect to agent? Email support? FAQ link?)

**Why ask these first?**
- Shows you understand scope before designing
- Identifies constraints (compliance, data availability)
- Helps estimate ROI and timeline

---

## Your Approach (Architecture Pitch)

### Step 1: Scope the Data & Tools
"First, I'd identify what data the agent needs access to:
- Customer profile (email, VIN, vehicle history)
- Service records (dates, costs, parts, labor)
- Warranty information (coverage, expiration)
- Promotion/offer eligibility
- Appointment slots availability

For MVP: Load into CSV/memory for fast prototyping. For production: HANA for concurrency + caching."

### Step 2: Design the Agent Architecture (LangGraph)
"I'd use **LangGraph** for multi-turn reasoning:

```
Why LangGraph (not Rasa/simple intent matching)?
- Rasa: Black-box, hard to customize, limited to 1-turn
- Simple intent: Can't maintain context for multi-step tasks
- LangGraph: State machine for agents, tool orchestration, streaming
```

The agent flow:
```
User: "When was my car last serviced?"
  ↓
Agent decides: "First identify customer by email, then fetch vehicles, then get service history"
  ↓
Calls tools in sequence: find_client() → list_vehicles() → get_service_history()
  ↓
Streams results in real-time: "Looking up your vehicle... Fetching history... Found 3 services"
```"

### Step 3: Define Tools (Agent Capabilities)
"I'd create these tools:

```python
# Tools the agent can call
tools = {
  'find_client': Find customer by email/phone/VIN,
  'list_vehicles': Get all vehicles for customer,
  'get_service_history': Fetch last 3 services,
  'get_warranty_status': Check warranty coverage,
  'get_promotions': Find applicable offers,
  'schedule_appointment': Book service slot,
  'get_documentation': Retrieve user manuals/guides
}
```

Each tool:
- Takes structured input (customer_id, vehicle_id)
- Returns structured output (JSON)
- Has clear error handling (tool fails → agent tries alternative)
"

### Step 4: Streaming for Better UX
"Instead of waiting 5 seconds for full answer:
- User sees: 'Looking up your vehicle...'
- Then: 'Fetching service history...'
- Then: 'Here are your last 3 services...'

This increases confidence + reduces bounce rate."

### Step 5: Frontend & Deployment
"Stack choice:
- **FastAPI**: Lightweight Python API, easy integration with LLM tools
- **UI5 Web Components**: Enterprise chat UI, responsive, SAP-branded
- **Cloud Foundry**: Scales horizontally (stateless API + Redis for sessions)"

---

## Key Architectural Decisions

### Decision 1: LangGraph (Not Traditional Chatbot Builders)

**Trade-offs:**
| Choice | Pros | Cons |
|--------|------|------|
| **LangGraph** | Custom logic, state control, streaming, any LLM | More code required |
| **Rasa** | Simple intent, out-of-box NLU | Black-box, limited customization |
| **Simple Rules** | Fast to build | No learning, brittle |

**What you'd say:**
"Rasa is great for generic chatbots. We chose LangGraph because we need:
- Multi-step reasoning (customer → vehicle → service history)
- Integration with real SAP data
- Custom business logic (warranty rules, appointment logic)
- State persistence across turns"

### Decision 2: In-Memory CSV → HANA (Progressive)

**Why phased approach?**
"MVP: Fast iteration with CSV
- Load customers.csv, vehicles.csv, services.csv into memory
- Perfect for <10k customers
- Easier to test and validate

Production: HANA for scale
- Handles 1M+ records
- Concurrent access (multi-customer sessions)
- Better caching + compression
- Integrates with SAP ecosystem"

### Decision 3: Session Management

**What you'd say:**
"For multiple bot instances (high availability):
- **Option 1 (MVP)**: In-memory dict with 30-min timeout
- **Option 2 (Production)**: Redis for distributed state
  - Key: `session_{session_id}`
  - Value: `{customer_id, vehicle_id, history}`
  - TTL: 30 minutes for security"

---

## Implementation Walk-Through

### Example Conversation Flow

```
User: "Hi, I'm John. When was my last oil change?"

STEP 1: Agent identifies customer
  Tool: find_client(name="John", context=user_email)
  Result: customer_id=12345, vehicle_id=5
  ✓ Now agent knows which customer
  
STEP 2: Agent fetches service history
  Tool: get_service_history(customer_id=12345, vehicle_id=5)
  Result: [
    {date: "2024-01-15", service: "Oil change", cost: "$150"},
    {date: "2023-10-22", service: "Tire rotation", cost: "$80"},
    {date: "2023-07-10", service: "Alignment", cost: "$120"}
  ]
  
STEP 3: Agent generates response
  "Your last oil change was January 15th, 2024. 
   Your next recommended service is in May 2024 based on mileage.
   Would you like to schedule an appointment?"
   
STEP 4: User says "Yes"
  Tool: schedule_appointment(vehicle_id=5, preferred_date="2024-05-11")
  Result: Appointment confirmed for May 11, 9:00 AM
  Response: "Your appointment is confirmed! You'll receive SMS reminder on May 10th."
```

### Error Handling Example

```
User: "When's my warranty expiring?"
Agent: "Looking for warranty info..."
Tool: get_warranty_status() → ERROR (data not available)

Instead of hallucinating:
Agent: "I don't have warranty data in my system. 
        Let me connect you with a specialist..."
         
→ Falls back to human agent with context
```

### Code Skeleton (Python)

```python
from langgraph.graph import StateGraph
from fastapi import FastAPI

# Define tools
def find_client(email: str) -> dict:
    customer = customers[customers['email'] == email].iloc[0]
    return {"customer_id": customer['id'], "name": customer['name']}

def get_service_history(customer_id: int) -> list:
    records = services[services['customer_id'] == customer_id].tail(3)
    return records.to_dict('records')

# Define agent graph
graph = StateGraph(state_schema=AgentState)
graph.add_node("identify_customer", find_client_node)
graph.add_node("fetch_history", get_service_history_node)
graph.add_node("generate_response", llm_response_node)

# Add edges (workflow)
graph.add_edge("identify_customer", "fetch_history")
graph.add_edge("fetch_history", "generate_response")

# FastAPI endpoint
@app.post("/chat")
async def chat(message: str, session_id: str):
    result = graph.invoke(
        {"messages": [message], "session_id": session_id},
        stream_mode="updates"  # Enable streaming
    )
    return result
```

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| **Agent calls wrong tool** | Medium | User confusion | Pre-flight validation: check tool exists, params required |
| **LLM hallucinates data** | Medium | Loss of trust | Constrain LLM to tool results only (no free-form responses) |
| **Session timeout mid-conversation** | Low | Poor UX | Log conversation, allow resume, show timeout message |
| **Tool slow (>5 sec)** | Medium | Timeout | Implement timeout + graceful fallback ("Service busy...") |
| **Tool fails completely** | Low | Bot failure | Error handler tells agent: "That didn't work, try alternative" |
| **Rate limiting on LLM API** | Low | Bot unavailable | Queue-based approach + budget per customer |
| **Privacy/Data leaks** | High | Compliance risk | Audit log every tool call, encryption at rest |

**What you'd say:**
"The biggest risk is the agent getting confused and calling wrong tools. I prevent this by:
1. Detailed tool descriptions in system prompt
2. Pre-flight validation before execution
3. Clear error messages that guide agent to retry
4. Monitoring dashboard showing error rates per tool"

---

## Success Metrics

### Financial ROI
- **Calls handled**: 30-40% of support volume → €100k/year savings
- **Cost per interaction**: LLM cost €0.01 vs. agent €5 → 500x cheaper
- **Time to resolution**: 1 min (bot) vs. 10 min (human)

### User Metrics
- **Satisfaction**: NPS > 50 (target: customer feels served)
- **Repeat usage**: >60% of customers return for self-service
- **Escalation rate**: <5% of conversations escalate to human

### Technical Metrics
- **Response time**: <2 seconds (user doesn't feel lag)
- **Tool success rate**: >95% (tools work reliably)
- **Session timeout rate**: <0.1% (sessions stable)

---

## Interview Tips

**If asked "What if customer context is scattered across 3 different systems?"**
- Answer: "I'd implement an abstraction layer that queries all 3 in parallel. Cache results in HANA for future lookups. This keeps the agent simple while fetching data from anywhere."

**If asked "How do you handle ambiguous customer names like 'John'?"**
- Answer: "I'd ask for clarification: 'I found 3 Johns. Can you provide your email or vehicle VIN?' Then disambiguate. If time-sensitive, escalate to human who can see customer history."

**If asked "What about multilingual support?"**
- Answer: "LLM handles this naturally. I'd store customer preferred language in profile. Prompt directs LLM to respond in that language."

---

## Related Use Cases

- **Email Agent** (Similar pattern: LLM + tool orchestration, but for email processing)
- **Agentic Chatbot** (Variation: Teams integration instead of web UI)
- **Customer Credit Check** (Different: Rule-based instead of LLM-based)
