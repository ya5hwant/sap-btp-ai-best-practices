# SAP BTP AI Interview - Comprehensive Problem-Solving Walk-Throughs

## How to Use This Document

This document provides **detailed walk-through talking points** for each use case. Practice articulating these points smoothly in an interview setting—aim for natural conversation, not memorized speech.

Each section follows this flow:
1. **Customer Pain Point** (What's the business problem?)
2. **Discovery Questions** (What would you ask first?)
3. **Your Approach** (How you'd solve it)
4. **Key Architectural Decisions** (Why this tech?)
5. **Implementation Walk-Through** (Step-by-step)
6. **Risk Mitigation** (What can go wrong?)
7. **Success Metrics** (How do you measure success?)

---

# USE CASE 1: Post-Sales Chatbot (Automotive Services)

## Customer Pain Point

**What you'd hear:**
"Our customers call support for simple questions—'When was my last service?', 'What's my warranty status?', 'Can I schedule an appointment?'. These are repetitive, consume support staff, and frustrate customers. We want conversational AI to handle these self-service."

## Discovery Questions (Show Strategic Thinking)

Start by asking:
1. **"How many customer inquiries per day are we talking about?"** 
   - (Helps scope: Is this 100s or 1000s? Affects architecture)
2. **"What are the top 5-10 customer questions we want the bot to handle?"**
   - (Not all questions—focus on high-volume, low-complexity)
3. **"Do you have customer data in a central system or scattered across multiple systems?"**
   - (Affects data layer design)
4. **"What's your acceptable response time—real-time or is 2-3 seconds okay?"**
   - (Affects whether you use streaming, async, etc.)
5. **"If the bot can't answer, what should happen?"**
   - (Escalation strategy: Connect to human agent? Email support?)

## Your Approach (Architecture Pitch)

**"Here's how I'd think about this:**

**Step 1: Scope the Data & Tools**
"First, I'd identify what data the agent needs access to:
- Customer profile (email, VIN, vehicle history)
- Service records (dates, costs, what was serviced)
- Warranty information
- Promotion/offer eligibility
- Appointment availability

I'd load this into memory as CSV initially for fast prototyping, with the plan to migrate to HANA for production."

**Step 2: Design the Agent Architecture**
"I'd use LangGraph—it's a state machine for agentic workflows. Here's why:
- It tracks conversation context (which customer? which vehicle?)
- It orchestrates tool calls in sequence
- It handles errors gracefully (if one tool fails, agent can try another)

The agent is like a smart dispatcher:
- User asks: 'When was my car last serviced?'
- Agent decides: 'First I need to identify the customer. Then fetch their vehicles. Then pull service history.'
- Agent calls tools in order, streams results to user in real-time

**Step 3: Define Tools (The Agent's Capabilities)**
"I'd define these tools:
- `find_client` - Search by email, phone, VIN, name
- `list_vehicles` - Show all vehicles for a client
- `get_service_history` - Last 3 services with dates/costs
- `get_recommendations` - Based on current mileage
- `get_promotions` - Active offers for this vehicle
- `schedule_appointment` - Book a service date

Each tool is a Python function that returns structured data."

**Step 4: Streaming for Better UX**
"Instead of waiting 5 seconds for the full answer, I'd stream results:
- User sees: 'Looking up your vehicle...'
- Then: 'Fetching service history...'
- Then: 'Here are your last 3 services...'

This gives users confidence that something is happening."

**Step 5: Frontend Choice**
"I'd use UI5 Web Components for several reasons:
- SAP's design system (consistent with enterprise apps)
- Responsive chat interface
- Can embed in existing portals
- Modern JavaScript (Vite build, fast)"

## Key Architectural Decisions

### Decision 1: FastAPI + LangGraph (not traditional chatbot builders like Rasa)

**Why FastAPI + LangGraph:**
- ✅ More control (Rasa is a black box)
- ✅ Easy to add custom business logic
- ✅ Scales better (stateless API)
- ✅ Can integrate with any LLM (OpenAI, Anthropic, SAP GenAI Hub)

**What you'd say:**
"I chose LangGraph over Rasa because we need to integrate with existing SAP data. Rasa is great for generic chatbots, but we need the agent to understand 'customer context' and make decisions about tool sequencing. LangGraph gives us that flexibility."

### Decision 2: In-Memory CSV for MVP → HANA for Production

**Why the progression:**
- ✅ MVP (fast to build, easy to iterate)
- ✅ Validate with real users first
- ✅ Then migrate to persistent database
- ✅ HANA for performance + integration with SAP systems

**What you'd say:**
"I'd start with CSVs loaded into memory. This gets us to production quickly. Once we have real usage patterns, we migrate to HANA—better concurrency, caching, and integration with your other SAP systems."

### Decision 3: Session Management Strategy

**What you'd say:**
"For session state (remembering which customer and vehicle):
- Single instance? In-memory dictionary is fine
- Multi-instance (high availability)? Use Redis for distributed state
- 30-minute session timeout for security
- Clear audit trail of all interactions for compliance"

## Implementation Walk-Through

**"Here's how a typical conversation would work:**

```
User: "Hi, I'm John. When was my last oil change?"

1. Agent sees: "John" - ambiguous (multiple customers named John)
   Tool call: find_client("John", context=user_email)
   Result: Customer ID #12345, vehicle_id #5
   
2. Agent now has context (customer #12345, vehicle #5)
   Tool call: get_service_history(customer_id=12345, vehicle_id=5)
   Result: [
       {date: "2024-01-15", service: "Oil change", cost: "$150"},
       {date: "2023-10-22", service: "Tire rotation", cost: "$80"},
       ...
   ]
   
3. Agent generates response:
   "Your last oil change was on January 15th, 2024. 
    Your next recommended service is in May 2024 based on mileage.
    Would you like to schedule an appointment?"
    
4. User: "Yes, can I schedule for next Saturday?"
   Tool call: schedule_appointment(vehicle_id=5, preferred_date="2024-05-11")
   Result: Appointment confirmed for May 11, 9:00 AM
```

**Error Handling Example:**

```
User: "When's my warranty expiring?"
Agent: 'I don't have warranty data in my system. 
        I'm connecting you with a specialist...'
        
→ Falls back to human agent (instead of hallucinating)
```

"

## Risk Mitigation (What Can Go Wrong)

| Risk | How You'd Handle It |
|------|-------------------|
| **Agent calls wrong tool** | Pre-flight validation: check tool exists, required params provided |
| **LLM hallucinates data** | Constrain LLM output to tool results only, no free-form responses |
| **Session timeout mid-conversation** | Log conversation, allow user to resume, show "Your session expired" message |
| **Tool slow (>5 sec)** | Implement timeout + graceful fallback ("Service busy, connecting to agent") |
| **Tool fails** | Error handler tells agent: "That didn't work, try different approach" |
| **Rate limiting on LLM** | Queue-based approach + budget per customer |
| **Privacy/Compliance** | Audit log every tool call + interaction, encryption at rest |

**What you'd say:**
"The biggest risk is the agent getting confused and calling the wrong tool. I'd prevent this by:
1. Detailed tool descriptions in the system prompt
2. Pre-flight validation before execution
3. Clear error messages that guide the agent to retry correctly
4. Monitoring dashboard showing error rates per tool"

## Success Metrics

**"How would we know this succeeded?**

**From Operations:**
- Reduction in support tickets by X% (e.g., 30%)
- Faster resolution time (agent-handled: 1 min vs. human: 10 min)
- Cost savings: X calls × $2 per agent ÷ $0.005 per LLM = ROI in months

**From Users:**
- High satisfaction score (NPS > 50)
- Repeat usage rate (% of customers who come back)
- Escalation rate (<10% of conversations escalate to human)

**From Operations (Technical):**
- Average response time: <2 seconds
- Tool error rate: <1%
- Session timeout/crash: <0.1%"

---

# USE CASE 2: Anomaly Detection in Sales Orders

## Customer Pain Point

**What you'd hear:**
"We're seeing unusual orders slip through—sometimes fraudulent, sometimes data entry errors. Last month we lost €50k on a huge discount given to a new customer. We need to flag high-risk orders automatically without creating so many false positives that our team ignores them."

## Discovery Questions

1. **"How many orders per day are we processing?"**
   - (100s? 1000s? 10000s? Affects real-time vs. batch)
2. **"What causes orders to be 'anomalous'?"** (Show the customer you understand)
   - Unusual discount depth?
   - New customer with large order?
   - Product mix never seen before?
   - Order at 2 AM?
3. **"How many false positives can your team tolerate?"**
   - (If 50% are false positives, they'll ignore the system)
4. **"Do you have historical data of known anomalies?"**
   - (Labeled data → supervised learning. Unlabeled → unsupervised)
5. **"If we flag an order, what happens next?"**
   - (Manual review? Auto-deny? Escalate to manager?)

## Your Approach

**"Here's my problem-solving framework:**

**Phase 1: Understand the Baseline**
"Before building any ML model, I'd ask: What are your current false positive and false negative rates? How much do anomalies actually cost you? This gives us a benchmark to beat.

For example:
- Current process: 5% false positive rate, 20% miss rate (anomalies slip through)
- Our goal: <1% false positive rate, 80% catch rate
- Business impact: Catch 80% of €100k/year in anomalies = €80k savings, minus €5k in review costs = €75k net savings"

**Phase 2: Feature Engineering**
"I'd identify features that distinguish normal from anomalous orders:
- Customer history deviation: 'Is this customer's order 10x their usual size?'
- Order timing: 'Orders from this customer usually at 9 AM, this one at 2 AM?'
- Product mix: 'These products never sell together'
- Discount depth: 'This 70% discount is unusual'
- Margin: 'This order would lose money'

These features capture business logic without me having to hard-code rules."

**Phase 3: Model Selection**
"I'd use Isolation Forest for several reasons:
- No labeled training data needed (good if you don't have 'known anomalies')
- Fast training and prediction
- Interpretable (I can explain why something's anomalous)
- Handles mixed data types (numeric + categorical)

In contrast:
- Neural networks: Need lots of labeled data (you might not have that)
- Simple rules: Miss complex patterns
- One-class SVM: Good, but slower and less interpretable"

**Phase 4: Explainability (The Critical Part)**
"Anomaly detection isn't useful if users don't trust it. So I'd add two layers of explanation:

1. **SHAP (Technical)**: Show which features pushed score toward anomalous
   - Example: 'Score 0.85 (anomalous) because: 
     - 10x order size: +0.4
     - High discount: +0.3
     - New customer: +0.15'

2. **LLM Explanation (Business Language)**: Convert to words
   - Example: 'This order is unusual because John Corp is buying 1000 units (normally 50-100), with a 60% discount, and they're a new customer. We recommend manual review.'

This dual explanation builds trust."

**Phase 5: Fine-Tuning Interface**
"I'd build a UI where analysts can:
- Adjust contamination rate (how many anomalies do you expect? 1%? 5%?)
- Enable/disable specific features
- Set confidence thresholds (only flag >0.9 confidence)
- See real-time impact on false positive rate

This gives them control and builds confidence in the system."

## Key Architectural Decisions

### Decision 1: Batch Processing vs. Real-Time

**What you'd say:**
"For V1, I'd do batch scoring:
- Every 4 hours, re-score all open orders
- Updates dashboard
- Alerts on new anomalies

Why? Because:
- Faster to build (no complex real-time infrastructure)
- More accurate (can look at full day's context)
- Cost-effective (one batch job vs. per-order API calls)

Future: Real-time scoring if needed, but batch usually sufficient."

### Decision 2: Model Retraining Strategy

**What you'd say:**
"Retraining schedule:
- Weekly: Retrain on last 12 months of data
- Trigger: If model performance drops below 80% precision
- Versioning: Keep last 5 model versions for rollback

Process:
1. Training data: Use analyst-validated decisions (what they marked as anomaly)
2. Validation: Test on holdout 20% of orders
3. Comparison: Is new model better than current? If yes → deploy. If no → keep current."

### Decision 3: Dashboard for Analysts

**What you'd say:**
"The UI is critical for adoption. I'd build:
1. **Alert Dashboard**: Red flags sorted by severity
2. **Detailed Order View**: Full order + explanation + recommendation
3. **Fine-tuning Panel**: Adjust contamination rate in real-time
4. **Performance Tracker**: False positive/negative rates over time"

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **False positive rate too high** | Use confidence threshold + manual review queue |
| **Model degrades over time** | Implement drift detection + automated retraining trigger |
| **Stakeholders don't trust model** | Weekly calibration meetings, show ROI metrics |
| **Model catches fraud but customer can't pay** | Add payment capacity check as separate tool |
| **Explainability doesn't work** | A/B test explanations with users, iterate |

**What you'd say:**
"The biggest risk is the team ignoring the system because of too many false positives. I'd prevent this by:
1. Starting conservative (high confidence threshold)
2. Gradually lowering threshold as we gain confidence
3. Weekly metrics review with stakeholders
4. Making sure explanations are clear and actionable"

## Success Metrics

"Success looks like:
- **Financial**: Catch 80% of anomalies, saving €75k annually
- **Operational**: <5% false positive rate (team trusts system)
- **Technical**: Model retraining every week, <1hr training time
- **User Adoption**: 90% of order reviewers using the dashboard"

---

# USE CASE 3: Customer Credit Check

## Customer Pain Point

**What you'd hear:**
"Our credit evaluation is manual and inconsistent. We receive documents from customers—KYC forms, CSF, vendor comments, payment history. One analyst says 'approve', another says 'deny'. We need:
- Consistent data extraction
- Validation across documents (does everything match?)
- Automated policy application
- Compliance audit trail"

## Discovery Questions

1. **"Walk me through your current credit evaluation process."**
   - (Understand current state, pain points)
2. **"How many documents per credit application?"**
   - (3? 5? 10? Affects document handling strategy)
3. **"What's acceptable accuracy for automated extraction?"**
   - (95%? 99%? Affects whether you need human review)
4. **"Who makes the final approval decision—algorithm or human?"**
   - (Compliance question: AI assists vs. AI decides)
5. **"How long does current process take?"**
   - (1 hour? 1 day? Affects ROI)

## Your Approach

**"Here's how I'd architect the solution:**

**Stage 1: Document Extraction (The Input)**
"I'd use SAP Document AI for structured documents (KYC, CSF forms) because:
- Pre-trained on financial documents
- High accuracy (95%+) on standard forms
- Confidence scores (I know which extractions are risky)
- For less structured docs, I'd use LLM vision

Output: Structured JSON with extracted fields and confidence"

**Stage 2: Validation (The Consistency Check)**
"This is critical. I'd implement cross-document validation:
- Does RFC number match across documents?
- Do addresses match (KYC vs. CSF)?
- Is legal name consistent?
- Are payment references consistent?

I'd score validation 0-100%:
- 100%: All checks passed, proceed to scoring
- 70-100%: Most checks passed, flag for review
- <70%: Major inconsistencies, reject or request new docs"

**Stage 3: Credit Policy Engine (The Decision Logic)**
"I'd implement a structured rule engine:
```
IF CAL_Score >= 80:
   Recommendation = APPROVE
   Limit = UNLIMITED
ELIF CAL_Score >= 60 AND Payment_Score >= 75:
   Recommendation = APPROVE_WITH_CONDITIONS
   Limit = €50,000
ELIF Director_Approval_Available:
   Recommendation = ESCALATE_TO_DIRECTOR
ELSE:
   Recommendation = DENY
```

Why rule engine instead of ML?
- Compliance requirement: Need explainability
- Policy changes frequently: Easy to update rules
- Audit trail: Clear reasoning for every decision"

**Stage 4: Scoring Layers**
"I'd calculate multiple scores:
- **CAL (Credit Assessment Level)**: Based on company financials
- **C3M (3-Month Performance)**: Recent payment behavior
- **Risk Score**: Composite of all factors
- **Approval Recommendation**: Final decision with conditions"

**Stage 5: Reporting & Audit**
"Every credit decision produces:
- Executive summary (2 pages: scores, recommendation, next steps)
- Detailed analysis (all checks, extracted data, policy reasoning)
- Audit trail (who approved? when? any overrides?)
- Export to ERP system"

## Key Architectural Decisions

### Decision 1: Phased Approach (Extract → Validate → Score → Report)

**What you'd say:**
"I break this into stages because each stage can be tested independently:
1. Extract: Did we get the data right?
2. Validate: Is the data consistent?
3. Score: Is the score fair?
4. Report: Is the recommendation clear?

This is better than building everything at once because if validation fails, we know it's not an extraction problem."

### Decision 2: Human Review Workflow

**What you'd say:**
"The system doesn't decide—it recommends. We implement three workflows:
1. **High Confidence (>95%)**: Auto-recommend, analyst clicks approve
2. **Medium Confidence (70-95%)**: Show reasoning, analyst reviews, makes decision
3. **Low Confidence (<70%)**: Require additional documents or manual review

This keeps humans in the loop while automating routine cases."

### Decision 3: Multi-Currency & Regional Policies

**What you'd say:**
"We need to handle MXN, USD, EUR. I'd:
- Store approval limits in base currency
- Support region-specific policies (Mexico limits vs. USA limits)
- Version control all policies (Git-based)
- A/B test new policies on historical data before deploying"

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **Document extraction fails** | Fallback to manual entry + OCR preprocessing |
| **Validation rejects legitimate applications** | Flag for manual review instead of auto-reject |
| **Policy too strict/lenient** | A/B test on historical data + quarterly calibration |
| **Director override not tracked** | Log all overrides with reasoning |
| **Compliance audit fails** | Implement complete audit trail with timestamps, signatures |

## Success Metrics

"Success metrics:
- **Speed**: Reduce from 1 day to 2 hours (7x faster)
- **Consistency**: Approval rate variance <5% across analysts
- **Accuracy**: 95%+ match with manual extractions
- **Audit**: 100% compliance on audit requirements
- **Cost**: €5 per application (vs. €30 manual)"

---

# USE CASE 4: Diagram-to-BPMN Converter

## Customer Pain Point

**What you'd hear:**
"Our business analysts draw process diagrams on whiteboards or Visio. Converting them to BPMN format for SAP Build is manual—I spend hours redrawing in Signavio. We need to automate this."

## Discovery Questions

1. **"What formats are these diagrams in?"** (Visio, images, hand-drawn scans?)
2. **"How complex are they?"** (5 steps? 50 steps? Multiple swimlanes?)
3. **"What happens with the BPMN output?"** (Imported to Signavio? SAP Build?)
4. **"How often do you create new diagrams?"** (Weekly? Monthly? Affects ROI)
5. **"Are diagrams mostly consistent or wildly different?"** (Affects prompt engineering)

## Your Approach

**"Here's my strategy:**

**Step 1: Vision Analysis**
"User uploads diagram image → encode as base64 → send to vision LLM (Claude or GPT-4).

The LLM job:
- Identify activities/tasks
- Find decision points
- Spot start/end events
- Trace flow connections
- Recognize swimlanes (if present)"

**Step 2: Structured Extraction**
"I'd use this prompt:

```
Analyze this business process diagram and extract:
1. All activities/tasks (name, type: userTask, serviceTask, etc.)
2. Decision points (condition text)
3. Start and end events
4. Connections between elements
5. Swimlanes (if present)

Return JSON:
{
  'activities': [
    {'id': 'task1', 'name': 'Review Order', 'type': 'userTask'},
    {'id': 'gate1', 'name': 'Approved?', 'type': 'exclusiveGateway'}
  ],
  'flows': [
    {'from': 'task1', 'to': 'gate1', 'label': ''},
    {'from': 'gate1', 'to': 'task2', 'label': 'Yes'}
  ]
}
```

Why JSON? Because it's easy to validate and convert to BPMN."

**Step 3: BPMN Generation**
"I'd use a template-based approach:

```xml
<?xml version="1.0"?>
<bpmn2:definitions ...>
  <bpmn2:process id="process1">
    <!-- Generate from extracted activities -->
    <bpmn2:startEvent id="start1" name="Start"/>
    <bpmn2:userTask id="task1" name="Review Order"/>
    <bpmn2:exclusiveGateway id="gate1" name="Approved?"/>
    
    <!-- Generate from extracted flows -->
    <bpmn2:sequenceFlow id="flow1" sourceRef="start1" targetRef="task1"/>
    <bpmn2:sequenceFlow id="flow2" sourceRef="task1" targetRef="gate1"/>
    <bpmn2:sequenceFlow id="flow3" sourceRef="gate1" targetRef="task2" name="Yes"/>
  </bpmn2:process>
</bpmn2:definitions>
```

"

**Step 4: Validation**
"I'd validate:
1. XSD schema (valid BPMN structure)
2. No orphaned elements (every task connected)
3. All flows have source/target
4. Proper BPMN semantics (gateway has 2+ outgoing flows)"

**Step 5: Preview & Export**
"Show user:
1. Visual preview of generated BPMN (render it)
2. JSON structure (editable)
3. Download as XML for import to Signavio"

## Key Architectural Decisions

### Decision 1: Multi-Model Fallback Strategy

**What you'd say:**
"I'd implement fallback:
1. Try Claude 3.5 Sonnet (best for diagrams)
2. If fails, try GPT-4o
3. If fails, try Gemini 2.5 Pro
4. If all fail, show user extracted structure for manual correction

This ensures we never leave user with nothing."

### Decision 2: Human Correction Workflow

**What you'd say:**
"Even if LLM extraction is 80% right, that's 20% wrong. So I'd:
1. Show extracted JSON
2. Allow user to edit (rename activities, add/remove flows)
3. Regenerate BPMN from corrected JSON
4. Export

This is 80% automatic + 20% human, which is way better than 100% manual."

### Decision 3: Handling Complex Diagrams

**What you'd say:**
"For large diagrams (50+ elements), I'd:
1. Split image into regions (top, middle, bottom)
2. Analyze each region independently
3. Stitch together flows between regions
4. Validate connections

This avoids overwhelming the LLM with a massive image."

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **LLM generates invalid BPMN** | XSD validation + fallback to template |
| **Vision model struggles with hand-drawn diagrams** | Image preprocessing (OCR, contrast enhancement) |
| **Swimlanes get lost** | Explicitly ask LLM about lanes in system prompt |
| **User edits JSON but breaks it** | JSON schema validation on client-side |

## Success Metrics

"Success:
- **Speed**: 5 minutes to convert (vs. 2 hours manual)
- **Accuracy**: 95% match with manual BPMN (in terms of flow logic)
- **Adoption**: 80% of diagrams processed automatically
- **Cost**: €1 per diagram (vs. €50 manual)"

---

# USE CASE 5: AI Log Analyzer

## Customer Pain Point

**What you'd hear:**
"We get thousands of error logs per day. Most are noise or repeats. Operators spend hours finding the critical errors and figuring out what to do. We need intelligent filtering and SAP-aware remediation steps."

## Discovery Questions

1. **"How many logs per day?"** (1000s? 100k? Affects infrastructure)
2. **"Where do logs come from?"** (Application, database, middleware?)
3. **"What percentage are actually critical?"** (1%? 5%?)
4. **"Do you have error codes that correlate to OSS notes?"** (Yes → can automate lookup)
5. **"Current process: How long from error to resolution?"** (30 min? 8 hours?)

## Your Approach

**"Here's my framework:**

**Phase 1: Log Ingestion & Normalization**
"Collect logs from all sources (app servers, DB, middleware) into a central system. Normalize into:
```
{
  'timestamp': '2024-03-22T10:15:30Z',
  'source': 'app-server-01',
  'severity': 'ERROR',
  'error_code': 'RFC_TIMEOUT',
  'message': 'Timeout calling RFC FM_EXECUTE_QUERY after 30s',
  'context': {...}
}
```

This structured format enables fast analysis."

**Phase 2: Intelligent Prioritization**
"Not all errors are equal. I'd use LLM to:
1. Assess severity (CRITICAL, HIGH, MEDIUM, LOW)
2. Identify impact (Which customers affected? Which systems?)
3. Find root cause (Likely causes based on SAP knowledge)
4. Recommend actions (How to fix? Escalation?)

Example:
```
Error: RFC_TIMEOUT
LLM Analysis: 
  Severity: HIGH
  Impact: All reports failing for 200+ users
  Root Cause: Database memory exhausted
  Action: Extend DBMS memory OR optimize query
  OSS Note: SAP Note 12345 - RFC Timeout Solutions
```

"

**Phase 3: Knowledge Grounding**
"I'd integrate SAP OSS notes:
- Extract error code from log
- Search SAP's OSS note database
- Return top 3 relevant notes
- Summarize solutions

This grounds the LLM's recommendations in SAP best practices."

**Phase 4: Correlation & Clustering**
"Related errors often come in bursts:
- Identify error patterns (same error 1000 times in 1 hour)
- Group similar errors
- Show trend over time

Alert operators: 'This error spiked 10x in last 30 minutes. It might be cascading failure.'"

**Phase 5: Dashboard for Operators**
"Build UI showing:
1. Critical alerts (sorted by impact)
2. Trend charts (error rate over time)
3. Detailed analysis (log + explanation + OSS notes)
4. Recommended actions"

## Key Architectural Decisions

### Decision 1: CAP + HANA (Not FastAPI + Postgres)

**What you'd say:**
"I'd use SAP CAP + HANA because:
- Logs can be huge (100GB+ per year)
- HANA's column-store gives fast aggregation queries
- Full-text indexing enables fast log search
- Type safety (TypeScript) reduces bugs in critical system
- XSUAA integration for enterprise auth

FastAPI + Postgres could work but wouldn't scale as well for logs this large."

### Decision 2: Async Processing

**What you'd say:**
"LLM analysis is slow (2-5s per log). We can't block on this. So:
1. Log arrives → immediately store in HANA
2. Async job queue (SAP Event Mesh) → analyze log
3. Update UI with analysis results as they complete
4. Operators see: 'Analysis in progress...' then results appear"

### Decision 3: HANA Optimization

**What you'd say:**
"For billions of logs, I'd:
- Partition by date (daily/weekly partitions)
- Create indexes on error_code, severity, timestamp
- Archive old logs to cold storage after 90 days
- Use columnar compression
- Regular HANA optimization tasks"

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **LLM analysis expensive at scale** | Batch process + cost throttling |
| **Logs arrive faster than analysis** | Implement backpressure, queue depth monitoring |
| **False correlations** | Use statistical correlation + human feedback loop |
| **OSS note integration manual** | Implement SAP API calls for automation |

## Success Metrics

"Success:
- **Speed**: Mean time to detect critical error: <5 min (vs. 30 min)
- **Accuracy**: Automated recommendations save 2 hours per critical incident
- **Coverage**: 95% of errors have actionable recommendations
- **Cost**: Cut log review costs by 40%"

---

# USE CASE 6: Video Incident & Safety Monitoring

## Customer Pain Point

**What you'd hear:**
"We have video feeds from our warehouse. Manually monitoring them for safety violations is expensive and error-prone. Workers aren't wearing hard hats, equipment is operated unsafely. We need automated detection with high confidence (we can't have false alarms that cause unnecessary evacuations)."

## Discovery Questions

1. **"What incidents are most important to catch?"** (Hard hat violations? Fire? Machinery misuse?)
2. **"What's your false alarm tolerance?"** (Evacuate 100 people = not okay to have false positives)
3. **"Do you have live streams or recorded videos?"** (Affects real-time vs. batch)
4. **"What's acceptable latency?"** (Real-time alert or 1-hour delayed analysis okay?)
5. **"Privacy concerns?"** (Recording workers—policy in place?)

## Your Approach

**"Here's my approach:**

**Phase 1: Video Intake & Storage**
"Accept video uploads or stream links. Store temporarily for analysis.

For large files:
- Implement chunked upload (avoid timeouts)
- Validate file format/size
- Store in object storage (not local disk)"

**Phase 2: AI Analysis (Gemini 2.5 Pro via SAP AI Core)**
"Send video/key frames to Gemini 2.5 Pro via SAP AI Core:
```
Analyze this video for workplace safety incidents:
- Hard hat violations (workers near equipment without hard hat)
- Equipment misuse (forklifts not following safety procedures)
- Restricted area breaches (unauthorized access to hazardous areas)
- Emergency situations (fire, injury, etc.)

Return JSON with:
{
  'incidents': [
    {
      'type': 'hard_hat_violation',
      'timestamp': '00:15:30',
      'confidence': 0.92,
      'description': 'Worker near heavy equipment without hard hat'
    }
  ],
  'overall_risk': 'HIGH'
}
```

"

**Phase 3: Incident Processing**
"Filter by confidence threshold:
- <70%: Ignore (probably false positive)
- 70-90%: Flag for human review
- >90%: Immediate alert

Example:
- Hard hat at 92% confidence → Alert supervisor immediately
- Movement that might be worker at 60% → Don't alert (probably shadow)"

**Phase 4: Alert Generation**
"For high-confidence incidents:
1. Alert supervisor in real-time
2. Provide video clip + timestamp
3. Allow 60-second cancel window (verify before evacuation)
4. Log incident for compliance"

**Phase 5: Reporting & Compliance**
"Generate PDF reports:
- Incident summary
- Video clip with timestamp
- Confidence score
- Action taken (alert sent? supervisor reviewed?)
- Audit trail"

## Key Architectural Decisions

### Decision 1: Confidence Thresholds (Not All-or-Nothing)

**What you'd say:**
"I wouldn't alert on every incident. Instead:
- 95%+ confidence: Auto-alert (low false positive risk)
- 85-95% confidence: Alert with 60-sec cancellation window
- 70-85% confidence: Dashboard only (human review)
- <70%: Ignore

This balances safety (we catch real incidents) with practicality (no constant false alarms)."

### Decision 2: Async Processing with Job Queues

**What you'd say:**
"Video analysis takes 5-10 minutes for 1-hour video. We can't block the user. So:
1. User uploads video → get job ID immediately
2. Backend processes video asynchronously
3. User checks progress on dashboard
4. Alerts sent as incidents detected
5. Final report available when complete"

### Decision 3: Privacy & Compliance

**What you'd say:**
"Video of employees is sensitive. I'd implement:
- Only analyze designated hazard areas (not entire warehouse)
- Face blurring (don't need to identify person, only detect hard hat)
- Strict audit trail (who reviewed? when? action taken?)
- Data retention policy (delete raw video after 30 days)"

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **False positive causes unnecessary evacuation** | Confidence threshold + cancellation window |
| **False negative misses real incident** | Start conservative, gradually lower threshold |
| **Privacy violation** | Face blurring + restricted analysis zones |
| **Video processing cost** | Batch off-peak + implement quota per facility |
| **Gemini API unavailable** | Fallback to local ML model (lower accuracy but available) |

## Success Metrics

"Success:
- **Safety**: 100% of hard-hat violations within 1 hour detected
- **False Alarm**: <5% false positive rate
- **Response**: Alert to supervisor in <5 seconds
- **Compliance**: 100% incident audit trail maintained
- **Cost**: €2 per hour of video analyzed"

---

# USE CASE 7: Intelligent Procurement Assistant

## Customer Pain Point

**What you'd hear:**
"Procurement teams spend days extracting contract data—commodity codes, vendor terms, pricing. Manual extraction is slow and error-prone. We need to automate this and integrate with our ERP."

## Discovery Questions

1. **"What data do you need to extract?"** (Commodity codes, prices, payment terms, vendor info?)
2. **"Do commodity codes follow a standard?"** (UNSPSC? CPV? Company-specific?)
3. **"What formats are contracts?"** (PDF? DOCX? Images?)
4. **"Acceptable extraction accuracy?"** (90%? 99%?)
5. **"What happens to extracted data?"** (Into ERP immediately? Manual review first?)

## Your Approach

**"Here's my hybrid approach:**

**Phase 1: Document Parsing**
"Extract text from contracts:
- PDF: Use PyMuPDF (Fitz)
- DOCX: Use python-docx
- Images: Use OCR (Tesseract or SAP Document AI)

Output: Clean text with structure (headers, tables, etc.)"

**Phase 2: Pattern-Based Extraction (Fast & Cheap)**
"Use regex to find commodity codes:
```python
UNSPSC_PATTERN = r'\b([0-9]{8})\b'
CPV_PATTERN = r'\b(CPV-?[0-9]{8})\b'

# Fast, deterministic, no LLM cost
codes = re.findall(UNSPSC_PATTERN, text)
```

If found in known catalog: Mark as VALIDATED (95% confidence)"

**Phase 3: LLM Enrichment (For Ambiguous Cases)**
"For codes not found via patterns, use LLM:
```
Extract commodity codes from this contract text:
{text}

Known codes include: [list of 100 common codes]

Return JSON: {'codes': [...], 'confidence': 0.7, 'reasoning': '...'}
```

This is cheaper than LLM-only because we only call LLM for ~20% of contracts."

**Phase 4: Validation**
"Cross-check extracted codes:
- Does code exist in known catalog?
- Does code make sense for this vendor?
- Is confidence >80%?

If validation fails: Flag for manual review"

**Phase 5: Streamlit UI for Review**
"Show extracted data in editable table:
- Code, description, quantity, unit price
- User can approve or correct
- Changes tracked for audit"

## Key Architectural Decisions

### Decision 1: Pattern-First, LLM Second (Not LLM-Only)

**What you'd say:**
"LLM-only approach would be slow and expensive:
- Each contract = 5-10 LLM calls = $0.50 per contract
- Processing 1000 contracts/day = $500/day = $150k/year

Hybrid approach:
- 80% via patterns = free
- 20% via LLM = $0.10 per contract
- Same accuracy, 1/10th the cost"

### Decision 2: Audit Trail for Compliance

**What you'd say:**
"Every extraction gets logged:
- Original extraction
- User review/corrections
- Timestamp and user ID
- Reasons for corrections

This enables:
- Audits (show compliance)
- Learning (feed corrections back to improve extraction)
- Accountability (track who approved what)"

### Decision 3: Integration with ERP

**What you'd say:**
"After user reviews and approves:
1. Export to CSV/JSON
2. API endpoint to push to ERP
3. Log success/failure
4. Alert user if integration fails"

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **Pattern misses codes** | LLM catches these + user review |
| **LLM hallucinates codes** | Confidence scoring + manual review |
| **User forgets to review** | Notification system + auto-escalation |
| **Integration fails** | Implement retry logic + queue for later |

## Success Metrics

"Success:
- **Speed**: 5 min extraction (vs. 30 min manual)
- **Accuracy**: 95% match with manual
- **Cost**: €0.10 per contract (vs. €5 manual)
- **Throughput**: Process 1000 contracts/day"

---

# USE CASE 8: Purchase Order Extractor (CAP + Document AI)

## Customer Pain Point

**What you'd hear:**
"We receive hundreds of POs daily as PDFs. We need to extract header info, line items, and match customer part numbers to supplier parts. Currently manual—takes 2 hours per PO."

## Discovery Questions

1. **"How many POs per day?"** (100? 1000?)
2. **"Do POs follow a standard format or vary widely?"** (Affects extraction difficulty)
3. **"Do you have customer-supplier part mappings?"** (For matching)
4. **"What's the current error rate?"** (Manual mistakes?)
5. **"Integration with SAP?"** (Need to feed data into MM, SD?)

## Your Approach

**"Here's my end-to-end approach:**

**Phase 1: Document AI Extraction**
"Use SAP Document AI Premium Edition:
- Upload PDF
- Specify document type (PO, Invoice, etc.)
- AI extracts: Header (vendor, dates, totals), line items (part numbers, quantities, prices)
- Outputs: Structured JSON

Why Document AI Premium?
- Pre-trained on financial documents
- High accuracy (95%+) for POs
- Handles table recognition
- Confidence scores included"

**Phase 2: Data Model in HANA**
"Store extracted data:
```
PurchaseOrders table:
- ID, vendor_name, vendor_number, order_date, total_amount, status

POLineItems table:
- ID, po_id, line_number, customer_part_number, description, quantity, unit_price

MaterialMappings table:
- ID, line_item_id, supplier_part_number, confidence, status
```

Why HANA?
- Structured data (POs are relational)
- SQL queries easy for reporting
- Integrates with SAP systems via destinations"

**Phase 3: Material Mapping (LLM)**
"Match customer part to supplier part:
1. Customer part: 'ABC-123'
2. Search internal catalog for matches
3. If exact match found → use it (confidence 95%)
4. If multiple candidates → use LLM to rank:

```
Match customer part ABC-123 ('Bearing assembly 10mm') to:
- Candidate 1: XYZ-456 ('Precision bearing 10mm, ISO standard')
- Candidate 2: XYZ-789 ('Generic bearing, 12mm')

Candidate 1 is better fit. Confidence: 0.85
Reasoning: ISO standard matches customer requirement.
```

"

**Phase 4: Sales Order Matching**
"Link PO line items to sales order items:
- PO line: 100x Part ABC-123 @ €10
- Search sales orders for matching part
- If found → Link PO↔SO for fulfillment tracking"

**Phase 5: Fiori UI**
"Build two Fiori apps (CAP generates OData automatically):
1. **PO Extraction**: Upload PDF, view extracted data, approve
2. **Material Mapping**: Manage customer↔supplier mappings, override if needed"

## Key Architectural Decisions

### Decision 1: Why CAP (Not FastAPI)

**What you'd say:**
"CAP + TypeScript gives us:
- Type safety (financial data can't have bugs)
- OData first-class (Fiori UI connects automatically)
- HANA integration (PO data is relational)
- XSUAA (enterprise auth)
- Rapid UI development (Fiori Elements generate forms automatically)

FastAPI could work, but we'd need to build more manually."

### Decision 2: Document AI vs. LLM Vision

**What you'd say:**
"Document AI for standard POs (95% of cases):
- Pre-trained, high accuracy
- Table extraction is excellent
- Confidence scores built-in

LLM for unusual documents (5% of cases):
- Handwritten notes
- Non-standard formats
- Custom layouts

Hybrid approach: Try Document AI first, fallback to LLM."

### Decision 3: Manual Material Mapping Review

**What you'd say:**
"I wouldn't auto-map without human review. Instead:
- LLM suggests mapping with confidence
- UI shows suggestion + alternatives
- Analyst clicks 'Approve' (1 second)
- Override if needed

This keeps quality high while speeding up workflow."

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **Document AI fails on poor scans** | OCR preprocessing + manual fallback |
| **Material mapping wrong** | Confidence scoring + human review |
| **Performance at scale** | Async batch processing + queue |
| **Data consistency** | Implement idempotency + transaction handling |

## Success Metrics

"Success:
- **Speed**: 2 hours → 5 minutes per PO (24x faster)
- **Accuracy**: 95% extraction accuracy
- **Cost**: €0.50 per PO (vs. €5 manual)
- **Throughput**: Process 1000 POs/day"

---

# USE CASE 9: AI Capability Matcher (Vector Search)

## Customer Pain Point

**What you'd hear:**
"We have 1000s of AI services and 100s of customer products. Matching them manually is impossible—'Which AI service solves your problem?' requires subject matter experts. We need semantic matching, not just keyword matching."

## Discovery Questions

1. **"How often are these catalogs updated?"** (Monthly? Yearly?)
2. **"How many matches per product?"** (Top 3? Top 10?)
3. **"False positive tolerance?"** (Wrong match frustrates customers)
4. **"Do you have descriptions or just names?"** (Affects embedding quality)

## Your Approach

**"Here's my vector search strategy:**

**Phase 1: Prepare Data**
"Upload two CSVs:
1. AI Services: Name, description, category, use cases
2. Client Products: Name, description, use case

Select columns for embedding:
- AI Services: description + category
- Client Products: description + use_case

Combine into single text per row:
- AI Service: 'Generative AI Hub provides LLM access including GPT-4o and Claude for text generation'
- Client Product: 'We need text generation for customer emails'"

**Phase 2: Generate Embeddings**
"Use SAP Gen AI Hub to generate embeddings:
```python
text = 'Generative AI Hub provides LLM access including GPT-4o and Claude'
embedding = genai.embed(text)
# Output: 1536-dimensional vector capturing semantic meaning
```

Store in HANA vector table:
```
service_id | embedding (REAL_VECTOR)
AI-001     | [0.45, 0.23, ..., 0.78]  # Vector with semantic meaning
```

"

**Phase 3: Vector Similarity Search**
"For each client product:
1. Generate embedding
2. Find nearest neighbors in HANA
3. Return top 5 matches

```sql
SELECT service_id, service_name, 
       COSINE_SIMILARITY(embedding, client_embedding) AS score
FROM services
ORDER BY score DESC
LIMIT 5
```

Pure vector search is fast (milliseconds)."

**Phase 4: Optional LLM Re-ranking**
"Vector search gives good results, but LLM adds business context:

```
Given client product 'Email generation' and top 5 AI services,
rank by business fit (1=best):

1. Generative AI Hub - cosine similarity 0.92
2. ChatGPT API - cosine similarity 0.89
3. Document AI - cosine similarity 0.72

Reasoning:
1. Best fit - directly provides LLM for text generation
2. Good - also provides text capabilities but less native
3. Poor fit - optimized for document processing, not text gen
```

"

**Phase 5: Streamlit Dashboard**
"Show results:
1. Match confidence scores
2. LLM reasoning (why is this a good match?)
3. Allow export to CSV"

## Key Architectural Decisions

### Decision 1: Vector Search vs. Keyword Matching

**What you'd say:**
"Keyword matching would miss semantic matches:
- Keyword: 'AI service' vs. 'machine learning' (same thing, different word)
- Vector search: Both have same direction in vector space → matched

Example:
- Keyword: Search for 'chat' won't find 'conversational AI'
- Vector: Both embed similarly → found"

### Decision 2: Optional LLM Ranking

**What you'd say:**
"Pure vector search is 80% of the solution. LLM ranking adds 20% value:
- Vector finds semantically similar
- LLM understands business context

For MVP: Just vectors (fast to build)
For V2: Add LLM ranking (if ROI justifies cost)"

### Decision 3: Refresh Strategy

**What you'd say:**
"Embeddings are expensive to recompute, so:
- If AI catalog updated: Recompute only new services
- If client catalog updated: Compute on-demand (one-time per run)
- Cache results for 1 day
- Full recompute monthly"

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **Embedding model poor quality** | Test multiple models (OpenAI, Sentencebert, SAP) |
| **Vector search returns obvious matches** | Use LLM re-ranking for business context |
| **Large embedding dimensions slow search** | Dimensionality reduction (PCA) or quantization |
| **Cost high with LLM ranking** | Run ranking as background job, return vectors immediately |

## Success Metrics

"Success:
- **Accuracy**: 95% of top matches are relevant
- **Speed**: <1 second to find 5 matches for 100 products
- **Adoption**: 80% of matchings use system recommendation
- **Cost**: €0.001 per match (vs. manual €1 per match)"

---

# USE CASE 10: Email Agent

## Customer Pain Point

**What you'd hear:**
"Email workflows are repetitive. We receive order confirmations, need to forward to fulfillment, create tasks, track follow-ups. A lot of this could be automated, but email systems are complex to integrate."

## Discovery Questions

1. **"What's the primary email workflow?"** (Forward? Categorize? Extract data?)
2. **"Email system?"** (Exchange? Gmail? Lotus?)
3. **"Integration with ERP?"** (Need to create SAP documents?)
4. **"False action tolerance?"** (Send email to wrong person = bad)

## Your Approach

**"Here's my agentic email approach:**

**Phase 1: Email Ingestion**
"Connect to email system (Exchange, Gmail, Lotus):
- New email arrives → extract subject, body, attachments
- Forward to agent
- Keep original in mailbox"

**Phase 2: Agent Analysis**
"LLM analyzes email:
```
Analyze this email:
From: customer@acme.com
Subject: Order #12345 - Status Update
Body: Can you confirm shipment date?

Determine:
1. Intent: [Order question, complaint, urgent request, etc.]
2. Category: [Sales, Support, Finance, etc.]
3. Action: [Respond, forward, create task, etc.]
4. Priority: [URGENT, HIGH, NORMAL, LOW]

Return JSON with recommendation.
```

"

**Phase 3: Tool Orchestration**
"Agent decides which tools to call:
- `categorize_email`: Assign to inbox/label
- `create_task`: Set reminder for follow-up
- `forward_to_team`: Route to fulfillment
- `extract_data`: Parse order number, customer, etc.
- `create_sap_order`: If need to create document in SAP
- `send_response`: Draft auto-reply

Streaming UI shows: 'Categorizing... Creating task... Forwarding to fulfillment...'"

**Phase 4: Human Approval (Optional)**
"For high-risk actions:
- Auto-response to new customers: Auto-send
- Forward to wrong team: Require approval
- Create SAP order: Require approval"

**Phase 5: Action Execution**
"Execute approved actions in order:
1. Label email
2. Create task
3. Forward (with context)
4. Create SAP document"

## Key Architectural Decisions

### Decision 1: Agentic Approach vs. Rules

**What you'd say:**
"Hard-coded rules are brittle:
- 'If subject contains ORDER, forward to fulfillment'
- But what if email says 'Order cancelled'? (should forward to customer service)

Agentic approach is flexible:
- LLM understands context
- Handles edge cases
- Learns from human feedback"

### Decision 2: Streaming Actions

**What you'd say:**
"Show agent working in real-time:
- User sees 'Analyzing email...'
- Then 'Extracting order number...'
- Then 'Forwarding to fulfillment...'

This builds trust that the system is doing what it says."

### Decision 3: Approval Workflow for Critical Actions

**What you'd say:**
"I'd approve certain actions upfront:
- Auto-responses: Yes (low risk)
- Forwarding within organization: Maybe (medium risk)
- Sending to external contacts: No (high risk)
- Creating SAP orders: No (financial impact)

This prevents errors that damage customer relationships."

## Success Metrics

"Success:
- **Volume**: 80% of routine emails processed automatically
- **Speed**: Email to action in <5 minutes (vs. 30 min manual)
- **Accuracy**: <1% wrong routing
- **Time saved**: 10 hours/day for email team"

---

# USE CASE 11: Vendor Selection Optimization (Procurement Analytics)

## Customer Pain Point

**What you'd hear:**
"Vendor selection is complex. We consider cost, lead time, on-time delivery, quality. Currently done manually—different buyers make different choices. We need data-driven vendor selection with AI insights."

## Discovery Questions

1. **"What's your cost model?"** (Just material? Include tariffs, logistics, holding costs?)
2. **"Data quality?"** (Do you have reliable delivery metrics?)
3. **"Vendor dynamics?"** (Exclusive suppliers or multiple options?)
4. **"Optimization goal?"** (Minimize cost? Minimize lead time? Balance both?)

## Your Approach

**"Here's my procurement analytics framework:**

**Phase 1: Data Integration**
"Ingest:
- Vendor master (names, countries, capabilities)
- Price lists (material × vendor × currency)
- Delivery metrics (lead time, on-time rate, in-full rate)
- Tariff data (country-specific import duties)
- Currency rates (for multi-currency comparison)"

**Phase 2: Cost Modeling**
"Calculate Total Cost of Ownership (TCO):
```
TCO = Material Cost 
      + Tariff Cost (material × tariff rate)
      + Holding Cost (inventory carrying cost)
      + Logistics Cost (transportation)
      - Quality Discount (if vendor has perfect track record)
```

Example:
- Vendor A (China): Material €100 + Tariff €10 + Logistics €5 + Holding €8 = €123 TCO
- Vendor B (Europe): Material €110 + Tariff €0 + Logistics €2 + Holding €3 = €115 TCO

Vendor B looks better despite higher material cost."

**Phase 3: Multi-Dimensional Scoring**
"Don't just look at cost:
```
Score = 0.4 × (1 - Cost/Max_Cost)
        + 0.3 × (1 - Lead_Time/Max_Lead_Time)
        + 0.2 × (1 - Late_Delivery_Rate)
        + 0.1 × Quality_Score
```

Example:
- Vendor A: Cost low (0.9), Lead time high (0.5), On-time excellent (0.95), Quality good (0.8)
  Score = 0.4×0.9 + 0.3×0.5 + 0.2×0.95 + 0.1×0.8 = 0.77

- Vendor B: Cost medium (0.7), Lead time low (0.9), On-time good (0.85), Quality excellent (0.95)
  Score = 0.4×0.7 + 0.3×0.9 + 0.2×0.85 + 0.1×0.95 = 0.80

Choose Vendor B."

**Phase 4: Optimization**
"Recommendation algorithm:
```
For each material:
  1. Get eligible vendors
  2. Calculate TCO for each
  3. Consider geographic diversification (not all from China)
  4. Consider vendor capacity constraints
  5. Recommend vendor with best TCO + risk balance
```

"

**Phase 5: AI Insights**
"LLM analyzes data and generates recommendations:
```
Based on procurement data:

Top Opportunity: Material ABC
- Current vendor: China (Cost €100, Lead time 4 weeks)
- Better option: India (Cost €92, Lead time 2 weeks)
- Potential savings: €8 per unit × 10,000 units/year = €80,000/year

Risk: New vendor. Recommendation:
- Start with small order (1000 units)
- Establish SLA for on-time delivery
- Phase in gradually over 6 months
```

"

**Phase 6: Visualization**
"Dashboards showing:
- Vendor performance (cost, lead time, quality)
- Geographic distribution
- Cost breakdown by component
- Optimization opportunities"

## Key Architectural Decisions

### Decision 1: Cost Model Complexity

**What you'd say:**
"Start simple, add complexity:
- V1: Just material cost (fast to build)
- V2: Add tariffs + logistics (more accurate)
- V3: Add holding costs, quality adjustments (production-grade)

Each version refines the recommendation."

### Decision 2: Manual Approval Before Vendor Switch

**What you'd say:**
"Recommendations from AI, but humans decide:
- System: 'Switch to Vendor B, save €80k/year'
- Buyer: 'Okay, but let's start with small pilot order'
- Implement guardrails: Don't switch without approval"

### Decision 3: Data Quality Handling

**What you'd say:**
"Procurement data is messy:
- Lead times vary ±50%
- Quality metrics incomplete
- Currency conversions complex

I'd implement:
- Data validation checks
- Flagging missing/unreliable data
- Conservative estimates (assume worst case) initially"

## Success Metrics

"Success:
- **Savings**: Identify €1M in procurement optimization opportunities
- **Accuracy**: 90% of AI recommendations adopted
- **Adoption**: 80% of procurement decisions use dashboard
- **Time**: Reduce vendor selection time from 2 hours to 30 min"

---

# USE CASE 12: Touchless Transactions (GR & Invoice Bot)

## Customer Pain Point

**What you'd hear:**
"Invoice validation is manual. We compare invoice amount to PO and goods receipt, classify the variance type, and take action. Currently this is done in SAP by operators—tedious, repetitive, error-prone. We want a Microsoft Teams bot that handles this."

## Discovery Questions

1. **"What variance scenarios do you have?"** (Over-invoice? Under-deliver? Late?)
2. **"Approval thresholds?"** (Under €250? Approve auto. Over €250? Need approval?)
3. **"Error tolerance?"** (What % variance is acceptable?)
4. **"How many invoices daily?"** (100s? 1000s?)

## Your Approach

**"Here's my Teams bot approach:**

**Phase 1: Data Ingestion**
"Users upload Excel with invoices:
```
Invoice_Number | PO# | Invoice_Amount | PO_Amount | GR_Amount | Status
INV-001        | PO-123 | 1000 | 1000 | 0 | PENDING
INV-002        | PO-124 | 1100 | 1000 | 0 | PENDING
```

Bot reads the Excel."

**Phase 2: Classification Algorithm**
"For each invoice, determine scenario:
```
Tolerance Rules:
- Acceptable variance: ±5% of PO amount AND ±€250

Scenario Classification:
If Invoice ≤ PO:
  If GR = 0: Scenario 1 (Full receipt confirmation needed)
  If GR > 0: Scenario 4 (Partial receipt)
  If Invoice < GR: Scenario 5 (Return received)

If Invoice > PO:
  Diff = Invoice - PO
  If Diff ≤ 5% AND Diff ≤ €250: Scenario 2 (Within tolerance)
  Elif Diff > 5% BUT Diff ≤ €250: Scenario 3A (Percent exceeded)
  Elif Diff > €250 BUT Diff ≤ 5%: Scenario 3B (Amount exceeded)
  Elif Diff > 5% AND Diff > €250: Scenario 3C (Both exceeded)
  Else: Scenario 7 (Needs investigation)

If PO missing: Scenario 6 (Invoice no PO)
```

"

**Phase 3: Adaptive Cards for User Interaction**
"Bot sends interactive card to Teams:
```
[SCENARIO 1: Full Receipt Confirmation]
Invoice €1000 ready for receipt.
[✅ Confirm Received] [❌ Reject] [❓ Investigate]

[SCENARIO 3C: Variance Investigation]
Invoice €1200 vs. PO €1000 (€200, 20% variance)
Both percentage AND amount exceeded acceptable limits.
[✅ Approve] [❌ Reject] [📋 Add Note] [👤 Escalate to Manager]
```

User clicks button → bot records action → updates SAP"

**Phase 4: Smart Notifications**
"Prioritization:
- Scenario 7 (Needs investigation): Immediate notification
- Scenario 3 (Over-receipt): Notification after 1 hour
- Scenario 1 (Simple receipt): Group 5 together, send once"

**Phase 5: Integration with SAP**
"Bot updates SAP MM (Materials Management):
- Scenario 1: Create goods receipt (GR amount = invoice amount)
- Scenario 3A/B: Partial GR + flag for approval
- Scenario 6: Create purchase order for invoice
- Scenario 7: Create ticket for buyer investigation"

## Key Architectural Decisions

### Decision 1: Microsoft Teams Integration

**What you'd say:**
"Why Teams bot vs. web portal?
- Users already in Teams (don't need new app)
- Notifications native to Teams
- Faster adoption (no training needed)
- Mobile-friendly (works on phone during meetings)"

### Decision 2: Tolerance Thresholds

**What you'd say:**
"Tolerance is business decision, not technical:
- Our system allows configuration: 5% OR €250
- Finance team sets tolerance per vendor/material
- We implement the rules as-is

If tolerance is wrong, tweak and redeploy (easy)."

### Decision 3: Escalation Workflow

**What you'd say:**
"Not all scenarios auto-execute:
- Scenario 1 (receipt): Auto-execute if no open issues
- Scenario 3 (over-receipt): Require approval
- Scenario 7 (investigation): Escalate to procurement manager

Human judgment required for edge cases."

## Success Metrics

"Success:
- **Throughput**: Process 1000 invoices/day (vs. 500 manually)
- **Time**: 30 seconds per invoice (vs. 5 min manual)
- **Error Rate**: <0.5% wrong decisions
- **Adoption**: 95% of team using bot by month 3
- **Cost**: €0.50 per invoice processed (vs. €5 manual)"

---

# Quick Comparison: When to Use Each Pattern

| Problem | Pattern | Why |
|---------|---------|-----|
| Customers want self-service chatbot | Agentic (LangGraph) | Multi-turn, context tracking |
| Detect anomalies in data | ML (Isolation Forest) + Explainability | Interpretability critical |
| Extract from documents | Document AI + LLM | Structured + unstructured |
| Prioritize logs | LLM + Knowledge grounding | Business context matters |
| Analyze images/video | Vision LLM (Gemini) | Advanced visual understanding |
| Pattern extraction | Regex first, LLM second | Fast and cheap baseline |
| Vector semantic search | Embeddings + HANA | Large catalog, semantic matching |
| Workflow automation | Teams bot + agentic | Users in Teams, event-driven |
| Financial decisions | Rule engine | Compliance, explainability |
| Multi-dimensional optimization | Scoring model | Multiple objectives to balance |

---

# Master Interview Preparation Tips

## Before the Interview

1. **Pick one use case to go deep on**
   - Practice the full walk-through (15 minutes)
   - Memorize key decisions and reasoning
   - Be ready for detailed follow-ups

2. **Prepare 2-minute versions of 3-4 use cases**
   - Problem → Solution → Why this tech → One key challenge

3. **Practice articulating trade-offs**
   - "I chose CAP over FastAPI because..."
   - "The risk here is..., so I'd mitigate by..."

## During the Interview

**If they say: "Tell me about a complex AI project"**
- Pick ONE use case (e.g., Credit Check)
- Walk through: problem → discovery questions → approach → architecture → risks → success metrics
- Show you think like a consultant

**If they say: "How would you build this?"**
- Ask clarifying questions first (shows you don't jump to conclusions)
- State your assumptions
- Walk through incrementally (V1 MVP, then V2, then V3)

**If they push back: "What if it fails?"**
- Show you've thought about failure modes
- Explain mitigation
- Show confidence without arrogance

## The Language to Use

**Instead of:** "I'd use FastAPI"
**Say:** "I'd use FastAPI because [reason]. This enables [benefit]. The trade-off is [trade-off]."

**Instead of:** "Machine learning is the answer"
**Say:** "This is a supervised learning problem because [reason]. I'd use [model] because [reason]. The alternative [alternative] doesn't work because [reason]."

**Instead of:** "We'll handle errors later"
**Say:** "Error handling is critical because [business impact]. I'd implement [pattern] to catch failures. Here's my monitoring strategy: [metrics]."

---

**You're now fully prepared to ace any AI architecture interview at SAP! Go get 'em! 🚀**
