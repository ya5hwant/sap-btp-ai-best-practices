# USE CASE 18: Vendor Selection Optimization

## Quick Summary
Multi-criteria vendor selection using scoring algorithm + optimization. Evaluate vendors on cost, quality, lead time, risk, compliance. Generate optimal vendor portfolio.

---

## Customer Pain Point

**What you'd hear:**
"We evaluate vendors based on multiple criteria. Current process is manual spreadsheets. Sometimes we choose expensive vendors when better options exist. We need data-driven vendor optimization."

**Business Impact:**
- Current vendor cost: Estimated 10% higher than optimal
- Procurement spend: €100M/year
- Opportunity: €10M cost reduction

---

## Your Approach

### Phase 1: Vendor Master Data
"Collect vendor attributes:

```
- Cost (unit price, volume discounts)
- Quality (defect rate, certifications)
- Lead time (average delivery days)
- Reliability (on-time % past 12 months)
- Risk (location, single-source, financial stability)
```"

### Phase 2: Scoring Model
"Multi-dimensional score:

```
Score = 0.40 * price_score +
        0.20 * quality_score +
        0.15 * leadtime_score +
        0.15 * reliability_score +
        0.10 * risk_score

(Weights adjustable by category)
```"

### Phase 3: Portfolio Optimization
"Allocate volume across vendors:

```
Goal: Minimize cost while ensuring resilience

Constraints:
- Single source not >40% of volume (risk)
- Geographic diversification (2+ regions)
- Quality/SLA minimums
- Total volume allocation = 100%

Optimization:
Use linear programming to find optimal allocation
```"

### Phase 4: Scenario Analysis
"Answer questions:

```
'What if Vendor A increases price 5%?'
'What if Vendor B goes out of business?'
'What if demand increases 20%?'

Run simulations, show impact on cost/risk
```"

---

## Implementation

```python
from scipy.optimize import minimize, LinearConstraint
import numpy as np

def optimize_vendor_portfolio(vendors, total_volume, constraints):
    # Scoring
    scores = [calculate_vendor_score(v) for v in vendors]
    
    # Optimization
    def objective(allocation):
        # Minimize cost
        cost = sum(allocation[i] * vendors[i]['unit_price'] 
                  for i in range(len(vendors)))
        return cost
    
    # Constraints
    bounds = [(0, total_volume * 0.4) for _ in vendors]  # Max 40% per vendor
    
    result = minimize(
        objective,
        x0=[total_volume / len(vendors)] * len(vendors),
        bounds=bounds,
        constraints=[
            LinearConstraint(np.ones(len(vendors)), 
                           total_volume, total_volume)  # Sum = total
        ]
    )
    
    optimal_allocation = result.x
    
    return {
        'allocation': optimal_allocation,
        'total_cost': objective(optimal_allocation),
        'risk_score': calculate_portfolio_risk(optimal_allocation),
        'savings': current_cost - objective(optimal_allocation)
    }
```

---

## Success Metrics

- Cost reduction: €10M (10% savings)
- Vendor onboarding time: Reduced 50%
- Supply chain resilience: Improved (fewer single sources)

---

## Related Use Cases

- **Intelligent Negotiation** (Similar: Supplier analysis)
