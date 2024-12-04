from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Read from .env
slack_token = os.getenv("SLACK_TOKEN")
bot_name = os.getenv("BOT_NAME")

# Initialize Slack client
client = WebClient(token=slack_token)


def test_auth():
    """
    Test Slack bot authentication and print basic details.
    """
    try:
        response = client.auth_test()
        print(f"Success! Bot Name: {response['user']}, Workspace: {response['team']}")
        return response
    except SlackApiError as e:
        print(f"Error during auth_test: {e.response['error']}")


def check_permissions():
    """
    Check the bot's permissions by listing available channels and users.
    """
    try:
        # Check channels
        print("\nChecking channels...")
        channels_response = client.conversations_list()
        print("Channels the bot can access:")
        for channel in channels_response["channels"]:
            print(f"- {channel['name']} (ID: {channel['id']})")

        # Check users
        print("\nChecking users...")
        users_response = client.users_list()
        print("Users in the workspace:")
        for user in users_response["members"]:
            print(f"- {user['name']} (ID: {user['id']})")
    except SlackApiError as e:
        if e.response["error"] == "missing_scope":
            print(f"Permission issue: {e.response['error']} - Add the required scopes.")
        else:
            print(f"Error during permissions check: {e.response['error']}")


if __name__ == "__main__":
    print("Running auth_test...")
    auth_info = test_auth()

    if auth_info:
        print("\nTesting permissions...")
        check_permissions()
