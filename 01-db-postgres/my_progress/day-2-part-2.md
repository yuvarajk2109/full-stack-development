# Day 2 Part 2 - DB Design

## Entities and Relationships
From messy-flat-file.csv:

### 1. Examples of Redundancy in the Flat File
```
a. instrument_ticker determines instrument_name, yet we have both the details in one table.
b. model_portfolio_name and instrument_ticker determine target_weight_pct.
```

### 2. First Normal Form (1NF)
Does the flat file satisfy 1NF? Justify your answer. What would a 1NF violation have looked like instead?
```
Yes, the file does satisfy 1NF, all values are atomic. A 1NF violation would have maybe looked like this:

Client Name: A
Advisor Names: B, C wherein B and C are different advisors separated by commas.
```

### 3. Second Normal Form (2NF) - Removing Partial Dependencies
What is the flat file's implicit composite key?

```
client_name and client_advisor determine subscribed_date.
model_portfolio_name and instrument_ticker determine target_weight_pct.
```

Partial dependencies found (columns that depend on only part of the composite key):
```
client_name alone can determine subscribed_date. client_advisor is not needed to determine it.
So, separate client_name and subscribed_date into an entity.
And client_name and client_advisor into another entity.
```

### 4. Third Normal Form (3NF) - Removing Transitive Dependencies
Transitive dependencies found (non-key column depending on another non-key column):
```
model_portfolio_name and instrument_ticker determine target_weight_pct, and can be brought to a separate entity.
instrument_ticker determines instrument_name, and can be separated as well.
```

### 5. Final Table List (3NF)
Clients --> client_name, subscribed_date
Client_Advisor --> client_name, client_advisor
Model_Portfolio --> model_portfolio_name, instrument_ticker, target_weight_pct
Instrument --> instrument_ticker, instrument_name