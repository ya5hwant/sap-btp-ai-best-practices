# USE CASE 4: Diagram-to-BPMN Converter

## Quick Summary
Convert hand-drawn or Visio business process diagrams to BPMN XML format. Uses vision LLM (Claude, GPT-4o) to understand diagram structure. Returns standard BPMN for import into SAP Build/Signavio.

---

## Customer Pain Point

**What you'd hear:**
"Our business analysts draw process diagrams on whiteboards or Visio. Converting them to BPMN format for SAP Build is manual—I spend hours redrawing in Signavio. We need to automate this."

**Business Impact:**
- Current conversion: 2 hours per diagram
- Diagrams created: 20/month
- Opportunity: Save 40 hours/month = 1 FTE

---

## Discovery Questions

1. **"What formats are these diagrams in?"** (Visio, images, hand-drawn scans, PDFs?)
2. **"How complex are they?"** (5 steps? 50 steps? Swimlanes?)
3. **"What happens with the BPMN output?"** (Imported to Signavio? SAP Build directly?)
4. **"How often do you create diagrams?"** (Weekly? Monthly?)
5. **"Are diagrams mostly consistent or wildly different?"** (Affects prompt engineering)

---

## Your Approach

### Step 1: Vision Analysis
"User uploads diagram → encode as base64 → send to **vision LLM** (Claude 3.5 Sonnet or GPT-4o).

The LLM's job:
- Identify all activities/tasks (rectangles with labels)
- Find decision points (diamonds with conditions)
- Spot start/end events (circles)
- Trace flow connections (arrows with labels)
- Recognize swimlanes (if present)
- Detect text annotations"

### Step 2: Structured Extraction
"I'd use this prompt:

```
Analyze this business process diagram and extract:
1. All activities (name, type: userTask, serviceTask, automaticTask)
2. Decision points (condition/label on each path)
3. Start and end events
4. Connections (flows between elements)
5. Swimlanes (if present) and element ownership

Return valid JSON:
{
  'activities': [
    {'id': 'task1', 'name': 'Review Order', 'type': 'userTask'},
    {'id': 'task2', 'name': 'Calculate Price', 'type': 'serviceTask'},
    {'id': 'gate1', 'name': 'Approved?', 'type': 'exclusiveGateway'}
  ],
  'flows': [
    {'from': 'task1', 'to': 'gate1', 'label': ''},
    {'from': 'gate1', 'to': 'task2', 'label': 'Yes'},
    {'from': 'gate1', 'to': 'reject', 'label': 'No'}
  ],
  'startEvent': 'start1',
  'endEvent': 'end1'
}
```

Why JSON? 
- Easy to validate (check all fields present)
- Trivial to convert to BPMN XML
- User can edit before final generation"

### Step 3: BPMN XML Generation
"Convert JSON to BPMN using templates:

```xml
<?xml version="1.0"?>
<bpmn2:definitions xmlns:bpmn2="http://www.omg.org/spec/BPMN/20100524/MODEL">
  <bpmn2:process id="process1" name="Main Process">
    
    <!-- Start Event -->
    <bpmn2:startEvent id="start1" name="Order Received"/>
    
    <!-- User Tasks -->
    <bpmn2:userTask id="task1" name="Review Order">
      <bpmn2:incoming>flow0</bpmn2:incoming>
      <bpmn2:outgoing>flow1</bpmn2:outgoing>
    </bpmn2:userTask>
    
    <!-- Service Tasks -->
    <bpmn2:serviceTask id="task2" name="Calculate Price">
      <bpmn2:incoming>flow2</bpmn2:incoming>
      <bpmn2:outgoing>flow3</bpmn2:outgoing>
    </bpmn2:serviceTask>
    
    <!-- Decision Gateway -->
    <bpmn2:exclusiveGateway id="gate1" name="Approved?">
      <bpmn2:incoming>flow1</bpmn2:incoming>
      <bpmn2:outgoing>flow2</bpmn2:outgoing>
      <bpmn2:outgoing>flow4</bpmn2:outgoing>
    </bpmn2:exclusiveGateway>
    
    <!-- Sequence Flows (connections) -->
    <bpmn2:sequenceFlow id="flow0" sourceRef="start1" targetRef="task1"/>
    <bpmn2:sequenceFlow id="flow1" sourceRef="task1" targetRef="gate1"/>
    <bpmn2:sequenceFlow id="flow2" sourceRef="gate1" targetRef="task2" name="Yes"/>
    <bpmn2:sequenceFlow id="flow4" sourceRef="gate1" targetRef="reject" name="No"/>
    
    <!-- End Event -->
    <bpmn2:endEvent id="end1" name="Order Processed">
      <bpmn2:incoming>flow3</bpmn2:incoming>
    </bpmn2:endEvent>
    
  </bpmn2:process>
</bpmn2:definitions>
```"

### Step 4: Validation
"Validate generated BPMN:
1. **XSD schema**: Does it conform to BPMN 2.0 spec?
2. **Connectivity**: Are all elements connected? Any orphaned tasks?
3. **Gateway semantics**: Do gateways have 2+ outgoing flows?
4. **Start/End**: Process has exactly 1 start + 1+ end events?

```python
from lxml import etree

# Validate against BPMN schema
bpmn_schema = etree.XMLSchema(file='bpmn20.xsd')
is_valid = bpmn_schema.validate(bpmn_tree)
if not is_valid:
  print(bpmn_schema.error_log)  # Show validation errors
```"

### Step 5: Preview & Export
"Show user:
1. **Visual preview** (render BPMN diagram)
2. **JSON structure** (editable fields)
3. **Validation report** (any issues?)
4. **Download options** (BPMN XML for Signavio, for SAP Build)"

---

## Key Architectural Decisions

### Decision 1: Multi-Model Fallback

**What you'd say:**
"Vision models vary in quality. I'd implement fallback:

1. Try Claude 3.5 Sonnet (best for diagrams, good context window)
2. If fails, try GPT-4o (alternative, slightly different understanding)
3. If fails, try Gemini 2.5 Pro (third-party check)
4. If all fail, show user extracted JSON for manual correction

This ensures we never fail completely."

### Decision 2: Human Correction Workflow

**What you'd say:**
"Even if LLM extraction is 85% right, that 15% wrong matters. So:

1. Show extracted JSON (editable)
2. User corrects: rename activities, add/remove flows, fix connections
3. Regenerate BPMN from corrected JSON
4. Export to Signavio

This is 85% automatic + 15% human, which is 8x faster than 100% manual."

### Decision 3: Handling Large Diagrams

**What you'd say:**
"For large diagrams (50+ elements), the image becomes too complex:

1. Split image into regions (top, middle, bottom)
2. Analyze each region independently
3. Use explicit mention of flows between regions
4. Stitch together into complete BPMN

Alternatively: Ask user to upload in sections if diagram is complex."

---

## Implementation Walk-Through

### Code Skeleton

```python
import base64
import anthropic
import json
import xml.etree.ElementTree as ET

# Step 1: Encode image
with open('diagram.png', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

# Step 2: Send to Claude
client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data,
                    },
                },
                {
                    "type": "text",
                    "text": "Extract business process diagram as JSON..."
                }
            ],
        }
    ],
)

# Step 3: Parse JSON response
extracted_json = json.loads(message.content[0].text)

# Step 4: Generate BPMN XML
def json_to_bpmn(data):
    root = ET.Element('bpmn2:definitions', xmlns='...')
    process = ET.SubElement(root, 'bpmn2:process', id='process1')
    
    # Add elements
    for activity in data['activities']:
        ET.SubElement(process, 'bpmn2:' + activity['type'],
                     id=activity['id'], name=activity['name'])
    
    # Add flows
    for flow in data['flows']:
        ET.SubElement(process, 'bpmn2:sequenceFlow',
                     sourceRef=flow['from'], targetRef=flow['to'])
    
    return ET.tostring(root, encoding='unicode')

bpmn_xml = json_to_bpmn(extracted_json)

# Step 5: Validate
validate_bpmn(bpmn_xml)

# Step 6: Export
with open('output.bpmn', 'w') as f:
    f.write(bpmn_xml)
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **LLM misidentifies task types** | Validate task types against BPMN spec, ask for clarification |
| **Connections get lost** | Validate flow connectivity, highlight orphaned elements |
| **Swimlanes incorrect** | LLM tends to miss swimlanes—ask explicit question in prompt |
| **Output invalid BPMN** | XSD validation before export, show errors to user |
| **Hand-drawn diagram illegible** | Pre-process: contrast enhancement, OCR if needed |

---

## Success Metrics

**Speed:**
- 5 minutes to convert (vs. 2 hours manual)
- 90% of diagrams require <2 min manual correction

**Accuracy:**
- 95%+ structural match with manual BPMN (flows correct)
- 100% BPMN spec compliance

**Adoption:**
- 80% of diagrams processed automatically
- User satisfaction: "Faster than manual"

**Cost:**
- €1 per diagram (vs. €50 manual)
- 20 diagrams/month → €20 vs. €1000 = €980 savings

---

## Related Use Cases

- **Sales Order Extractor** (Similar: Structured extraction from documents)
- **AI PDF Information Extraction** (Similar: Vision-based extraction)
