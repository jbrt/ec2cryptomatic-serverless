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
      "End": true
    }
  }
}
EOF
}
