# ── terraform.tfvars.example ──────────────────────────────────────
#  Copie para terraform.tfvars e preencha os valores
#  NUNCA commite o terraform.tfvars no repositório!
# ─────────────────────────────────────────────────────────────────

db_name     = "taskflow"
db_user     = "taskuser"
db_password = "troque_esta_senha_123"
app_image   = "seuusuario/taskflow-api:latest"
app_port    = 8000
