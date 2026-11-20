terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  skip_credentials_validation = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true
}