import threading

pause_event = threading.Event()
stop_event = threading.Event()

# Start unpaused
pause_event.set()
