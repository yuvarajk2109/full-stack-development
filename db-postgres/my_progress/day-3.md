# Day 3

## Structured Problem Solving

> "Can we get a way to see which of our clients have drifted significantly from their model
> portfolio? We keep finding out about this too late."

---

## 1. Clarifying Questions and Assumptions

```
Question: What is the actual measure of a significant drift?
Assumption: 5% is considered as a significant drift.
```

```
Question: What is the minimum value for target weight percentage? Is it portfolio-based or a fixed universal value?
Assumption: It is portfolio based and depends on the portfolio.
```

```
Question: Are we categorising portfolios into high risk, low risk, etc.?
Assumption: We could do that - put a risk profile to each portfolio. Can potentially just add an atrribute.
```

```
Question: What really is drift, when does it happen, is it manual or automatic?
Assumption: It has to be automatic, at least detection of drift has to be automatic or something that should be triggered when the current value changes. 
```

```
Question: Does drift correspond to the client changing their portfolio, or the portfolio itself changing its value?
Assumption: The assumption we are making is that drift is something that happens when a portfolio value / market changes and that affects the client's holding. Another assumption is that the client himself shifts / alters his portfolio holdings, which automatically causes an intentional/explicit drift.
```

---

## 2. Entities and Data Needed

| Table | Columns Used | Why |
|-------|--------------|-----|
| Client  | client_id, name, email, password | Store of client details  |
| Model Portfolio | portfolio_id, name, risk_value | Store of portfolio details |
| Instruments | instrument_ticker, name | Store of instrument details |
| Portfolio Target | portfolio_id, version_id, target_weight_pct, effective_from, instrument_id | Latest portfolio details |
| Portfolio Version | portfolio_id, version_id, targert_weight_pct, effective_from, effective_to | History/Log Table of portfolio details |
| Client Holdings | client_id, instrument_id |
| Client Portfolio | client_id, portfolio_id |
---

## 3. Modelling Changes

Does anything need to be added to the schema, or is this answerable with the tables you
already have?

SO all the data that is required is present in the schema, but not directly answerable via a simple select query. There needs to be computation between past and present portfolios to calculate drift, which the schema does support.

---

## 4. Approach (Plain English)

Drift, when happens, has to trigger/interrupt the backend/DB. When done so, we trigger a computation that performs the necessary calculations to calculate the drift percentage for each client based on their different portfolio holdings. 

This calculation happens as a scheduled batch job, synchronising with when the portfolio holdings themselves change.

---

## 5. Validation Sentence for Compliance

We are triggering/performing this computation whenever the portfolio updates.

---

## Bonus: Draft SQL (Extension Task)

```
Simply the addition of risk profile attribute and a potential significant drift percentage for each specific portfolio.
```