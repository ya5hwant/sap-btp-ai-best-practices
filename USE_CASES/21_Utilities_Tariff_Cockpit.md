# USE CASE 21: Utilities Tariff Mapping Cockpit

## Quick Summary
React-based cockpit for managing utility tariffs. Map tariff structures to company billing systems. Track rate changes. Alert on optimization opportunities.

---

## Customer Pain Point

**What you'd hear:**
"We have contracts with multiple utility suppliers. Rates change quarterly. We need centralized tracking of all rates and automatic alerts when better options become available."

**Business Impact:**
- Current tracking: Scattered emails, spreadsheets
- Missed opportunities: 5-10 better deals per year
- Potential savings: €200k+/year

---

## Your Approach

### Phase 1: Tariff Master Data
"Build tariff database:

```
- Supplier, tariff name, effective date
- Rate structure (fixed/variable/tiers)
- Surcharges, discounts
- Contract terms (duration, lock-in)
```"

### Phase 2: React Cockpit UI
"Dashboard showing:

```
- All active tariffs (visual table)
- Rate change alerts
- Savings opportunities
- Comparison tools
- Contract renewal dates
```"

### Phase 3: Rate Change Monitoring
"Alert when:

```
- Rates increase (review terms)
- Better deal available (evaluate switch)
- Contract renewal approaching (renegotiate)
- Competitor offers better rate
```"

### Phase 4: Optimization Engine
"Calculate savings:

```
Current spend: €500k/year
Competitor A: €480k/year (saves €20k)
Competitor B: €465k/year (saves €35k)

Switch cost: €5k (exit current, setup new)
Net benefit: €30k/year
Payback: 2 months
```"

---

## Implementation

```typescript
// React component for tariff cockpit
import React, { useState } from 'react';

const TariffCockpit = () => {
  const [tariffs, setTariffs] = useState([]);
  const [savings, setSavings] = useState(null);

  useEffect(() => {
    // Load tariffs from API
    fetch('/api/tariffs')
      .then(r => r.json())
      .then(data => setTariffs(data));
  }, []);

  const calculateSavings = () => {
    const current_cost = tariffs
      .filter(t => t.is_active)
      .reduce((sum, t) => sum + t.annual_cost, 0);

    const best_alternative = Math.min(
      ...tariffs.map(t => t.annual_cost)
    );

    setSavings(current_cost - best_alternative);
  };

  return (
    <div className="cockpit">
      <h1>Utility Tariff Cockpit</h1>
      
      <div className="metrics">
        <Metric label="Annual Spend" value={totalSpend} />
        <Metric label="Savings Opportunity" value={savings} />
        <Metric label="Contract Renewals" value={renewalCount} />
      </div>

      <table>
        <tr>
          <th>Supplier</th>
          <th>Annual Cost</th>
          <th>Valid Until</th>
          <th>Status</th>
        </tr>
        {tariffs.map(t => (
          <tr key={t.id}>
            <td>{t.supplier}</td>
            <td>{t.annual_cost}</td>
            <td>{t.valid_until}</td>
            <td>{t.is_active ? '✓ Active' : '○ Backup'}</td>
          </tr>
        ))}
      </table>

      <button onClick={calculateSavings}>Calculate Savings</button>
    </div>
  );
};

export default TariffCockpit;
```

---

## Success Metrics

- Tariff visibility: 100% (all tracked)
- Savings identified: €200k+/year
- Alert latency: <1 day for opportunities
- Switch time: Reduced 50%

---

## Related Use Cases

- **Utilities Rate Compare** (Similar: Rate comparison, different UI)
