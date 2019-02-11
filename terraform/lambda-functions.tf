# Lambda functions

provider "aws" {
  region = "${var.region}"
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "files"
  output_path = "lambda.zip"
}

resource "aws_lambda_function" "take_snapshot" {
  filename         = "lambda.zip"
  source_code_hash = "${data.archive_file.lambda_zip.output_base64sha256}"
  function_name    = "EC2Cryptomatic_take_snapshot"
  role             = "${aws_iam_role.iam_role_lambda.arn}"
  description      = "Take snapshot on existing EBS volumes"
  handler          = "ebs_take_snapshot.lambda_handler"
  runtime          = "python3.6"
  timeout          = 300
}

resource "aws_lambda_function" "encrypt_snapshot" {
  filename         = "lambda.zip"
  source_code_hash = "${data.archive_file.lambda_zip.output_base64sha256}"
  function_name    = "EC2Cryptomatic_encrypt_snapshot"
  role             = "${aws_iam_role.iam_role_lambda.arn}"
  description      = "Encrypt an existing snapshot and encrypt it"
  handler          = "ebs_encrypt_snapshot.lambda_handler"
  runtime          = "python3.6"
  timeout          = 300
}
