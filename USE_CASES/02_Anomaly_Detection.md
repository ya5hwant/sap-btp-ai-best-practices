# USE CASE 2: Anomaly Detection in Sales Orders

## Quick Summary
Detect unusual sales orders (fraud, data entry errors, unusual discounts) using unsupervised ML. Isolation Forest scores orders in real-time. SHAP explains why each order is flagged. LLM translates explanations into business language.

---

## Customer Pain Point

**What you'd hear:**
"We're seeing unusual orders slip through—sometimes fraudulent, sometimes data entry errors. Last month we lost €50k on a huge discount given to a new customer. We need to flag high-risk orders automatically without creating so many false positives that our team ignores the system."

**Business Impact:**
- Current loss rate: €500k/year in anomalies
- Current false positive: 40% (team ignores alerts)
- Target: Catch 80% of anomalies with <5% false positives

---

## Discovery Questions

1. **"How many orders per day are we processing?"**
   - (100s? 1000s? 10,000s? Affects architecture: real-time vs. batch)
2. **"What causes orders to be 'anomalous'?"** (Show customer you understand)
   - Unusual discount depth? (70% discount vs. normal 10%)
   - New customer with large order? (€100k first order)
   - Product mix never seen before?
   - Order at 2 AM? (Orders normally 9 AM-5 PM)
   - From unusual geography?
3. **"How many false positives can your team tolerate?"**
   - (If 50% false positives, team will ignore system)
4. **"Do you have historical data of known anomalies?"**
   - (Labeled data → supervised learning. Unlabeled → unsupervised)
5. **"If we flag an order, what happens next?"**
   - (Manual review? Auto-deny? Escalate to manager?)

---

## Your Approach

### Phase 1: Understand the Baseline
"Before building any model, I'd ask: What are your current false positive and false negative rates?

Example baseline:
- Current: 5% false positive (manual review catches noise)
- Current: 20% miss rate (anomalies slip through)
- **ROI target**: Catch 80% of anomalies, maintain <1% false positive rate
- **Financial impact**: 80% of €500k anomalies = €400k savings, minus €5k review costs = €395k net"

### Phase 2: Feature Engineering (Critical)
"I'd identify features that distinguish normal from anomalous orders:

```
Customer history features:
- How many orders from this customer before? (1st order = higher risk)
- What's typical order size? (Is this 10x their average?)
- What's typical order value? (€10k order from €1k customer = anomaly)
- Days since last order? (New customer after 1 year = risky)

Order characteristics:
- Discount depth: Is 70% discount unusual? (Normal: 10%, Unusual: >30%)
- Product mix: Do these products normally sell together?
- Order timing: Is 2 AM order unusual? (Order pattern by hour)
- Margin: Would this order lose money?

Geographic/seasonal:
- From typical region?
- Typical quarter for this product?
```

Why features matter:
- Capture business logic without hard-coding rules
- Model learns which features correlate with anomalies
- SHAP explains predictions via features"

### Phase 3: Model Selection (Isolation Forest)
"I'd use **Isolation Forest** for several reasons:

```python
from sklearn.ensemble import IsolationForest

# Why IF?
✓ No labeled training data needed (unsupervised)
✓ Fast training & prediction (O(n) complexity)
✓ Interpretable (SHAP works well with trees)
✓ Handles mixed data types (numeric + categorical)
✓ Outliers naturally isolated

✗ Not: Neural networks (need 1000s of labeled anomalies)
✗ Not: Simple rules (miss complex patterns)
✗ Not: One-Class SVM (slower, less interpretable)
```"

### Phase 4: Explainability (The Critical Part)
"Anomaly detection is useless if users don't trust it. I'd add **two layers** of explanation:

**Layer 1 - SHAP (Technical Explainability):**
```python
import shap

explainer = shap.TreeExplainer(isolation_forest)
shap_values = explainer.shap_values(order_features)

# Output: Show which features pushed score toward anomalous
print(f"Score: 0.85 (anomalous) because:")
print(f"  - 10x order size: +0.4")
print(f"  - High discount (70%): +0.3")
print(f"  - New customer: +0.15")
```

**Layer 2 - LLM Explanation (Business Language):**
```python
explanation = llm.generate(f'''
  Order anomaly explanation:
  Score: 0.85 (highly anomalous)
  SHAP drivers: Order size 10x normal, discount 70%, new customer
  
  Write in plain English for business user.
''')
# Output: 'This order is unusual because John Corp (new customer) is buying 
#          1000 units (normally 50-100), with a 60% discount. 
#          We recommend manual review.'
```

This dual-layer approach builds trust."

### Phase 5: Fine-Tuning Interface
"I'd build a UI where analysts can:
- Adjust contamination rate (how many anomalies expected? 1%? 5%?)
- Enable/disable specific features
- Set confidence thresholds (only flag >0.9 confidence)
- See real-time impact on false positive rate

This gives them control + confidence in the system."

---

## Key Architectural Decisions

### Decision 1: Batch vs. Real-Time Scoring

**What you'd say:**
"For V1, I'd do **batch scoring**:
- Every 4 hours, re-score all open orders
- Updates dashboard with flagged orders
- Alerts on new anomalies

Why batch?
- Faster to build (no complex streaming infrastructure)
- More accurate (can look at full day's context)
- Cost-effective (one batch job vs. per-order API calls)
- Sufficient for most workflows

Future: Real-time scoring if needed."

### Decision 2: Model Retraining

**What you'd say:**
"Retraining schedule:
- **Weekly**: Retrain on last 12 months of data
- **Trigger**: If model performance drops below 80% precision
- **Versioning**: Keep last 5 model versions for rollback

Process:
1. Training: Use analyst-validated decisions (what they marked as anomaly)
2. Validation: Test on holdout 20% of orders
3. Comparison: Is new model better than current? If yes → deploy. If no → keep current."

### Decision 3: Storage & Scalability

**Stack:**
- **HANA**: Store orders + features + anomaly scores
  - Columnar storage: Fast aggregation queries
  - Indexes: Fast lookup by customer/order_id
  - Partitioning: By date for old order archive
  - Vector search: Could add for semantic similarity
- **Redis**: Cache model + recent anomaly flags
- **ML Pipeline**: Batch job (can be hourly/daily)

---

## Implementation Walk-Through

### Example Score Interpretation

```
Order: €150k to new customer, 60% discount, 2 AM

Feature values:
- customer_age_days: 0 (new customer) → high anomaly signal
- order_size_ratio: 10 (10x normal) → high anomaly signal  
- discount_depth: 0.60 (vs. normal 0.10) → high anomaly signal
- order_hour: 2 (vs. normal 9-17) → medium anomaly signal

Isolation Forest Score: 0.85 (0=normal, 1=anomalous)

SHAP Explanation:
- customer_age_days=0: contributes +0.4
- order_size_ratio=10: contributes +0.3
- discount_depth=0.60: contributes +0.15

Human-readable: "New customer buying 10x normal amount with 60% discount 
                  at 2 AM. Recommend review."
```

### Code Skeleton

```python
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import shap

# Training
features = ['customer_age_days', 'order_size_ratio', 'discount_depth', 'order_hour']
X_train = orders[features].fillna(0)
X_train_scaled = StandardScaler().fit_transform(X_train)

model = IsolationForest(contamination=0.05)  # Expect 5% anomalies
model.fit(X_train_scaled)

# Inference
new_orders = incoming_orders[features]
new_orders_scaled = StandardScaler().transform(new_orders)
anomaly_scores = model.score_samples(new_orders_scaled)  # -1 to 0 scale

# Explainability
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(new_orders_scaled)

# Flag anomalies
flagged = new_orders[anomaly_scores < -0.5]  # Score < -0.5 = anomalous
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **False positive rate too high** | Start conservative (high confidence threshold 0.8+), gradually lower as confidence increases |
| **Model degrades over time** | Drift detection: monitor prediction distribution, retrain if changes >5% |
| **Stakeholders don't trust model** | Weekly calibration meetings, show ROI metrics, explain top features |
| **Model catches fraud but customer can't pay** | Add payment capacity check as separate tool |
| **Explainability doesn't work** | A/B test explanations with users, iterate based on feedback |

---

## Success Metrics

**Financial:**
- Catch 80% of anomalies → €320k savings annually
- Maintain <5% false positive rate (analysts trust system)

**Operational:**
- Mean time to detect: <30 min
- Review time per flag: <5 min
- System uptime: >99.5%

**User Adoption:**
- 90% of order reviewers use the dashboard
- NPS score >60
- Escalation handling: <1% user overrides of recommendation

---

## Interview Tips

**If asked "Why not deep learning?"**
- Answer: "Deep learning needs labeled training data (1000s of anomalies). You don't have that. Isolation Forest needs zero labeled data and is 100x faster. Unless you have massive labeled dataset, tree-based anomaly detection wins."

**If asked "How do you handle class imbalance?"**
- Answer: "Anomalies are rare (5% of orders). Isolation Forest doesn't care about imbalance—it doesn't learn 'anomaly' vs. 'normal', it isolates outliers. This is why it's better than supervised models for anomaly detection."

**If asked "What about false negatives?"**
- Answer: "Set lower contamination rate (expect 10% anomalies instead of 5%) to be more aggressive. Or reduce score threshold (flag >0.7 instead of >0.8). Trade-off: higher false positives but lower false negatives."

---

## Related Use Cases

- **Document Outlier Detection** (Similar: Unsupervised outlier detection, different domain)
- **Video Incident Detection** (Different: Vision-based, threshold-based rules)
