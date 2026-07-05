# Architecture and failure checklist

## Contents

1. Requirement baseline
2. Concurrency invariants
3. MQ failure matrix
4. Real-time and LLM boundaries
5. Production evolution
6. Evidence quality

## Requirement baseline

Derive the baseline from the authoritative requirement rather than assuming that every system needs microservices, a Gateway, Redis, MQ, or Kubernetes. Record the requested capabilities, trust boundaries, state owners, acceptance evidence, and explicitly excluded scope. Treat a dependency as relevant only when it solves a stated business or operational problem.

For each important flow, trace the request or event from ingress to its durable fact. Identify every boundary where identity, ownership, atomicity, delivery, or recovery semantics change. If the task is a Web backend course project, additionally read `course-project-profile.md` for the common rubric and scenario traces.

## Concurrency invariants

### Seckill

1. Stock never becomes negative.
2. A user never exceeds the configured limit.
3. Activity time and status are checked in the same atomic decision as deduction.
4. Duplicate delivery creates no duplicate order.
5. Repeated compensation increases stock at most once.
6. Recovery does not make sold stock available again.
7. Durable orders, pending messages, qualifications, and remaining stock can be reconciled.

### Interaction and ranking

1. A like record is unique for the chosen user and article semantics.
2. Concurrent requests cannot lose updates.
3. Repeated reads follow a documented window or identity policy.
4. ZSET score and database counters have a stated consistency model.
5. Rate-limit rule changes can be observed without a process restart.

## MQ failure matrix

| Failure | State to inspect | Expected behavior |
|---|---|---|
| Broker unavailable before publish | Outbox row, retry count, oldest pending age | Business request remains traceable; retry is bounded and observable |
| Confirm timeout or nack | Publish state and confirm callback | Do not mark sent; schedule retry |
| Duplicate delivery | Unique index and consumer path | Return success or ACK without a second business row |
| Database failure | Transaction rollback and ACK order | Do not ACK committed work that does not exist |
| Consumer crash after commit | Database row and redelivery | Unique constraint makes redelivery harmless |
| Poison message | Retry count and DLQ | Avoid a rapid infinite requeue loop |
| Notification failure | Durable order and delivery metric | Keep the order; expose query fallback |

## Real-time and LLM boundaries

Verify that WebSocket or SSE is a delivery channel rather than the durable fact source. Define authentication, disconnect handling, heartbeat or timeout, completion events, query fallback, and multi-instance routing.

For LLM calls, record provider, model, protocol, timeout, rate limit, retry policy, maximum concurrency, queue capacity, cache key version, prompt version, tool allowlist, source attribution, and failure response. A mock response cannot prove provider integration. A real response cannot by itself prove injection resistance or cache correctness.

## Production evolution

Separate local implementation from planned production deployment. Cover:

1. Multiple stateless service and Gateway instances behind load balancing.
2. Nacos or another registry in high-availability mode.
3. MySQL primary-replica, backups, failover, RPO, and RTO.
4. Redis Sentinel or Cluster, persistence, hot-key handling, and recovery warmup.
5. RabbitMQ quorum queues, publisher confirms, DLQ, and backlog alarms.
6. HPA for CPU or latency and KEDA for queue depth where appropriate.
7. Admission control, load shedding, circuit breaking, and bounded retries.
8. LLM request queues, semantic cache, provider routing, budgets, and quality evaluation.
9. Metrics, traces, logs, dashboards, alerts, and fault drills.

## Evidence quality

Use this order from strongest to weakest:

1. Reproducible automated test plus final database, Redis, and MQ state.
2. Raw load-test output plus reconciliation query.
3. API collection assertion and service logs.
4. Source and configuration inspection.
5. Report statement without executable evidence.

An implementation can be complete while evidence is missing. Record these as separate statuses.
