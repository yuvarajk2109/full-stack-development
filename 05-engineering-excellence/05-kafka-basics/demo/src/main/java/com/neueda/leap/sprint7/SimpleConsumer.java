package com.neueda.leap.sprint7;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.TopicPartition;

import java.time.Duration;
import java.util.List;
import java.util.Properties;

// A REAL consumer, reading from the SAME real broker SimpleProducer wrote
// to. Run SimpleProducer first (or in another terminal), then this.
public class SimpleConsumer {

    public static void main(String[] args) {
        String topic = "trade-events";

        // Same remote Linux broker used by the producer.
        Properties props = new Properties();
        props.put("bootstrap.servers", "10.8.78.105:9092");
        props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("enable.auto.commit", "false");

        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props)) {
            // Keep the demo deterministic: read directly from partition 0.
            List<TopicPartition> partitions = List.of(new TopicPartition(topic, 0));
            consumer.assign(partitions);
            // Replay from the beginning each run so messages are always visible.
            consumer.seekToBeginning(partitions);

            System.out.println("Assigned partitions=" + partitions);
            System.out.println("Consumer polling for up to 30 seconds...");
            long deadline = System.currentTimeMillis() + 30_000;
            int received = 0;
            while (System.currentTimeMillis() < deadline) {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(500));
                for (ConsumerRecord<String, String> record : records) {
                    System.out.printf("Received partition=%d offset=%d key=%-7s value=%s%n",
                            record.partition(), record.offset(), record.key(), record.value());
                    received++;
                }
                if (received >= 5) break; // this demo only produced 5 events
            }
            System.out.println("Consumer finished - received " + received + " events.");
        }
    }
}
