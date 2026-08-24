# Day 2 Part 1 - Advanced Queries

## Production-Grade Queries, Subqueries and CTEs

1. Scalar subquery: every BUY transaction with a price above the average BUY price.

Finding average:
```
SELECT AVG(price) from transactions where txn_type = 'BUY'
```

BUY > AVG BUY:
```
select account_id,  price as AMOUNT
from transactions
where txn_type = 'BUY'
and  price > (SELECT AVG(price) from transactions where txn_type = 'BUY');
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
```
SELECT * FROM (
	select account_id, sum(quantity * price) as total
	from transactions
	where txn_type = 'BUY'
	group by account_id
)
where TOTAL > (
 SELECT AVG(total) FROM (
	select account_id, sum(quantity * price) as total
	from transactions
	where txn_type = 'BUY'
	group by account_id
 )
)
```

5. Try task 3 again using a window function instead of a second aggregate pass.

```
SELECT * FROM (
	select account_id, sum(quantity * price) as total,
	avg(sum(quantity * price)) OVER() as avg_total
	from transactions
	where txn_type = 'BUY'
	group by account_id
) where total > avg_total
```

## Data Validation

raw_client_intake holds client applications exactly as they arrived: nobody has checked them yet. Write a query for each task below.

1. Missing data: find every row with a missing full_name or a missing date_of_birth.
```
SELECT * FROM raw_client_intake where full_name is NULL or date_of_birth is null 
```

2. Exact duplicates: find applications that are exact duplicates, same full_name, same date_of_birth, same email, submitted more than once.
```
select full_name, date_of_birth, email, count(*)
from raw_client_intake
group by full_name, date_of_birth, email
having count(*) > 1
```

3. Distinct values: list every distinct value present in risk_profile. How many actual underlying values do you think this represents?
```
select distinct risk_profile from raw_client_intake
```

Output
```
"balanced"
"cautious"
"adventurous"
"Balanced"
"Adventurous"
"Cautious"
"Moderate"
"ADVENTUROUS"
```

Semantically this is wrong. We have Adventurous, adventurous, and ADVENTUROUS, all of which point to the same thing but are instead stored as different values.

4. Invalid values: find rows whose risk_profile is invalid, that is, not Cautious, Balanced, or Adventurous once you account for casing. Careful, one of these values isn't a casing problem at all, it's not a real risk profile no matter how you normalise it.
```
select * from raw_client_intake where risk_profile NOT in ('Cautious', 'Balanced', 'Adventurous');
```

5. Whitespace: find rows where full_name has leading or trailing whitespace. This is invisible in a normal SELECT, think about how you'd prove it's there before you write the query.
```
select full_name, 
LENGTH(full_name) as full_length,
LENGTH(TRIM(full_name)) as actual_length
from raw_client_intake
where LENGTH(full_name) <> LENGTH(TRIM(full_name))
```

6. Referential consistency: find rows whose advisor_name doesn't match any real advisor in the advisors table. Reuse the LEFT JOIN ... WHERE ... IS NULL pattern from Module 04.
```
select advisor_name
from raw_client_intake
left join advisors
on LOWER(advisor_name) = LOWER(name)
where advisor_id is NULL
```

7. Classify the fix: for each category of issue above (missing, duplicate, inconsistent casing, invalid value, whitespace, referential), write one line saying whether it's safe to fix automatically, and if so how, or whether it needs a human decision, and why.
```
1: Missing Data, safe to fix automatically by adding constraints and marking fields as mandatory wherever required.
2: Duplicate Data, safe to fix automatically by deleting the duplicate record.
3: Inconsistent Casing, needs a human touch to define the enums/constants
4: Invalid Value, needs a human touch to understand what an invalid value is as per the requirements
5: Whitespace: safe to fix automatically, can simply TRIM()
6: Referential Inconsistency, needs a human touch to resolve minor inconsistences; alternatively, need to reference via proper keys.
```