# Lambda functions

data "archive_file" "layer_zip" {
  type        = "zip"
  source_dir  = "files/layer"
  output_path = "layer.zip"
}

data "archive_file" "archives_zip" {
  for_each = toset(
    [
      "files/ebs_take_snapshot.py",
      "files/ebs_encrypt_snapshot.py",
      "files/ebs_create_volume_from_snapshot.py",
      "files/ec2_swap_volumes.py",
      "files/ec2_extract_volumes.py",
      "files/ebs_cleanup_snapshot.py",
      "files/ec2_check_instance.py"
    ]
  )

  type        = "zip"
  source_file = each.value
  output_path = "${split("/", each.value)[1]}.zip"
}

resource "aws_lambda_layer_version" "lambda_layer" {
  filename   = "layer.zip"
  layer_name = "EC2Cryptomatic_BaseLibraryLayer"

  compatible_runtimes = ["python3.6", "python3.7"]
}

resource "aws_lambda_function" "take_snapshot" {
  filename      = "ebs_take_snapshot.py.zip"
  function_name = "EC2Cryptomatic_take_snapshot"
  layers        = [aws_lambda_layer_version.lambda_layer.arn]
  role          = aws_iam_role.iam_role_lambda.arn
  description   = "Take snapshot on existing EBS volumes"
  handler       = "ebs_take_snapshot.lambda_handler"
  runtime       = "python3.6"
  timeout       = var.lambda_timeout
}

resource "aws_lambda_function" "encrypt_snapshot" {
  filename      = "ebs_encrypt_snapshot.py.zip"
  function_name = "EC2Cryptomatic_encrypt_snapshot"
  layers        = [aws_lambda_layer_version.lambda_layer.arn]
  role          = aws_iam_role.iam_role_lambda.arn
  description   = "Encrypt an existing snapshot and encrypt it"
  handler       = "ebs_encrypt_snapshot.lambda_handler"
  runtime       = "python3.6"
  timeout       = var.lambda_timeout
}

resource "aws_lambda_function" "create_volume" {
  filename      = "ebs_create_volume_from_snapshot.py.zip"
  function_name = "EC2Cryptomatic_create_volume"
  layers        = [aws_lambda_layer_version.lambda_layer.arn]
  role          = aws_iam_role.iam_role_lambda.arn
  description   = "Create a new volume from an existing snapshot"
  handler       = "ebs_create_volume_from_snapshot.lambda_handler"
  runtime       = "python3.6"
  timeout       = var.lambda_timeout
}

resource "aws_lambda_function" "swap_volumes" {
  filename      = "ec2_swap_volumes.py.zip"
  function_name = "EC2Cryptomatic_swap_volumes"
  layers        = [aws_lambda_layer_version.lambda_layer.arn]
  role          = aws_iam_role.iam_role_lambda.arn
  description   = "Exchange volumes for a given instance"
  handler       = "ec2_swap_volumes.lambda_handler"
  runtime       = "python3.6"
  timeout       = var.lambda_timeout
}

resource "aws_lambda_function" "extract_volumes" {
  filename      = "ec2_extract_volumes.py.zip"
  function_name = "EC2Cryptomatic_extract_volumes"
  layers        = [aws_lambda_layer_version.lambda_layer.arn]
  role          = aws_iam_role.iam_role_lambda.arn
  description   = "Produce a EBS volume list from an instance ID"
  handler       = "ec2_extract_volumes.lambda_handler"
  runtime       = "python3.6"
  timeout       = var.lambda_timeout
}

resource "aws_lambda_function" "cleanup_snapshot" {
  filename      = "ebs_cleanup_snapshot.py.zip"
  function_name = "EC2Cryptomatic_cleanup"
  layers        = [aws_lambda_layer_version.lambda_layer.arn]
  role          = aws_iam_role.iam_role_lambda.arn
  description   = "Delete the encrypted snapshot and source volume"
  handler       = "ebs_cleanup_snapshot.lambda_handler"
  runtime       = "python3.6"
  timeout       = var.lambda_timeout
}

resource "aws_lambda_function" "check_instance" {
  filename      = "ec2_check_instance.py.zip"
  function_name = "EC2Cryptomatic_check_instance"
  layers        = [aws_lambda_layer_version.lambda_layer.arn]
  role          = aws_iam_role.iam_role_lambda.arn
  description   = "Check if the given instance is suitable for conversion"
  handler       = "ec2_check_instance.lambda_handler"
  runtime       = "python3.6"
  timeout       = var.lambda_timeout
}
