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

-- 1. List every client's name and risk profile.
```
select name, risk_profile from clients;
```

-- 2. List the names of all clients with a "Cautious" risk profile.
```
select name, risk_profile from clients where risk_profile = 'Cautious';
```

-- 3. List all clients who joined before 2018-01-01, ordered by join date, oldest first.
```
 select * from clients where joined_date < '2018-01-01' order by joined_date desc;
```

-- 4. List all clients with a risk profile of either "Cautious" or "Adventurous".
```
select name, risk_profile from clients where risk_profile in ('Cautious', 'Adventurous');
```

-- 4b. Same query using OR instead of IN.
```
 select name, risk_profile from clients where risk_profile = 'Cautious' or risk_profile = 'Adventurous';
```

-- 5. List the name and date of birth of every client born in the 1980s.
```
 select name, date_of_birth from clients where date_of_birth >= '1980-01-01' AND date_of_birth < '1990-01-01';
```

-- 6. List every instrument's ticker and name, ordered alphabetically by name.
```
select ticker, name from instruments order by name;
```

-- 7. List all transactions of type 'DIVIDEND', most recent first.
```
select * from transactions where txn_type = 'DIVIDEND' order by txn_date desc;
```

-- 8. Find every transaction that has no associated instrument (instrument_id IS NULL).
```
select * from transactions where instrument_id IS NULL;
```

-- 9. List the distinct list of account types that actually exist in the accounts table.
```
select DISTINCT account_type from accounts;
```

-- 10. List every client along with their date of birth, only for clients whose DOB is not null.
```
 select name, date_of_birth from clients where date_of_birth IS NOT NULL;
 ```

 ## 