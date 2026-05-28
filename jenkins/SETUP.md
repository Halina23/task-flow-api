# Configuração do Jenkins — Passo a Passo

## 1. Subir o Jenkins

O Jenkins já está no `docker-compose.yml`.

Rode:

```bash
docker compose up -d jenkins
```

---

## 2. Acessar e desbloquear

Abra:

```text
http://localhost:8080
```

Pegue a senha inicial:

```bash
docker exec taskflow-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

---

## 3. Instalar plugins essenciais

Na tela **Customize Jenkins**, escolha:

```text
Install suggested plugins
```

Depois adicione:

* Docker Pipeline
* Docker plugin
* Pipeline: GitHub
* Credentials Binding

---

## 4. Configurar credenciais do DockerHub

Acesse:

```text
Jenkins → Manage Jenkins → Credentials → (global) → Add Credentials
```

Configure:

* Kind: Secret text
* ID: dockerhub-user → usuário DockerHub
* ID: dockerhub-password → senha/token DockerHub

---

## 5. Criar o Pipeline

Acesse:

```text
Jenkins → New Item
```

Configure:

* Nome: `taskflow-pipeline`
* Tipo: `Pipeline`

Em **Pipeline Definition**:

* Definition: Pipeline script from SCM
* SCM: Git
* Repository URL: URL do repositório GitHub
* Branch: `*/main`
* Script Path: `Jenkinsfile`

---

## 6. Configurar Webhook (Opcional)

No GitHub:

```text
Settings → Webhooks → Add webhook
```

Configure:

* Payload URL: `http://SEU_IP:8080/github-webhook/`
* Content type: `application/json`
* Events: `Push events`

---

## 7. Instalar Docker no container Jenkins

```bash
docker exec -u root taskflow-jenkins bash -c "
apt-get update &&
apt-get install -y docker.io &&
chmod 666 /var/run/docker.sock
"
```

---

## 8. Variáveis de Ambiente no Jenkins

Acesse:

```text
Manage Jenkins → Configure System → Global properties → Environment variables
```

Adicione:

```text
COMPOSE_PROJECT_NAME = taskflow
```
