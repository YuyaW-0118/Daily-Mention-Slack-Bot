variable "project_name" {
  type    = string
  default = "slack-random-mention-bot"
}

variable "region" {
  type    = string
  default = "ap-northeast-1"
}

variable "slack_channel_id" {
  type = string
}

variable "secret_name" {
  type    = string
  default = "slack-random-mention-bot"
}

variable "lambda_memory_mb" {
  type    = number
  default = 256
}

variable "lambda_timeout_s" {
  type    = number
  default = 15
}
