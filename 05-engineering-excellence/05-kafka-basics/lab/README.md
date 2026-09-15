# Module 5 Lab — Hands-on: Standing Up Kafka & Producing/Consuming Messages

## Objectives

By the end of this lab you will have:

- Stood up your own Kafka broker in Docker and created your own topic
- Written a real producer that sends keyed events to that broker
- Written a real consumer that reads them back and confirms Module 4's ordering guarantee
  against genuine infrastructure, not a simulation

## Setup

Stand up the broker on the Linux host (skip if the demo broker is already running there):

Replace `PRIVATE_IP` with your own Linux machine private IP address in the commands below.

```bash
docker run -d --name kafka -p PRIVATE_IP:9092:9092 \
  -e KAFKA_NODE_ID=1 \
  -e KAFKA_PROCESS_ROLES=broker,controller \
  -e KAFKA_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://PRIVATE_IP:9092 \
  -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT \
  -e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER \
  -e KAFKA_CONTROLLER_QUORUM_VOTERS=1@127.0.0.1:9093 \
  -e KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT \
  -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
  -e KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1 \
  -e KAFKA_TRANSACTION_STATE_LOG_MIN_ISR=1 \
  -e CLUSTER_ID=4L6g3nShT-eMCtK--X86sw \
  apache/kafka:latest
```

Run these topic commands on the Linux host too:

Create the topic this lab uses:

```bash
docker exec kafka /opt/kafka/bin/kafka-topics.sh --create \
  --topic settlement-events --bootstrap-server localhost:9092 \
  --partitions 3 --replication-factor 1
```

Confirm it exists:

```bash
docker exec kafka /opt/kafka/bin/kafka-topics.sh --describe \
  --topic settlement-events --bootstrap-server localhost:9092
```

Run the Java commands in this lab from Windows.

## The Scenario

Settlement events, keyed by account ID, need to reach a downstream consumer in the order they
were produced, per account — same requirement Module 4's worksheet reasoned about.

## Task

### Part A — `SimpleProducer`

Open `src/main/java/com/neueda/leap/sprint7/SimpleProducer.java` and complete the three TODOs:

1. Build a `Properties` object with `bootstrap.servers`, `key.serializer`, and `value.serializer`.
2. Build a `ProducerRecord` for topic `settlement-events`, keyed by `accountId`, with the given
   value.
3. Send it, `.get()` the result so the send is confirmed before moving on, and print the
   partition and offset the broker assigned.

Run it:

```bash
mvn compile
mvn dependency:build-classpath -Dmdep.outputFile=cp.txt
java -cp "target/classes;$(cat cp.txt)" com.neueda.leap.sprint7.SimpleProducer
```

Until you implement it, running the producer throws immediately — that's expected. It's
verifying it fails loudly, not silently, before you've filled anything in.

### Part B — `SimpleConsumer`

Open `SimpleConsumer.java` and complete the three TODOs:

1. Build a `Properties` object with `bootstrap.servers`, `key.deserializer`/`value.deserializer`,
   `group.id`, and `auto.offset.reset`.
2. Subscribe to the `settlement-events` topic.
3. Poll for records and, for each one, print its partition, offset, key, and value, incrementing
   `received`.

Run it:

```bash
java -cp "target/classes;$(cat cp.txt)" com.neueda.leap.sprint7.SimpleConsumer
```

## Deliverable

A working producer/consumer pair. Run the consumer, then check: do ACC-001's events (both in the
same partition) appear in production order? Does the same hold for ACC-002?

## Acceptance criteria

- Producer sends all 5 events and prints the broker-assigned partition/offset for each
- Consumer reports "received 5 events"
- Events sharing a key arrive in production order (verifiable directly from the printed offsets)
