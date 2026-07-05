# Architecture evidence candidates

Matches are evidence candidates only. Inspect implementation and tests before assigning completion status.

Files scanned: 42

## gateway-security

1. `gateway/src/main/java/example/SecurityGatewayFilter.java:37` [implementation] remove untrusted X-User-* headers before writing authenticated identity
2. `gateway/src/test/java/example/SecurityGatewayFilterTest.java:52` [test] rejects forged internal identity headers

## cache-concurrency

1. `service/src/main/resources/lua/reserve.lua:12` [implementation] use Redis Lua to atomically validate activity, limit user purchase, and decrement stock

## messaging-reliability

1. `order/src/main/java/example/OutboxPublisher.java:44` [implementation] publish pending outbox messages with confirm callback
2. `order/src/test/java/example/OutboxPublisherTest.java:68` [test] keeps message pending when broker is unavailable

## database-consistency

1. `db/migration/V3__orders.sql:19` [deployment] create unique index uk_activity_user on orders(activity_id, user_id)

## realtime

1. `notify/src/main/java/example/OrderSseController.java:23` [implementation] produces text/event-stream for order result delivery

## llm-governance

1. `ai/src/main/java/example/AgentService.java:81` [implementation] allow only read-only tools and set provider timeout

## api-contracts

1. `pom.xml:76` [deployment] springdoc-openapi-starter-webmvc-ui

## deployment

1. `docker-compose.yml:42` [deployment] healthcheck waits for RabbitMQ before starting order service

## observability

1. `service/src/main/java/example/BusinessMetrics.java:29` [implementation] exposes order.created and outbox.pending metrics

## tests-evidence

1. `postman/seckill-flow.postman_collection.json:12` [test] asserts queueing response and final order status
