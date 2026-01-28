"""
Simple experiment logging for tracking decisions and events.
Professionals track decisions, not just results.
"""
from datetime import datetime

def log_event(message):
    """Log an event with timestamp to experiment.log"""
    with open("experiment.log", "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

def log_experiment(name, params, notes=""):
    """
    Log a Data Science experiment to experiments.csv.
    This is real DS hygiene for tracking model performance and configurations.
    """
    with open("experiments.csv", "a") as f:
        # CSV header: Timestamp, Experiment_Name, Parameters, Notes
        f.write(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},{name},\"{params}\",\"{notes}\"\n"
        )
