resource "aws_lambda_function" "bot" {
  function_name = var.project_name
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.lambda_handler"
  runtime       = "python3.11"
  timeout       = var.lambda_timeout_s
  memory_size   = var.lambda_memory_mb
  filename      = "${path.module}/../build/package.zip"
  source_code_hash = filebase64sha256("${path.module}/../build/package.zip")

  environment {
    variables = {
      slack_channel_id           = var.slack_channel_id
      secrets_manager_secret_name = var.secret_name
    }
  }
}
