# CountIt
Because it count's!


## CountIt API Endpoints
This API provides endpoints for managing and tracking metrics. Authentication is required for most of the endpoints via an `Authorization` header.

### 1. Home

**Endpoint**: `/`  
**Method**: `GET`  
**Description**: Displays a random motivational phrase.  
**Authorization**: None

#### Response Example:
```json
"Count It! - You can Count on It!"
```



### 2. Test Connection

**Endpoint**: `/test`  
**Method**: `GET`  
**Description**: Tests the connection and returns current metrics if authorized.  
**Authorization**: Required (`Authorization` header)

#### Response Example (Success):
```json
{
  "success": {
    "metric_1": 100,
    "metric_2": 200
  }
}
```

#### Response Example (Unauthorized):
```json
{
  "error": "Access Denied"
}
```



### 3. Get Metrics

**Endpoint**: `/metrics`  
**Method**: `GET`  
**Description**: Retrieves the current metrics values.  
**Authorization**: Required (`Authorization` header)

#### Response Example:
```json
{
  "success": {
    "metric_1": 100,
    "metric_2": 200
  }
}
```



### 4. Add New Metric

**Endpoint**: `/new/<metric_name>`  
**Method**: `POST`  
**Description**: Adds a new metric if it does not already exist. You can also use the `overwrite` flag to overwrite an existing metric.  
**Authorization**: Required (`Authorization` header)  
**Body Parameters**:
- `overwrite` (boolean, optional) – Set to `true` to overwrite an existing metric.

#### Response Example (Created):
```json
{
  "success": "metric_1 created"
}
```

#### Response Example (Existing Metric):
```json
{
  "success": "metric_1 exists"
}
```



### 5. Update Metric

**Endpoints**:  
- `/inc/<metric_name>`  
- `/update/<metric_name>`  

**Method**: `POST`  
**Description**: Updates the value of a metric. You can also provide a label and value to update specific labels within a metric.  
**Authorization**: Required (`Authorization` header)  
**Body Parameters**:
- `label` (optional, defaults to `"__default_label__"`) – The label to update.
- `value` (optional, defaults to `1`) – The value to increment or set for the metric.

#### Response Example (Updated):
```json
{
  "success": 105
}
```



### 6. Get Labels of a Metric

**Endpoint**: `/labels/<metric_name>`  
**Method**: `GET`  
**Description**: Retrieves all labels associated with a specific metric.  
**Authorization**: Required (`Authorization` header)

#### Response Example:
```json
{
  "success": ["label1", "label2", "__default_label__"]
}
```



### 7. Get Value of a Specific Label

**Endpoint**: `/get/<metric_name>`  
**Method**: `POST`  
**Description**: Retrieves the value of a specific label within a metric.  
**Authorization**: Required (`Authorization` header)  
**Body Parameters**:
- `label` (optional, defaults to `"__default_label__"`) – The label to fetch the value for.

#### Response Example (Label Found):
```json
{
  "success": 50
}
```

#### Response Example (Label Not Found):
```json
{
  "error": "Label not found"
}
```


### 8. Delete Metric

**Endpoint**: `/delete/<metric_name>`  
**Method**: `POST`  
**Description**: Deletes a specific metric.  
**Authorization**: Required (`Authorization` header)

#### Response Example (Deleted):
```json
{
  "success": "metric_1 removed"
}
```



### 9. Sum All Labels of a Metric

**Endpoint**: `/sum/<metric_name>`  
**Method**: `GET`  
**Description**: Sums all the values of the labels for a specific metric. You can exclude the default label if desired.  
**Authorization**: Required (`Authorization` header)  
**Query Parameters**:
- `except_default` (optional) – Set to `true` to exclude the default label from the sum.

#### Response Example:
```json
{
  "success": 300
}
```



### 10. Get All Data of a Metric

**Endpoint**: `/data/<metric_name>`  
**Method**: `GET`  
**Description**: Retrieves all the data for a specific metric, including all labels and their values.  
**Authorization**: Required (`Authorization` header)

#### Response Example:
```json
{
  "success": [
    {"label": "label1", "value": 50},
    {"label": "label2", "value": 100}
  ]
}
```




## Notes

**Auth-Token**: The Auth-Token `auth.token` is generated in a file, making the app easier to debug and adaptable to environments beyond Docker. This approach allows developers to store tokens locally for testing or development purposes without needing to rely on environment-specific configurations. Another possible, and easy-to-implement, alternative is using `os.getenv`, which is ideal for handling sensitive information securely in production environments by leveraging environment variables. Both methods promote flexibility in deployment while maintaining ease of use and security.



**Gunicorn:** Gunicorn *can* start multiple instances of the service, but since this service functions as an **in-memory database for counters**, it is **not advisable to run it with more than one worker**. Running multiple workers would result in each worker having its own isolated memory, leading to inconsistent counter values across instances. To ensure the counters remain accurate, only a **single Gunicorn worker** should be used.

Source: https://flask.palletsprojects.com/en/3.0.x/deploying/gunicorn/