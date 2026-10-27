# Runbook: OpsHub Unavailable

## Objetivo

Este runbook descreve como diagnosticar e recuperar a aplicação OpsHub quando o alerta `OpsHub unavailable` entrar em estado `Firing` no Grafana.

## Sintomas

O alerta pode indicar:

- o container da aplicação está parado;
- a aplicação não está respondendo na porta 8000;
- o Prometheus não consegue coletar `/metrics`;
- o alvo `opshub` aparece como indisponível no Prometheus.

## Arquitetura

```text
OpsHub
  │
  ├── /health
  └── /metrics
          │
          ▼
      Prometheus
          │
          ▼
       Grafana
