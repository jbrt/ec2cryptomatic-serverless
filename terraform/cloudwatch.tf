# CloudWatch LogGroup & log retention

resource "aws_cloudwatch_log_group" "lg_take_snapshot" {
  name              = "/aws/lambda/${aws_lambda_function.take_snapshot.function_name}"
  retention_in_days = "${var.log_retention}"
}
