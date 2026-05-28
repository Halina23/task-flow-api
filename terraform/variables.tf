variable "db_name" {
  type    = string
  default = "taskflow"
}

variable "db_user" {
  type    = string
  default = "taskuser"
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "app_image" {
  type = string
}

variable "app_port" {
  type    = number
  default = 8000
}
