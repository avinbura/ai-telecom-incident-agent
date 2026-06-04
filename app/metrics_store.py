metrics = {
    "total_alerts_processed": 0,
    "critical_alerts": 0,
    "medium_alerts": 0,
    "low_alerts": 0,
    "failed_requests": 0
}


def update_metrics(result: dict):
    metrics["total_alerts_processed"] += 1

    severity = result.get("severity", "").lower()

    if severity == "critical":
        metrics["critical_alerts"] += 1

    elif severity == "medium":
        metrics["medium_alerts"] += 1

    elif severity == "low":
        metrics["low_alerts"] += 1


def update_failed_requests():
    metrics["failed_requests"] += 1


def get_metrics():
    return metrics
