# Module 6 Lab — Designing a Kafka Pipeline for Trade Events

## Objectives

By the end of this lab you will have:

- Produced a written design for the mission's real Kafka pipeline — topic(s), partition key,
  partition count, and consumer groups
- Justified every design decision against a concrete downstream requirement, not guesswork

## Format

A design document. No code — Module 9 is where this gets built.

## The Mission's Requirements

Sprint 6's trading platform accepts orders and executes trades. Starting this sprint, every
executed trade must also be published as an event, because four downstream systems now need to
react to trades without polling the mission service directly:

- **Settlement** — needs every trade, and for any given account, needs them in the order they
  happened (a SELL must never be seen as happening before its BUY).
- **The risk dashboard** — needs every trade, needs each account's own trades in order, but
  doesn't care about ordering across different accounts.
- **The compliance audit log** — needs every trade, doesn't care about ordering at all, just a
  complete record.
- **A new fraud-detection service** (added this sprint) — needs every trade for a given account,
  in order, within a few seconds of it happening, to catch suspicious patterns (e.g. rapid
  buy-sell-buy cycles on the same ticker).

## Task

### Part A — Topic Design

1. How many topics does this pipeline need? Justify your answer against the four systems above —
   don't default to "one topic" or "one topic per consumer" without reasoning through it.

`All the components of the pipeline - Settlement report, risk dashboard, compliance audit log, and the fraud detection service - 
need essentially the same topic, as they all consume the same data in different forms. So the topic remains the same.`

2. Name the topic(s).

`trade-events`

### Part B — Partition Key

1. Choose a partition key. Name it, and explain specifically why it satisfies Settlement, the
   risk dashboard, and fraud detection simultaneously.

`One partition key for all. Chosen key is accountId. It satisfies Settlement and risk dashboard,
both of which require a particular account's trades to be viewed in order, which can only be achieved by putting
all trades of an account in the same partition, achieved by the unique identifier that is accountId. 
Compliance Audit Log just needs every trade, so any partition handles that, and the fraud-detection service as well
requires trade for an account in order, which this partition key satisfies.`


2. Explain why `eventId` (a unique ID generated per trade) would be the wrong choice, using the
   demo's evidence, not just "it feels wrong."

`eventId is generated uniquely for a trade. Let us prove why it fails the account trades in order requirement 
 via one simple example. Consider trade 1 by acc-101 and trade 2 by acc-101, both with a unique eventId. Now
 trade 1 enters a different partition from trade 2 because the partition happens via eventId. 
 Now account trades are no longer processed in order. So, clearly, eventId is the wrong choice.`

3. Is there a downstream requirement here that a single key CANNOT satisfy alongside the others?
   If yes, name it and explain the conflict. If no, explain why account-level ordering happens to
   cover every requirement in this scenario.

`There isn't a downstream requirement, so accountId as the single source/partition key should indeed suffice!`

### Part C — Partition Count & Consumer Groups

1. How many partitions would you start with, and what's the actual trade-off you're weighing
   (not "more is always better")?

`I think it depends on the number of accounts we have and the number of accounts we are expecting. 
We have to ensure that a single partition doesn't get too many accounts, but we also need to ensure that we don't add
an infinite number of partitions such that the design becomes something akin to 'one partition for one account', which is just incredibly inefficient.`

2. List the consumer groups this pipeline needs — one per system, or fewer? Justify.

`Since we have 4 different systems, 4 consumer groups makes sense.`

3. Fraud detection needs trades "within a few seconds." Does partition count or consumer group
   design affect that latency requirement at all? Why or why not?

`No - partition count and consumer group design control ordering and parallelism, not
latency.** Fraud detection's "within a few seconds" requirement is about how often/promptly
its consumer polls and processes, and how quickly a trade is produced and acknowledged — not
about how many partitions exist. A single-partition topic with a fast-polling consumer can meet
a latency target; a 50-partition topic with a consumer that only polls once a minute cannot.
This is worth flagging explicitly: partitioning is a design lever, not a substitute for actually
checking that a consumer runs often enough.`

## Deliverable

A short design document (half a page to a page) covering Parts A, B, and C, written as if it
will be handed to whoever implements Module 9 — specific enough that they don't have to guess.

## Acceptance criteria

- Topic design is justified against all four downstream systems, not asserted
- Partition key choice is justified with the SAME reasoning demonstrated in the demo (order is
  guaranteed only within a partition, only for a shared key)
- The eventId-as-key mistake is explicitly ruled out, with a reason
- Partition count and consumer group answers distinguish between what Kafka's design actually
  controls (ordering, parallelism) and what it doesn't (network/processing latency)
