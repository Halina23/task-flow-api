output "app_url" {
  value = "http://localhost:${var.app_port}"
}

output "postgres_container" {
  value = docker_container.postgres.name
}
