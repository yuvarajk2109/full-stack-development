# Day 3 Part 2

## Choosing the Right Store

### Scenario 1: Session Storage for PaySprint Mobile

Every time a customer logs in, the app needs to store a session token and check it on every subsequent request, for as long as tens of thousands of customers are logged in at once, with lookups needing to complete in a few milliseconds. Sessions expire automatically.

**Chosen store type:** Key Value Pair

**Justification:** Session storage stores specific data, like a JWT token or user info, like their name. This requires fast, instant access that is only possible via a key-value store.

**What goes wrong with a different choice?**
RDBMS - this data requires fast access and by definition making a server call and a DB connection and querying a DB is significantly slower than instant session storage access via key-value pair.
Document Store - this is overkill for the requirement as Document Store is meant to capture more varied data, whereas Key Value pair satisfies the requirements with its simplicity.
Columnar Store - this is for huge data insertion, session storage for quick data fetch.

---

### Scenario 2: Market-Data Ingestion Pipeline (Price Ticks)

An external feed pushes millions of individual price ticks per second, across thousands of instruments, each tick just a timestamp, an instrument ID, and a price. The main access pattern is "give me instrument X's price history over this time range," almost never "give me everything about this one tick alongside a dozen other related facts."

**Chosen store type:** Columnar

**Justification:** Insertion of huge volume of data - perfect for columnar. And access is only for one particular column essentially, which is exactly how columnar stores and accesses data.

**What goes wrong with a different choice?**
RDBMS - possible, but infeasible and inefficient as it reads all rows and only then fetches required columns.
Key Value Store - Not feasible to maintain a large value of pairs.
Document Store - again, possible, but doesn't make sense to store such large, column oriented data 

---

## Scenario 3: Client Financial Goals Feature

Clients can set up personal financial goals (e.g. "save for a house deposit," "retirement planning," "children's education"), and each type of goal captures genuinely different details: a house deposit goal needs a target amount and a target date; a retirement goal needs a target retirement age and expected monthly income; an education goal needs a number of years and an estimated annual cost. New goal types get added periodically as the product evolves.

**Chosen store type:** Document Type Store

**Justification:** Each client has a different goal, a different description, and it is ideal to highlight them under a separate category, which is possible only with a Document Type Store.

**What goes wrong with a different choice?**
RDBMS - lot of redundancy or requirement to simplify into a meaningless column.
Key Value Pair - not the same key for every client, and thus doesn't work.
Columnar - similar problem to RDBMS, more redundant columns introduced to satisfy the requirements of each client.

---

## Extension: Could scenario 1 work in Postgres?

While slower, it is possible to do so in Postgres with an indexed table that maintains the user_id and their active jwt_token from which we validate.