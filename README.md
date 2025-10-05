# Event-Driven Architecture with Kafka & Spring Cloud Stream

![Java](https://img.shields.io/badge/Java-17+-orange.svg)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.x-brightgreen.svg)
![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-3.x-black.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A comprehensive demonstration of event-driven architecture using Apache Kafka and Spring Cloud Stream. This project showcases real-time data processing, stream analytics, and microservices communication through asynchronous events.

<img width="1319" height="910" alt="Image" src="https://github.com/user-attachments/assets/d3783187-368b-4149-9748-087f8b81c87a" />

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Key Features](#key-features)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
  - [Option 1: Manual Kafka Installation](#option-1-manual-kafka-installation)
  - [Option 2: Docker Setup](#option-2-docker-setup)
  - [Option 3: KRaft Mode](#option-3-kraft-mode-without-zookeeper)
- [Service Components](#service-components)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [API Documentation](#api-documentation)
- [Real-Time Analytics](#real-time-analytics)
- [Web Dashboard](#web-dashboard)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Contributing](#contributing)
- [Resources](#resources)

---

## 🎯 Overview

This project demonstrates a production-ready implementation of event-driven architecture featuring:

- **Producer Service**: REST API for publishing events to Kafka
- **Consumer Service**: Processes events and executes business logic
- **Supplier Service**: Auto-generates events for testing and simulation
- **Analytics Service**: Real-time stream processing with Kafka Streams
- **Web Dashboard**: Live visualization of analytics data

### What You'll Learn

- Setting up Apache Kafka (3 different methods)
- Building microservices with Spring Cloud Stream
- Implementing event producers, consumers, and suppliers
- Real-time data analytics with Kafka Streams
- Creating live dashboards with Server-Sent Events (SSE)
- Best practices for event-driven systems

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Event-Driven Architecture                     │
│                                                                  │
│  ┌────────────┐       ┌──────────────┐       ┌──────────────┐  │
│  │   Client   │──────▶│   Producer   │──────▶│    Kafka     │  │
│  │  (REST)    │       │   Service    │       │   Broker     │  │
│  └────────────┘       │  Port: 8081  │       │  Port: 9092  │  │
│                       └──────────────┘       └──────┬───────┘  │
│                                                     │           │
│                        ┌────────────────────────────┘           │
│                        │                                        │
│         ┌──────────────┼──────────────┬─────────────┐          │
│         │              │              │             │          │
│         ▼              ▼              ▼             ▼          │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐  ┌──────────┐    │
│  │ Consumer │   │ Supplier │   │Analytics │  │Dashboard │    │
│  │ Service  │   │ Service  │   │ Service  │  │ Service  │    │
│  │Port: 8082│   │Port: 8083│   │Port: 8084│  │Port: 8085│    │
│  └──────────┘   └──────────┘   └──────────┘  └──────────┘    │
│   Processes      Generates       Aggregates    Visualizes     │
│   events         events           statistics   real-time      │
└─────────────────────────────────────────────────────────────────┘
```

### Component Interactions

1. **Client** → Sends HTTP requests to Producer Service
2. **Producer** → Publishes events to Kafka topics
3. **Kafka** → Distributes events to all subscribers
4. **Consumer** → Processes events and executes business logic
5. **Supplier** → Auto-generates test events every second
6. **Analytics** → Performs real-time aggregations and computations
7. **Dashboard** → Displays live analytics via WebSocket/SSE

---

## ✨ Key Features

### Event-Driven Benefits
- **Loose Coupling**: Services communicate through events, not direct calls
- **Scalability**: Each service can scale independently
- **Resilience**: Failure in one service doesn't affect others
- **Flexibility**: Easy to add new consumers without changing producers
- **Audit Trail**: Complete history of all events

### Technical Features
- ✅ Multiple Kafka setup options (Manual, Docker, KRaft)
- ✅ Spring Cloud Stream functional programming model
- ✅ Real-time stream processing with Kafka Streams
- ✅ Automatic event generation for testing
- ✅ Live analytics dashboard with SSE
- ✅ Comprehensive error handling and retry logic
- ✅ Production-ready configurations
- ✅ Docker Compose for easy deployment

---

## 🛠️ Technologies

### Core Stack
- **Java 17+** - Modern Java features
- **Spring Boot 3.2** - Application framework
- **Spring Cloud Stream 2023.0.0** - Messaging abstraction
- **Apache Kafka 3.6** - Distributed streaming platform
- **Kafka Streams** - Stream processing library
- **Maven** - Build and dependency management

### Additional Technologies
- **Project Lombok** - Reduce boilerplate code
- **Jackson** - JSON serialization
- **Spring WebFlux** - Reactive programming
- **Docker & Docker Compose** - Containerization
- **SLF4J & Logback** - Logging

---

## 📁 Project Structure

```
event-driven-architecture-kafka-spring-cloud-stream/
│
├── producer-service/              # REST API Producer
│   ├── src/main/java/com/example/producer/
│   │   ├── controller/
│   │   │   └── EventController.java
│   │   ├── service/
│   │   │   └── EventProducerService.java
│   │   ├── model/
│   │   │   └── PageEvent.java
│   │   └── ProducerApplication.java
│   ├── src/main/resources/
│   │   └── application.yml
│   └── pom.xml
│
├── consumer-service/              # Event Consumer
│   ├── src/main/java/com/example/consumer/
│   │   ├── service/
│   │   │   └── EventConsumerService.java
│   │   ├── model/
│   │   │   └── PageEvent.java
│   │   └── ConsumerApplication.java
│   ├── src/main/resources/
│   │   └── application.yml
│   └── pom.xml
│
├── supplier-service/              # Auto Event Generator
│   ├── src/main/java/com/example/supplier/
│   │   ├── service/
│   │   │   └── EventSupplierService.java
│   │   ├── model/
│   │   │   └── PageEvent.java
│   │   └── SupplierApplication.java
│   ├── src/main/resources/
│   │   └── application.yml
│   └── pom.xml
│
├── analytics-service/             # Stream Processing
│   ├── src/main/java/com/example/analytics/
│   │   ├── service/
│   │   │   └── StreamAnalyticsService.java
│   │   ├── model/
│   │   │   ├── PageEvent.java
│   │   │   └── PageViewStats.java
│   │   └── AnalyticsApplication.java
│   ├── src/main/resources/
│   │   └── application.yml
│   └── pom.xml
│
├── web-dashboard/                 # Real-time Dashboard
│   ├── src/main/java/com/example/dashboard/
│   │   ├── controller/
│   │   │   └── DashboardController.java
│   │   ├── service/
│   │   │   └── DashboardService.java
│   │   └── DashboardApplication.java
│   ├── src/main/resources/
│   │   ├── static/
│   │   │   ├── index.html
│   │   │   ├── css/style.css
│   │   │   └── js/dashboard.js
│   │   └── application.yml
│   └── pom.xml
│
├── docker/
│   ├── docker-compose.yml         # Traditional (ZooKeeper)
│   └── docker-compose-kraft.yml   # Modern (KRaft mode)
│
├── docs/
│   ├── KAFKA_SETUP.md
│   ├── KRAFT_GUIDE.md
│   └── API_DOCUMENTATION.md
│
├── .gitignore
├── README.md
└── pom.xml
```

---

## 📦 Prerequisites

Before starting, ensure you have:

### Required
- **JDK 17+** 
  ```bash
  java -version
  ```
- **Maven 3.8+**
  ```bash
  mvn -version
  ```
- **Docker & Docker Compose** (for containerized setup)
  ```bash
  docker --version
  docker-compose --version
  ```

### Optional
- **Git** - For cloning the repository
- **Postman** or **cURL** - For API testing
- **IntelliJ IDEA** or **VS Code** - Recommended IDEs

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/malakzaidi/event-driven-architecture-kafka-spring-cloud-stream.git
cd event-driven-architecture-kafka-spring-cloud-stream
```

### 2. Start Kafka with Docker (Easiest Method)

```bash
cd docker
docker-compose -f docker-compose-kraft.yml up -d
```

Wait 30 seconds for Kafka to start, then verify:

```bash
docker-compose ps
```

### 3. Build All Services

```bash
# From project root
mvn clean install
```

### 4. Start Services (Each in Separate Terminal)

**Terminal 1 - Producer:**
```bash
cd producer-service
mvn spring-boot:run
```

**Terminal 2 - Consumer:**
```bash
cd consumer-service
mvn spring-boot:run
```

**Terminal 3 - Supplier:**
```bash
cd supplier-service
mvn spring-boot:run
```

**Terminal 4 - Analytics:**
```bash
cd analytics-service
mvn spring-boot:run
```

**Terminal 5 - Dashboard:**
```bash
cd web-dashboard
mvn spring-boot:run
```

### 5. Test the System

**Send an event via REST API:**
```bash
curl -X POST http://localhost:8081/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "pageName": "home",
    "username": "john_doe",
    "duration": 1500
  }'
```

**View the dashboard:**
```
http://localhost:8085
```

**Check logs:**
- Consumer will log received events
- Analytics will show aggregated statistics
- Dashboard will update in real-time

---

## 📖 Detailed Setup

Choose one of three methods to set up Kafka:

### Option 1: Manual Kafka Installation

#### Step 1: Download Kafka

```bash
# Download Kafka
wget https://downloads.apache.org/kafka/3.6.0/kafka_2.13-3.6.0.tgz

# Extract
tar -xzf kafka_2.13-3.6.0.tgz
cd kafka_2.13-3.6.0
```

#### Step 2: Start ZooKeeper

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

**Expected output:**
```
[2024-10-05 10:30:00] INFO binding to port 0.0.0.0/0.0.0.0:2181
```

#### Step 3: Start Kafka Server

Open a new terminal:

```bash
bin/kafka-server-start.sh config/server.properties
```

**Expected output:**
```
[2024-10-05 10:31:00] INFO [KafkaServer id=0] started
```

#### Step 4: Create Topics

Open a third terminal:

```bash
# Create events topic
bin/kafka-topics.sh --create \
  --topic events-topic \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1

# Create analytics topic
bin/kafka-topics.sh --create \
  --topic analytics-results-topic \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1

# List topics
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

#### Step 5: Test with Console Tools

**Producer:**
```bash
bin/kafka-console-producer.sh \
  --topic events-topic \
  --bootstrap-server localhost:9092
```

Type messages:
```
> Hello Kafka
> Testing message 2
```

**Consumer (new terminal):**
```bash
bin/kafka-console-consumer.sh \
  --topic events-topic \
  --bootstrap-server localhost:9092 \
  --from-beginning
```

### Option 2: Docker Setup

**Reference**: [Confluent Kafka Docker Quickstart](https://developer.confluent.io/quickstart/kafka-docker/)

#### Traditional Mode (with ZooKeeper)

**Create `docker-compose.yml`:**

```yaml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    container_name: zookeeper
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    volumes:
      - zookeeper-data:/var/lib/zookeeper/data

  kafka-broker:
    image: confluentinc/cp-kafka:7.5.0
    container_name: kafka-broker
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka-broker:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'
    volumes:
      - kafka-data:/var/lib/kafka/data

volumes:
  zookeeper-data:
  kafka-data:
```

**Start services:**
```bash
docker-compose up -d
```

**Test with Docker:**
```bash
# Producer
docker exec -it kafka-broker kafka-console-producer \
  --topic events-topic \
  --bootstrap-server localhost:9092

# Consumer (new terminal)
docker exec -it kafka-broker kafka-console-consumer \
  --topic events-topic \
  --bootstrap-server localhost:9092 \
  --from-beginning
```

### Option 3: KRaft Mode (Without ZooKeeper)

**Modern approach - Recommended for new projects!**

**Create `docker-compose-kraft.yml`:**

```yaml
version: '3.8'

services:
  kafka-controller:
    image: confluentinc/cp-kafka:7.5.0
    container_name: kafka-controller
    ports:
      - "9093:9093"
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: controller
      KAFKA_CONTROLLER_QUORUM_VOTERS: '1@kafka-controller:9093'
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_LISTENERS: CONTROLLER://kafka-controller:9093
      CLUSTER_ID: 'MkU3OEVBNTcwNTJENDM2Qk'
      KAFKA_LOG_DIRS: /var/lib/kafka/data
    volumes:
      - kafka-controller-data:/var/lib/kafka/data

  kafka-broker:
    image: confluentinc/cp-kafka:7.5.0
    container_name: kafka-broker
    depends_on:
      - kafka-controller
    ports:
      - "9092:9092"
    environment:
      KAFKA_NODE_ID: 2
      KAFKA_PROCESS_ROLES: broker
      KAFKA_CONTROLLER_QUORUM_VOTERS: '1@kafka-controller:9093'
      KAFKA_LISTENERS: PLAINTEXT://kafka-broker:19092,PLAINTEXT_HOST://0.0.0.0:9092
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka-broker:19092,PLAINTEXT_HOST://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'
      CLUSTER_ID: 'MkU3OEVBNTcwNTJENDM2Qk'
      KAFKA_LOG_DIRS: /var/lib/kafka/data
    volumes:
      - kafka-broker-data:/var/lib/kafka/data

volumes:
  kafka-controller-data:
  kafka-broker-data:
```

**Start KRaft cluster:**
```bash
docker-compose -f docker-compose-kraft.yml up -d
```

**Why KRaft?**
- ✅ No ZooKeeper dependency
- ✅ Simpler architecture
- ✅ Faster recovery
- ✅ Better scalability (10M+ partitions)
- ✅ Future of Kafka (ZooKeeper removed in Kafka 4.0)

---

## 🔧 Service Components

### 1️⃣ Producer Service (Port 8081)

**Purpose**: REST API for publishing events to Kafka

**Key Files:**

`PageEvent.java`:
```java
@Data
@AllArgsConstructor
@NoArgsConstructor
public class PageEvent {
    private String id;
    private String pageName;
    private String username;
    private LocalDateTime timestamp;
    private long duration;
}
```

`EventController.java`:
```java
@RestController
@RequestMapping("/api/events")
@RequiredArgsConstructor
public class EventController {
    
    private final EventProducerService producerService;
    
    @PostMapping
    public ResponseEntity<Map<String, String>> publishEvent(@RequestBody PageEvent event) {
        if (event.getId() == null) {
            event.setId(UUID.randomUUID().toString());
        }
        if (event.getTimestamp() == null) {
            event.setTimestamp(LocalDateTime.now());
        }
        
        producerService.publishEvent(event);
        
        return ResponseEntity.ok(Map.of(
            "status", "SUCCESS",
            "eventId", event.getId()
        ));
    }
}
```

`EventProducerService.java`:
```java
@Service
@Slf4j
public class EventProducerService {
    private final Sinks.Many<PageEvent> eventSink;
    
    public EventProducerService() {
        this.eventSink = Sinks.many().multicast().onBackpressureBuffer();
    }
    
    public void publishEvent(PageEvent event) {
        log.info("Publishing event: {}", event);
        eventSink.tryEmitNext(event);
    }
    
    public Sinks.Many<PageEvent> getEventSink() {
        return eventSink;
    }
}
```

`ProducerApplication.java`:
```java
@SpringBootApplication
public class ProducerApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(ProducerApplication.class, args);
    }
    
    @Bean
    public Supplier<Flux<PageEvent>> produceEvent(EventProducerService service) {
        return () -> service.getEventSink().asFlux();
    }
}
```

`application.yml`:
```yaml
spring:
  application:
    name: producer-service
  cloud:
    stream:
      kafka:
        binder:
          brokers: localhost:9092
      bindings:
        produceEvent-out-0:
          destination: events-topic
          content-type: application/json
      function:
        definition: produceEvent

server:
  port: 8081

logging:
  level:
    org.springframework.cloud.stream: DEBUG
```

### 2️⃣ Consumer Service (Port 8082)

**Purpose**: Consumes and processes events from Kafka

`EventConsumerService.java`:
```java
@Service
@Slf4j
public class EventConsumerService {
    
    public Consumer<PageEvent> consumeEvent() {
        return event -> {
            log.info("============================================");
            log.info("📥 Received Event:");
            log.info("   ID: {}", event.getId());
            log.info("   Page: {}", event.getPageName());
            log.info("   User: {}", event.getUsername());
            log.info("   Duration: {} ms", event.getDuration());
            log.info("   Time: {}", event.getTimestamp());
            log.info("============================================");
            
            processEvent(event);
        };
    }
    
    private void processEvent(PageEvent event) {
        // Business logic here:
        // - Save to database
        // - Send notifications
        // - Update cache
        // - Trigger workflows
        log.info("✅ Event processed successfully");
    }
}
```

`ConsumerApplication.java`:
```java
@SpringBootApplication
public class ConsumerApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(ConsumerApplication.class, args);
    }
    
    @Bean
    public Consumer<PageEvent> consumeEvent(EventConsumerService service) {
        return service.consumeEvent();
    }
}
```

`application.yml`:
```yaml
spring:
  application:
    name: consumer-service
  cloud:
    stream:
      kafka:
        binder:
          brokers: localhost:9092
        bindings:
          consumeEvent-in-0:
            consumer:
              start-offset: earliest
      bindings:
        consumeEvent-in-0:
          destination: events-topic
          content-type: application/json
          group: event-consumer-group
      function:
        definition: consumeEvent

server:
  port: 8082
```

### 3️⃣ Supplier Service (Port 8083)

**Purpose**: Auto-generates events every second for testing

`EventSupplierService.java`:
```java
@Service
@Slf4j
public class EventSupplierService {
    
    private final Random random = new Random();
    private final String[] pages = {"home", "products", "cart", "checkout", "profile", "settings"};
    private final String[] users = {"alice", "bob", "charlie", "david", "eve", "frank"};
    
    public Supplier<PageEvent> supplyEvent() {
        return () -> {
            PageEvent event = generateRandomEvent();
            log.info("🔄 Supplying event: {} visited {} for {} ms", 
                event.getUsername(), event.getPageName(), event.getDuration());
            return event;
        };
    }
    
    private PageEvent generateRandomEvent() {
        return new PageEvent(
            UUID.randomUUID().toString(),
            pages[random.nextInt(pages.length)],
            users[random.nextInt(users.length)],
            LocalDateTime.now(),
            500 + random.nextInt(5000) // 500ms to 5500ms
        );
    }
}
```

`application.yml`:
```yaml
spring:
  application:
    name: supplier-service
  cloud:
    stream:
      kafka:
        binder:
          brokers: localhost:9092
      bindings:
        supplyEvent-out-0:
          destination: events-topic
          content-type: application/json
      function:
        definition: supplyEvent
      poller:
        fixed-delay: 1000  # Generate event every 1 second

server:
  port: 8083
```

### 4️⃣ Analytics Service (Port 8084)

**Purpose**: Real-time stream processing with Kafka Streams

**Additional Dependencies** (`pom.xml`):
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-stream-binder-kafka-streams</artifactId>
</dependency>
<dependency>
    <groupId>org.apache.kafka</groupId>
    <artifactId>kafka-streams</artifactId>
</dependency>
```

`PageViewStats.java`:
```java
@Data
@AllArgsConstructor
@NoArgsConstructor
public class PageViewStats {
    private String pageName;
    private long count;
    private double averageDuration;
    private long totalDuration;
    private long minDuration;
    private long maxDuration;
}
```

`StreamAnalyticsService.java`:
```java
@Service
@Slf4j
public class StreamAnalyticsService {
    
    @Bean
    public Function<KStream<String, PageEvent>, KStream<String, PageViewStats>> processEvents() {
        return input -> {
            // Group events by page name
            KGroupedStream<String, PageEvent> groupedByPage = input
                .selectKey((key, event) -> event.getPageName())
                .groupByKey();
            
            // Aggregate in 1-minute tumbling windows
            KTable<Windowed<String>, PageViewStats> stats = groupedByPage
                .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(1)))
                .aggregate(
                    // Initializer
                    () -> new PageViewStats("", 0, 0.0, 0, Long.MAX_VALUE, 0),
                    
                    // Aggregator
                    (pageName, event, aggregate) -> {
                        long newCount = aggregate.getCount() + 1;
                        long newTotal = aggregate.getTotalDuration() + event.getDuration();
                        double newAvg = (double) newTotal / newCount;
                        long newMin = Math.min(aggregate.getMinDuration(), event.getDuration());
                        long newMax = Math.max(aggregate.getMaxDuration(), event.getDuration());
                        
                        return new PageViewStats(
                            pageName, newCount, newAvg, newTotal, newMin, newMax
                        );
                    }
                );
            
            // Convert to stream
            KStream<String, PageViewStats> result = stats
                .toStream()
                .map((windowedKey, value) -> {
                    value.setPageName(windowedKey.key());
                    return new KeyValue<>(windowedKey.key(), value);
                });
            
            // Log results
            result.foreach((key, value) -> 
                log.info("📊 Analytics: Page={}, Count={}, Avg={}ms, Min={}ms, Max={}ms", 
                    key, value.getCount(), (long)value.getAverageDuration(), 
                    value.getMinDuration(), value.getMaxDuration())
            );
            
            return result;
        };
    }
}
```

`application.yml`:
```yaml
spring:
  application:
    name: analytics-service
  cloud:
    stream:
      kafka:
        binder:
          brokers: localhost:9092
        streams:
          binder:
            configuration:
              commit.interval.ms: 1000
              default.key.serde: org.apache.kafka.common.serialization.Serdes$StringSerde
      bindings:
        processEvents-in-0:
          destination: events-topic
          content-type: application/json
        processEvents-out-0:
          destination: analytics-results-topic
          content-type: application/json
      function:
        definition: processEvents

server:
  port: 8084
```

### 5️⃣ Web Dashboard (Port 8085)

**Purpose**: Real-time visualization of analytics data

`DashboardController.java`:
```java
@RestController
@RequestMapping("/api/dashboard")
@RequiredArgsConstructor
public class DashboardController {
    
    private final DashboardService dashboardService;
    
    @GetMapping("/stats")
    public ResponseEntity<List<PageViewStats>> getStats() {
        return ResponseEntity.ok(dashboardService.getLatestStats());
    }
    
    @GetMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<PageViewStats> streamStats() {
        return dashboardService.getStatsStream();
    }
}
```

`DashboardService.java`:
```java
@Service
@Slf4j
public class DashboardService {
    
    private final Sinks.Many<PageViewStats> statsSink = 
        Sinks.many().multicast().onBackpressureBuffer();
    
    private final List<PageViewStats> latestStats = new CopyOnWriteArrayList<>();
    
    @Bean
    public Consumer<PageViewStats> consumeAnalytics() {
        return stats -> {
            log.info("📈 Received analytics: {}", stats);
            latestStats.add(stats);
            if (latestStats.size() > 100) {
                latestStats.remove(0);
            }
            statsSink.tryEmitNext(stats);
        };
    }
    
    public List<PageViewStats> getLatestStats() {
        return new ArrayList<>(latestStats);
    }
    
    public Flux<PageViewStats> getStatsStream() {
        return statsSink.asFlux();
    }
}
```

`index.html` (in `src/main/resources/static/`):
```html
<!DOCTYPE html>
<html>
<head>
    <title>Real-Time Analytics Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .stat-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            transition: transform 0.3s;
        }
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .stat-card h3 {
            margin: 0 0 15px 0;
            color: #667eea;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }
        .stat-label {
            font-size: 14px;
            color: #666;
            margin-top: 5px;
        }
        .status {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }
        .status.connected {
            background: #d4edda;
            color: #155724;
        }
        .status.disconnected {
            background: #f8d7da;
            color: #721c24;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Real-Time Analytics Dashboard</h1>
        <div style="text-align: center; margin-bottom: 20px;">
            <span id="status" class="status disconnected">Disconnected</span>
        </div>
        <div id="stats" class="stats-grid"></div>
    </div>

    <script>
        const eventSource = new EventSource('/api/dashboard/stream');
        const statusEl = document.getElementById('status');
        const statsEl = document.getElementById('stats');

        eventSource.onopen = () => {
            statusEl.textContent = 'Connected';
            statusEl.className = 'status connected';
        };

        eventSource.onmessage = (event) => {
            const stats = JSON.parse(event.data);
            updateStats(stats);
        };

        eventSource.onerror = () => {
            statusEl.textContent = 'Disconnected';
            statusEl.className = 'status disconnected';
        };

        function updateStats(stats) {
            const card = `
                <div class="stat-card">
                    <h3>📄 ${stats.pageName}</h3>
                    <div class="stat-value">${stats.count}</div>
                    <div class="stat-label">Total Views</div>
                    <hr style="margin: 15px 0;">
                    <div><strong>Avg Duration:</strong> ${Math.round(stats.averageDuration)} ms</div>
                    <div><strong>Min:</strong> ${stats.minDuration} ms</div>
                    <div><strong>Max:</strong> ${stats.maxDuration} ms</div>
                    <div><strong>Total:</strong> ${stats.totalDuration} ms</div>
                </div>
            `;
            statsEl.innerHTML += card;
            
            // Keep only last 10 cards
            const cards = statsEl.querySelectorAll('.stat-card');
            if (cards.length > 10) {
                cards[0].remove();
            }
        }
    </script>
</body>
</html>
```

`application.yml`:
```yaml
spring:
  application:
    name: web-dashboard
  cloud:
    stream:
      kafka:
        binder:
          brokers: localhost:9092
      bindings:
        consumeAnalytics-in-0:
          destination: analytics-results-topic
          content-type: application/json
          group: dashboard-consumer-group
      function:
        definition: consumeAnalytics

server:
  port: 8085
```

---

## ⚙️ Configuration

### Common Application Properties

All services share similar base configuration with service-specific variations:

```yaml
spring:
  application:
    name: service-name
  cloud:
    stream:
      kafka:
        binder:
          brokers: localhost:9092  # Kafka broker address
          auto-create-topics: true  # Auto-create topics if they don't exist
      bindings:
        # Input binding (for consumers)
        functionName-in-0:
          destination: topic-name
          content-type: application/json
          group: consumer-group-name
        # Output binding (for producers)
        functionName-out-0:
          destination: topic-name
          content-type: application/json
      function:
        definition: functionName  # Spring Cloud Function name

server:
  port: 808X  # Unique port for each service

logging:
  level:
    org.springframework.cloud.stream: DEBUG
    org.apache.kafka: INFO
```

### Environment-Specific Configuration

Create `application-dev.yml` and `application-prod.yml` for different environments:

**application-prod.yml**:
```yaml
spring:
  cloud:
    stream:
      kafka:
        binder:
          brokers: kafka-prod-1:9092,kafka-prod-2:9092,kafka-prod-3:9092
          replication-factor: 3
          min-partition-count: 3

logging:
  level:
    org.springframework.cloud.stream: INFO
    org.apache.kafka: WARN
```

---

## 🎮 Running the Application

### Complete Startup Sequence

#### 1. Start Kafka Infrastructure

```bash
# Using Docker (Recommended)
cd docker
docker-compose -f docker-compose-kraft.yml up -d

# Wait for Kafka to be ready (30 seconds)
sleep 30

# Verify Kafka is running
docker-compose ps
```

#### 2. Build All Services

```bash
# From project root
mvn clean install -DskipTests
```

#### 3. Start Services in Order

**Terminal 1 - Producer Service:**
```bash
cd producer-service
mvn spring-boot:run
```
Wait for: `Started ProducerApplication in X seconds`

**Terminal 2 - Consumer Service:**
```bash
cd consumer-service
mvn spring-boot:run
```
Wait for: `Started ConsumerApplication in X seconds`

**Terminal 3 - Supplier Service:**
```bash
cd supplier-service
mvn spring-boot:run
```
You'll see events being generated every second.

**Terminal 4 - Analytics Service:**
```bash
cd analytics-service
mvn spring-boot:run
```
You'll see aggregated statistics being computed.

**Terminal 5 - Web Dashboard:**
```bash
cd web-dashboard
mvn spring-boot:run
```
Access at: http://localhost:8085

#### 4. Verify All Services

```bash
# Check health endpoints
curl http://localhost:8081/actuator/health  # Producer
curl http://localhost:8082/actuator/health  # Consumer
curl http://localhost:8083/actuator/health  # Supplier
curl http://localhost:8084/actuator/health  # Analytics
curl http://localhost:8085/actuator/health  # Dashboard
```

All should return: `{"status":"UP"}`

---

## 🧪 Testing

### 1. Manual Testing with REST API

**Send a single event:**
```bash
curl -X POST http://localhost:8081/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "pageName": "checkout",
    "username": "test_user",
    "duration": 2500
  }'
```

**Expected Response:**
```json
{
  "status": "SUCCESS",
  "eventId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**Send multiple events:**
```bash
# Create a script
for i in {1..10}; do
  curl -X POST http://localhost:8081/api/events \
    -H "Content-Type: application/json" \
    -d "{\"pageName\":\"page$i\",\"username\":\"user$i\",\"duration\":$((RANDOM % 5000))}"
  sleep 0.5
done
```

### 2. Testing with Kafka Console Tools

**Produce messages:**
```bash
# Manual installation
bin/kafka-console-producer.sh \
  --topic events-topic \
  --bootstrap-server localhost:9092

# Docker
docker exec -it kafka-broker kafka-console-producer \
  --topic events-topic \
  --bootstrap-server localhost:9092
```

Type JSON messages:
```json
{"id":"1","pageName":"home","username":"alice","timestamp":"2024-10-05T10:00:00","duration":1500}
{"id":"2","pageName":"products","username":"bob","timestamp":"2024-10-05T10:00:05","duration":2000}
```

**Consume messages:**
```bash
# Manual installation
bin/kafka-console-consumer.sh \
  --topic events-topic \
  --bootstrap-server localhost:9092 \
  --from-beginning

# Docker
docker exec -it kafka-broker kafka-console-consumer \
  --topic events-topic \
  --bootstrap-server localhost:9092 \
  --from-beginning
```

### 3. View Consumer Groups

```bash
# List consumer groups
docker exec -it kafka-broker kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --list

# Describe a specific group
docker exec -it kafka-broker kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --group event-consumer-group \
  --describe
```

**Expected Output:**
```
GROUP                TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
event-consumer-group events-topic    0          45              45              0
event-consumer-group events-topic    1          43              43              0
event-consumer-group events-topic    2          47              47              0
```

### 4. Integration Testing

Create `IntegrationTest.java`:

```java
@SpringBootTest
@EmbeddedKafka(partitions = 1, topics = {"events-topic"})
public class EventIntegrationTest {
    
    @Autowired
    private EventProducerService producerService;
    
    @Test
    public void testEventPublishing() {
        PageEvent event = new PageEvent(
            "test-id", "home", "testuser", LocalDateTime.now(), 1000
        );
        
        producerService.publishEvent(event);
        
        // Add assertions
        assertNotNull(event.getId());
    }
}
```

### 5. Load Testing with Apache Bench

```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Create a JSON file
cat > event.json << EOF
{
  "pageName": "home",
  "username": "loadtest",
  "duration": 1500
}
EOF

# Run load test (1000 requests, 10 concurrent)
ab -n 1000 -c 10 -p event.json -T application/json \
  http://localhost:8081/api/events
```

---

## 📡 API Documentation

### Producer Service Endpoints

#### POST /api/events
Publish a new event to Kafka

**Request:**
```http
POST /api/events HTTP/1.1
Host: localhost:8081
Content-Type: application/json

{
  "pageName": "products",
  "username": "john_doe",
  "duration": 2500
}
```

**Response:**
```json
{
  "status": "SUCCESS",
  "eventId": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Status Codes:**
- `200 OK` - Event published successfully
- `400 Bad Request` - Invalid event data
- `500 Internal Server Error` - Server error

#### GET /actuator/health
Check service health

**Response:**
```json
{
  "status": "UP"
}
```

### Dashboard Service Endpoints

#### GET /api/dashboard/stats
Get latest statistics snapshot

**Response:**
```json
[
  {
    "pageName": "home",
    "count": 45,
    "averageDuration": 1850.5,
    "totalDuration": 83272,
    "minDuration": 500,
    "maxDuration": 5500
  },
  {
    "pageName": "products",
    "count": 38,
    "averageDuration": 2100.3,
    "totalDuration": 79812,
    "minDuration": 600,
    "maxDuration": 5400
  }
]
```

#### GET /api/dashboard/stream
Stream real-time statistics (Server-Sent Events)

**Response:** Continuous stream of events
```
data: {"pageName":"cart","count":12,"averageDuration":1500,...}

data: {"pageName":"checkout","count":8,"averageDuration":2200,...}
```

**Usage with JavaScript:**
```javascript
const eventSource = new EventSource('http://localhost:8085/api/dashboard/stream');
eventSource.onmessage = (event) => {
    const stats = JSON.parse(event.data);
    console.log(stats);
};
```

---

## 📊 Real-Time Analytics

### Kafka Streams Concepts

#### 1. Stream vs Table
- **KStream**: Represents an unbounded stream of events (insert-only)
- **KTable**: Represents a changelog stream (updates/deletes)

#### 2. Windowing
Groups events into time-based windows for aggregation:

**Types of Windows:**
- **Tumbling Window**: Fixed-size, non-overlapping
  ```java
  TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(1))
  ```
- **Hopping Window**: Fixed-size, overlapping
  ```java
  TimeWindows.ofSizeAndGrace(Duration.ofMinutes(5), Duration.ofSeconds(30))
            .advanceBy(Duration.ofMinutes(1))
  ```
- **Session Window**: Dynamic size based on inactivity gaps
  ```java
  SessionWindows.ofInactivityGapWithNoGrace(Duration.ofMinutes(5))
  ```

#### 3. Aggregations

**Count:**
```java
groupedStream.count()
```

**Custom Aggregation:**
```java
groupedStream.aggregate(
    () -> initialValue,           // Initializer
    (key, value, aggregate) -> {  // Aggregator
        // Update aggregate
        return updatedAggregate;
    }
)
```

**Reduce:**
```java
groupedStream.reduce((value1, value2) -> combinedValue)
```

### Analytics Examples

#### Page View Analytics
Tracks page visits, average duration, min/max times per page in 1-minute windows.

#### User Activity Analytics
Monitors user behavior, total visits, most visited pages per user.

#### Real-Time Alerts
Detect anomalies (e.g., page load > 10 seconds):

```java
input.filter((key, event) -> event.getDuration() > 10000)
     .foreach((key, event) -> 
         log.warn("⚠️ Slow page load: {} took {}ms", 
                  event.getPageName(), event.getDuration())
     );
```

---

## 🖥️ Web Dashboard

### Features

1. **Real-Time Updates**: Automatic updates via Server-Sent Events (SSE)
2. **Statistics Cards**: Visual representation of analytics data
3. **Connection Status**: Shows connection state to backend
4. **Responsive Design**: Works on desktop and mobile devices

### Accessing the Dashboard

1. Ensure all services are running
2. Open browser: http://localhost:8085
3. Watch real-time statistics appear as events are processed

### Dashboard Metrics

Each card shows:
- **Page Name**: Which page the statistics are for
- **Total Views**: Number of page visits
- **Average Duration**: Mean time spent on page
- **Min Duration**: Fastest page load
- **Max Duration**: Slowest page load
- **Total Duration**: Sum of all durations

### Customization

Modify `static/index.html` to:
- Change colors and styling
- Add charts (Chart.js, D3.js)
- Add filtering and sorting
- Export data to CSV

---

## 📈 Monitoring

### Kafka Monitoring

#### Topic Information
```bash
# List all topics
docker exec kafka-broker kafka-topics \
  --bootstrap-server localhost:9092 \
  --list

# Describe topic
docker exec kafka-broker kafka-topics \
  --bootstrap-server localhost:9092 \
  --describe \
  --topic events-topic
```

#### Consumer Group Lag
```bash
docker exec kafka-broker kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --group event-consumer-group \
  --describe
```

**Healthy Output:** LAG should be 0 or low
```
GROUP                TOPIC         PARTITION  LAG
event-consumer-group events-topic  0          0
event-consumer-group events-topic  1          0
event-consumer-group events-topic  2          0
```

#### Message Count
```bash
docker exec kafka-broker kafka-run-class kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 \
  --topic events-topic \
  --time -1
```

### Application Monitoring

#### Spring Boot Actuator

Add to `pom.xml`:
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

Enable endpoints in `application.yml`:
```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: always
```

**Available Endpoints:**
- `/actuator/health` - Service health status
- `/actuator/metrics` - Application metrics
- `/actuator/info` - Application information
- `/actuator/prometheus` - Prometheus metrics

#### Logging

**View service logs:**
```bash
# Producer logs
tail -f producer-service/logs/application.log

# All services with grep
tail -f */logs/application.log | grep "ERROR"
```

**Docker logs:**
```bash
# Kafka logs
docker logs kafka-broker -f

# All containers
docker-compose logs -f
```

### Performance Metrics

Monitor these key metrics:
- **Throughput**: Events processed per second
- **Latency**: Time from event creation to consumption
- **Consumer Lag**: Messages waiting to be processed
- **Error Rate**: Failed message percentage
- **Resource Usage**: CPU, memory, disk I/O

---

## 🔧 Troubleshooting

### Common Issues

#### Issue 1: Kafka Connection Refused

**Symptom:**
```
Connection to node -1 (localhost/127.0.0.1:9092) could not be established
```

**Solutions:**
```bash
# Check if Kafka is running
docker-compose ps

# Check Kafka logs
docker logs kafka-broker

# Restart Kafka
docker-compose restart kafka-broker

# Verify port is not in use
lsof -i :9092
```

#### Issue 2: Consumer Not Receiving Messages

**Symptom:** Producer sends messages but consumer doesn't process them

**Solutions:**
```bash
# 1. Check if topic exists
docker exec kafka-broker kafka-topics \
  --bootstrap-server localhost:9092 \
  --list

# 2. Check consumer group status
docker exec kafka-broker kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --group event-consumer-group \
  --describe

# 3. Reset consumer offsets (CAUTION: reprocesses all messages)
docker exec kafka-broker kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --group event-consumer-group \
  --reset-offsets \
  --to-earliest \
  --topic events-topic \
  --execute
```

#### Issue 3: Services Fail to Start

**Symptom:**
```
Port 8081 is already in use
```

**Solutions:**
```bash
# Find process using the port
lsof -i :8081

# Kill the process
kill -9 <PID>

# Or change port in application.yml
server:
  port: 8091
```

#### Issue 4: Out of Memory

**Symptom:**
```
java.lang.OutOfMemoryError: Java heap space
```

**Solutions:**
```bash
# Increase JVM heap size
export MAVEN_OPTS="-Xmx2048m -Xms512m"
mvn spring-boot:run

# Or in application.yml
spring:
  kafka:
    producer:
      properties:
        max.request.size: 1048576
```

#### Issue 5: Slow Performance

**Symptom:** High latency or low throughput

**Solutions:**
1. **Increase Partitions:**
```bash
docker exec kafka-broker kafka-topics \
  --bootstrap-server localhost:9092 \
  --alter \
  --topic events-topic \
  --partitions 6
```

2. **Tune Consumer Configuration:**
```yaml
spring:
  cloud:
    stream:
      kafka:
        bindings:
          consumeEvent-in-0:
            consumer:
              concurrency: 3  # Number of consumer threads
```

3. **Enable Batch Processing:**
```yaml
spring:
  cloud:
    stream:
      kafka:
        binder:
          consumer-properties:
            max.poll.records: 500
```

### Debug Mode

Enable detailed logging:

```yaml
logging:
  level:
    root: INFO
    org.springframework.cloud.stream: DEBUG
    org.springframework.kafka: DEBUG
    org.apache.kafka: DEBUG
    com.example: TRACE
```

---

## 🎯 Best Practices

### Event Design

1. **Use Meaningful Names**
   ```java
   // Good
   class OrderCreatedEvent { }
   
   // Bad
   class Event1 { }
   ```

2. **Include Metadata**
   ```java
   class PageEvent {
       private String id;           // Unique identifier
       private LocalDateTime timestamp;  // When it occurred
       private String source;       // Which service produced it
       private String correlationId; // For tracing
   }
   ```

3. **Version Your Events**
   ```java
   class PageEvent {
       private String eventVersion = "1.0";
       // ...
   }
   ```

### Kafka Configuration

1. **Production Settings:**
```yaml
spring:
  cloud:
    stream:
      kafka:
        binder:
          replication-factor: 3
          min-partition-count: 3
          auto-create-topics: false  # Create topics manually
```

2. **Idempotent Producer:**
```yaml
spring:
  cloud:
    stream:
      kafka:
        binder:
          producer-properties:
            enable.idempotence: true
            acks: all
```

3. **Consumer Reliability:**
```yaml
spring:
  cloud:
    stream:
      kafka:
        bindings:
          consumeEvent-in-0:
            consumer:
              enable-auto-commit: false  # Manual commit
              auto-offset-reset: earliest
```

### Error Handling

1. **Dead Letter Queue (DLQ):**
```yaml
spring:
  cloud:
    stream:
      bindings:
        consumeEvent-in-0:
          consumer:
            max-attempts: 3
          destination: events-topic
        consumeEvent-in-0.errors:
          destination: events-topic-dlq
```

2. **Retry Logic:**
```java
@Bean
public Consumer<PageEvent> consumeEvent() {
    return Retry.decorateConsumer(
        Retry.of("eventConsumer", RetryConfig.custom()
            .maxAttempts(3)
            .waitDuration(Duration.ofSeconds(2))
            .build()),
        this::processEvent
    );
}
```

### Security

1. **Enable SSL:**
```yaml
spring:
  cloud:
    stream:
      kafka:
        binder:
          brokers: kafka:9093
          configuration:
            security.protocol: SSL
            ssl.truststore.location: /path/to/truststore.jks
            ssl.truststore.password: password
```

2. **SASL Authentication:**
```yaml
spring:
  cloud:
    stream:
      kafka:
        binder:
          configuration:
            security.protocol: SASL_SSL
            sasl.mechanism: PLAIN
            sasl.jaas.config: org.apache.kafka.common.security.plain.PlainLoginModule required username="user" password="pass";
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Code Standards

- Follow Java coding conventions
- Write unit tests for new features
- Update documentation
- Add comments for complex logic
- Ensure all tests pass before submitting

### Reporting Issues

When reporting issues, please include:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Java version, etc.)
- Relevant logs or screenshots

---

## 📚 Resources

### Official Documentation
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Spring Cloud Stream Reference](https://spring.io/projects/spring-cloud-stream)
- [Kafka Streams Documentation](https://kafka.apache.org/documentation/streams/)
- [Spring Boot Documentation](https://spring.io/projects/spring-boot)

### Kafka Resources
- [Confluent Kafka Docker Quickstart](https://developer.confluent.io/quickstart/kafka-docker/)
- [KRaft: Kafka Without ZooKeeper](https://developer.confluent.io/learn/kraft/)
- [KIP-500: Replace ZooKeeper](https://cwiki.apache.org/confluence/display/KAFKA/KIP-500)

### Tutorials & Guides
- [Event-Driven Microservices](https://www.confluent.io/blog/event-driven-microservices/)
- [Spring Cloud Stream with Kafka](https://spring.io/guides/gs/spring-cloud-stream/)
- [Kafka Streams Tutorial](https://kafka.apache.org/documentation/streams/tutorial)

### Books
- **"Kafka: The Definitive Guide"** by Neha Narkhede, Gwen Shapira, Todd Palino
- **"Building Event-Driven Microservices"** by Adam Bellemare
- **"Designing Data-Intensive Applications"** by Martin Kleppmann
- **"Enterprise Integration Patterns"** by Gregor Hohpe

### Community
- [Kafka Users Mailing List](https://kafka.apache.org/contact)
- [Stack Overflow - Apache Kafka](https://stackoverflow.com/questions/tagged/apache-kafka)
- [Confluent Community](https://www.confluent.io/community/)

---

## 🙏 Acknowledgments

- **Apache Kafka Team** - For the amazing streaming platform
- **Spring Team** - For Spring Cloud Stream framework
- **Confluent** - For excellent Kafka resources and documentation
- **Community Contributors** - For feedback and improvements

---

## 📞 Support

Need help? Here's how to get support:

- 📧 **Email**: [e.malakzaidi@example.com]
- 💬 **Issues**: [GitHub Issues](https://github.com/malakzaidi/event-driven-architecture-kafka-spring-cloud-stream/issues)
- 📖 **Wiki**: [Project Wiki](https://github.com/malakzaidi/event-driven-architecture-kafka-spring-cloud-stream/wiki)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

**Made with ❤️ by [Malak Zaidi](https://github.com/malakzaidi)**

---




---

**Last Updated**: October 2024
**Project Status**: ✅ Active Development
