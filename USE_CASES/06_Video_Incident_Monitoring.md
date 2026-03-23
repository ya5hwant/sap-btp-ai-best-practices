# USE CASE 6: Video Incident & Safety Monitoring

## Quick Summary
Analyze warehouse video streams for safety violations using vision LLM (Gemini 2.5 Pro). Detect hard hat violations, equipment misuse, restricted area breaches. Alert with high confidence thresholds to avoid false alarms.

---

## Customer Pain Point

**What you'd hear:**
"We have video feeds from our warehouse. Manually monitoring them is expensive and error-prone. Workers aren't wearing hard hats, equipment is misused. We need automated detection with high confidence—false alarms that cause unnecessary evacuations are problematic."

**Business Impact:**
- Safety incidents: 5-10 per month
- Cost per incident: €10k (injury + investigation + downtime)
- Current monitoring: Manual (expensive, inconsistent)

---

## Discovery Questions

1. **"What incidents are most important to catch?"** (Hard hat? Fire? Machinery misuse?)
2. **"What's your false alarm tolerance?"** (Evacuate 100 workers = can't have false positives)
3. **"Live streams or recorded videos?"** (Affects real-time vs. batch architecture)
4. **"Acceptable latency?"** (Real-time alert or 1-hour delayed analysis okay?)
5. **"Privacy concerns?"** (Recording workers—policy in place?)

---

## Your Approach

### Phase 1: Video Intake & Storage
"Accept video uploads or stream links. Store temporarily:

```
For large files:
- Implement chunked upload (avoid timeouts)
- Validate format/size
- Store in object storage (not local disk)

Processing options:
- Real-time: Analyze video stream directly (low latency)
- Batch: Process uploaded videos hourly (cheaper)
```"

### Phase 2: Frame Extraction
"Video is too large to send in one piece. Extract key frames:

```
Strategy 1: Sample every N frames (1/30 = 1 second interval)
Strategy 2: Motion detection (only process frames with movement)
Strategy 3: Uniform distribution (spread frames across video duration)

Why?
- Gemini 2.5 Pro can only handle videos of reasonable size
- Reduces processing cost significantly
- Captures most incidents
```"

### Phase 3: Vision LLM Analysis
"Send frame to Gemini 2.5 Pro:

```
Prompt:
\"Analyze this warehouse video frame for safety violations:
- Hard hat compliance (workers near equipment with/without hard hat)
- Equipment misuse (forklifts, pallet jacks following safety)
- Restricted area breaches (unauthorized access)
- Emergency situations (fire, injury, spills)
- Environmental hazards (obstacles in aisles, poor lighting)

For each incident detected:
- Type (hard hat violation, restricted area breach, etc.)
- Location in frame (if possible)
- Severity (CRITICAL, HIGH, MEDIUM, LOW)
- Confidence (0-100%)
- Recommended action

Return JSON:
{
  'incidents': [
    {
      'type': 'hard_hat_violation',
      'severity': 'HIGH',
      'confidence': 92,
      'location': 'worker near pallet jack',
      'action': 'Alert supervisor'
    }
  ],
  'overall_risk': 'HIGH'
}
\"
```"

### Phase 4: Incident Processing
"Filter by confidence threshold:

```
<70% confidence: Ignore (probably false positive)
70-90% confidence: Flag for human review
>90% confidence: Immediate alert

Example:
- Hard hat at 92% → Alert supervisor immediately
- Movement that might be worker at 60% → Don't alert (shadow/reflection)
```"

### Phase 5: Alert Generation
"Build notification system:

```
Critical alerts (>90% confidence):
- SMS to supervisor: 'HARD HAT VIOLATION at Packing Area - Frame #123'
- Alert dashboard: Show video frame + incident
- Log incident: Timestamp, location, severity, image

Medium alerts (70-90%):
- Add to review queue for human verification
- Don't escalate yet

Escalation:
- 3+ incidents in 1 hour → Escalate to Manager
- Repeated violators → Generate report
```"

---

## Key Architectural Decisions

### Decision 1: Batch vs. Real-Time

**What you'd say:**
"I'd start with **batch processing**:

- Process videos every 4 hours
- Analyze frames in parallel
- Store incidents in database
- Alert if severity warrants immediate attention

Why batch?
- Lower cost (can batch process at off-peak)
- Better accuracy (can apply post-processing)
- Simpler to implement

Future: Real-time if needed (more complex, more expensive)"

### Decision 2: Confidence Thresholds

**What you'd say:**
"High false positive rate is worse than missing incidents:

```
Hard hat violation threshold: >85% (very high)
  Why? False alarm evacuates warehouse
  
Restricted area breach: >80% (high)
  Why? Fewer false positives than hard hat

General safety: >70% (medium)
  Why? More tolerance for false positives
```

I'd A/B test thresholds and adjust based on feedback."

### Decision 3: Multi-Camera Coordination

**What you'd say:**
"For multiple cameras:

- Process independently
- Correlate incidents: 'If incident detected in 2+ cameras simultaneously → higher severity'
- Track worker movement across zones
- Identify repeat violators

Example: 'Worker without hard hat moved from Zone A to Zone B in 30 seconds'
→ Alert about the same worker (not duplicate alerts)"

---

## Implementation Walk-Through

### Code Skeleton

```python
import anthropic
import base64
from pathlib import Path

# Extract frames from video
import cv2
def extract_frames(video_path, sample_rate=30):
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % sample_rate == 0:
            # Save frame temporarily
            frame_path = f'/tmp/frame_{frame_count}.jpg'
            cv2.imwrite(frame_path, frame)
            frames.append(frame_path)
        
        frame_count += 1
    
    cap.release()
    return frames

# Analyze frame with Gemini
def analyze_frame(frame_path):
    client = anthropic.Anthropic()
    
    with open(frame_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",  # or gemini-2.5-pro via SAP AI Core
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": "Analyze this warehouse frame for safety violations..."
                    }
                ],
            }
        ],
    )
    
    return json.loads(message.content[0].text)

# Process video
frames = extract_frames('warehouse.mp4')
incidents = []

for frame in frames:
    analysis = analyze_frame(frame)
    
    # Filter by confidence
    for incident in analysis['incidents']:
        if incident['confidence'] > 70:  # Only flagged incidents
            incidents.append(incident)
            
            if incident['confidence'] > 90:
                # Send immediate alert
                send_alert(incident)

# Store for review
store_incidents(incidents)
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **False alarms cause disruption** | High confidence threshold (>85%), human review for medium confidence |
| **Privacy concerns** | Frame retention policy (delete after 24 hours), anonymize faces if possible |
| **Vision model misses incidents** | Combination with motion detection, zone-based alerts |
| **Video processing too slow** | Batch processing, parallel frame analysis, adaptive sampling |
| **Worker pushback on monitoring** | Transparent policy, explain safety purpose, focus on incident not identity |

---

## Success Metrics

**Safety:**
- Incidents detected: 95% of safety violations caught before escalation
- False alarm rate: <5% (trust in system maintained)
- Response time: <5 minutes from detection to alert

**Operational:**
- Supervisor productivity: 50% of monitoring time freed up
- Incident tracking: 100% complete audit trail

**Financial:**
- Reduced incidents by 40% (lower injury costs)
- Monitoring cost reduction: 60%

---

## Related Use Cases

- **Anomaly Detection** (Similar: Anomaly scoring, different domain)
