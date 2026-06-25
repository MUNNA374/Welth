from prometheus_client import Counter, Histogram, Gauge

# HTTP request metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests processed",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Latency of HTTP requests in seconds",
    ["method", "endpoint"]
)

# Business metrics
TRANSACTIONS_PROCESSED = Counter(
    "transactions_processed_total",
    "Total number of processed transactions",
    ["category", "source"]
)

AI_API_CALLS = Counter(
    "ai_api_calls_total",
    "Total number of AI requests made to models",
    ["model", "service", "status"]
)

ACTIVE_SESSIONS = Gauge(
    "active_sessions_total",
    "Number of active user sessions"
)
