# Module 5 Demo Guide - Remote Kafka + Java Producer/Consumer

This is a minimal, reliable demo using one Kafka broker running in Docker on a remote Linux machine.
The Java code in this project connects to that remote broker at PRIVATE_IP:9092.

## 1) Launch Kafka on the Linux Machine

Run this on the Linux host (replace PRIVATE_IP with your Linux machine private IP address):

```bash
docker run -d --name kafka -p 10.8.78.105:9092:9092 \
  -e KAFKA_NODE_ID=1 \
  -e KAFKA_PROCESS_ROLES=broker,controller \
  -e KAFKA_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://10.8.78.105:9092 \
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

Optional quick checks on Linux:

```bash
docker ps
docker logs kafka --tail 50
```

Topic creation:

- Kafka can auto-create a topic on first produce/consume if `auto.create.topics.enable=true`.
- For this demo, creating the topic explicitly is recommended because it guarantees the name and partition count.

Create the demo topic once (recommended):

```bash
docker exec kafka /opt/kafka/bin/kafka-topics.sh --create \
  --topic trade-events --bootstrap-server 10.8.78.105:9092 \
  --partitions 1 --replication-factor 1
```

```bash
docker exec kafka /opt/kafka/bin/kafka-topics.sh --create \
  --topic trade-events --bootstrap-server localhost:9092 \
  --partitions 1 --replication-factor 1
```

If the topic already exists, that is fine.

## 2) Run the Java Demo from This Project (Windows)

From this project folder:

```powershell
mvn -q -DskipTests compile
```

Run producer:

```powershell
mvn -q exec:java "-Dexec.mainClass=com.neueda.leap.sprint7.SimpleProducer"
```

Run consumer:

```powershell
mvn -q exec:java "-Dexec.mainClass=com.neueda.leap.sprint7.SimpleConsumer"
```

Notes:

- In PowerShell, keep `-Dexec.mainClass=...` inside quotes.
- Producer should print sent records with partition/offset.
- Consumer should print received records from `trade-events`.

## Current Demo Behavior

- Producer sends 5 trade messages to topic `trade-events`.
- Consumer manually reads partition `0` and seeks to the beginning.
- Because it seeks to beginning, rerunning consumer can show older messages too.
