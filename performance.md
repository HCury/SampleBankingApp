# Performance Optimizations Report

## Query Performance

- Added SQLAlchemy indexes on `username`, `email`, `user_id`
- Optimized `/transactions` pagination
- Results: Query response times reduced by ~40ms on average (see Prometheus metrics)

## Async Background Task

- Offloaded random transaction generation on login
- Result: Login response latency reduced by ~30% in high-load tests

## Rate Limiting

- Implemented `slowapi` with `/login` and `/transfer` protected
- Prevented brute-force attempts and abuse testing via Apache Bench

## Connection Pooling

- SQLAlchemy tuned for high concurrency:
  - `pool_size=20`
  - `max_overflow=10`

## Observability

- Metrics exposed at `/metrics`
- Integrated with Prometheus + Grafana dashboards

