# 🏗️ Infrastructure as Code - Terraform & Deployment

**Version:** 1.3.0 | **Updated:** February 19, 2026 | **Part:** 7/9  
**Status:** Production Ready ✅  
**Purpose:** Define reproducible, version-controlled cloud infrastructure via code

---

## 📍 Purpose

This file teaches you to deploy AI agents to production using **Infrastructure as Code (IaC)** principles:

- **Never click cloud console buttons** (define everything in code)
- **Reproducible deployments** (same config = same result every time)
- **Version-controlled infrastructure** (track changes in Git)
- **Fast disaster recovery** (rebuild everything in 10 minutes)
- **Cost predictability** (know exactly what you're paying for)

**Core Philosophy:** "If it's not in Terraform, it doesn't exist in production."

---

## 🗺️ Quick Navigation

- [Philosophy & Why It Matters](#-philosophy--why-infrastructure-as-code-matters)
- [Cost Estimation by Tier](#-cost-estimation-by-tier)
- [File Structure](#-file-structure)
- [Terraform Basics](#-terraform-basics-5-min-intro)
- [Azure Container Apps Template](#-azure-container-apps-template)
- [Google Cloud Run Template](#-google-cloud-run-template)
- [Docker Compose (Local Dev)](#-docker-compose-local-development)
- [Kill Switch Patterns](#-kill-switch-patterns-mandatory)

---

## 🛑 Kill Switch Patterns (Mandatory)

For agents with a Risk Score of 11-17, you must implement an infrastructure-level kill switch that completely isolates the agent from the outside world without deleting the database.

**Terraform Implementation (AWS/GCP Network Isolation):**
Create a specific Security Group/VPC rule that drops all outbound traffic. In an emergency, apply this tag to the agent's container/instance. The agent can stay "on," but its requests to APIs or external targets will blackhole.

---

## 🐳 Docker Compose (Local Development)

Always define your local multi-agent environment alongside your observability stack so you can trace agent decisions before pushing to the cloud.

```yaml
version: '3.8'
services:
  agent-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/agents
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://jaeger:4317
    depends_on:
      - db
      - jaeger

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=agents
    ports:
      - "5432:5432"

  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686" # UI
      - "4317:4317"   # OTLP gRPC
```

---

## 🔧 Troubleshooting Deployment

If a deployment fails or an agent crashes in production, check in this exact order:
1. `terraform plan` (what changed?)
2. Cloud provider console (what does the infrastructure state show?)
3. Application logs / Jaeger traces (are they running?)
4. Environment variables (are the API keys/secrets mounted?)
5. Network (can the agent reach the database and external tools?)

---

## ✅ Deployment Checklist

### Before Production Deployment

- [ ] Terraform code reviewed and tested
- [ ] Docker image built, scanned for vulnerabilities
- [ ] Secrets stored in Key Vault / Secret Manager
- [ ] Database backups configured
- [ ] Monitoring and alerting configured
- [ ] Runbook written (how to deploy, rollback, troubleshoot)
- [ ] Team trained on Terraform workflow
- [ ] CI/CD pipeline configured

### After Deployment

- [ ] Verify application is running
- [ ] Test critical endpoints
- [ ] Check logs for errors
- [ ] Verify database connection
- [ ] Monitor resource usage
- [ ] Update `.claude-context.md` with deployment details

---

## 📌 File Meta

**Version:** 1.3.0  
**Released:** February 19, 2026  
**Status:** Production Ready ✅  
**Part of:** 9-Part AI Agent Framework  

**Next File:** [07_CONFIGURATION_CONTROL.md](./07_CONFIGURATION_CONTROL.md) (Cost controls)