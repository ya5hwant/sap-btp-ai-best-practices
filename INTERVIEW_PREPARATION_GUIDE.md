# SAP BTP AI Senior Architect Interview - Use Case Preparation Guide

## Executive Overview

The SAP BTP AI Best Practices repository contains 24+ production-ready AI use cases spanning **Generative AI, Machine Learning, Document Processing, and Agentic AI**. You'll be evaluated on your ability to:
1. Architect end-to-end AI solutions on SAP BTP
2. Make tech stack decisions (FastAPI, Streamlit, CAP, UI5)
3. Integrate SAP AI services (Document AI, AI Core, Gen AI Hub)
4. Design scalable, secure, and maintainable systems

---

## Use Case Landscape Summary

| Category | Use Cases | Key Pattern |
|----------|-----------|------------|
| **Generative AI** | Agentic Chatbot, Email Agent, Post-Sales Chatbot, Diagram-to-BPMN, Intelligent Negotiation | LLM-driven agents + streaming |
| **Document Intelligence** | PDF Information Extraction, Customer Credit Check, Sales/PO Extractor | Document AI + LLM extraction |
| **Machine Learning** | Anomaly Detection, AI Capability Matcher | ML models + visualization |
| **Structured Data Processing** | Log Analyzer, Email Cockpit, Intelligent Procurement | Data analysis + rule engines |
| **Video/Media Analysis** | Video Incident Monitoring | Gemini 2.5 Pro + binary files |

---

## Deep Dive: Key Use Cases & Talking Points

### 1. **Post-Sales Chatbot** (Agentic AI - LangGraph Pattern)
**Problem**: Automotive customers need conversational access to service info without navigating complex systems.

**Architecture Highlights**:
- **Backend**: FastAPI + LangGraph (agentic framework)
- **LLM**: OpenAI GPT-4o with multi-tool orchestration
- **Streaming**: NDJSON responses for progressive chat updates
- **Data**: In-memory CSV-based client/vehicle/service data

**Key Components**:
- **Tool System**: LangChain tools for client search, vehicle lookup, service history, recommendations, promotions, appointment booking
- **Session Management**: Persistent conversation context across interactions
- **State Machine**: Track user context (client ID, vehicle ID) across tool calls

**Talking Points**:
- "The agent architecture uses LangGraph's state machine to maintain conversation context and orchestrate tool calls sequentially"
- "Streaming responses (NDJSON) enable real-time tool visibility to users—they see 'Tool: Finding client...' before results"
- "How would you handle session timeout after 30 mins? Consider Redis for distributed state if scaling beyond single instance"
- "Trade-off: In-memory data vs. database—acceptable for MVP, but production needs persistent storage with caching layer"
- **Real-world challenge**: "If a customer asks about a vehicle's warranty, how would you enrich LLM context with external warranty APIs?"

---

### 2. **Anomaly Detection** (Machine Learning - Explainability Focus)
**Problem**: Sales order fraud/anomalies in financial processes need detection with business-friendly explanations.

**Architecture Highlights**:
- **Backend**: FastAPI + scikit-learn (Isolation Forest)
- **Frontend**: SAP UI5 Web Components + Vite
- **Explainability**: SHAP values + LLM-generated natural language explanations
- **Dashboard**: Calendar view + monthly trends + detailed order analysis

**Key Components**:
- **ML Pipeline**: Feature engineering → model training → batch predictions → explainability
- **SHAP Integration**: Feature importance analysis with business context
- **Fine-tuning Interface**: UI for adjusting contamination rate and model parameters
- **Rule-based Fallback**: When ML explanations unavailable, use business rules

**Talking Points**:
- "Explainability is non-negotiable in finance. We combine SHAP (technical) + LLM (business language)"
- "How do you handle retraining? Consider triggered retraining on new data volumes or drift detection"
- "Dashboard pagination strategy for 1M+ orders—use aggregation tables and lazy loading"
- "Model versioning: Store model artifacts with deployment timestamps for audit trails"
- **Real-world challenge**: "A stakeholder rejects an anomaly score. How do you build confidence in the model? A/B test with human reviewers"

---

### 3. **Customer Credit Check** (Document Intelligence + Policy Engine)
**Problem**: Credit evaluation requires extracting data from multiple document types, validating consistency, and applying credit rules.

**Architecture Highlights**:
- **Backend**: FastAPI with multi-stage pipeline
- **Document AI**: SAP Document AI for structured extraction (KYC, CSF, vendor comments)
- **Verification**: Cross-document validation (RFC consistency, address matching)
- **Policy Engine**: Configurable credit rules with multi-currency support
- **Frontend**: Streamlit for interactive workflow

**Key Components**:
- **Extraction Layer**: Document type-specific schemas → AI-powered field extraction
- **Validation Layer**: Consistency checks across documents (legal names, addresses)
- **Scoring Layer**: CAL (Credit Assessment Level), C3M (3-month payment), historical scores
- **Approval Layer**: Role-based decision support (analyst vs. director approval limits)
- **Reporting**: Executive-ready credit reports with AI reasoning

**Talking Points**:
- "Multi-document validation is the hard problem—you need a consistency scoring model, not just string matching"
- "How do you version credit policies? Git-based policy definitions with audit trails of approvals"
- "Currency handling: Do you validate approval limits per currency or convert to base currency?"
- "What's your fallback if Document AI extraction fails? Human review workflow + manual data entry"
- **Real-world challenge**: "A director overrides a denial. How do you track this and recalibrate future decisions?"
- "Explainability: 'Your credit was denied because...'. How do you explain AI decisions to non-technical stakeholders?"

---

### 4. **Diagram-to-BPMN Converter** (Generative AI + Vision)
**Problem**: Manual conversion of process diagrams to BPMN XML is time-consuming and error-prone.

**Architecture Highlights**:
- **Backend**: FastAPI + LLM vision capabilities (Claude, GPT-4, Gemini 2.5)
- **AI Integration**: SAP GenAI Hub for model orchestration
- **Input**: Process diagram images (PNG, SVG, WEBP)
- **Output**: BPMN 2.0 XML compatible with Signavio/SAP Build

**Key Components**:
- **Image Parsing**: Base64 encoding + LLM vision analysis
- **BPMN Generation**: LLM-driven XML generation with validation
- **Multi-model Support**: Fallback to alternative models if primary fails
- **Streaming**: Progressive XML generation with user feedback

**Talking Points**:
- "Vision models excel at diagram understanding, but BPMN XML generation is structured—combine both capabilities"
- "Prompt engineering is critical: How do you enforce valid BPMN syntax? Include schema in system prompt or use structured output"
- "Multi-provider strategy: SAP GenAI Hub abstracts Claude/GPT/Gemini—what's your fallback chain?"
- "Validation: How do you catch invalid BPMN before sending to Signavio? XSD validation + visual preview"
- **Real-world challenge**: "A complex diagram with 50+ nodes. Does LLM output valid BPMN? Implement chunking or hierarchical processing"

---

### 5. **AI Log Analyzer** (CAP Framework + Document Intelligence)
**Problem**: Massive error logs need intelligent prioritization and SAP-aware remediation steps.

**Architecture Highlights**:
- **Stack**: SAP CAP (Cloud Application Programming) + TypeScript + HANA
- **Frontend**: SAP UI5
- **AI Integration**: SAP Generative AI Hub via destinations
- **Database**: HANA-native persistence

**Key Components**:
- **Log Ingestion**: Error log parsing and normalization
- **Prioritization**: LLM-based severity assessment with SAP context
- **Remediation**: SAP-aware next steps (OSS notes, configuration changes)
- **Knowledge Grounding**: Cross-reference SAP documentation

**Talking Points**:
- "CAP provides first-class SAP HANA integration—why use CAP vs. FastAPI? Type safety, OData out-of-box, XSUAA integration"
- "Destination-based AI configuration: How do you rotate API keys? Use SAP Credential Store"
- "Knowledge grounding: Implement RAG (Retrieval-Augmented Generation) for OSS notes context"
- "Rate limiting: What's your strategy for large log ingestion? Queue-based processing with SAP Event Mesh"
- **Real-world challenge**: "Logs arrive faster than processing. How do you handle backpressure?"

---

### 6. **Video Incident & Safety Monitoring** (Enterprise Vision AI)
**Problem**: Real-time workplace safety incident detection from video/audio feeds.

**Architecture Highlights**:
- **Backend**: FastAPI + Google Gemini 2.5 Pro (via SAP AI Core)
- **Frontend**: SAP Fiori (SAP UI5 1.136.7)
- **Media Processing**: Multipart upload + async analysis
- **Authentication**: OAuth 2.0 with SAP AI Core

**Key Components**:
- **Media Management**: Video/audio file library + streaming support
- **AI Analysis**: Gemini 2.5 Pro for safety incident detection
- **Report Generation**: PDF reports with incident details
- **Integration**: OData-style endpoints for enterprise integration

**Talking Points**:
- "Binary media handling at scale: How do you avoid timeouts on large video files? Implement chunked upload + async job processing"
- "OAuth complexity: How do you refresh tokens without disrupting user experience? Background token refresh with exponential backoff"
- "Fiori vs. Web Components: When to use each? Fiori for enterprise UIs with complex role-based workflows; Web Components for custom brand UIs"
- "Cost consideration: Video analysis is expensive—how do you rate-limit or prioritize? Implement quota system with admin controls"
- **Real-world challenge**: "A false positive causes evacuation. How do you handle AI confidence scores and human review workflows?"

---

### 7. **Intelligent Procurement Assistant** (Document Extraction + E-commerce Pattern)
**Problem**: Contract data extraction for procurement—commodity codes, vendor terms, pricing.

**Architecture Highlights**:
- **Backend**: FastAPI + pattern matching + optional LLM
- **Frontend**: Streamlit
- **Document Support**: PDF, DOCX, Excel
- **Data Output**: CSV/JSON for downstream systems

**Key Components**:
- **Text Extraction**: PyMuPDF for PDFs, python-docx for Word files
- **Pattern Matching**: Regex-based commodity code detection
- **Contextual Validation**: Code verification against known catalogues
- **User Review**: Editable interface with audit trails

**Talking Points**:
- "Pattern-based first, LLM as enrichment: Why not pure LLM? Cost and latency—patterns are fast and deterministic"
- "Audit trail: Every user edit must be logged for compliance—implement change tracking in Streamlit session state"
- "Integration: How do you push validated data to SAP? Implement OData endpoints or RFC calls"
- "Commodity code standardization: UNSPSC vs. company-specific codes—how do you handle multiple taxonomies?"
- **Real-world challenge**: "A contract has 10 commodity codes. How do you extract hierarchy and relationships?"

---

### 8. **Purchase Order Extractor** (CAP + Document AI - Enterprise Pattern)
**Problem**: Extract PO data from PDFs and map supplier materials to customer catalogs using AI.

**Architecture Highlights**:
- **Stack**: SAP CAP with TypeScript + SAP HANA + Fiori Elements
- **Document AI**: SAP Document AI - Premium Edition
- **AI Hub**: SAP Generative AI Hub for material mapping
- **UI**: Dual Fiori apps (PO extraction + material mapping)
- **MTA Deployment**: Multi-Target Application on BTP

**Key Components**:
- **PO Extraction**: Document AI → header and line item data
- **AI-Powered Mapping**: LLM-driven customer↔supplier material matching
- **Sales Order Integration**: PO line items matched to SO items
- **Master Data**: Customer, material, CMIR (customer-material reference)
- **Document Preview**: Embedded PDF viewer

**Talking Points**:
- "Document AI capabilities: Structured field extraction + table recognition. How do you handle unstructured sections?"
- "Material mapping complexity: Customer part ABC123 = Supplier XYZ456. How do you validate mapping quality? Training set with manual validations"
- "MTA deployment: Why CAP over microservices? Tight HANA integration, type safety, built-in auth with XSUAA"
- "Performance: Batch PO processing. How do you handle 1000s of PDFs? Async job queues + progress tracking"
- **Real-world challenge**: "Document AI fails on a scanned PDF. How do you handle OCR? Fallback to manual review or implement OCR preprocessing"

---

### 9. **AI Capability Matcher** (Vector Search + Embeddings)
**Problem**: Match client product lists to AI service catalog using semantic similarity.

**Architecture Highlights**:
- **Backend**: FastAPI + SAP HANA vector search
- **Embeddings**: Generated via SAP Gen AI Hub
- **Ranking**: Optional LLM-based re-ranking with reasoning
- **Frontend**: Streamlit with progress tracking

**Key Components**:
- **CSV Upload**: Two catalogs (AI services, client products)
- **Embedding Generation**: Batch embeddings via LLM API
- **Vector Storage**: SAP HANA vector tables for similarity search
- **Ranking & Reasoning**: LLM generates match explanations
- **CSV Export**: Results with confidence scores

**Talking Points**:
- "Vector search strategy: How do you index millions of vectors? Use HANA's built-in vector indexing with appropriate dimensions"
- "Embedding quality: Semantic similarity depends on model choice—how do you evaluate embeddings? Use validation set with known good matches"
- "LLM ranking: Pure vector search often returns obvious matches. LLM adds contextual reasoning—worth the latency trade-off?"
- "Scalability: Batch processing strategy for large catalogs. How do you monitor job status?"
- **Real-world challenge**: "Two companies use different taxonomies. How do you handle semantic mismatches in matching?"

---

### 10. **Email Agent & Agentic Chatbot** (Multi-turn Conversation Pattern)
**Problem**: Email workflows and customer interactions require conversational AI with tool access.

**Architecture Highlights**:
- **Backend**: FastAPI + LangChain/LangGraph
- **Frontend**: UI5 Web Components or Streamlit
- **Tool Integration**: Email APIs, customer data, knowledge bases
- **Streaming**: Real-time response updates

**Key Components**:
- **Tool Definition**: LangChain tools for business operations
- **Agent Loop**: LLM decides which tool to call based on user intent
- **Session State**: Conversation history + tool execution context
- **Streaming**: NDJSON for progressive updates

**Talking Points**:
- "Tool vs. function calling: Which LLM APIs support structured tool calling? GPT-4 Turbo, Claude 3, Gemini 2—SAP GenAI Hub abstracts this"
- "Hallucination risk: Agent calls non-existent email address. How do you validate before execution? Pre-flight checks + error recovery"
- "Cost control: Agents can loop indefinitely. How do you set limits? Max iterations + timeout + cost budgets"
- **Real-world challenge**: "User asks ambiguous question. How does agent clarify? Implement clarification tools that ask follow-up questions"

---

## Architecture Patterns & Design Decisions

### **Pattern 1: FastAPI + Frontend Choice (Vite Web Components vs. Streamlit)**
**When to use**:
- **FastAPI + Streamlit**: Rapid prototyping, internal tools, data science workflows (AI Log Analyzer, Intelligent Procurement)
- **FastAPI + UI5 Web Components (Vite)**: Customer-facing apps, enterprise branding, complex workflows (Post-Sales, Anomaly Detection)
- **CAP + Fiori**: Deep SAP integration, HANA workflows, enterprise governance (Purchase Order Extractor, Log Analyzer v2)

**Talking Points**:
- "Streamlit is great for speed but limited for enterprise UIs—lack of fine-grained control"
- "UI5 Web Components offer SAP design system but require JavaScript skills"
- "CAP gives HANA-first architecture with type safety and OData"

---

### **Pattern 2: Document Intelligence Pipeline**
1. **Extraction**: SAP Document AI or LLM vision
2. **Validation**: Cross-document consistency checks
3. **Enrichment**: External data lookups (KYC, regulatory)
4. **Decision**: Apply business rules (credit scoring, compliance)
5. **Output**: Structured data for downstream systems

**Talking Points**:
- "Document AI is best for structured forms; LLM vision for unstructured diagrams"
- "Validation layer prevents garbage-in-garbage-out"
- "How do you version extraction schemas? Use JSON Schema with versioning"

---

### **Pattern 3: Agentic AI with Streaming**
1. **User Input**: Natural language query
2. **LLM Planning**: Agent decides tool sequence
3. **Tool Execution**: Stream tool calls to user
4. **Response Generation**: Final answer with context
5. **Streaming**: NDJSON chunks for progressive display

**Talking Points**:
- "Streaming visibility improves UX—users see agent thinking"
- "Error recovery: What if a tool fails mid-sequence? Implement retry logic + alternative tools"
- "Cost: Each LLM call is expensive—how do you minimize calls? Use prompt caching and tool result summarization"

---

### **Pattern 4: Machine Learning with Explainability**
1. **Model Training**: Feature engineering + hyperparameter tuning
2. **Prediction**: Batch or real-time inference
3. **Explainability**: SHAP + LLM-generated explanations
4. **Human Review**: Dashboard for expert validation
5. **Feedback Loop**: Retraining on validated decisions

**Talking Points**:
- "Explainability is non-negotiable in regulated industries"
- "SHAP computational cost—how do you handle large feature spaces? Use SHAP approximations or tree explainers"
- "Model drift: How do you detect when model performance degrades? Implement drift detection + automated retraining"

---

## Common Interview Questions & Answers

### Q1: "How do you approach building an AI system on SAP BTP?"
**Answer Structure**:
1. **Understand the problem**: What's the business outcome? (Not "apply AI")
2. **Choose the AI pattern**: Generative AI agents, ML models, document intelligence, vector search
3. **Select tech stack**: Evaluate SAP services (Document AI, AI Core, Gen AI Hub) vs. external (OpenAI, Anthropic, Google)
4. **Design architecture**: Frontend (Fiori, Web Components, Streamlit), backend (FastAPI, CAP), data layer (HANA, external DBs)
5. **Plan for scale**: Async processing, caching, rate limiting, monitoring
6. **Security & governance**: XSUAA, encryption, audit trails, compliance

**Example**: "If I were building an email agent, I'd:
- Confirm the business goal (reduce support ticket volume by 30%?)
- Choose LangGraph for multi-turn orchestration
- Use SAP GenAI Hub to abstract LLM provider
- Build FastAPI backend with tool definitions
- Create Streamlit UI for internal testing
- Implement session management with Redis
- Set up monitoring for hallucination detection"

---

### Q2: "You're asked to extract data from unstructured PDFs at scale. What's your approach?"
**Answer Structure**:
1. **Evaluate extraction methods**: SAP Document AI (structured forms), LLM vision (diagrams), OCR (scanned documents)
2. **Design validation**: Cross-document checks, schema validation, confidence scoring
3. **Handle failures**: Fallback to manual review, implement retry logic
4. **Scale considerations**: Async job queues, batch processing, result caching
5. **Audit & compliance**: Track extraction confidence, log all changes, versioning

**Example**: "I'd use a three-tier approach:
- SAP Document AI for structured invoices (90% accuracy)
- GPT-4 vision for semi-structured contracts (70% accuracy, requires validation)
- Manual review queue for low-confidence results
- Batch processing pipeline with SAP Event Mesh for async jobs
- Redis caching for frequently extracted documents"

---

### Q3: "An LLM agent keeps calling non-existent tools. How do you fix it?"
**Answer Structure**:
1. **Prompt engineering**: Clarify tool definitions, constraints, examples
2. **Validation**: Pre-flight checks before tool execution
3. **Error recovery**: Graceful fallbacks, error messages to user
4. **Monitoring**: Log hallucinations, analyze patterns
5. **Testing**: Implement test suite with adversarial inputs

**Example**: "I'd implement:
- Detailed tool documentation in system prompt with examples
- Pre-call validation (check tool exists, required params provided)
- Error handler that tells agent 'Tool not found, try: [list alternatives]'
- Monitoring dashboard for hallucination rates
- Regular prompt tuning based on failure logs"

---

### Q4: "How do you ensure security for AI applications on SAP BTP?"
**Answer**:
- **Authentication**: XSUAA + OpenID Connect, OAuth 2.0 for service-to-service
- **Encryption**: Data in transit (TLS) + at rest (HANA encryption)
- **API Security**: API keys for service calls, rate limiting, input validation
- **Secrets Management**: SAP Credential Store for API keys, model credentials
- **Audit**: Log all AI decisions, user actions, model changes
- **Data Privacy**: Implement data masking for PII, anonymization for training data

---

### Q5: "How do you measure AI model performance in production?"
**Answer**:
- **Accuracy Metrics**: Precision, recall, F1-score (per use case)
- **Business Metrics**: Throughput, latency, cost per prediction, user satisfaction
- **Drift Detection**: Monitor input distribution changes, prediction drift
- **Explainability**: Audit trail of top factors influencing decisions
- **Feedback Loop**: Collect user feedback, retrain on validated decisions

---

## Deployment & Operations

### Deployment Strategy
1. **Local Development**: `.env` files, Docker for consistency
2. **SAP BTP Cloud Foundry**: 
   - Push with `cf push` or automated deploy scripts
   - Use `manifest.yaml` for app configuration
   - Destinations for service connectivity
   - Buildpacks: `python_buildpack`, `staticfile_buildpack`, `nodejs_buildpack`
3. **Secrets Management**: SAP Credential Store, environment variables
4. **CI/CD**: GitHub Actions → Cloud Foundry deployment

### Key Operations Concepts
- **Scaling**: Horizontal scaling via Cloud Foundry instances
- **Monitoring**: SAP Solution Manager, custom dashboards
- **Logging**: Cloud Foundry logs service + centralized ELK/Splunk
- **Rate Limiting**: Implement per API key quotas
- **Cost Optimization**: Monitor LLM API calls, batch processing, caching

---

## Sample Architecture Decision Questions

**Q: "Should we use SAP GenAI Hub or call OpenAI directly?"**
- GenAI Hub: Abstraction layer, compliance, multi-provider support
- Direct OpenAI: Lower latency, simpler setup, less control
- Answer: "GenAI Hub for enterprise (compliance, audit), direct for MVP (speed)"

**Q: "FastAPI or CAP for this microservice?"**
- FastAPI: Lightweight, Python ML ecosystem, flexible
- CAP: HANA-first, type safety, OData, XSUAA integration
- Answer: "CAP if tightly coupled with HANA; FastAPI if independent services"

**Q: "Streamlit or React for this dashboard?"**
- Streamlit: Rapid prototyping, data science focus, limited customization
- React: Full control, complex workflows, larger team effort
- Answer: "Streamlit for internal tools; React/UI5 for customer-facing apps"

---

## Red Flags & How to Avoid Them

| Risk | What Interviewers Listen For |
|------|------------------------------|
| **Ignoring explainability** | "This model is accurate—trust it" | Do you discuss SHAP, audit trails, human review? |
| **No error handling** | No mention of fallbacks or retry logic | Can you handle Document AI failures? |
| **Scaling afterthought** | Single-instance architecture | Do you address batch processing, caching, async jobs? |
| **Security gaps** | No mention of XSUAA, secrets, encryption | How do you protect API keys and PII? |
| **Unclear business value** | "We need an ML model" vs. "This reduces cost by X%" | Can you tie AI to business metrics? |
| **Over-engineering** | Using Kubernetes when Cloud Foundry suffices | Can you balance simplicity and scalability? |

---

## Key Takeaways for Interview

1. **Understand the business problem first**—not "use AI" but "reduce manual effort by 40%"
2. **Know the SAP BTP AI services**: Document AI, AI Core, GenAI Hub—when to use each
3. **Familiar with common patterns**: Agentic AI, document intelligence, ML with explainability, vector search
4. **Operational thinking**: Scaling, monitoring, security, cost optimization
5. **Real-world challenges**: How do you handle failures, edge cases, compliance?
6. **Trade-offs**: Speed vs. accuracy, cost vs. performance, complexity vs. simplicity
7. **Be precise about architecture**: Why FastAPI + Streamlit vs. CAP + Fiori?
8. **Discuss governance**: Model versioning, audit trails, human-in-the-loop workflows

---

## Pre-Interview Checklist

- [ ] Clone the repo and run one use case locally
- [ ] Review the `best-practices/` folder for AI fundamentals
- [ ] Understand each use case's business value
- [ ] Identify the AI pattern used in each (agentic, ML, document intelligence, vector search)
- [ ] Review the tech stack choices and be ready to defend them
- [ ] Think about how you'd scale each application
- [ ] Prepare 3-5 thoughtful questions about their architecture
- [ ] Have a mental model of common failure points

---

## Resources for Deeper Learning

1. **SAP BTP Documentation**: https://cap.cloud.sap/docs/
2. **SAP AI Services**: Document AI, AI Core, GenAI Hub
3. **LangGraph/LangChain**: https://python.langchain.com/docs/langgraph/
4. **Streamlit**: https://docs.streamlit.io/
5. **SAP UI5**: https://ui5.sap.com/
6. **FastAPI**: https://fastapi.tiangolo.com/
7. **SHAP**: https://shap.readthedocs.io/
8. **SAP Cloud Foundry**: https://help.sap.com/viewer/product/SAP_BTP/Cloud

---

**Good luck with your interview! Focus on understanding the business problem, making thoughtful architecture decisions, and showing operational maturity.**

---

# COMPREHENSIVE USE CASE Q&A - INTERVIEW ANSWERS

## Format: How to Practice These Answers

For each use case, prepare a **2-3 minute elevator pitch** covering:
1. **Problem Statement** (What's the business challenge?)
2. **Your Proposed Solution** (Architecture + tech stack)
3. **Key Implementation Details** (Specific patterns/technologies)
4. **Challenges & How You'd Handle Them** (Real-world complexity)
5. **Scaling Considerations** (How do you make it production-ready?)

---

## Use Case 1: Post-Sales Chatbot

### Full Answer:

**Problem Statement:**
"In the automotive industry, customers want quick answers about their service history, vehicle details, and appointment scheduling without calling support. Currently, they have to navigate a complex customer portal or wait for support agents—this creates friction and support costs."

**My Proposed Solution:**
"I'd build an AI agent-powered chatbot using LangGraph for orchestration. Here's why:
- **LangGraph** gives us a state machine to track conversation context (which customer, which vehicle)
- **LangChain tools** let us define discrete business operations—each one becomes a callable tool
- **Streaming responses** (NDJSON format) make the agent's thinking visible to users
- **CSV-based data** for MVP, with plan to migrate to persistent database for production

The agent works like this:
1. User sends natural language query: 'When was my last service?'
2. Agent invokes 'find_client' tool, retrieves client ID
3. Agent invokes 'list_vehicles' tool, shows options if multiple vehicles
4. Agent invokes 'get_service_history' tool, retrieves last 3 services
5. Agent generates natural language response

This is better than a hard-coded chatbot because the agent can reason about tool sequencing."

**Architecture:**
```
User → UI5 Frontend
  ↓
FastAPI Backend (Session management)
  ↓
LangGraph Agent (Orchestration)
  ↓
LangChain Tools:
  - find_client_by_email()
  - list_vehicles(client_id)
  - get_service_history(vehicle_id)
  - get_recommendations(vehicle_id, mileage)
  - find_promotions(vehicle_id)
  - schedule_appointment(vehicle_id, preferred_date)
  ↓
Data Layer (CSV for MVP → HANA for prod)
```

**Key Implementation Details:**

1. **Session Management**: 
   - Store conversation history per session
   - Track identified client and selected vehicle
   - Implement 30-min timeout with Redis for distributed instances

2. **Tool Definitions**:
   ```python
   tools = [
       Tool(name="find_client", 
            func=find_client_by_email,
            description="Find customer by email, phone, VIN, etc."),
       Tool(name="get_service_history",
            func=get_service_history,
            description="Get last 3 service visits for vehicle"),
       # ... more tools
   ]
   ```

3. **Streaming Architecture**:
   - Each tool call gets streamed to UI as it executes
   - Users see "🔍 Looking up service history..." in real-time
   - Final response combines all results

4. **Error Handling**:
   - If client not found, agent asks for clarification
   - If multiple vehicles, agent presents options
   - Tool failures trigger fallback ("Let me connect you to an agent")

**Challenges & Solutions:**

| Challenge | Solution |
|-----------|----------|
| **Agent hallucinates non-existent tools** | Pre-flight validation: check tool exists before execution |
| **Tool execution takes >30s** | Implement timeout + graceful degradation |
| **Session data explodes with history** | Summarize conversation every N turns with LLM |
| **Rate limiting on LLM calls** | Queue-based approach + cost monitoring |
| **Agent gets stuck in loop** | Max iteration limit (e.g., 10 calls per turn) |

**Scaling Considerations:**

1. **Data Layer**: 
   - MVP: In-memory CSVs (acceptable for <10k customers)
   - Production: HANA with caching layer (Redis for hot data)

2. **Session Management**:
   - Single instance: In-memory dict
   - Multiple instances: Redis backend for state sharing

3. **Tool Performance**:
   - Parallelize independent tool calls (e.g., service history + promotions simultaneously)
   - Implement caching for customer lookups

4. **Cost Control**:
   - Monitor LLM calls per user
   - Implement circuit breaker if costs spike
   - Batch similar queries to LLM

**Real-World Complexity:**
"What if a customer asks 'Is my car covered by warranty?' and we don't have warranty data in-system? I'd:
1. Add a 'check_warranty_system' tool that calls external warranty API
2. Cache warranty data with TTL
3. Implement fallback: 'I don't have warranty details—let me connect you with a specialist'
4. Track these scenarios for future system improvements"

---

## Use Case 2: Anomaly Detection in Sales Orders

### Full Answer:

**Problem Statement:**
"Sales orders are getting through with unusual patterns—either fraudulent or data entry errors. We're losing money on unusual discounts, quantities, or customer combinations. We need to flag high-risk orders for review without creating too many false positives that frustrate your teams."

**My Proposed Solution:**
"I'd implement a machine learning pipeline with explainability built-in. Here's the approach:

1. **Feature Engineering**: Extract features like:
   - Customer history deviation (new customer? unusual for this region?)
   - Order size vs. historical average
   - Discount depth vs. margin
   - Product mix (do these products sell together?)
   - Timestamp patterns (order at 2 AM?)

2. **Model**: Isolation Forest for anomaly detection (good for this because):
   - No labeled training data needed
   - Fast training and prediction
   - Works well with mixed feature types

3. **Explainability**: 
   - Use SHAP for feature importance
   - LLM generates business-friendly explanation
   - Example: 'This order is unusual because: (1) Customer bought 10x normal quantity [SHAP: 0.4 importance], (2) 60% discount [SHAP: 0.3], (3) New product category for this customer [SHAP: 0.2]'

4. **Dashboard**: 
   - Calendar view showing anomaly trends
   - Detailed order analysis page
   - Fine-tuning interface for contamination rate
   - Export for compliance/audit"

**Architecture:**
```
Sales Order Data
  ↓
Feature Engineering Pipeline
  ↓
Isolation Forest Model
  ↓
SHAP Explainability + LLM Explanations
  ↓
Dashboard + Fine-tuning UI
  ↓
Human Review + Feedback Loop
```

**Key Implementation Details:**

1. **ML Pipeline**:
   ```python
   from sklearn.ensemble import IsolationForest
   
   model = IsolationForest(contamination=0.05)  # Expect 5% anomalies
   predictions = model.predict(features)  # -1 = anomaly, 1 = normal
   scores = model.score_samples(features)
   ```

2. **Explainability Stack**:
   ```python
   import shap
   explainer = shap.TreeExplainer(model)
   shap_values = explainer.shap_values(features)
   
   # Get top 3 factors + generate LLM explanation
   top_factors = get_top_shap_values(shap_values[i], k=3)
   explanation = llm.explain_anomaly(order, top_factors)
   # Output: "Unusual due to: 10x quantity, high discount, new customer"
   ```

3. **Fine-tuning Interface**:
   - Slider for contamination rate (0-20%)
   - Feature selection checkboxes
   - Real-time model update + performance metrics

4. **Feedback Loop**:
   - Analyst marks order as "confirmed anomaly" or "false positive"
   - Feed back into retraining
   - Monthly model performance review

**Challenges & Solutions:**

| Challenge | Solution |
|-----------|----------|
| **False positive rate too high** | Implement confidence scoring + human review queue |
| **Model degrades on new products** | Implement drift detection + triggered retraining |
| **Feature engineering is manual** | Use automated feature selection + SHAP importance |
| **SHAP computation is slow** | Use SHAP approximations or sample-based explanation |
| **Explaining why something is NOT anomalous** | Train classifier on normal orders + show proximity to boundary |

**Scaling Considerations:**

1. **Training Data**:
   - Batch retraining weekly with accumulated data
   - Sliding window (e.g., last 12 months)
   - Stratified by customer segment

2. **Prediction Latency**:
   - Isolation Forest prediction is O(n*log(n)) trees = fast
   - Run predictions in background batch job
   - Cache results for real-time lookup

3. **Feature Store**:
   - Implement feature computation pipeline
   - Cache historical aggregations (customer avg order size, etc.)
   - Update features daily

4. **Model Versioning**:
   - Version each model with timestamp + performance metrics
   - Rollback capability if new version performs poorly
   - A/B test new model on subset of orders

**Real-World Complexity:**
"What if stakeholders disagree on what's 'anomalous'? Different regions have different norms.
- Implement regional models
- Allow custom rules per segment
- Track model performance by segment
- Quarterly calibration meetings with domain experts"

---

## Use Case 3: Customer Credit Check

### Full Answer:

**Problem Statement:**
"Credit evaluation is complex and manual. We receive KYC documents, CSF forms, payment history, vendor comments, and legal investigations. We need to:
- Extract data from all these documents consistently
- Validate consistency across documents (address matches? legal name consistent?)
- Apply credit policy rules (CAL scoring, payment behavior analysis)
- Make approval/denial recommendations
- Generate audit trails for compliance"

**My Proposed Solution:**
"I'd build a multi-stage pipeline:

**Stage 1: Document Extraction**
- Use SAP Document AI for structured forms (KYC, CSF)
- Use LLM vision for semi-structured documents (vendor comments)
- Output: Standardized JSON with extracted fields + confidence scores

**Stage 2: Validation**
- Cross-document checks: RFC numbers match? Addresses consistent?
- Implement validation scoring (0-100%)
- Flag mismatches for manual review

**Stage 3: Credit Policy Engine**
- Structured rule engine with if-then-else logic
- Inputs: CAL score, payment history, risk factors
- Outputs: Recommendation (approve/deny), approval limit, required documentation

**Stage 4: Reporting**
- AI-generated credit report with reasoning
- Visualization of all checks and scores
- Export for decision-maker review

Frontend: Streamlit for workflow clarity"

**Architecture:**
```
User Uploads Documents (KYC, CSF, etc.)
  ↓
Document AI Extraction (SAP Document AI for forms)
  ↓
LLM Extraction (for unstructured docs)
  ↓
Validation Layer (Cross-document consistency)
  ↓
Credit Policy Engine (Rule-based decisions)
  ↓
Scoring & Risk Analysis (Payment behavior, CAL)
  ↓
Report Generation (AI explanations)
  ↓
UI Dashboard (Streamlit workflow)
```

**Key Implementation Details:**

1. **Document Processing**:
   ```python
   # SAP Document AI for structured extraction
   extraction_result = document_ai.extract(
       document=kyc_pdf,
       doc_type="KYC"
   )
   # Output: {
   #   "legal_name": "John Doe",
   #   "address": "123 Main St",
   #   "confidence": 0.95
   # }
   ```

2. **Validation Engine**:
   ```python
   def validate_consistency(extractions):
       checks = []
       if kyc["legal_name"] != csf["company_name"]:
           checks.append({
               "check": "legal_name_match",
               "status": "FAILED",
               "kyc_value": kyc["legal_name"],
               "csf_value": csf["company_name"]
           })
       return checks
   ```

3. **Credit Policy Rules**:
   ```python
   if cal_score >= 80:
       approval = "AUTO_APPROVE"
       limit = "UNLIMITED"
   elif cal_score >= 60 and payment_score >= 75:
       approval = "APPROVED_WITH_CONDITIONS"
       limit = 50000  # EUR
   elif director_approval_available:
       approval = "ESCALATE_TO_DIRECTOR"
   else:
       approval = "DENY"
   ```

4. **Scoring Layers**:
   - **CAL (Credit Assessment Level)**: Based on revenue, industry, age
   - **C3M (3-month performance)**: Recent payment behavior
   - **Risk Score**: Composite of all factors
   - **Approval Recommendation**: Based on policy rules

**Challenges & Solutions:**

| Challenge | Solution |
|-----------|----------|
| **Document AI extraction fails** | Fallback to manual data entry + implement OCR preprocessing |
| **Ambiguous validation failures** | Implement confidence-based handling—low confidence → manual review |
| **Stakeholders disagree on policy** | Version control for policies + A/B test new rules on historical data |
| **Multi-currency complexity** | Store approval limits in base currency or per-currency |
| **Director override tracking** | Log all overrides with reasoning for future model calibration |

**Scaling Considerations:**

1. **Batch Processing**:
   - Async job queue for document extraction
   - SAP Event Mesh for orchestration
   - Track job progress + notify users

2. **Document Processing**:
   - Parallelize extraction (KYC, CSF, legal docs simultaneously)
   - Cache extraction results (same document PDF might be re-processed)

3. **Policy Management**:
   - Git-based policy definitions (YAML or JSON)
   - Version tracking + audit trails
   - Dry-run capability before deployment

4. **Data Storage**:
   - Store raw extractions (JSON)
   - Store validation results + scores
   - Permanent audit trail of all decisions

**Real-World Complexity:**
"What if a customer is classified as high-risk but you later discover the risk was a false positive?
- Implement appeal process with human review
- Track performance metrics (approval rate by country, false positive rate)
- Quarterly calibration with compliance + credit teams
- Build feedback loop: Actual payment behavior vs. predicted risk"

---

## Use Case 4: Diagram-to-BPMN Converter

### Full Answer:

**Problem Statement:**
"Business analysts draw process diagrams on whiteboards or Visio, but converting them to standardized BPMN 2.0 XML is manual and error-prone. We need to:
- Allow users to upload diagram images
- Use AI to understand the diagram structure and flow
- Generate valid BPMN 2.0 XML
- Export to Signavio/SAP Build Process Automation
- Handle complex diagrams with multiple swimlanes"

**My Proposed Solution:**
"I'd use a vision-to-XML approach:

1. **Image Analysis**: Upload diagram → base64 encode → send to vision LLM
2. **LLM Analysis**: Claude/GPT-4 analyzes image and extracts:
   - Activities/tasks
   - Decision points
   - Start/end events
   - Flow connections
   - Swimlanes (if present)

3. **BPMN Generation**: LLM generates BPMN 2.0 XML with:
   - Validated syntax (via schema)
   - Consistent IDs and references
   - Proper geometry for visualization

4. **Quality Assurance**:
   - XSD validation to ensure valid BPMN
   - Visual preview for user confirmation
   - Fallback: Show extracted structure for user to correct

Frontend: UI5 Web Components with drag-drop upload"

**Architecture:**
```
User Uploads Diagram Image (PNG, SVG, WEBP)
  ↓
Base64 Encoding + SAP GenAI Hub
  ↓
Vision LLM (Claude/GPT-4/Gemini)
  ↓
LLM Extracts:
  - Activities
  - Decision points
  - Flows
  - Gateways
  ↓
BPMN XML Generation (with LLM)
  ↓
XSD Validation
  ↓
Visual Preview + Download
```

**Key Implementation Details:**

1. **Prompt Engineering**:
   ```
   System Prompt:
   "You are a BPMN expert. Analyze business process diagrams and extract:
   1. All activities/tasks (name + type)
   2. Decision points and conditions
   3. Start and end events
   4. Connections between elements
   5. Swimlanes if present
   
   Format output as JSON:
   {
     'activities': [{'id': 'task1', 'name': 'Review Order', 'type': 'userTask'}],
     'flows': [{'from': 'task1', 'to': 'gate1', 'label': ''}],
     'gateways': [{'id': 'gate1', 'type': 'exclusiveGateway'}]
   }"
   ```

2. **BPMN Generation**:
   ```python
   # Template-based BPMN generation
   bpmn_xml = generate_bpmn_xml(
       activities=extracted['activities'],
       flows=extracted['flows'],
       gateways=extracted['gateways']
   )
   
   # Validate against BPMN XSD
   if validate_bpmn_schema(bpmn_xml):
       return bpmn_xml
   else:
       raise BPMNValidationError()
   ```

3. **Multi-Model Fallback**:
   ```python
   models = [
       ("claude-3.5-sonnet", SAP_GENAI_HUB),
       ("gpt-4o", SAP_GENAI_HUB),
       ("gemini-2.5-pro", SAP_GENAI_HUB)
   ]
   
   for model, provider in models:
       try:
           result = llm.analyze_diagram(image, model=model)
           return result
       except Exception as e:
           logger.warning(f"{model} failed: {e}, trying next...")
   ```

4. **User Correction Workflow**:
   - Show extracted structure as JSON
   - User can manually adjust (rename activities, add/remove flows)
   - Regenerate BPMN XML from corrected JSON

**Challenges & Solutions:**

| Challenge | Solution |
|-----------|----------|
| **Complex diagrams with 50+ elements** | Implement chunking: split diagram into regions, analyze each, stitch together |
| **LLM generates invalid BPMN XML** | Use structured output format + XML validator + fallback to template |
| **Vision model struggles with low-quality scans** | Implement OCR preprocessing + image enhancement |
| **Swimlanes get lost in translation** | Explicitly ask LLM about lanes in system prompt |
| **User disagrees with extracted structure** | Provide JSON editor interface + regenerate from corrected JSON |

**Scaling Considerations:**

1. **Image Processing**:
   - Resize large images before sending to LLM (reduce tokens)
   - Cache diagram analysis results
   - Batch processing for bulk diagram uploads

2. **LLM Calls**:
   - SAP GenAI Hub provides multi-provider support
   - Implement cost tracking (Claude is expensive)
   - Retry logic with backoff for rate limits

3. **Storage**:
   - Store original image + extracted JSON + generated BPMN
   - Version history for diagrams
   - Audit trail of all conversions

**Real-World Complexity:**
"What if the diagram has hand-drawn annotations or external process references?
- Implement image preprocessing (contrast enhancement, deskewing)
- For external references, ask user to specify (dropdown of standard processes)
- Store process templates in system for reference
- Implement reference linking in BPMN output"

---

## Use Case 5: AI Log Analyzer

### Full Answer:

**Problem Statement:**
"We're drowning in error logs. Thousands of logs per day, but most are noise or repeats. Operators spend hours finding the critical errors, and understanding what to do is hard. We need:
- Intelligent filtering and prioritization
- SAP context-aware remediation steps
- Correlation of related errors
- Integration with OSS notes and documentation"

**My Proposed Solution:**
"I'd use SAP CAP (Cloud Application Programming) for this because:
- Deep HANA integration (logs can be massive—100GB+)
- Type safety + OData first-class support
- XSUAA integration for enterprise auth
- Destinations for calling SAP systems

Architecture:
1. **Ingestion**: Collect logs from various sources (application servers, databases)
2. **Parsing**: Normalize logs into structured format
3. **Indexing**: HANA full-text search for quick lookup
4. **LLM Analysis**: Prioritize + generate SAP-aware remediation
5. **Knowledge Grounding**: Cross-reference OSS notes, documentation
6. **UI**: SAP UI5 dashboard with drill-down capability"

**Architecture:**
```
Log Sources (App servers, DB, Systems)
  ↓
Log Collection Service (Syslog, File Watch)
  ↓
CAP Service Layer (TypeScript)
  ↓
HANA Database (Full-text index)
  ↓
LLM Analysis (SAP GenAI Hub)
  ↓
Knowledge Grounding (OSS notes, SAP Docs)
  ↓
SAP UI5 Dashboard
```

**Key Implementation Details:**

1. **Log Ingestion**:
   ```typescript
   // CAP service for log collection
   async function ingestLog(logEntry: LogEntry) {
       const parsed = parseLog(logEntry);
       const normalized = normalizeFields(parsed);
       
       // Insert into HANA
       await INSERT.into(Logs).entries(normalized);
       
       // Trigger analysis if critical
       if (normalized.severity >= 'ERROR') {
           await analyzeLog(normalized);
       }
   }
   ```

2. **Log Prioritization**:
   ```typescript
   async function prioritizeLog(log: LogEntry) {
       const analysis = await genai.analyze(`
           Log: ${log.message}
           Context: ${log.context}
           
           Provide:
           1. Severity (CRITICAL, HIGH, MEDIUM, LOW)
           2. Impact (what's affected?)
           3. Root cause (likely causes)
           4. Next steps (how to fix?)
           5. SAP OSS notes (if known)
       `);
       
       return analysis;
   }
   ```

3. **Knowledge Grounding**:
   ```typescript
   async function findOSSNotes(errorCode: string) {
       const ossNotes = await grounder.search(
           `${errorCode} fix solution`
       );
       return ossNotes;  // Top 3 relevant OSS notes
   }
   ```

4. **HANA Full-Text Search**:
   ```sql
   CREATE FULLTEXT INDEX LogIndex ON LOGS(MESSAGE);
   
   -- Fast lookup for related logs
   SELECT * FROM LOGS 
   WHERE CONTAINS(MESSAGE, 'timeout', LANGUAGE 'EN')
   ORDER BY TIMESTAMP DESC
   LIMIT 10;
   ```

**Challenges & Solutions:**

| Challenge | Solution |
|-----------|----------|
| **Log volume overwhelming** | Implement sampling + hash-based deduplication |
| **LLM calls expensive at scale** | Batch process + implement cost throttling |
| **Logs arrive faster than LLM analysis** | Async background job + queue (SAP Event Mesh) |
| **OSS notes integration is manual** | Implement SAP API calls for automatic note retrieval |
| **False positive correlations** | Use statistical correlation + human feedback loop |

**Scaling Considerations:**

1. **HANA Partitioning**:
   - Partition logs by date (daily/weekly partitions)
   - Archive old logs to cold storage
   - Implement retention policy

2. **Log Processing**:
   - Async job queue for LLM analysis
   - Batch correlations (hourly) instead of real-time
   - Implement backpressure handling

3. **HANA Optimization**:
   - Create indexes on severity, timestamp, error_code
   - Implement columnar compression for large datasets
   - Regular maintenance tasks (optimize, analyze)

4. **Monitoring**:
   - Track analysis queue depth
   - Monitor LLM API response times
   - Alert on anomalies (sudden spike in ERRORs)

**Real-World Complexity:**
"What if a critical error occurs but the LLM analysis is pending?
- Implement priority queue: CRITICAL logs analyzed immediately
- Show raw error with confidence while analysis is in progress
- Implement human escalation: Unanalyzed critical errors → page on-call"

---

## Use Case 6: Video Incident & Safety Monitoring

### Full Answer:

**Problem Statement:**
"Workplace safety requires monitoring video feeds for incidents—hard hats not worn, unsafe equipment operation, restricted area breaches. Manual monitoring is expensive and error-prone. We need:
- Automated video analysis
- Real-time incident detection
- Confidence scoring (avoid false alarms)
- Audit trail for compliance
- Integration with safety management systems"

**My Proposed Solution:**
"I'd use Google Gemini 2.5 Pro via SAP AI Core because:
- Advanced vision capabilities for complex scenes
- Enterprise-grade security via SAP AI Core wrapper
- OAuth integration for service-to-service auth
- Cost-effective for batch analysis

Architecture:
1. **Media Upload**: Video files (MP4, MOV) or stream links
2. **Preprocessing**: Frame extraction if needed, file validation
3. **Async Analysis**: Queue-based processing via SAP Event Mesh
4. **AI Analysis**: Gemini 2.5 Pro via SAP AI Core
5. **Incident Detection**: Parse LLM output, generate alerts
6. **Dashboard**: SAP Fiori for incident review + export
7. **Integration**: Send incidents to safety management systems"

**Architecture:**
```
User Uploads Video / Provides Stream Link
  ↓
Media Validation + Storage (Temp)
  ↓
Async Job Queue (SAP Event Mesh)
  ↓
Media Processing (Extract key frames if needed)
  ↓
SAP AI Core OAuth Token Management
  ↓
Gemini 2.5 Pro API Call (Vision Analysis)
  ↓
Incident Detection + Confidence Scoring
  ↓
PDF Report Generation
  ↓
SAP Fiori Dashboard + Alerts
```

**Key Implementation Details:**

1. **Media Upload Handling**:
   ```python
   from fastapi import UploadFile, File
   
   @app.post("/api/upload-video")
   async def upload_video(file: UploadFile = File(...)):
       # Validate file type + size
       if file.size > 5_000_000_000:  # 5GB limit
           raise ValueError("File too large")
       
       # Store temporarily
       temp_path = f"/tmp/{file.filename}"
       with open(temp_path, "wb") as f:
           f.write(await file.read())
       
       # Queue for analysis
       job_id = await queue_analysis_job(temp_path)
       return {"job_id": job_id, "status": "processing"}
   ```

2. **SAP AI Core OAuth**:
   ```python
   async def get_ai_core_token():
       token_response = await http_client.post(
           url=f"{AI_CORE_AUTH_ENDPOINT}/oauth/token",
           data={
               "grant_type": "client_credentials",
               "client_id": AI_CORE_CLIENT_ID,
               "client_secret": AI_CORE_CLIENT_SECRET
           }
       )
       return token_response["access_token"]
   ```

3. **Gemini Vision Analysis**:
   ```python
   async def analyze_video_for_incidents(video_path: str):
       token = await get_ai_core_token()
       
       # Convert video to base64
       with open(video_path, "rb") as f:
           video_base64 = base64.b64encode(f.read()).decode()
       
       response = await http_client.post(
           url=f"{AI_CORE_ENDPOINT}/deployments/{DEPLOYMENT_ID}/infer",
           headers={"Authorization": f"Bearer {token}"},
           json={
               "instances": [{
                   "prompt": """Analyze this video for workplace safety incidents:
                       - Hard hat violations
                       - Equipment misuse
                       - Restricted area breaches
                       - Emergency situations
                       
                       Return JSON:
                       {
                           "incidents": [
                               {
                                   "type": "hard_hat_violation",
                                   "timestamp": "00:15:30",
                                   "confidence": 0.92,
                                   "description": "Worker near heavy equipment without hard hat"
                               }
                           ],
                           "overall_risk": "HIGH"
                       }""",
                   "video": video_base64
               }]
           }
       )
       
       return response["predictions"][0]
   ```

4. **Incident Processing**:
   ```python
   async def process_incidents(analysis_result):
       incidents = analysis_result["incidents"]
       
       for incident in incidents:
           if incident["confidence"] >= 0.85:  # High confidence
               # Create alert
               alert = Alert(
                   incident_type=incident["type"],
                   confidence=incident["confidence"],
                   timestamp=incident["timestamp"],
                   description=incident["description"],
                   status="PENDING_REVIEW"
               )
               
               # If CRITICAL, send immediate notification
               if incident_type in ["FIRE", "SEVERE_INJURY"]:
                   await send_critical_alert(alert)
               
               await db.insert(alert)
   ```

**Challenges & Solutions:**

| Challenge | Solution |
|-----------|----------|
| **Video analysis takes 5+ min for 1-hour video** | Extract key frames (1 per second) + analyze separately |
| **False positives (shadows, reflections)** | Implement confidence threshold (85%+) + human review for 50-85% |
| **Privacy concerns (recording workers)** | Implement policy: Only analyze designated hazard areas, blur faces |
| **Cost: Gemini charges per video** | Batch videos for off-peak analysis, implement cost budgets |
| **Network timeouts on large files** | Use resumable uploads + chunked processing |

**Scaling Considerations:**

1. **Async Processing**:
   - Queue framework: SAP Event Mesh or RabbitMQ
   - Worker pool: Multiple FastAPI workers
   - Job monitoring: Dashboard showing queue depth, processing rates

2. **Storage**:
   - Temporary storage: Object store (SAP BTP Cloud Storage)
   - Results: HANA database
   - Archives: Long-term storage (cheaper tier)

3. **Cost Optimization**:
   - Batch videos (combine 10 videos, analyze once)
   - Schedule analysis off-peak
   - Implement quota per facility/shift

4. **Availability**:
   - Multi-region deployment
   - Failover to alternative LLM if Gemini is unavailable
   - Local fallback rules for critical scenarios

**Real-World Complexity:**
"What if a video contains multiple incidents at different severities?
- Segment video into incidents (timestamp ranges)
- Generate separate alerts per incident
- Implement escalation: 3+ incidents in 30 min → critical alert
- Track incident patterns (same worker multiple violations → retraining needed)"

---

## Use Case 7: Intelligent Procurement Assistant

### Full Answer:

**Problem Statement:**
"Procurement teams spend hours extracting contract data—commodity codes, vendor terms, pricing, payment terms. Manual extraction is error-prone and slow. We need:
- Automated extraction of structured data
- Validation against commodity code catalogs
- Audit trail of all extractions
- Export-ready format for downstream systems"

**My Proposed Solution:**
"I'd use a hybrid approach: Pattern matching first, LLM for enrichment.

Why? Because:
- Patterns are fast, deterministic, cost-effective
- LLM provides context when patterns can't find answers
- User can review/correct extracted data
- Streamlit UI allows quick iteration

Architecture:
1. **Document Parsing**: Extract text (PDF, DOCX, Excel)
2. **Pattern Matching**: Find commodity codes using regex + known patterns
3. **LLM Enrichment**: For ambiguous cases, use LLM
4. **Validation**: Cross-check against known commodity catalogs
5. **UI Review**: Streamlit interface for human validation
6. **Export**: CSV/JSON output + system integration"

**Architecture:**
```
Document Upload (PDF, DOCX, Excel)
  ↓
Text Extraction (PyMuPDF, python-docx, openpyxl)
  ↓
Pattern Matching (Regex + Dictionaries)
  ↓
LLM Enrichment (For ambiguous cases)
  ↓
Validation (Cross-catalog checks)
  ↓
Streamlit UI (User review + correction)
  ↓
Change Tracking (Audit trail)
  ↓
Export (CSV/JSON)
```

**Key Implementation Details:**

1. **Text Extraction**:
   ```python
   import PyPDF2
   from docx import Document
   
   def extract_text(file_path):
       if file_path.endswith('.pdf'):
           with open(file_path, 'rb') as f:
               reader = PyPDF2.PdfReader(f)
               text = ''.join([page.extract_text() for page in reader.pages])
       elif file_path.endswith('.docx'):
           doc = Document(file_path)
           text = '\n'.join([para.text for para in doc.paragraphs])
       else:
           raise ValueError("Unsupported format")
       
       return text
   ```

2. **Commodity Code Pattern Matching**:
   ```python
   UNSPSC_PATTERN = r'\b([0-9]{8})\b'  # UNSPSC format: 12345678
   CPV_PATTERN = r'\b(CPV-?[0-9]{8})\b'
   
   def extract_commodity_codes(text):
       codes = []
       
       # UNSPSC
       for match in re.finditer(UNSPSC_PATTERN, text):
           code = match.group(1)
           if code in KNOWN_UNSPSC_CODES:
               codes.append({
                   'code': code,
                   'type': 'UNSPSC',
                   'status': 'VALIDATED',
                   'confidence': 0.95
               })
       
       # CPV
       for match in re.finditer(CPV_PATTERN, text):
           code = match.group(1)
           if code in KNOWN_CPV_CODES:
               codes.append({
                   'code': code,
                   'type': 'CPV',
                   'status': 'VALIDATED',
                   'confidence': 0.95
               })
       
       return codes
   ```

3. **LLM Enrichment**:
   ```python
   async def llm_extract_commodities(text: str):
       response = await llm.generate(
           prompt=f"""
           Extract commodity codes and service descriptions from this contract:
           
           CONTRACT TEXT:
           {text[:2000]}  # First 2000 chars to limit tokens
           
           Return JSON:
           {{
               "commodities": [
                   {{
                       "code": "72000000",
                       "description": "IT Services",
                       "quantity": "100 hours",
                       "unit_price": "150 EUR",
                       "confidence": 0.8
                   }}
               ],
               "reasoning": "Found service description matching commodity X"
           }}
           """,
           temperature=0.3  # Lower temp for factual extraction
       )
       
       return response
   ```

4. **Streamlit UI**:
   ```python
   import streamlit as st
   
   st.title("Intelligent Procurement Assistant")
   
   uploaded_file = st.file_uploader("Upload Contract", type=['pdf', 'docx', 'xlsx'])
   
   if uploaded_file:
       text = extract_text(uploaded_file)
       initial_extraction = extract_commodity_codes(text)
       
       st.write("### Extracted Commodity Codes")
       
       for i, code in enumerate(initial_extraction):
           col1, col2 = st.columns([0.8, 0.2])
           
           with col1:
               edited_code = st.text_input(
                   f"Code {i+1}", 
                   value=code['code'],
                   key=f"code_{i}"
               )
           
           with col2:
               st.write(f"Conf: {code['confidence']:.0%}")
       
       if st.button("Export"):
           export_to_csv(updated_extraction)
           st.success("Exported to CSV!")
   ```

**Challenges & Solutions:**

| Challenge | Solution |
|-----------|----------|
| **Contract documents use different commodity taxonomies** | Support multiple standards (UNSPSC, CPV, company-specific) |
| **Commodity codes scattered throughout document** | Implement context analysis—extract surrounding text for validation |
| **User edits but forgets to save** | Use Streamlit session state to auto-save on each edit |
| **Audit trail of all changes** | Log user ID, timestamp, before/after values |
| **Integration with downstream systems** | API endpoint that returns standardized JSON output |

**Scaling Considerations:**

1. **Document Processing**:
   - Batch mode: Process 100s of documents
   - Async job queue for large batches
   - Progress tracking UI

2. **Pattern Library**:
   - Maintain regex patterns + commodity mappings
   - Version control for audit
   - Regular updates as new codes appear

3. **LLM Cost Control**:
   - Use patterns first (free)
   - LLM only for unmatched items
   - Batch LLM calls to reduce API overhead

**Real-World Complexity**:
"What if a contract has 20 different commodities? The user spends 30 minutes reviewing.
- Implement confidence-based filtering: Show only <70% confidence for review
- Auto-accept high-confidence matches
- Provide keyboard shortcuts for bulk operations
- Show recommended commodity codes based on context"

---

## Use Case 8: Purchase Order Extractor (CAP + Document AI)

### Full Answer:

**Problem Statement:**
"We receive hundreds of POs daily as PDF files. We need:
- Extract header data (vendor, dates, amounts)
- Extract line items (part numbers, quantities, prices)
- Match customer part numbers to supplier part numbers
- Integrate with sales order system
- Maintain audit trail for compliance"

**My Proposed Solution:**
"I'd use SAP CAP with TypeScript for several reasons:
- Deep HANA integration (PO data is structured, benefits from SQL)
- Type safety (reduces bugs in financial data)
- OData first-class support (easy integration with SAP UI5 frontend)
- XSUAA built-in (enterprise auth)
- Fiori Elements for rapid UI development

Architecture:
1. **Document AI**: SAP Document AI Premium for PO extraction
2. **Data Modeling**: CAP service layer with HANA persistence
3. **Material Mapping**: LLM-driven matching of customer↔supplier parts
4. **Sales Order Integration**: Match PO lines to SO lines
5. **Fiori UI**: Two apps—PO extraction and material mapping
6. **MTA Deployment**: Single deployment package"

**Architecture:**
```
PDF Upload
  ↓
SAP Document AI (Extract header + line items)
  ↓
CAP Service (TypeScript)
  ↓
Extraction Validation
  ↓
HANA Storage
  ↓
Material Mapping (LLM-driven)
  ↓
Sales Order Matching
  ↓
Fiori UI Applications
  ↓
Approval Workflow
```

**Key Implementation Details:**

1. **Document AI Extraction**:
   ```typescript
   // CAP service for PO extraction
   async function extractPO(pdfFile: Buffer) {
       const formData = new FormData();
       formData.append('file', new Blob([pdfFile]), 'po.pdf');
       
       const response = await fetch(
           `${DOX_ENDPOINT}/document-processing/v1/jobs`,
           {
               method: 'POST',
               headers: {
                   'Authorization': `Bearer ${await getDestinationToken('DOX-PREMIUM')}`
               },
               body: formData
           }
       );
       
       const jobResult = await response.json();
       
       // Poll for extraction completion
       const extraction = await pollExtractionResult(jobResult.jobId);
       
       return {
           header: extraction.header,
           lineItems: extraction.lineItems,
           confidence: extraction.confidence
       };
   }
   ```

2. **CAP Data Model**:
   ```typescript
   // db/schema.cds
   namespace po_extractor;
   
   entity PurchaseOrders {
       key ID: UUID;
       vendorName: String;
       vendorNumber: String;
       orderDate: Date;
       deliveryDate: Date;
       totalAmount: Decimal;
       currency: String;
       extractionConfidence: Decimal;
       
       lineItems: Composition of many POLineItems on lineItems.po = $self;
       materialMappings: Composition of many MaterialMappings on materialMappings.po = $self;
   }
   
   entity POLineItems {
       key ID: UUID;
       po: Association to PurchaseOrders;
       lineNumber: Integer;
       customerPartNumber: String;
       description: String;
       quantity: Decimal;
       unitPrice: Decimal;
       amount: Decimal;
       
       mappings: Composition of many MaterialMappings on mappings.lineItem = $self;
   }
   
   entity MaterialMappings {
       key ID: UUID;
       lineItem: Association to POLineItems;
       po: Association to PurchaseOrders;
       customerPartNumber: String;
       supplierPartNumber: String;
       confidence: Decimal;
       matchedSOItem: String;  // Link to sales order
       mappingStatus: String;  // MANUAL, AUTOMATIC, PENDING_REVIEW
   }
   ```

3. **Material Mapping (LLM)**:
   ```typescript
   async function mapMaterials(lineItem: POLineItem) {
       const candidates = await db
           .run(SELECT.from('InternalMaterials')
               .where({customerPartNumber: lineItem.customerPartNumber}));
       
       if (candidates.length === 1) {
           return {
               supplierPartNumber: candidates[0].supplierPartNumber,
               confidence: 0.95,
               method: 'EXACT_MATCH'
           };
       }
       
       // Use LLM for fuzzy matching
       const response = await genAI.analyze(`
           Match customer part to supplier part:
           Customer Part: ${lineItem.customerPartNumber}
           Description: ${lineItem.description}
           
           Known supplier parts:
           ${candidates.map(c => `${c.supplierPartNumber}: ${c.description}`).join('\n')}
           
           Return JSON: {"supplierPart": "...", "confidence": 0.8, "reasoning": "..."}
       `);
       
       return response;
   }
   ```

4. **Fiori Elements UI** (Automatic via CAP):
   ```typescript
   // srv/service.cds - OData automatically creates RESTful endpoints
   service PurchaseOrderService {
       entity PurchaseOrders as projection on po_extractor.PurchaseOrders;
       entity POLineItems as projection on po_extractor.POLineItems;
       
       action extractPO(file: LargeBinary) returns {
           success: Boolean;
           message: String;
       };
       
       action mapMaterials(poId: UUID) returns {
           mappedCount: Integer;
           unmappedCount: Integer;
       };
   }
   ```

**Challenges & Solutions:**

| Challenge | Solution |
|-----------|----------|
| **Document AI extraction fails on poor-quality scans** | Implement OCR preprocessing + manual fallback |
| **Material mapping ambiguous** | Show LLM confidence score + human review UI |
| **Performance: Large number of POs** | Implement async batch processing + progress tracking |
| **Data consistency across systems** | Implement idempotency keys + transaction handling |

**Scaling Considerations**:

1. **Batch Processing**:
   - Queue-based approach (SAP Event Mesh)
   - Worker processes N POs in parallel
   - Results stored incrementally

2. **HANA Optimization**:
   - Indexes on vendor, date, status
   - Partition POs by date (monthly)
   - Archive processed POs

3. **Performance**:
   - Cache material mappings
   - Parallelize extraction + mapping
   - Async LLM calls

**Real-World Complexity**:
"What if a vendor uses non-standard PO format?
- Implement vendor-specific extraction profiles
- Allow users to define custom field locations
- Provide template builder UI for recurring vendors"

---

## Use Case 9: AI Capability Matcher (Vector Search)

### Full Answer:

**Problem Statement:**
"We have 1000s of AI services in our catalog and 100s of customer products. Matching them manually is impossible. We need:
- Semantic similarity matching (not just keyword)
- Ranking by relevance
- Explainability (why is this match good?)
- Batch processing for large catalogs"

**My Proposed Solution:**
"I'd use vector embeddings + SAP HANA vector search because:
- Embeddings capture semantic meaning (not just keywords)
- HANA vector search is fast and scalable
- Optional LLM ranking adds business context
- Streamlit UI tracks progress and allows customization

Architecture:
1. **Upload CSVs**: AI services and customer products
2. **Embedding Generation**: Use SAP Gen AI Hub to generate embeddings
3. **Vector Storage**: Store embeddings in HANA vector tables
4. **Similarity Search**: Find nearest neighbors for each product
5. **LLM Ranking**: Optional—re-rank with business context
6. **Export Results**: CSV with match confidence"

**Architecture:**
```
Upload AI Catalog CSV + Client CSV
  ↓
Select columns for embedding text construction
  ↓
Batch Generate Embeddings (SAP Gen AI Hub)
  ↓
Create HANA Vector Tables
  ↓
Vector Similarity Search (k-NN)
  ↓
Optional: LLM Ranking (Add business context)
  ↓
Streamlit Progress Display
  ↓
Export CSV Results
```

**Key Implementation Details:**

1. **Embedding Generation**:
   ```python
   from genai_hub import EmbeddingClient
   
   async def generate_embeddings(texts: List[str]):
       embedding_client = EmbeddingClient()
       embeddings = []
       
       # Batch process (e.g., 100 texts per batch)
       batch_size = 100
       for i in range(0, len(texts), batch_size):
           batch = texts[i:i+batch_size]
           batch_embeddings = await embedding_client.embed(batch)
           embeddings.extend(batch_embeddings)
       
       return embeddings
   ```

2. **HANA Vector Storage**:
   ```sql
   -- Create vector table
   CREATE TABLE AI_SERVICES_EMBEDDINGS (
       SERVICE_ID NVARCHAR(50) PRIMARY KEY,
       SERVICE_NAME NVARCHAR(255),
       EMBEDDING_VECTOR REAL_VECTOR,
       METADATA NVARCHAR(5000)
   );
   
   -- Create vector index for fast search
   CREATE VECTOR INDEX AI_SERVICES_IDX 
   ON AI_SERVICES_EMBEDDINGS(EMBEDDING_VECTOR)
   USING HANA;
   
   -- k-NN search example
   SELECT SERVICE_ID, SERVICE_NAME, 
          COSINE_SIMILARITY(
              (SELECT EMBEDDING_VECTOR FROM AI_SERVICES_EMBEDDINGS 
               WHERE SERVICE_ID = 'client_product_1'),
              EMBEDDING_VECTOR
          ) AS SIMILARITY
   FROM AI_SERVICES_EMBEDDINGS
   ORDER BY SIMILARITY DESC
   LIMIT 5;
   ```

3. **Similarity Search**:
   ```python
   async def find_matches(client_product_text: str, k: int = 5):
       # Generate embedding for client product
       client_embedding = await embedding_client.embed([client_product_text])
       client_vec = client_embedding[0]
       
       # Search in HANA
       query = f"""
           SELECT SERVICE_ID, SERVICE_NAME, SIMILARITY FROM (
               SELECT TOP {k}
                   SERVICE_ID, SERVICE_NAME,
                   COSINE_SIMILARITY(
                       CAST('{client_vec}' AS REAL_VECTOR),
                       EMBEDDING_VECTOR
                   ) AS SIMILARITY
               FROM AI_SERVICES_EMBEDDINGS
               ORDER BY SIMILARITY DESC
           )
       """
       
       results = await db.run(query)
       return results
   ```

4. **Optional LLM Re-ranking**:
   ```python
   async def rank_with_llm(matches: List[Dict]):
       prompt = f"""
       Given this customer product and candidate AI services,
       rank them by business fit (1=best, 5=worst):
       
       Customer Product: {client_product}
       
       Candidates:
       1. {matches[0]['service_name']} - Vector score: {matches[0]['similarity']:.2f}
       2. {matches[1]['service_name']} - Vector score: {matches[1]['similarity']:.2f}
       ...
       
       Provide reasoning for top 3 matches.
       """
       
       ranking = await llm.analyze(prompt)
       return ranking
   ```

5. **Streamlit UI**:
   ```python
   import streamlit as st
   
   st.title("AI Capability Matcher")
   
   col1, col2 = st.columns(2)
   
   with col1:
       ai_catalog = st.file_uploader("Upload AI Services CSV")
       ai_columns = st.multiselect(
           "Select columns for matching",
           ["name", "description", "category"],
           default=["name", "description"]
       )
   
   with col2:
       client_catalog = st.file_uploader("Upload Client Products CSV")
       client_columns = st.multiselect(
           "Select columns for matching",
           ["name", "description", "use_case"],
           default=["name", "description"]
       )
   
   if st.button("Run Matching"):
       progress = st.progress(0)
       status = st.empty()
       
       for i, product in enumerate(client_products):
           status.write(f"Matching {i+1}/{len(client_products)}...")
           matches = await find_matches(product)
           results.append((product, matches))
           progress.progress((i+1) / len(client_products))
       
       st.success("Matching complete!")
       st.dataframe(results_df)
       st.download_button("Download CSV", results_csv)
   ```

**Challenges & Solutions:**

| Challenge | Solution |
|-----------|----------|
| **Embeddings capture irrelevant features** | Manually curate high-quality text descriptions + domain-specific prompt |
| **Large embedding dimension → slow search** | Use dimensionality reduction (PCA) or smaller embedding models |
| **LLM re-ranking adds latency** | Run ranking as async background job + return vector results immediately |
| **Embedding quality varies by model** | Test multiple embedding models (e.g., OpenAI, SentenceTransformers) |

**Scaling Considerations**:

1. **Batch Processing**:
   - Process 1000s of products with parallel workers
   - Partition embeddings across HANA nodes

2. **Embedding Updates**:
   - Refresh embeddings when catalogs change
   - Incremental updates for new products

3. **Cost Optimization**:
   - Cache embeddings (don't recompute for same text)
   - Batch embedding API calls

---

## Use Case 10: Email Agent

### Full Answer:

**Problem Statement:**
"Email workflows are manual and repetitive—forwards, categorization, action items. We need:
- Agents that read emails and understand intent
- Automated categorization and routing
- Action extraction (tasks, follow-ups)
- Integration with SAP systems"

**My Proposed Solution:**
"I'd use an agentic approach similar to Post-Sales Chatbot but for email:

Architecture:
1. **Email Ingestion**: Connect to email system (Exchange, Gmail via connectors)
2. **Agent Loop**: LLM reads email, decides action (forward, file, action, escalate)
3. **Tool Integration**: Email tools (move, forward, create task), SAP tools (create ticket, update record)
4. **Streaming UI**: Show agent decisions to user before executing
5. **Human Approval**: Option to review before sending emails"

**Architecture**:
```
Email Received (Exchange/Gmail)
  ↓
LLM Analysis (Intent, Category, Action)
  ↓
Agent Decides: Forward? Categorize? Create task?
  ↓
Tools Available:
  - Move email to folder
  - Forward to person/team
  - Create task/reminder
  - Update SAP ticket
  - Flag for follow-up
  ↓
Streaming UI (Show decisions)
  ↓
Human Approval (Optional)
  ↓
Execute Actions
```

---

## Use Case 11: Vendor Selection Optimization

### Full Answer:

**Problem Statement:**
"Procurement teams manually evaluate vendors based on cost, delivery time, on-time rate, and other factors. This is subjective and time-consuming. We need:
- Automated vendor scoring across dimensions
- Cost component breakdown (material, tariffs, logistics)
- Geographic analysis
- AI-powered recommendations
- What-if analysis (if we change supplier, what's the impact?)"

**My Proposed Solution:**
"I'd build a procurement analytics dashboard (Streamlit) with optimization engine:

Components:
1. **Data Ingestion**: Import vendor master, prices, delivery metrics
2. **Cost Modeling**: Calculate total cost of ownership (material + tariffs + holding + logistics)
3. **Vendor Scoring**: Multi-dimensional analysis (cost, lead time, OTIF)
4. **Optimization**: Recommend optimal vendor mix for each material
5. **AI Insights**: LLM generates procurement recommendations
6. **Dashboards**: Multiple visualization perspectives"

---

## Use Case 12: Touchless Transactions (GR & Invoice Bot)

### Full Answer:

**Problem Statement:**
"Invoice validation in SAP is manual. Teams compare invoice amounts to PO + goods receipt, classify mismatches, and take action. This is repetitive and error-prone. We need:
- Automated PO↔invoice matching
- Classification of variance scenarios
- Teams Chat bot integration (Microsoft Teams)
- Approval workflows with Adaptive Cards"

**My Proposed Solution:**
"I'd use a Teams bot (Microsoft Bot Framework) because it meets users where they are (Teams).

Architecture:
1. **Bot receives message**: User uploads Excel with invoices
2. **Data Processing**: Parse invoice↔PO↔GR data
3. **Classification**: Tolerance-based classification (7 scenarios)
4. **Adaptive Cards**: Present interactive options to user
5. **Action Execution**: Mark as received, escalate, etc.

Scenarios:
- S1: Full receipt confirmation (items invoiced but not received)
- S2: Over-receipt with tolerance
- S3: Over-receipt exceeds tolerance
- S4: Partial receipt
- S5: Return received
- S6: Invoice no PO
- S7: Variance investigation needed"

---

## Additional Use Cases (Brief Summaries)

### Use Case: Diagram Outlier Detection
Similar to anomaly detection but for diagrams/images. Identify unusual design patterns or deviations from standards using vision models.

### Use Case: RFQx Doc Analysis Utilities
Automated RFQ (Request for Quotation) analysis. Extract terms, compare supplier responses, identify best value.

### Use Case: Product Catalog Search
Semantic search across product catalog using embeddings. Similar to AI Capability Matcher but for e-commerce.

### Use Case: Utilities Rate Compare and Export
Utility tariff analysis and comparison. Optimize based on usage patterns and contract terms.

### Use Case: Utilities Tariff Mapping Cockpit
React + Node.js stack for tariff mapping UI. Full-stack modern approach (different from Python stacks we've seen).

---

## How to Practice These Answers

### Format 1: 2-Minute Elevator Pitch
Focus on:
1. Problem in 1 sentence
2. Solution approach (architecture)
3. Why this tech stack?
4. One key implementation detail
5. One scalability challenge

### Format 2: Deep Dive (5-7 minutes)
If they ask follow-up questions:
1. Explain each component in detail
2. Show code/pseudocode if relevant
3. Discuss trade-offs
4. Address specific challenges
5. Explain how you'd measure success

### Format 3: Design Challenge
"You have 1 week to build this. What do you start with?"
- Start with data model
- Then API layer
- Then UI
- Then optimization

### Format 4: Production-Ready Thinking
"This works in a POC. How do you move to production?"
- Security, scaling, monitoring, cost

---

## Quick Reference: Tech Stack Patterns

| Pattern | Stack | When to Use |
|---------|-------|------------|
| **Rapid Prototyping** | FastAPI + Streamlit + CSV | MVP, internal tools, low volume |
| **Enterprise UI** | FastAPI + UI5 Web Components (Vite) | Customer-facing, brand consistency |
| **SAP-Native** | CAP + TypeScript + HANA + Fiori | Deep integration, structured data |
| **Agentic AI** | FastAPI + LangGraph + LLM | Multi-turn workflows, tool orchestration |
| **Document Intelligence** | FastAPI/CAP + Document AI | Extraction from structured documents |
| **ML + Explainability** | FastAPI/CAP + scikit-learn + SHAP + Streamlit | Regulated industries, audit trail |
| **Vector Search** | FastAPI + HANA Vector + Streamlit | Semantic matching, embeddings |
| **Video/Media** | FastAPI + Vision LLM + Fiori | Real-time analysis, compliance |
| **Teams Integration** | Flask/FastAPI + Bot Framework | Teams-native automation |

---

## Final Preparation Tips

✅ **Practice articulating**:
- Each answer out loud (2-3 minutes)
- Record yourself and listen critically
- Adjust based on clarity and confidence

✅ **Be ready for follow-ups**:
- "What if the data is 10x larger?"
- "How do you handle errors?"
- "What's the cost model?"
- "How do you ensure quality?"

✅ **Show operational thinking**:
- Don't just say "I'd use FastAPI"
- Explain why + trade-offs + scaling
- Mention monitoring, logging, error handling

✅ **Connect to business value**:
- Reduce manual effort by X%?
- Improve accuracy from Y% to Z%?
- Reduce cost by ${amount}?

✅ **Be honest about unknowns**:
- "I haven't worked with that specific SAP service, but I'd..."
- "That's a great question—here's my approach..."
- Don't fake expertise

---

**You're ready! Go ace this interview!**
