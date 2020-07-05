# Input variables

variable "region" {
  description = "The AWS region where to deploy"
  default     = "eu-west-1"
}

variable "log_retention" {
  description = "Define the CloudWatch log retention"
  default     = 1
}

variable "lambda_timeout" {
  description = "The timout applyied on each Lambda function"
  default     = 900
}

locals {
  tags = {
    Project = "EC2Cryptomatic"
  }
}

