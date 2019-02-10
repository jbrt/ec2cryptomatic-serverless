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
  function_name    = "EC2Cryptomator_take_snaphot"
  role             = "${aws_iam_role.iam_role_lambda.arn}"
  description      = "Some AWS lambda"
  handler          = "ebs_take_snapshot.lambda_handler"
  runtime          = "python3.6"
  timeout          = 300
}
