# Day 1 - Setup and Foundational Queries

## Start Postgres and Switch to DB

In Windows CMD,

```
psql -U postgres -h localhost
n3u3d4!
```

Create and Switch to DB

```
CREATE DATABASE paysprint_wealth;
\c paysprint_wealth
```

Load Enterprise Schema
```
\i {{ PATH TO enterprise-schema.sql }}
```

## Basic Queries Against the Enterprise Schema

1. List every client's name and risk profile.
```
select name, risk_profile from clients;
```

2. List the names of all clients with a "Cautious" risk profile.
```
select name, risk_profile from clients where risk_profile = 'Cautious';
```

3. List all clients who joined before 2018-01-01, ordered by join date, oldest first.
```
 select * from clients where joined_date < '2018-01-01' order by joined_date desc;
```

4. List all clients with a risk profile of either "Cautious" or "Adventurous".
```
select name, risk_profile from clients where risk_profile in ('Cautious', 'Adventurous');
```
5. Same query using OR instead of IN.
```
 select name, risk_profile from clients where risk_profile = 'Cautious' or risk_profile = 'Adventurous';
```

6. List the name and date of birth of every client born in the 1980s.
```
 select name, date_of_birth from clients where date_of_birth >= '1980-01-01' AND date_of_birth < '1990-01-01';
```

7. List every instrument's ticker and name, ordered alphabetically by name.
```
select ticker, name from instruments order by name;
```

8. List all transactions of type 'DIVIDEND', most recent first.
```
select * from transactions where txn_type = 'DIVIDEND' order by txn_date desc;
```

9. Find every transaction that has no associated instrument (instrument_id IS NULL).
```
select * from transactions where instrument_id IS NULL;
```

10. List the distinct list of account types that actually exist in the accounts table.
```
select DISTINCT account_type from accounts;
```

11. List every client along with their date of birth, only for clients whose DOB is not null.
```
 select name, date_of_birth from clients where date_of_birth IS NOT NULL;
 ```

 ## Joins and Aggregation

Module 04 Lab: Joins and Aggregation Against the Enterprise Schema
NOTE: Nadia Farouk (client 11) is already in the schema with no accounts.

1. INNER JOIN: list every client's name alongside their advisor's name.
```
select c.name, a.name from clients c inner join advisors a on c.advisor_id = a.advisor_id;   
```

2. LEFT JOIN: list every client's name alongside any account they have.
Confirm Nadia Farouk appears with NULL account columns.
```
 select c.client_id, c.name, account_id, account_type, opened_date, currency from clients c left join accounts a on c.client_id = a.client_id;
```

3. Rewrite 2a as an INNER JOIN and confirm Nadia Farouk disappears. Why?
```
select c.client_id, c.name, account_id, account_type, opened_date, currency from clients c inner join accounts a on c.client_id = a.client_id;
```

4. Three-table join: account ID and type, client name, advisor name.
```
select a.account_id, a.account_type, c.name, ad.name from clients c inner join accounts a on c.client_id = a.client_id inner join advisors ad on c.advisor_id = ad.advisor_id;
```

5. GROUP BY: for each advisor, count how many clients they manage.
```
 select a.name, count(c.name) as NO_OF_CLIENTS from advisors a inner join clients c on a.advisor_id = c.advisor_id group by a.name;
```

6. HAVING: advisors managing three or more clients.
```
 select a.name, count(c.name) as NO_OF_CLIENTS from advisors a inner join clients c on a.advisor_id = c.advisor_id group by a.name having count(c.name) >= 3;
```

7. Total value of all BUY transactions per account, highest first.
```
SELECT account_id, SUM(quantity * price) 
FROM transactions
WHERE txn_type = 'BUY'
GROUP BY account_id
ORDER BY SUM(quantity * price) DESC;
```

8. Window function: client name and join date, with RANK() by join date.
```
select name, joined_date, RANK() over (ORDER BY joined_date)
FROM clients;
```