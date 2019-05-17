# Lambda functions

# WARNING: the 2.x version of the AWS Terraform provider has introducing some 
# breaking chances into the syntax of a lot of objects.
# https://www.terraform.io/docs/providers/aws/guides/version-2-upgrade.html

provider "aws" {
  region  = "${var.region}"
  version = "1.60.0"
}

data "archive_file" "layer_zip" {
  type        = "zip"
  source_dir  = "files/layer"
  output_path = "layer.zip"
}

data "archive_file" "take_snapshot_zip" {
  type        = "zip"
  source_file = "files/ebs_take_snapshot.py"
  output_path = "take_snapshot.zip"
}

data "archive_file" "encrypt_snapshot_zip" {
  type        = "zip"
  source_file = "files/ebs_encrypt_snapshot.py"
  output_path = "encrypt_snapshot.zip"
}

data "archive_file" "create_volume_zip" {
  type        = "zip"
  source_file = "files/ebs_create_volume_from_snapshot.py"
  output_path = "create_volume.zip"
}

data "archive_file" "swap_volumes_zip" {
  type        = "zip"
  source_file = "files/ec2_swap_volumes.py"
  output_path = "swap_volumes.zip"
}

data "archive_file" "extract_volumes_zip" {
  type        = "zip"
  source_file = "files/ec2_extract_volumes.py"
  output_path = "extract_volumes.zip"
}

data "archive_file" "cleanup_snapshot_zip" {
  type        = "zip"
  source_file = "files/ebs_cleanup_snapshot.py"
  output_path = "cleanup_snapshot.zip"
}

data "archive_file" "check_instance_zip" {
  type        = "zip"
  source_file = "files/ec2_check_instance.py"
  output_path = "check_instance.zip"
}

resource "aws_lambda_layer_version" "lambda_layer" {
  filename   = "layer.zip"
  layer_name = "EC2Cryptomatic_BaseLibraryLayer"

  compatible_runtimes = ["python3.6", "python3.7"]
}

resource "aws_lambda_function" "take_snapshot" {
  filename         = "take_snapshot.zip"
  source_code_hash = "${data.archive_file.take_snapshot_zip.output_base64sha256}"
  function_name    = "EC2Cryptomatic_take_snapshot"
  layers           = ["${aws_lambda_layer_version.lambda_layer.layer_arn}"]
  role             = "${aws_iam_role.iam_role_lambda.arn}"
  description      = "Take snapshot on existing EBS volumes"
  handler          = "ebs_take_snapshot.lambda_handler"
  runtime          = "python3.6"
  timeout          = "${var.lambda_timeout}"
}

resource "aws_lambda_function" "encrypt_snapshot" {
  filename         = "encrypt_snapshot.zip"
  source_code_hash = "${data.archive_file.encrypt_snapshot_zip.output_base64sha256}"
  function_name    = "EC2Cryptomatic_encrypt_snapshot"
  layers           = ["${aws_lambda_layer_version.lambda_layer.layer_arn}"]
  role             = "${aws_iam_role.iam_role_lambda.arn}"
  description      = "Encrypt an existing snapshot and encrypt it"
  handler          = "ebs_encrypt_snapshot.lambda_handler"
  runtime          = "python3.6"
  timeout          = "${var.lambda_timeout}"
}

resource "aws_lambda_function" "create_volume" {
  filename         = "create_volume.zip"
  source_code_hash = "${data.archive_file.create_volume_zip.output_base64sha256}"
  function_name    = "EC2Cryptomatic_create_volume"
  layers           = ["${aws_lambda_layer_version.lambda_layer.layer_arn}"]
  role             = "${aws_iam_role.iam_role_lambda.arn}"
  description      = "Create a new volume from an existing snapshot"
  handler          = "ebs_create_volume_from_snapshot.lambda_handler"
  runtime          = "python3.6"
  timeout          = "${var.lambda_timeout}"
}

resource "aws_lambda_function" "swap_volumes" {
  filename         = "swap_volumes.zip"
  source_code_hash = "${data.archive_file.swap_volumes_zip.output_base64sha256}"
  function_name    = "EC2Cryptomatic_swap_volumes"
  layers           = ["${aws_lambda_layer_version.lambda_layer.layer_arn}"]
  role             = "${aws_iam_role.iam_role_lambda.arn}"
  description      = "Exchange volumes for a given instance"
  handler          = "ec2_swap_volumes.lambda_handler"
  runtime          = "python3.6"
  timeout          = "${var.lambda_timeout}"
}

resource "aws_lambda_function" "extract_volumes" {
  filename         = "extract_volumes.zip"
  source_code_hash = "${data.archive_file.extract_volumes_zip.output_base64sha256}"
  function_name    = "EC2Cryptomatic_extract_volumes"
  layers           = ["${aws_lambda_layer_version.lambda_layer.layer_arn}"]
  role             = "${aws_iam_role.iam_role_lambda.arn}"
  description      = "Produce a EBS volume list from an instance ID"
  handler          = "ec2_extract_volumes.lambda_handler"
  runtime          = "python3.6"
  timeout          = "${var.lambda_timeout}"
}

resource "aws_lambda_function" "cleanup_snapshot" {
  filename         = "cleanup_snapshot.zip"
  source_code_hash = "${data.archive_file.cleanup_snapshot_zip.output_base64sha256}"
  function_name    = "EC2Cryptomatic_cleanup"
  layers           = ["${aws_lambda_layer_version.lambda_layer.layer_arn}"]
  role             = "${aws_iam_role.iam_role_lambda.arn}"
  description      = "Delete the encrypted snapshot and source volume"
  handler          = "ebs_cleanup_snapshot.lambda_handler"
  runtime          = "python3.6"
  timeout          = "${var.lambda_timeout}"
}

resource "aws_lambda_function" "check_instance" {
  filename         = "check_instance.zip"
  source_code_hash = "${data.archive_file.check_instance_zip.output_base64sha256}"
  function_name    = "EC2Cryptomatic_check_instance"
  layers           = ["${aws_lambda_layer_version.lambda_layer.layer_arn}"]
  role             = "${aws_iam_role.iam_role_lambda.arn}"
  description      = "Check if the given instance is suitable for conversion"
  handler          = "ec2_check_instance.lambda_handler"
  runtime          = "python3.6"
  timeout          = "${var.lambda_timeout}"
}
