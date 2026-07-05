# Evidence passport

Use one passport for each scoring highlight. Store passports in JSON, YAML, a report table, or an issue tracker. Keep field names stable so the report and test index can be generated from the same data.

```yaml
title: Duplicate event delivery is idempotent
formal_topic: Order fulfillment
score_category: core architecture
requirement: Reprocessing the same event creates at most one durable business record
business_consequence: Duplicate fulfillment charges or ships the same order twice
implementation_status: implemented-and-tested
service: fulfillment-service
api: POST /internal/events/order-created
code:
  - path: src/consumers/order_created.py
    symbol: handle_order_created
database:
  tables: [fulfillment, consumed_event]
  constraints: [uk_consumed_event_id]
redis:
  keys: []
  operation: none
mq:
  exchange: order.events
  queues: [fulfillment.order-created, fulfillment.dlq]
tests:
  automated: tests/test_order_created.py::test_duplicate_event_is_harmless
  collection_step: Replay order-created event
evidence:
  raw_result: evidence/duplicate-delivery.json
  reconciliation: evidence/fulfillment-count.json
report_section: Reliability / Idempotency
scope: local-measurement
limitations: Single-host Docker Compose run
```

Use only these implementation statuses:

1. `implemented-and-tested`
2. `implemented-not-tested`
3. `design-only`
4. `contradicted`
5. `missing`

Use only these scopes:

1. `local-measurement`
2. `source-inspection`
3. `production-design`

Do not list a database table, Redis key, queue, test, or result file when it does not exist. Record `missing` and create a repair task.
