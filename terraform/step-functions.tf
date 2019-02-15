# Creation of the State Machine

resource "aws_sfn_state_machine" "state_machine" {
  name     = "EC2Cryptomatic-state-machine"
  role_arn = "${aws_iam_role.iam_role_stepfunctions.arn}"
  tags     = "${local.tags}"

  definition = <<EOF
{
  "Comment": "EC2Cryptomatic state machine used for converting uncrypted volumes to encrypted ones",
  "StartAt": "TakeSnapshot",
  "States": {
    "TakeSnapshot": {
      "Type": "Task",
      "Resource": "${aws_lambda_function.take_snapshot.arn}",
      "Next": "EncryptSnapshot"
    },
    "EncryptSnapshot": {
      "Type": "Task",
      "Resource": "${aws_lambda_function.encrypt_snapshot.arn}",
      "Next": "CreateVolume"
    },
     "CreateVolume": {
      "Type": "Task",
      "Resource": "${aws_lambda_function.create_volume.arn}",
      "Next": "SwapVolume"
    },
    "SwapVolume": {
      "Type": "Task",
      "Resource": "${aws_lambda_function.swap_volumes.arn}",
      "End": true
    }
  }
}
EOF
}
