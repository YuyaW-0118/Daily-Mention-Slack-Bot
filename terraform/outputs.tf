output "lambda_name" {
  value = aws_lambda_function.bot.function_name
}
output "secret_arn" {
  value = aws_secretsmanager_secret.slack.arn
}
