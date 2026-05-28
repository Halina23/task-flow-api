resource "docker_network" "taskflow" {
  name = "taskflow-terraform-net"
}

resource "docker_volume" "postgres_data" {
  name = "taskflow-postgres-data"
}

resource "docker_container" "postgres" {
  name  = "taskflow-tf-postgres"
  image = "postgres:16-alpine"

  env = [
    "POSTGRES_DB=${var.db_name}",
    "POSTGRES_USER=${var.db_user}",
    "POSTGRES_PASSWORD=${var.db_password}"
  ]

  volumes {
    volume_name    = docker_volume.postgres_data.name
    container_path = "/var/lib/postgresql/data"
  }

  networks_advanced {
    name = docker_network.taskflow.name
  }
}

resource "docker_container" "app" {
  name  = "taskflow-tf-app"
  image = var.app_image

  ports {
    internal = 8000
    external = var.app_port
  }

  env = [
    "DB_HOST=${docker_container.postgres.name}",
    "DB_PORT=5432",
    "DB_NAME=${var.db_name}",
    "DB_USER=${var.db_user}",
    "DB_PASSWORD=${var.db_password}"
  ]

  networks_advanced {
    name = docker_network.taskflow.name
  }

  depends_on = [docker_container.postgres]
}
