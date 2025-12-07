# Deployment Research: Cloudflare Containers vs Google Cloud Run

## Decision

**Stack**: FastAPI + Docker Container

**Options**: Cloudflare Containers vs Google Cloud Run

---

## Quick Comparison

| Feature | Cloudflare Containers | Google Cloud Run |
|---------|----------------------|------------------|
| **Status** | Public beta (June 2025) | Production-ready |
| **Global** | 320+ cities | 35+ regions |
| **Scale to zero** | Yes | Yes |
| **Cold starts** | Minimal (edge) | ~1-2s (can use min-instances) |
| **Billing** | Per 10ms | Per 100ms |
| **Base cost** | $5/month (Workers Paid) | Free tier available |
| **Free tier** | Limited | 180,000 vCPU-seconds/month |
| **FastAPI support** | Yes (Docker) | Yes (native) |
| **Deploy command** | `wrangler deploy` | `gcloud run deploy` |

---

## Cloudflare Containers

### Overview

- Launched public beta June 24, 2025
- Run Docker containers on Cloudflare's edge network
- Workers act as API gateway in front of containers
- Deploy once, run globally ("Region: Earth")

### Instance Types

| Type | RAM | vCPU | Use Case |
|------|-----|------|----------|
| dev | 256 MB | 1/16 | Testing |
| basic | 1 GB | 0.25 | Light workloads |
| standard | 4 GB | 0.5 | Production |

### Pricing

- $5/month Workers Paid plan required
- Billed per 10ms of active runtime
- Scale to zero (no charge when idle)
- Charges: vCPU + RAM + Disk + Requests + Egress

### Deployment

```bash
# wrangler.toml
[[containers]]
name = "api"
image = "./Dockerfile"

# Deploy
wrangler deploy
```

### FastAPI Example

See: https://github.com/abyesilyurt/fastapi-on-cloudflare-containers

```typescript
// Worker routes to container
export default {
  async fetch(request, env) {
    const container = await env.API.start();
    return container.fetch(request);
  }
};
```

### Pros

- Edge deployment (320+ cities = low latency globally)
- Simple `wrangler deploy` workflow
- Integrates with Workers, KV, R2, D1
- 10ms billing granularity

### Cons

- Still in beta
- Limited instance sizes (max 4GB RAM, 0.5 vCPU)
- Requires Workers as gateway layer
- Newer ecosystem, less documentation

---

## Google Cloud Run

### Overview

- Fully managed, production-ready
- Auto-scales containers based on traffic
- Deploy from source or Docker image
- Integrated with GCP ecosystem

### Pricing

| Resource | Cost |
|----------|------|
| vCPU | $0.000024/vCPU-second (~$0.086/hour) |
| Memory | $0.0000025/GiB-second |
| Requests | $0.40/million (after free tier) |

### Free Tier

- 180,000 vCPU-seconds/month (~50 hours)
- 360,000 GiB-seconds/month
- 2 million requests/month

### Deployment

```bash
# Build and deploy
gcloud run deploy api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

### Cold Start Optimization

```dockerfile
# Multi-stage build for smaller image
FROM python:3.12-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.12-slim
COPY --from=builder /root/.local /root/.local
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

```bash
# Keep instances warm (costs more)
gcloud run services update api --min-instances=1
```

### Pros

- Production-ready, battle-tested
- Generous free tier
- Native FastAPI quickstart docs
- Up to 8 vCPU, 32GB RAM
- Integrated with Gemini API, Vertex AI

### Cons

- Cold starts (~1-2s without min-instances)
- 100ms billing granularity
- Single region per deployment (not global edge)
- GCP complexity

---

## Cost Comparison

### Scenario: 50M requests/month, 500ms avg response

| Platform | Estimated Cost |
|----------|---------------|
| Cloudflare Containers | ~$XX (competitive) |
| Google Cloud Run | ~$XX |

Cloudflare claims similar or slightly lower than Cloud Run.

### Scenario: Low traffic (hobby/dev)

| Platform | Cost |
|----------|------|
| Cloudflare | $5/month base |
| Cloud Run | $0 (within free tier) |

---

## Recommendation

### Choose Cloudflare Containers if:

- Need global edge deployment (low latency worldwide)
- Already using Cloudflare (Workers, R2, D1)
- Want simple `wrangler deploy` workflow
- Comfortable with beta software
- Workload fits in 4GB RAM / 0.5 vCPU

### Choose Google Cloud Run if:

- Need production stability
- Want generous free tier for development
- Need more resources (up to 8 vCPU, 32GB RAM)
- Using GCP services (Vertex AI, Gemini API)
- Need mature monitoring/logging

---

## For Vibe Coding Tool (agent-tools)

### Requirements

| Need | Cloudflare | Cloud Run |
|------|------------|-----------|
| Run FastAPI | Yes | Yes |
| Execute generated code | Limited (4GB) | Yes (32GB) |
| Run pytest/ruff/mypy | Yes | Yes |
| SSE streaming | Yes | Yes |
| LLM API calls | Yes | Yes (native Gemini) |
| Global low latency | Better | Good |
| Free dev tier | No ($5 min) | Yes |

### My Pick: **Google Cloud Run**

**Reasons:**
1. Free tier for development
2. More resources for code execution/evaluation
3. Native Gemini API integration (for competition)
4. Production-ready (no beta surprises)
5. Better docs for FastAPI

**Consider Cloudflare if:**
- Competition judges value global edge deployment
- Want to demo "deploy anywhere" capability

---

## Sources

- [Cloudflare Containers Docs](https://developers.cloudflare.com/containers/)
- [Cloudflare Containers Pricing](https://developers.cloudflare.com/containers/pricing/)
- [Cloudflare Containers Announcement](https://blog.cloudflare.com/containers-are-available-in-public-beta-for-simple-global-and-programmable/)
- [FastAPI on Cloudflare Containers](https://github.com/abyesilyurt/fastapi-on-cloudflare-containers)
- [Google Cloud Run FastAPI Quickstart](https://docs.cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-fastapi-service)
- [Cloud Run Performance Tuning](https://davidmuraya.com/blog/fastapi-performance-tuning-on-google-cloud-run/)
- [Cloudflare vs Cloud Run Pricing](https://hamy.xyz/blog/2025-04_cloudflare-containers-comparison)
- [Cloud Run Pricing Guide 2025](https://cloudchipr.com/blog/cloud-run-pricing)
