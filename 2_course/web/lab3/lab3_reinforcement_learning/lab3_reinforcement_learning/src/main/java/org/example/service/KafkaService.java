package org.example.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Named;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;

import java.math.BigDecimal;
import java.time.Duration;
import java.util.Collections;
import java.util.Properties;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicReference;

@Named("kafkaService")
@ApplicationScoped
public class KafkaService {

    private static final String DEFAULT_BOOTSTRAP_SERVERS = "localhost:9092";
    private static final String STATE_TOPIC = "rl_state_in";
    private static final String ACTION_TOPIC = "rl_action_out";

    private final ObjectMapper mapper = new ObjectMapper();
    private KafkaProducer<String, String> producer;
    private KafkaConsumer<String, String> consumer;
    private ExecutorService executor;
    private final AtomicReference<BigDecimal> recommendedRadius = new AtomicReference<>(BigDecimal.valueOf(3));

    @PostConstruct
    public void init() {
        String bootstrap = System.getenv().getOrDefault("KAFKA_BOOTSTRAP_SERVERS", DEFAULT_BOOTSTRAP_SERVERS);

        Properties producerProps = new Properties();
        producerProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrap);
        producerProps.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        producerProps.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        producer = new KafkaProducer<>(producerProps);

        Properties consumerProps = new Properties();
        consumerProps.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrap);
        consumerProps.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        consumerProps.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        consumerProps.put(ConsumerConfig.GROUP_ID_CONFIG, "java-backend-rl");
        consumerProps.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "latest");
        consumer = new KafkaConsumer<>(consumerProps);
        consumer.subscribe(Collections.singletonList(ACTION_TOPIC));

        executor = Executors.newSingleThreadExecutor(r -> {
            Thread t = new Thread(r, "kafka-action-consumer");
            t.setDaemon(true);
            return t;
        });
        executor.submit(this::consumeLoop);
    }

    public void sendState(int hitsLast10, BigDecimal currentRadius) {
        if (producer == null) return;
        try {
            ObjectNode node = mapper.createObjectNode();
            node.put("hits_last_10", hitsLast10);
            node.put("current_radius", currentRadius);
            String payload = mapper.writeValueAsString(node);
            producer.send(new ProducerRecord<>(STATE_TOPIC, null, payload));
        } catch (Exception e) {
            System.err.println("Failed to send state to Kafka: " + e.getMessage());
        }
    }

    public BigDecimal getRecommendedRadius() {
        return recommendedRadius.get();
    }

    private void consumeLoop() {
        while (!Thread.currentThread().isInterrupted()) {
            try {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofSeconds(1));
                for (ConsumerRecord<String, String> record : records) {
                    handleAction(record.value());
                }
            } catch (Exception e) {
                System.err.println("Kafka consume error: " + e.getMessage());
            }
        }
    }

    private void handleAction(String payload) {
        try {
            JsonNode node = mapper.readTree(payload);
            if (node.has("new_radius")) {
                double val = node.get("new_radius").asDouble();
                BigDecimal clamped = clampRadius(BigDecimal.valueOf(val));
                recommendedRadius.set(clamped);
            }
        } catch (Exception e) {
            System.err.println("Failed to parse action payload: " + e.getMessage());
        }
    }

    private BigDecimal clampRadius(BigDecimal value) {
        BigDecimal min = BigDecimal.ONE;
        BigDecimal max = BigDecimal.valueOf(5);
        if (value.compareTo(min) < 0) return min;
        if (value.compareTo(max) > 0) return max;
        return value.setScale(0, java.math.RoundingMode.HALF_UP);
    }

    @PreDestroy
    public void destroy() {
        try {
            if (producer != null) producer.close();
        } catch (Exception ignored) {
        }
        try {
            if (consumer != null) consumer.wakeup();
        } catch (Exception ignored) {
        }
        try {
            if (executor != null) executor.shutdownNow();
        } catch (Exception ignored) {
        }
    }
}
