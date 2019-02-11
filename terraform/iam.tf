# IAM Role & Policies

resource "aws_iam_role" "iam_role_lambda" {
  name = "EC2CryptomaticRole"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "lambda_logging" {
  name        = "EC2Cryptomatic_lambda_logging"
  description = "IAM policy for logging from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "ec2_permissions" {
  name        = "EC2Cryptomatic_ec2_permissions"
  description = "EC2Cryptomatic EC2/EBS rights"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Stmt1504425390448",
            "Action": [
                "ec2:AttachVolume",
                "ec2:CopyImage",
                "ec2:CopySnapshot",
                "ec2:CreateSnapshot",
                "ec2:CreateVolume",
                "ec2:CreateTags",
                "ec2:DeleteSnapshot",
                "ec2:DeleteVolume",
                "ec2:DescribeInstances",
                "ec2:DescribeSnapshots",
                "ec2:DescribeVolumes",
                "ec2:DetachVolume",
                "ec2:ModifyInstanceAttribute"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = "${aws_iam_role.iam_role_lambda.name}"
  policy_arn = "${aws_iam_policy.lambda_logging.arn}"
}

resource "aws_iam_role_policy_attachment" "ec2_volumes" {
  role       = "${aws_iam_role.iam_role_lambda.name}"
  policy_arn = "${aws_iam_policy.ec2_permissions.arn}"
}
