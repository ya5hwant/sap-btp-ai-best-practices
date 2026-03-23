# USE CASE 22: Agentic Chatbot (Teams Integration)

## Quick Summary
Conversational bot deployed to Microsoft Teams using Microsoft Bot Framework. Integrates with SAP data. Handles employee queries: expense reports, leaves, IT tickets. Similar to Post-Sales Chatbot but for internal employees.

---

## Customer Pain Point

**What you'd hear:**
"Our HR and IT teams field hundreds of employee questions daily. 'How many vacation days do I have?', 'What's my expense report status?', 'How do I reset my password?'. We need a bot that handles these self-service."

**Business Impact:**
- Current HR/IT support: 4 FTE
- Queries/day: 200+
- Opportunity: Save 60% of support time

---

## Your Approach

### Phase 1: Intent Mapping
"Define employee intents:

```
HR queries:
- Leave balance check
- Expense report status
- Benefits information
- Payroll info

IT queries:
- Password reset
- Access request
- System status
- Ticket tracking
```"

### Phase 2: Teams Bot Framework
"Build bot on Microsoft Bot Framework:

```
Integration:
- Connect to Teams (via Teams API)
- Authenticate via Azure AD (enterprise SSO)
- Link to SAP for employee data
```"

### Phase 3: LangGraph State Machine
"Multi-turn conversation:

```
User: 'How many vacation days do I have?'
Bot: 'I'll look that up for you...'
Bot calls: get_leave_balance(employee_id)
Bot responds: 'You have 15 days remaining (2 planned for next month)'
```"

### Phase 4: Action Execution
"For some queries, take action:

```
User: 'I need to request 3 days off'
Bot: 'I can help with that. What dates?'
User: 'March 25-27'
Bot: 'Creating leave request for approval...'
Bot updates HR system
Bot: 'Your leave request #1234 submitted for approval'
```"

### Phase 5: Escalation
"For complex questions:

```
User: 'I have a complex compensation question'
Bot: 'This requires HR review. Connecting you with an HR specialist...'
Bot: Routes to HR team in Teams thread
Human takes over conversation
```"

---

## Key Architectural Decisions

### Decision 1: Teams vs. Web UI

**What you'd say:**
"I'd use Teams because:

✓ Employees already use Teams (adoption)
✓ Native notification (Adaptive Cards)
✓ Integrated with identity (Azure AD)
✓ Rich interaction (buttons, cards, threading)

Web UI would work but lower adoption (another system to learn)."

### Decision 2: Azure Bot Framework

**What you'd say:**
"Bot Framework provides:

✓ Teams integration built-in
✓ Multi-turn conversation support
✓ State management
✓ Rich messaging (cards, buttons)

Could build custom, but Bot Framework saves weeks."

### Decision 3: LangGraph for Logic

**What you'd say:**
"LangGraph for state machine:

✓ Multi-turn conversations
✓ Tool orchestration (call HR API, then IT API)
✓ Error handling (if HR API fails, notify user)
✓ Context persistence (remember employee throughout conversation)"

---

## Implementation

```python
from langgraph.graph import StateGraph
from azure.bot.builder import Bot, BotFrameworkAdapter
from azure.identity import DefaultAzureCredential
import json

# Teams bot
adapter = BotFrameworkAdapter()

@adapter.process_activity
async def on_message(turn_context):
    # Get employee intent
    message = turn_context.activity.text
    
    # LangGraph agent
    result = await agent.invoke({
        'messages': [{'role': 'user', 'content': message}],
        'employee_id': turn_context.activity.from_property.id,
        'channel': 'teams'
    })
    
    # Send response
    await turn_context.send_activity(f"{result['response']}")

# Tools available to agent
tools = {
    'get_leave_balance': get_leave_balance,
    'get_expense_status': get_expense_status,
    'create_leave_request': create_leave_request,
    'reset_password': reset_password,
    'escalate_to_hr': escalate_to_hr
}

# LangGraph definition
graph = StateGraph(state_schema=BotState)
graph.add_node('interpret', interpret_intent)
graph.add_node('execute', execute_action)
graph.add_node('respond', generate_response)

graph.add_edge('interpret', 'execute')
graph.add_edge('execute', 'respond')
```

---

## Success Metrics

- 60% of queries self-served (no human needed)
- Employee satisfaction: NPS > 60
- HR/IT FTE savings: 2-3 FTE
- Response time: <1 minute

---

## Related Use Cases

- **Post-Sales Chatbot** (Similar: LLM + tools, different context)
- **Email Agent** (Similar: Intelligent routing)
