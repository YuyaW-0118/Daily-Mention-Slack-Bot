from __future__ import annotations
import json
import os
from functools import cached_property

import boto3
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AliasChoices


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="",
    )
    aws_region: str = Field(
        default="ap-northeast-1",
        validation_alias=AliasChoices("AWS_REGION", "aws_region"),
    )
    slack_channel_id: str = Field(
        default=os.getenv("SLACK_CHANNEL_ID", ""),
        validation_alias=AliasChoices("SLACK_CHANNEL_ID", "slack_channel_id"),
    )
    slack_bot_token_env: str | None = Field(
        default=None,
        validation_alias=AliasChoices("SLACK_BOT_TOKEN", "slack_bot_token_env"),
    )

    secrets_manager_secret_name: str = Field(default="slack-random-mention-bot")
    secret_key_slack_bot_token: str = Field(default="SLACK_BOT_TOKEN")

    @cached_property
    def slack_bot_token(self) -> str:
        """
        Retrieves the Slack bot token from AWS Secrets Manager.

        Returns:
            str: The Slack bot token.
        """
        if self.slack_bot_token_env:
            # If the environment variable is set, use it directly
            return self.slack_bot_token_env

        client = boto3.client("secretsmanager", region_name=self.aws_region)
        try:
            response = client.get_secret_value(
                SecretId=self.secrets_manager_secret_name
            )
            secret_str = response["SecretString"]
            secret = json.loads(secret_str)
            return secret.get(self.secret_key_slack_bot_token)
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve Slack bot token: {e}") from e


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
