"""
Simple experiment logging for tracking decisions and events.
Professionals track decisions, not just results.
"""
from datetime import datetime

def log_event(message):
    """Log an event with timestamp to experiment.log"""
    with open("experiment.log", "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
