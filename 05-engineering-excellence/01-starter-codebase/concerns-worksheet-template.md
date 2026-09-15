# Technical Debt Review — `TradeReportGenerator.java`

**Reviewers:**

## Concern 1

**Where:** Line 39, 40

```
catch (Exception e) {
// skip bad row
}
```

**What's the concrete cost or risk?**

```
Bad rows are skipped. This leads to missing entries in report.csv.
In this data of trades.csv, we have 12 records. 
Meanwhile, report.csv only has 10 records. 
So 2 unprocessed records silently disappear, leaving no trace.
At a larger scale, this is even more concerning as thousands of records are lost without reason.
```

## Concern 2

**Where:** TradeReportGenerator.java, the entire doIt() method.

**What's the concrete cost or risk?**

```
The entire process flow is dependent on one method. 
Different functionalities are not properly segregated.
This makes the function harder to understand and also fix.
It keeps a lot of dependencies instead of separating them logically and functionally.
```

## Concern 3

**Where:** TradeReportGenerator.java, pretty much all the variables.

**What's the concrete cost or risk?**

```
The variable names are bad. 
There are no comments as well to make us understand the logical flow of the doIt() method.
So any new developer would have to go through the whole method, which is already long, to understand it.
This is made worse if the only task of said developer was to just make one small fix for one small functionality.
```

## The Row-Count Question

`trades.csv` row count (excluding header):

Program's own reported count:

Do they match? If not, why not?

They don't. There is a count mismatch. This is because the Report Generator skips 'bad' rows.

## In One Sentence Each

What would make this codebase expensive to **extend**?

```
doIt() does everything. 
It is not properly separated by functionality, making it difficult to extend.
```
What would make this codebase expensive to **trust**?

```
Improper variable names. 
Difficult to map out and understand/trust the codebase.
``` 
