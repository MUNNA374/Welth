# Admin Operations Manual

Administration users have elevated privileges.

## Audit Logs
All security mutations (logins, register, failures) are logged to the `AuditLog` database table. Admin users can review these logs to assess for potential security anomalies or intrusions.

## Health Metrics Monitoring
- **Prometheus Metrics**: Exposes custom API performance and usage metrics at `/metrics`.
- **System Health Diagnostics**: Live API health reports (PostgreSQL connectivity status, Redis ping, disk memory metrics) are found at `/api/v1/health`.
