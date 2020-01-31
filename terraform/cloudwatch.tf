# CloudWatch LogGroup & log retention

resource "aws_cloudwatch_log_group" "lg_take_snapshot" {
  name              = "/aws/lambda/${aws_lambda_function.take_snapshot.function_name}"
  retention_in_days = var.log_retention
}

resource "aws_cloudwatch_log_group" "lg_encrypt_snapshot" {
  name              = "/aws/lambda/${aws_lambda_function.encrypt_snapshot.function_name}"
  retention_in_days = var.log_retention
}

resource "aws_cloudwatch_log_group" "lg_create_volume" {
  name              = "/aws/lambda/${aws_lambda_function.create_volume.function_name}"
  retention_in_days = var.log_retention
}

resource "aws_cloudwatch_log_group" "lg_swap_volumes" {
  name              = "/aws/lambda/${aws_lambda_function.swap_volumes.function_name}"
  retention_in_days = var.log_retention
}

resource "aws_cloudwatch_log_group" "lg_cleanup" {
  name              = "/aws/lambda/${aws_lambda_function.cleanup_snapshot.function_name}"
  retention_in_days = var.log_retention
}

resource "aws_cloudwatch_log_group" "lg_check_instance" {
  name              = "/aws/lambda/${aws_lambda_function.check_instance.function_name}"
  retention_in_days = var.log_retention
}

resource "aws_cloudwatch_log_group" "lg_extract_volumes" {
  name              = "/aws/lambda/${aws_lambda_function.extract_volumes.function_name}"
  retention_in_days = var.log_retention
}

