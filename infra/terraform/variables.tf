variable "project" {
  description = "Nome do projeto (prefixo dos recursos)"
  type        = string
  default     = "servicedesk"
}

variable "environment" {
  description = "Ambiente (dev, staging, prod)"
  type        = string
  default     = "dev"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment deve ser dev, staging ou prod."
  }
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "vpc_cidr" {
  type    = string
  default = "10.20.0.0/16"
}

variable "az_count" {
  description = "Quantidade de zonas de disponibilidade"
  type        = number
  default     = 2
}

variable "container_port" {
  type    = number
  default = 8000
}

variable "image_tag" {
  description = "Tag da imagem no ECR (o pipeline usa o SHA do commit)"
  type        = string
  default     = "latest"
}

variable "task_cpu" {
  type    = number
  default = 256
}

variable "task_memory" {
  type    = number
  default = 512
}

variable "desired_count" {
  type    = number
  default = 2
}

variable "db_instance_class" {
  type    = string
  default = "db.t4g.micro"
}

variable "db_username" {
  type    = string
  default = "servicedesk"
}
