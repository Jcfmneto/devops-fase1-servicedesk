terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.80"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }

  # Estado remoto (habilitar após criar o bucket/tabela de lock):
  # backend "s3" {
  #   bucket         = "servicedesk-tfstate"
  #   key            = "fase1/terraform.tfstate"
  #   region         = "us-east-1"
  #   dynamodb_table = "servicedesk-tflock"
  #   encrypt        = true
  # }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = var.project
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}
