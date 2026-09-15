# Module 4 Lab — Kafka Fundamentals: Topics, Producers, Consumers, Partitions, Offsets

## Objectives

By the end of this lab you will have:

- Matched every core Kafka term to a concrete piece of a real trade-event scenario
- Reasoned about partition key choice and its consequence for ordering, before writing any code

## Format

A guided worksheet. No code — Module 5 is hands-on with real Kafka.

## The Scenario

The mission's trading platform needs to tell downstream systems whenever a trade is executed.
Three systems care:

- **Settlement** needs every trade, and for any given account, needs them in the order they
  happened.
- **The risk dashboard** needs every trade, doesn't care about order across different accounts,
  but does need each account's own trades in order (a sell after a buy must be seen as after it).
- **The compliance audit log** needs every trade, and doesn't care about ordering at all — it's
  just building a complete historical record.

## Task

### Part A — Match the Terms

For each term, write **one sentence** naming the specific thing in this scenario it corresponds
to:

1. **Topic**
`Trade Events are the topic. Every trade essentially gets added to this topic. It is essentially a record/queue.`
2. **Producer**
`It takes a single trade event, finds the partition that it has to go into, and updates the offset.`
3. **Consumer**
`It can be either the Settlement consumer or Risk Dashboard consumer or Compliance Audit Log consumer, reading trade events.`
4. **Consumer group** 
`Three independent systems, each reading the whole topic, each tracking its own progress) — Essentially, each system gets the same data, but processes it in different ways due to the differing partitions.
It is a necessary reduplication of data.`
5. **Partition**
`
For Settlement, I think it should just be one partition.
For risk dashboard, partitions should be based on account ID.
For compliance audit log, which just needs each trade in any order, we can use any logic for partitioning that speeds up the process.
`
6. **Offset** —
`
Offset is necessary for each partition - so every event in a partition is always processed in order
`
### Part B — Choose a Partition Key

The mission's trading platform needs to decide what to use as the partition key for trade events.
Two candidates: **account ID**, or **ticker**.

1. Given Settlement's requirement above, which key satisfies it, and why?
`It has to be accountId, as the requirement is that for any given account, it needs the trades in the order that they happened.`
2. Is there a key choice that would satisfy Settlement's ordering requirement AND still spread
   events across multiple partitions (rather than everything landing in one partition)? Explain
   your reasoning — don't just name a key, justify it against what "same key = same partition"
   actually guarantees. 
`It doesn't depend on just the key. We of course choose the accountId as partition key - this means that all the trades for an account
will always end up in the same partition, and since the producer actually processes trade data in the order that they come in, we implicity ensure
that the trades are in the proper order as well.`
3. The risk dashboard and the compliance log both consume the *same* topic as Settlement. Does
   the partition key chosen for Settlement's benefit cause either of them a problem? Why or why
   not?
`Not necessarily. In fact, it's a good thing for the risk dashboard which alse needs account-wise trade orders, and compliance log just needs all data, so the order in which data is received for that doesn't matter.`

### Part C — Offsets in Practice

Settlement's consumer crashes after processing offset 47 in partition 2, and restarts five
minutes later.

1. What does Settlement need to have stored *before* the crash, to pick up correctly where it
   left off?
`Just the partition and the offset, which any Consumer implicitly stores. This is why we have both partition and offset.`
2. If Settlement had NOT stored that, what are the two possible failure modes it could hit on
   restart? Name both, specifically.
`The consumer would have to reprocess the same data, or it might skip some data - both of which are bad.`

## Deliverable

Your answers to Parts A, B, and C.

## Acceptance criteria

- Part A's six answers are specific to this scenario, not textbook definitions
- Part B correctly identifies that ordering is guaranteed only per-key, and reasons about whether
  a single key can serve multiple consumers' needs
- Part C names both failure modes (reprocessing already-handled trades, or skipping unprocessed
  ones) explicitly, tied to what "offset" actually tracks
