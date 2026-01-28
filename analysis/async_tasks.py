import threading

def run_async(task, *args):
    """
    Simple threading wrapper to simulate asynchronous task execution.
    Professionals use this to keep the main UI thread responsive.
    """
    thread = threading.Thread(target=task, args=args)
    thread.daemon = True  # Ensure thread closes when main process exits
    thread.start()
