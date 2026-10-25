# Runbook: Service Unavailable

## Purpose

This runbook describes the initial checks to perform when the OpsHub service is unavailable.

## Initial checks

1. Confirm whether the container is running.
2. Check the container logs.
3. Verify the service health endpoint.
4. Check whether the expected port is listening.
5. Review the most recent change.

## Recovery

Do not restart the service blindly. First collect the relevant evidence:

- container status;
- recent logs;
- health-check response;
- recent deployment or configuration changes.

## Follow-up

If the service is restored, document:

- the observed symptom;
- the root cause;
- the recovery action;
- the preventive action.
