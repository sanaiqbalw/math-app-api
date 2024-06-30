# Backend-engineer-math-app-main:V1.0.0

## Overview of the Repo

This project delivers an api for calculating p-values for employee compensation analysis based on department data.

## Project Contents

Project is laid out in a single folder containing:
1. app.py - API script, serves API on server $PORT env variable
2. pvalue.py -functions that drive the API request
3. config.py -with Global Variables
4. utils.py - logger set up
5. employees.db -sqlite database containing the data
6. Additionally for API deployment - dockerfile and requirements.txt
   
## API Description

**GET /pvalue/**

**_Description:_** Retrieves the p-value for the specified department.

**_Input:_** Accepts a query parameter *department* which specifies the department name.

**_Responses:_**

- **200 OK:** Returns a JSON object containing the p-value, e.g.:
  
```
{"pvalue":0.334}
```
- **400 Bad Request:** Triggered if there's a validation error with the data.
- **404 Not Found** Triggered if no data is found for the specified department.
- **500 Internal Server Error:** Indicates a server-side error during the p-value calculation process, responding with a general error message

## Setup & Installation

**Prerequisites:**
- Docker installed on your machine.
- Git (for cloning the repository).

### 1. Clone the repository to your local machine. Open a terminal and run:

```bash
git clone https://github.com/sanaiqbalw/math-app-api.git
cd math-app-api
```
Check if there is a PORT ENV variable set:
```
echo "$PORT"
```

If not, and you want to set the PORT to say 5000, run:
```
export PORT=5000
```
### 2. API deployment on the local environment
Run these from your terminal.

```bash
chmod +x deploy.sh    [for any permission issues]
./deploy.sh

```
This deploys the API at the specified port, if you do not specify any port it defaults to 8000 port.

### 3. To stop and remove the container after deployment:

**NOTE: Dont shut down the API, before testing**

```bash
./shut.sh
chmod +x shut.sh [for any permission issues]
```


### 3. Using the API once deployed:


**Curl from terminal:**


_Note: If you did not set the PORT variable(let it default or set a different port altogether) or you are running curl from a new window, you have to set the port again or use the exact PORT number in the curl (Because curl is again reading the PORT variable from env if not provided)._

```
curl -X 'GET' "http://localhost:$PORT/pvalue"

curl -X 'GET' "http://localhost:$PORT/pvalue?department=Engineering"

# Sample Output: {"pvalue":0.334}

if you run into port issues -export PORT=xxxx for the port that your are planing to use.
```

**In the browser:**
```
http://0.0.0.0:<USE YOUR PORT VALUE>/pvalue

http://0.0.0.0:<USE YOUR PORT VALUE>/pvalue?department=Engineering

# Sample Output: {"pvalue":0.334}
```

**Python:**

```python
import requests
import os
os.environ['PORT'] = '3000' 
BASE_URL = f"http://localhost:{os.getenv('PORT')}"
response = requests.get(f"{BASE_URL}/pvalue", params={"department": "Engineering"})
print(response.json())

# Sample Output: {"pvalue":0.334}
```


**Additionally**

**If you want to check the logs in the container:**
```bash
docker logs math-app-api-con
```

**If you want to get into the container:**
```bash
docker exec -it logs math-app-api-con bash
```
