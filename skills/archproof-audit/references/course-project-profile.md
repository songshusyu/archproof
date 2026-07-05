# Web backend course project profile

Read this profile only when the authoritative rubric asks for a microservice-oriented Web backend prototype. The assignment remains the source of truth; this file is a reusable starting point, not a universal definition of good architecture.

## Common acceptance baseline

Check the rubric for independently runnable services, a unified Gateway entry, relational persistence, Redis, MQ, OpenAPI, reproducible local deployment, an API collection, runtime evidence, and a report containing architecture, sequence, ER, tradeoffs, testing, and production evolution. Do not award completion merely because a dependency appears in a build file.

## Typical scenario traces

### High-concurrency purchase

Trace Gateway identity and limiting to Redis atomic qualification, durable message intent, publish confirmation, idempotent order transaction, acknowledgement, reconciliation, and WebSocket or SSE delivery. Distinguish an accepted qualification from a committed order.

### AI-assisted ticket processing

Trace ticket submission to durable message intent, asynchronous LLM classification, idempotent write-back, high-priority alert deduplication, and query fallback. Verify that a slow or unavailable provider does not block the submission transaction.

### Knowledge and content publication

Trace dynamic rate-limit configuration, read or like concurrency semantics, ZSET ranking updates, fanout publication, independent worker results, and streaming completion. Verify that one slow subscriber does not consume another subscriber's copy of the event.

## Evidence expected in a high-scoring submission

Prefer executable tests, API collection assertions, raw load-test output, final database/Redis/MQ reconciliation, failure drills, and rendered report figures. Keep local measurements separate from Kubernetes, multi-zone, autoscaling, or HA designs that were not run locally.
