# Creation of the State Machine

resource "aws_sfn_state_machine" "state_machine" {
  name     = "EC2Cryptomatic-state-machine"
  role_arn = aws_iam_role.iam_role_stepfunctions.arn
  tags     = local.tags

  definition = <<EOF
{
  "Comment": "EC2Cryptomatic state machine used for converting uncrypted volumes to encrypted ones",
  "StartAt": "CheckInstance",
  "States": {
    "CheckInstance": {
      "Type": "Task",
      "Resource": "${aws_lambda_function.check_instance.arn}",
      "Comment": "Check if instance is suitable for conversion",
      "Next": "ExtractVolumes",
      "Catch": [
        {
          "ErrorEquals": ["InstanceNotSuitable"],
          "ResultPath": "$.error",
          "Next": "Done"
        }
      ]
    },
    "ExtractVolumes": {
      "Type": "Task",
      "Resource": "${aws_lambda_function.extract_volumes.arn}",
      "Comment": "Extract of the EBS volumes from the given instance and create a list",
      "Next": "CheckForMoreVolumes"
    },
    "CheckForMoreVolumes": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.has_elements",
          "BooleanEquals": true,
          "Next": "TakeSnapshot"
        }
      ],
      "Default": "Done"
    },
    "TakeSnapshot": {
      "Type": "Task",
      "Resource": "${aws_lambda_function.take_snapshot.arn}",
      "Comment": "Take a snapshot of the given EBS volume",
      "Next": "EncryptSnapshot"
    },
    "EncryptSnapshot": {
      "Type": "Task",
      "Resource": "${aws_lambda_function.encrypt_snapshot.arn}",
      "Comment": "Encrypt a given snapshot",
      "Next": "CreateVolume"
    },
    "CreateVolume": {
      "Type": "Task",
      "Resource": "${aws_lambda_function.create_volume.arn}",
      "Comment": "Create a new volume from the given snapshot",
      "Next": "SwapVolumeIntoInstance"
    },
    "SwapVolumeIntoInstance": {
      "Type": "Task",
      "Resource": "${aws_lambda_function.swap_volumes.arn}",
      "Comment": "Exchange a volume by an another for the given instance",
      "Next": "Cleanup"
    },
     "Cleanup": {
      "Type": "Task",
      "Resource": "${aws_lambda_function.cleanup_snapshot.arn}",
      "Comment": "Delete the encrypted snapshot and source volume if delete_source True",
      "Next": "CheckForMoreVolumes"
    },
    "Done": {
      "Type": "Pass",
      "End": true
    }
  }
}
EOF

}

