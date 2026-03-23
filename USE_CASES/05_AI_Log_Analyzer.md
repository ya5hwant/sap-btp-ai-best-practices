# USE CASE 5: AI Log Analyzer

## Quick Summary
Intelligent system log analysis: Ingest logs from multiple sources → Cluster similar errors → Prioritize by impact → Generate remediation recommendations → Link to SAP OSS notes.

---

## Customer Pain Point

**What you'd hear:**
"We get thousands of error logs per day. Most are noise or repeats. Operators spend hours finding critical errors and figuring out what to do. We need intelligent filtering and SAP-aware remediation steps."

**Business Impact:**
- Current MTTR (mean time to resolution): 8 hours
- Target: 30 minutes
- Operator productivity: 50% of time spent sorting logs

---

## Discovery Questions

1. **"How many logs per day?"** (1000s? 100k? 1M? Affects infrastructure)
2. **"Where do logs come from?"** (App servers? DB? Middleware? All of above?)
3. **"What percentage are actually critical?"** (1%? 5%?)
4. **"Do you have error codes mapping to OSS notes?"** (If yes → can automate lookup)
5. **"Current process: Log detection to resolution time?"** (30 min? 8 hours?)

---

## Your Approach

### Phase 1: Log Ingestion & Normalization
"Collect logs from all sources and normalize:

```
Raw log: [2024-03-22 10:15:30.123 ERROR] RFC Timeout calling FM_EXECUTE_QUERY

Normalized:
{
  'timestamp': '2024-03-22T10:15:30Z',
  'source': 'app-server-01',
  'severity': 'ERROR',
  'error_code': 'RFC_TIMEOUT',
  'message': 'Timeout calling RFC FM_EXECUTE_QUERY after 30s',
  'stack_trace': '...',
  'context': {
    'function': 'FM_EXECUTE_QUERY',
    'timeout_seconds': 30
  }
}
```

Why normalize?
- Fast search & filtering
- Enables pattern detection
- LLM can understand structured format"

### Phase 2: Intelligent Prioritization (LLM)
"Use LLM to assess each error:

```
For each error_code, calculate:
1. Severity (CRITICAL, HIGH, MEDIUM, LOW)
   - Is this blocking users?
   - How many systems affected?
   
2. Impact (user count, customer impact)
   - How many users can't work?
   - Which customers affected?
   
3. Root cause (likely diagnosis)
   - DB memory? Network? Application bug?
   
4. Recommended action
   - Restart service? Scale resources? Contact vendor?
```

Example:
```
Error: RFC_TIMEOUT
LLM Analysis:
  Severity: HIGH (function blocking all reports)
  Impact: 200+ users unable to run monthly reports
  Root cause: Database memory exhausted (typical pattern)
  Recommended action: Increase DBMS memory OR optimize query
  Relevant OSS Note: SAP Note 2345678 - RFC Timeout Solutions
```"

### Phase 3: Knowledge Grounding (OSS Integration)
"Link errors to SAP OSS notes:

```
For each error_code:
1. Query SAP OSS database (via API if available)
2. Return top 3 relevant notes
3. Summarize: What's the problem? What's the fix?

This grounds LLM recommendations in SAP best practices
(not just general knowledge).
```"

### Phase 4: Correlation & Clustering
"Related errors often come in bursts—identify patterns:

```python
# Group similar errors
error_spikes = {
  'RFC_TIMEOUT': 1000 in last hour (vs. 100 normal),
  'DBMS_MEMORY': 500 in last hour,
  'NETWORK_ERROR': 300 in last hour
}

# Alert: 'Multiple related errors spiked 10x in last hour.
#         Likely cascading failure. Escalate to DevOps.'
```"

### Phase 5: Operator Dashboard
"Build UI showing:

1. **Critical Alerts** (sorted by impact)
   - Error type, frequency, impact summary
   
2. **Trend Charts** (error rate over time)
   - Spike detection with anomaly highlighting
   
3. **Detailed Analysis** (per error)
   - Log sample + LLM analysis + OSS notes
   
4. **Recommended Actions**
   - What to do, who to notify, escalation path"

---

## Key Architectural Decisions

### Decision 1: CAP + HANA (Not FastAPI + Postgres)

**What you'd say:**
"I'd use **SAP CAP + HANA** because:

✓ Logs can be huge (100GB+ per year)
✓ HANA columnar storage: Fast aggregation queries
✓ Full-text indexing: Instant error_code search
✓ TypeScript: Type safety in critical system
✓ XSUAA: Enterprise auth baked-in
✓ Integration: Native SAP ecosystem

FastAPI + Postgres could work but wouldn't scale as well for this volume."

### Decision 2: Async LLM Analysis

**What you'd say:**
"LLM analysis is slow (2-5s per log). We can't block:

1. Log arrives → immediately store in HANA (fast)
2. Async job (SAP Event Mesh) → analyze via LLM
3. Update dashboard with results as they complete
4. Operators see: 'Analysis in progress...' then results appear"

### Decision 3: HANA Optimization for Scale

**What you'd say:**
"For billions of logs, I'd:

- **Partitioning**: By date (daily or weekly)
- **Indexes**: On error_code, severity, timestamp, source
- **Compression**: Use columnar compression
- **Archival**: Move logs >90 days to cold storage
- **Statistics**: Regular HANA optimization tasks"

---

## Implementation Walk-Through

### Example Flow

```
1. Error stream arrives in Kafka/Event Mesh
2. Consumer parses, normalizes to JSON
3. Stores in HANA (takes 10ms)
4. Publishes event: 'new_error_RFC_TIMEOUT'
5. Async worker receives event
6. Calls LLM: "Analyze this RFC_TIMEOUT"
7. Calls SAP OSS API: "Get notes for RFC_TIMEOUT"
8. Scores impact: "Affects 200 users"
9. Updates HANA: error record + analysis
10. Dashboard queries HANA, shows analysis

Total latency:
- Store in HANA: 10ms
- Analyze async: 3-5 seconds
- Display on dashboard: Real-time
```

### Code Skeleton

```python
# Log ingestion
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('log-topic')
for log_message in consumer:
    log = json.loads(log_message.value)
    normalized = normalize_log(log)
    
    # Store in HANA
    hana_client.insert('errors', normalized)
    
    # Trigger async analysis
    event_mesh.publish('error_analysis', {'error_id': normalized['id']})

# Async analysis
async def analyze_error(error_id):
    error = hana_client.query(f"SELECT * FROM errors WHERE id = {error_id}")
    
    # LLM analysis
    analysis = llm.analyze(f'''
        Error: {error['error_code']}
        Message: {error['message']}
        Analyze severity, impact, root cause, recommended action.
    ''')
    
    # OSS lookup
    oss_notes = sap_oss_api.search(error['error_code'])
    
    # Update HANA
    hana_client.update('errors', error_id, {
        'analysis': analysis,
        'oss_notes': oss_notes,
        'timestamp_analyzed': now()
    })
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **LLM analysis expensive at scale** | Batch process, cost throttling, cache results for duplicate errors |
| **Logs arrive faster than analysis** | Queue depth monitoring, implement backpressure |
| **False correlations** | Use statistical correlation, require human confirmation |
| **OSS lookup fails** | Graceful fallback: show generic remediation advice |
| **HANA disk fills** | Partition by date, archive to cold storage after 90 days |

---

## Success Metrics

**MTTR Improvement:**
- Current: 8 hours → Target: 30 minutes (16x faster)

**Accuracy:**
- 95% of recommended actions correct
- Operators follow LLM recommendations 80% of time

**Scale:**
- Handle 100k logs/day without degradation
- Analysis latency <5 seconds

**Cost:**
- Reduce log analysis effort by 60% (FTE savings)

---

## Related Use Cases

- **Video Incident Detection** (Similar: Event prioritization, different domain)
- **Anomaly Detection** (Similar: Anomaly scoring, different domain)
