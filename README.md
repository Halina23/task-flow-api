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
