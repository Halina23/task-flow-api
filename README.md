# TaskFlow API

Projeto para treinar DevOps com uma API FastAPI, Postgres, Docker Compose, Jenkins, Terraform, Prometheus e Grafana.

## Como rodar

```bash
cp .env.example .env
docker compose up -d --build
```

## Verificar

```bash
docker compose ps
docker compose logs app
```

Acesse:

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## Parar

```bash
docker compose down
```

## Testes

```bash
python3 -m pip install -r app/requirements.txt
python3 -m pytest app/test_main.py -v
```

## Terraform

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
```

### ## Aprendizados do projeto

Neste projeto, pratiquei um fluxo DevOps local completo, passando por versionamento com Git/GitHub, execução de infraestrutura com Terraform, criação e execução de containers com Docker Compose e automação de pipeline com Jenkins.

Também trabalhei com variáveis de ambiente usando `.env`, integração com banco PostgreSQL, execução de testes automatizados e troubleshooting de erros reais durante o processo.

Ferramentas utilizadas:
- Git e GitHub
- Docker e Docker Compose
- Terraform
- Jenkins
- FastAPI
- PostgreSQL
- Prometheus
- Grafana