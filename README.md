# Service Desk API — DevOps na Prática (Fase 1)

API REST de chamados de suporte de TI usada como base para o projeto da disciplina
**DevOps na Prática**. Esta fase cobre a **configuração do pipeline de Integração
Contínua (GitHub Actions)**, **testes automatizados** e os **scripts de Infraestrutura como Código (Terraform/AWS)**.

## Estrutura

```
app/                  Código da API (FastAPI)
tests/                Testes automatizados (pytest) — unidade e API
infra/terraform/      Provisionamento AWS: VPC, ALB, ECS Fargate, ECR, RDS, Secrets Manager
.github/workflows/    Pipeline de CI (lint, testes, terraform validate, build Docker)
Dockerfile            Imagem da aplicação
```

## Executar localmente

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload        # http://localhost:8000/docs
pytest --cov                          # testes + cobertura
```

## Docker

```bash
docker build -t servicedesk-api .
docker run -p 8000:8000 servicedesk-api
```

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/health` | Health check (usado pelo ALB e pelo smoke test) |
| POST | `/tickets` | Abre um chamado (SLA calculado pela prioridade) |
| GET | `/tickets?status=` | Lista chamados, com filtro opcional |
| GET | `/tickets/{id}` | Detalha um chamado |
| PATCH | `/tickets/{id}/status` | Altera status (respeita as transições permitidas) |
| DELETE | `/tickets/{id}` | Remove um chamado |

## Pipeline de CI

Executado a cada push/PR em `main`, `develop` e `feature/**`:

1. **lint** — `ruff check` e `ruff format --check`
2. **test** — pytest em matriz Python 3.11/3.12, cobertura mínima de 80%, relatórios JUnit/Cobertura publicados como artefatos
3. **terraform** — `fmt -check`, `init -backend=false`, `validate`
4. **build** — build da imagem Docker e smoke test no endpoint `/health`

## Infraestrutura (Terraform)

```bash
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

Recursos: VPC com 2 AZs (sub-redes públicas e privadas, IGW, NAT), Application Load
Balancer, ECS Fargate com auto scaling por CPU, ECR com scan de imagens, RDS PostgreSQL
16 criptografado em sub-rede privada, senha no Secrets Manager e logs no CloudWatch.
