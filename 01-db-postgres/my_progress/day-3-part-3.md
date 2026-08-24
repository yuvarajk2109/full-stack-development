# Day 3 Part 3

## Snowflake Exploration

## 1. **Find the sample data**: switch to the `SNOWFLAKE_SAMPLE_DATA` database and the `TPCH_SF1` schema. List its tables.

```
USE DATABASE snowflake_sample_data;
USE SCHEMA tpch_sf1;
SHOW TABLES;
```

## 2. **Run a simple query**: select the first 10 rows from the `CUSTOMER` table.

```
SELECT * FROM CUSTOMER LIMIT 10;
```

## 3. **Run an aggregated query**: count customers by market segment (`c_mktsegment`), ordered from most to fewest.

```
SELECT c_mktsegment, COUNT(*) as TOTAL_COUNT
FROM CUSTOMER
GROUP BY c_mktsegment
ORDER BY c_mktsegment DESC;
```

## 4. **A join**: find the total order value (`SUM(o_totalprice)`) per customer market segment, by joining `CUSTOMER` and `ORDERS`. 

```
SELECT c_mktsegment, SUM(o_totalprice)
FROM CUSTOMER c
INNER JOIN ORDERS o
ON c.c_custkey = o.o_custkey
GROUP BY c_mktsegment
ORDER BY c_mktsegment DESC;
```

## 5. **Compare the experience**: write a short comparison of using Snowflake's Snowsight interface versus `psql`/pgAdmin for the same kind of exploration you did in Module 02. What felt similar? What felt different?

- The query editors felt pretty similar in some aspects yet pretty different as well.
- Snowflake provides visualizations other than just a table - it provides graphical visualizations, the option to use a pivot table like in Excel, all of which speak to its OLAP capabilities. These are either not even available in pgAdmin or are available but haven't been explored by me/is difficult to find or understand in pgAdmin.
- Querying itself felt similar because of the sample data - there wasn't much historical data.

## 6. **Reflect on trade-offs**: in two or three sentences, explain what you'd gain and what you'd give up if PaySprint Wealth moved its transaction reporting into a warehouse like this, instead of querying the live OLTP database directly.

- Separation of transaction and analytics, providing higher availability and lower downtime for real-time transactions.
- An analytics-specific warehouse is faster as it is purposefully made for that specific job.
- We incur additional costs and storage in keeping a copy of data or moving data from the actual database to the Snowflake warehouse.