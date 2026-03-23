# USE CASE 10: Email Agent

## Quick Summary
Intelligent email triage system: Classifies emails, extracts entities, routes to appropriate team, generates draft responses. Uses LLM for understanding + rule-based routing.

---

## Customer Pain Point

**What you'd hear:**
"We receive 500+ customer emails daily. Routing them to the right team is manual. Some emails are sales inquiries, some are support tickets, some are complaints. We need intelligent triage with automatic routing."

**Business Impact:**
- Current triage: Manual 2 hours/day (1 FTE)
- Misrouting: 20% of emails go to wrong team
- Response delay: Some emails stuck in queue for hours

---

## Discovery Questions

1. **"What teams receive emails?"** (Sales, Support, Finance, HR?)
2. **"What percentage get misrouted?"** (20%? 50%?)
3. **"Should system generate draft responses?"** (Yes = higher value)
4. **"Any compliance requirements?"** (GDPR, audit trail?)
5. **"Integration with email system?"** (Outlook, Gmail, SAP system?)

---

## Your Approach

### Phase 1: Email Intake
"Monitor email inbox, trigger on new message:

```
Integration:
- Outlook: Use Microsoft Graph API
- Gmail: Use Gmail API
- SAP: Use email routing

For each email:
- Extract: sender, subject, body, attachments
- Parse: HTML to plain text
- Store: In processing queue
```"

### Phase 2: Email Classification
"Classify by intent:

```
Intent types:
- SALES_INQUIRY: 'I want to buy...'
- SUPPORT_TICKET: 'Product not working...'
- COMPLAINT: 'Very disappointed...'
- BILLING_ISSUE: 'Invoice incorrect...'
- GENERAL_QUESTION: 'Can you tell me...'
- FEEDBACK: 'Great product...'

LLM prompt:
'Classify this email by intent:
{email_subject}
{email_body}

Return JSON: {\"intent\": \"SALES_INQUIRY\", \"confidence\": 0.95}'
```"

### Phase 3: Entity Extraction
"Extract key information:

```
Entities:
- Customer name, email, company
- Product mentioned
- Issue/request described
- Priority signals ('urgent', 'today', etc.)
- Sentiment (positive, negative, neutral)

LLM prompt:
'Extract entities from this email:
{email_body}

Return JSON: {
  \"customer_name\": \"\",
  \"product\": \"\",
  \"issue\": \"\",
  \"priority\": \"NORMAL\",
  \"sentiment\": \"NEUTRAL\"
}'
```"

### Phase 4: Intelligent Routing
"Route to appropriate team based on classification:

```
Rules:
- SALES_INQUIRY → Sales team
- SUPPORT_TICKET + URGENT → Support (escalated)
- SUPPORT_TICKET + NORMAL → Support queue
- COMPLAINT + HIGH_SENTIMENT → Management review
- BILLING_ISSUE → Finance team
- FEEDBACK → Archive (log for analysis)

Fallback: If confidence <70%, flag for human review
```"

### Phase 5: Draft Response Generation
"Generate draft response:

```
For each intent type, have template + personalization:

SALES_INQUIRY template:
'Thank you for your interest in [PRODUCT].
We'd be happy to discuss your needs.
Here are some resources: [LINKS]
Our sales team will contact you within 24 hours.'

Generate draft:
llm_response = llm.generate(f'''
Generate professional email response to:
Intent: {intent}
Customer concern: {issue}
Sentiment: {sentiment}

Keep response under 150 words, professional tone.
''')

Routes to team member for approval before sending.
```"

---

## Key Architectural Decisions

### Decision 1: LLM + Rules Hybrid

**What you'd say:**
"I'd combine LLM + rules:

LLM (extraction):
- Classify intent
- Extract entities
- Gauge sentiment

Rules (routing):
- Intent + priority → team assignment
- Sentiment + intent → escalation logic

Why hybrid?
- LLM handles ambiguity
- Rules ensure consistency
- Cheaper than pure LLM (LLM only for extraction, rules for logic)"

### Decision 2: Human Review for Low Confidence

**What you'd say:**
"For emails where classification confidence <70%:

1. Flag for human review (don't auto-route)
2. Show LLM's analysis + alternative classifications
3. Human chooses correct classification
4. Feedback loop improves model

This prevents misrouting of ambiguous emails."

### Decision 3: Response Generation as Draft, Not Auto-Send

**What you'd say:**
"Generate draft responses but don't auto-send:

1. LLM generates draft
2. Routes with email to team member
3. Human reviews + edits
4. Human clicks 'send'

Why?
- Maintains human oversight
- Builds trust (not bot-first)
- Allows personalization
- Complies with compliance requirements"

---

## Implementation Walk-Through

### Code Skeleton

```python
from anthropic import Anthropic
import json

async def process_email(email):
    client = Anthropic()
    
    # Step 1: Classify intent
    intent_response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": f'''
                Classify this email:
                Subject: {email['subject']}
                Body: {email['body'][:500]}
                
                Return JSON:
                {{
                  "intent": "SALES_INQUIRY|SUPPORT_TICKET|COMPLAINT|etc",
                  "confidence": 0.95,
                  "reasoning": "brief explanation"
                }}
                '''
            }
        ]
    )
    intent_data = json.loads(intent_response.content[0].text)
    
    # Step 2: Extract entities
    entity_response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": f'''
                Extract entities from this email:
                {email['body']}
                
                Return JSON:
                {{
                  "customer_name": "",
                  "product": "",
                  "issue": "",
                  "priority": "NORMAL|HIGH|URGENT",
                  "sentiment": "POSITIVE|NEUTRAL|NEGATIVE"
                }}
                '''
            }
        ]
    )
    entities = json.loads(entity_response.content[0].text)
    
    # Step 3: Route based on rules
    team = route_email(intent_data, entities)
    
    # Step 4: Generate draft response
    if should_generate_response(intent_data):
        draft_response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=200,
            messages=[
                {
                    "role": "user",
                    "content": f'''
                    Generate professional email response to customer:
                    Intent: {intent_data['intent']}
                    Issue: {entities['issue']}
                    Keep under 150 words.
                    '''
                }
            ]
        )
        draft = draft_response.content[0].text
    else:
        draft = None
    
    # Step 5: Queue for team review
    queue_for_team_review({
        'email': email,
        'intent': intent_data,
        'entities': entities,
        'team': team,
        'draft_response': draft,
        'confidence': intent_data['confidence']
    })
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **Misclassification routes to wrong team** | Confidence threshold + human review for <70% confidence |
| **Draft response inappropriate** | Require human approval before send |
| **Privacy breach** | Encrypt emails at rest, audit trail for access |
| **LLM cost** | Batch process, cache similar emails, use cheaper models where possible |

---

## Success Metrics

**Speed:**
- Email routed within 5 seconds (vs. manual)
- 80% automated (20% require human review)

**Accuracy:**
- 95% correct routing (vs. current 80%)
- <1% misrouted to completely wrong team

**Cost:**
- Save 1 FTE in email triage (€50k/year)

**User Satisfaction:**
- Faster response times
- Better email organization

---

## Related Use Cases

- **Post-Sales Chatbot** (Similar: LLM + tool orchestration)
- **Intelligent Negotiation Assistant** (Similar: LLM for business processes)
