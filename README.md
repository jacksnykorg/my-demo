# Snyk Vulnerable Demo Application: Task Prioritizer

⚠️ **Warning:** This application is intentionally insecure and is designed for demonstration purposes only. Do not deploy it to a production environment.

This repository contains a simple three-tier microservice application called "Task Prioritizer." Its purpose is to provide a realistic target for demonstrating the capabilities of the Snyk platform, with easily discoverable vulnerabilities across **Open Source dependencies**, **Application Code (SAST)**, and **Infrastructure as Code (IaC)**.

-----

## 🏛️ Application Architecture

The application consists of three services that work together:

  * **`frontend` (React/TypeScript)**: A web interface running on port `8080` (Docker) or `5173` (local) where a user can input a task title and description.
  * **`api` (Node.js/Express)**: The main backend service running on port `3000`. It receives requests from the frontend and communicates with the `risk-service` to get a score.
  * **`risk-service` (Python/FastAPI)**: A microservice running on port `8000` that performs a "risk calculation" based on the length of the task's text.

The data flow is simple: `Frontend` ➡️ `API` ➡️ `Risk Service`

-----

## 🎯 Intended Vulnerabilities for Snyk

This repository has been seeded with the following security issues for Snyk to discover.

| Snyk Product | Vulnerability Description | Location |
| :--- | :--- | :--- |
| **Snyk Open Source** | High Severity Prototype Pollution via an old version of `lodash`. | `frontend/package.json` |
| **Snyk Open Source** | Multiple vulnerabilities (e.g., XSS) via an old version of `express`. | `api/package.json` |
| **Snyk Open Source** | High Severity Sandbox Escape via an old version of `Jinja2` (transitive). | `risk-service/requirements.txt` |
| **Snyk Code** | Hardcoded Secret: A fake API key is committed directly into the source code. | `api/index.js` |
| **Snyk IaC / Container** | Base image `python:3.9` has known vulnerabilities and is non-minimal. | `risk-service/Dockerfile` |
| **Snyk IaC / Container** | The container is configured to run as the `root` user by default. | `risk-service/Dockerfile` |
| **Snyk IaC** | Kubernetes deployment manifest uses the insecure `:latest` image tag. | All files in `kubernetes/` |
| **Snyk IaC** | Kubernetes deployment is missing CPU/memory resource limits. | `kubernetes/api-deployment.yaml` |

-----

## 🚀 Running the Application

You can run the application using Docker (recommended for a full demo) or locally on your machine.

### Method 1: Using Docker (Recommended)

This is the easiest way to get all services running and is required for demonstrating Snyk Container scans.

**Prerequisites:**

  * Docker and Docker Compose installed.

**Instructions:**

1.  Clone this repository.
2.  Navigate to the root directory (`snyk-vulnerable-demo/`).
3.  Run the following command:
    ```bash
    docker-compose up --build
    ```
4.  Once all services are running, access the frontend at **`http://localhost:8080`**.

### Method 2: Running Locally (Without Docker)

This method is useful if you don't have Docker installed. You will need to run each service in a separate terminal.

**Prerequisites:**

  * Node.js installed.
  * Python 3 installed.

**Terminal 1: Start the `risk-service`**

```bash
cd risk-service
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Terminal 2: Start the `api` service**

1.  **❗️ Important:** Open `api/index.js` and change the `RISK_SERVICE_URL` to point to localhost:
    ```javascript
    // Change this line
    const RISK_SERVICE_URL = 'http://risk-service:8000/calculate';
    // To this
    const RISK_SERVICE_URL = 'http://localhost:8000/calculate';
    ```
2.  Now run the server:
    ```bash
    cd api
    npm install
    npm start
    ```

**Terminal 3: Start the `frontend`**

```bash
cd frontend
npm install
npm run dev
```

3.  Access the frontend at the URL provided in the terminal, usually **`http://localhost:5173`**.

-----

## 🔍 Running Snyk Scans

Once the code is on your machine, you can run Snyk scans from the root directory to find the vulnerabilities.

```bash
# Authenticate with Snyk (first time only)
snyk auth

# Find and fix open source vulnerabilities
snyk test

# Find security issues in your own code
snyk code test

# Find misconfigurations in Dockerfiles and Kubernetes manifests
snyk iac test

# Find vulnerabilities in a container image (requires building it first)
docker build -t my-demo/api:latest ./api
snyk container test my-demo/api:latest --file=api/Dockerfile
```