# OpsHub

OpsHub is a fictional operations portal built as a hands-on DevOps learning project.

The project simulates a small production-like environment with application runtime, containerization, automated testing, CI, monitoring, alerting and incident response.

All systems, services, data and incidents in this project are fictional.

## Current capabilities

- Python HTTP application
- Docker containerization
- Docker Compose orchestration
- Automated unit and HTTP tests
- Git and GitHub workflow
- GitHub Actions CI
- Prometheus metrics collection
- Grafana dashboard
- Grafana availability alert
- Incident simulation and recovery runbook
- Reproducible Grafana provisioning

## Architecture

```text
OpsHub application
        │
        ├── /health
        └── /metrics
                │
                ▼
          Prometheus
                │
                ▼
            Grafana
Services
Service
Description
Address
OpsHub
Python HTTP application
http://localhost:8000
Prometheus
Metrics collection and querying
http://localhost:9090
Grafana
Dashboards and alerting
http://localhost:3000
Run with Docker Compose
Create the local environment file:
Bash
cp .env.example .env
Start the complete stack:
Bash
docker compose up -d --build
Check the services:
Bash
docker compose ps
Test the application:
Bash
curl http://localhost:8000/health
curl http://localhost:8000/metrics
Check Prometheus:
Bash
curl http://localhost:9090/-/ready
View logs:
Bash
docker compose logs --tail=50
Stop the stack:
Bash
docker compose down
Grafana
Open:
text
http://localhost:3000
The project provisions automatically:
the Prometheus data source;
the OpsHub Overview dashboard;
the total requests panel;
the health checks panel;
the Grafana alert for OpsHub availability.
The dashboard and provisioning files are versioned under:
text
grafana/
Metrics
The application exposes Prometheus-compatible metrics:
text
opshub_requests_total
opshub_health_checks_total
opshub_uptime_seconds
The availability query used by Grafana is:
promql
up{job="opshub"}
Expected values:
text
1 = OpsHub available
0 = OpsHub unavailable
Tests
Run all tests:
Bash
python3 -m unittest discover -s tests -v
The GitHub Actions workflow runs the automated tests and Docker build on every relevant push and pull request.
Incident response
The availability alert follows this lifecycle:
text
Normal → Pending → Firing → Normal
To diagnose and recover an unavailable application, use:
text
docs/runbooks/opshub-unavailable.md
The runbook covers:
container status;
health endpoint verification;
metrics verification;
Prometheus target verification;
service recovery;
log inspection;
post-incident actions.
Project roadmap
Completed:
Linux and networking fundamentals
Application containerization
Automated tests
GitHub Actions CI
Prometheus metrics
Grafana dashboard
Availability alert
Incident simulation and recovery runbook
Planned:
Improve application structure
Add persistent application data
Add integration tests
Add log aggregation
Add Kubernetes deployment
Add infrastructure as code
Add more incident simulations
Create post-incident reports
Learning approach
OpsHub is developed incrementally using feature branches, pull requests, automated validation and documented operational procedures.
The goal is to practice real DevOps workflows while keeping the infrastructure safe, reproducible and easy to understand.
