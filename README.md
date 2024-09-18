# CountIt
Because it count's!


## Notes

**Gunicorn:** Gunicorn *can* start multiple instances of the service, but since this service functions as an **in-memory database for counters**, it is **not advisable to run it with more than one worker**. Running multiple workers would result in each worker having its own isolated memory, leading to inconsistent counter values across instances. To ensure the counters remain accurate, only a **single Gunicorn worker** should be used.