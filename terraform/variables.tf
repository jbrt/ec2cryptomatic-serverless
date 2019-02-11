# Input variables

variable "region" {
  description = "The AWS region where to deploy"
  default     = "eu-west-1"
}

variable "log_retention" {
  description = "Define the CloudWatch log retention"
  default     = 1
}
