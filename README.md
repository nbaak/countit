# CountIt
Because it count's!


## Notes

**Auth-Token**: The Auth-Token `auth.token` is generated in a file, making the app easier to debug and adaptable to environments beyond Docker. This approach allows developers to store tokens locally for testing or development purposes without needing to rely on environment-specific configurations. Another possible, and easy-to-implement, alternative is using `os.getenv`, which is ideal for handling sensitive information securely in production environments by leveraging environment variables. Both methods promote flexibility in deployment while maintaining ease of use and security.



**Gunicorn:** Gunicorn *can* start multiple instances of the service, but since this service functions as an **in-memory database for counters**, it is **not advisable to run it with more than one worker**. Running multiple workers would result in each worker having its own isolated memory, leading to inconsistent counter values across instances. To ensure the counters remain accurate, only a **single Gunicorn worker** should be used.

Source: https://flask.palletsprojects.com/en/3.0.x/deploying/gunicorn/