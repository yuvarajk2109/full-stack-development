# Day 2

## Production-Grade Queries, Subqueries and CTEs

1. Scalar subquery: every BUY transaction with a price above the average BUY price.

Finding average:
```
SELECT AVG(quantity * price) from transactions where txn_type = 'BUY'
```

BUY > AVG BUY:
```
select account_id, quantity * price as AMOUNT
from transactions
where txn_type = 'BUY'
and quantity * price > (SELECT AVG(quantity * price) from transactions where txn_type = 'BUY');
```

2. Correlated subquery: every account alongside the date of its most recent transaction.
Explain in one sentence why this subquery has to run once per account.

```
SELECT account_id, 
(SELECT MAX(txn_date) from transactions t where t.account_id = account_id) as latest_txn_date
from ACCOUNTS;
```

3. CTE: clients whose total BUY value is above the average total BUY value.
```
with client_buy_totals AS (
	select account_id, sum(quantity * price) as total
	from transactions
	where txn_type = 'BUY'
	group by account_id
)
select * from client_buy_totals where total > (SELECT AVG(total) from client_buy_totals);
```

4. Same result as task 3, using a derived table instead of a CTE. Compare readability with your partner.


Finish early: try task 3 again using a window function instead of a second aggregate pass.