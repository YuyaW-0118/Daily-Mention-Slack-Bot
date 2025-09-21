# MON-FRI 00:30 UTC（= JST 09:30）
resource "aws_cloudwatch_event_rule" "weekday_0930_jst" {
  name                = "${var.project_name}-schedule"
  schedule_expression = "cron(30 0 ? * MON-FRI *)"
  description         = "Weekdays 09:30 JST (00:30 UTC)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.weekday_0930_jst.name
  target_id = "lambda"
  arn       = aws_lambda_function.bot.arn
}

resource "aws_lambda_permission" "allow_events" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.bot.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.weekday_0930_jst.arn
}
