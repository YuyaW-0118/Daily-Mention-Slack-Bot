import random

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from credentials import get_settings


def get_channel_member_ids(client: WebClient, channel_id: str) -> list[str]:
    """
    Fetches the member IDs of a Slack channel.

    Args:
           client (WebClient): The Slack WebClient instance.
           channel_id (str): The ID of the Slack channel.
    """
    members: list[str] = []
    cursor = None
    while True:
        response = client.conversations_members(
            channel=channel_id, cursor=cursor, limit=1000
        )
        members.extend(response.get("members", []))
        cursor = response.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break
    return members


def choose_random_user(user_ids: list[str]) -> str:
    """
    Chooses a random user ID from the provided list.

    Args:
        user_ids (list[str]): List of user IDs.

    Returns:
        str: A randomly selected user ID.

    Raises:
        ValueError: If the user_ids list is empty.
    """

    if not user_ids:
        raise ValueError("The user_ids list is empty.")
    return random.choice(user_ids)


def post_message(client: WebClient, channel_id: str, text: str) -> None:
    """
    Posts a message to a Slack channel.

    Args:
        client (WebClient): The Slack WebClient instance.
        channel_id (str): The ID of the Slack channel.
        text (str): The message text to post.
    """
    try:
        client.chat_postMessage(
            channel=channel_id,
            text=text,
        )
    except SlackApiError as e:
        raise RuntimeError(f"Failed to post message: {e.response['error']}") from e


def lambda_handler(event, context):
    """
    AWS Lambda handler function.

    Args:
        event: The event data passed to the Lambda function.
        context: The context object provided by AWS Lambda.
    """
    settings = get_settings()
    client = WebClient(token=settings.slack_bot_token)

    channel_id = settings.slack_channel_id
    if not channel_id:
        return {
            "ok": False,
            "error": "SLACK_CHANNEL_ID is not set in environment variables.",
        }

    member_ids = get_channel_member_ids(client, channel_id)
    bot_user_id = client.auth_test()["user_id"]
    member_ids = [mid for mid in member_ids if mid != bot_user_id]
    if not member_ids:
        return {
            "ok": False,
            "error": "No members found in the specified Slack channel.",
        }

    chosen_user_id = choose_random_user(member_ids)
    chosen_user_id = "U07ACDNLLUD"

    message_text = f"[test] <@{chosen_user_id}>"
    post_message(client, channel_id, message_text)

    return {
        "ok": True,
        "message": f"Message posted to channel {channel_id} successfully.",
        "member_count": len(member_ids),
    }


if __name__ == "__main__":
    result = lambda_handler({}, {})
    print(result)
