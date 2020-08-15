provider "aws" {
  region  = var.region
  version = "2.46"
}

provider "archive" {
  version = "1.3"
}

terraform {
  required_version = ">= 0.13"
}
