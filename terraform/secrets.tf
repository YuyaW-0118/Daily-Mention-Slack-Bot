resource "aws_secretsmanager_secret" "slack" {
  name = var.secret_name
}

variable "slack_bot_token" {
  type      = string
  sensitive = true
}

resource "aws_secretsmanager_secret_version" "slack" {
  secret_id     = aws_secretsmanager_secret.slack.id
  secret_string = jsonencode({ SLACK_BOT_TOKEN = var.slack_bot_token })
}
