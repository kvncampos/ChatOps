import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Initialize the Slack app
app = App(token=os.environ["SLACK_BOT_TOKEN"])

DEFAULT_SERVER = os.getenv("ENVIRONMENT", "http://localhost:3000")
DASHBOARD_SHORTCUTS = {"kafka": os.environ["KAFKA_DASHBOARD_NAME"]}

# Predefined shortcuts for graphs
GRAPH_SHORTCUTS = {
    "kafka": f"http://{DEFAULT_SERVER}/d/{DASHBOARD_SHORTCUTS["kafka"]}/",
    "prometheus": f"http://{DEFAULT_SERVER}/dashboard/file/Prometheus.json?orgId=1",
}

GRAFANA_RENDER_URL = os.getenv("GRAFANA_URL", DEFAULT_SERVER)
GRAFANA_API_KEY = os.getenv("GRAFANA_API_KEY", "")


# --- Feature 1: Respond to app mentions ---
@app.event("app_mention")
def handle_app_mention_events(body, say):
    user = body["event"]["user"]
    say(f"Hi there, <@{user}>! 👋 How can I assist you today?")


# --- Feature 2: List Graph Shortcuts ---
@app.command("/list_graphs")
def list_graphs(ack, say):
    ack()  # Acknowledge the command
    shortcuts = "\n".join(
        [f"- *{name}*: {url}" for name, url in GRAPH_SHORTCUTS.items()]
    )
    say(f"Here are the available graphs:\n{shortcuts}")


# --- Feature 3: Respond to Graph Commands ---
@app.command("/graph")
def generate_graph(ack, command, say):
    ack()  # Acknowledge the command
    graph_name = command["text"].strip().lower()
    if graph_name in GRAPH_SHORTCUTS:
        url = GRAPH_SHORTCUTS[graph_name]
        say(f"Here's the graph for *{graph_name}*:\n<{url}>")
    else:
        say(f"Sorry, I don't know the graph *{graph_name}*. Try `/list_graphs`.")


# --- Feature 4: Help Command ---
@app.command("/help")
def help_command(ack, say):
    ack()  # Acknowledge the command
    commands = """
    Here are the commands I understand:
    - `/list_graphs`: List available graph shortcuts.
    - `/graph <shortcut>`: Show a specific graph (e.g., `/graph kafka`).
    - `/download_graph <shortcut>`: Provides a Graph PNG.
    - `/help`: Show this help message.
    """
    say(commands)


# --- Feature 5: File Upload ---
@app.command("/download_graph")
def download_graph(ack, say, command):
    ack()  # Acknowledge the command
    graph_name = command["text"].strip().lower()

    # Check if the requested graph exists
    if graph_name in GRAPH_SHORTCUTS:
        # Generate the full URL for the dashboard
        dashboard_path = DASHBOARD_SHORTCUTS[graph_name]
        render_url = f"{GRAFANA_RENDER_URL}/render/d/{dashboard_path}"
        print(render_url)
        params = {
            "orgId": 1,
            "theme": "light",
            "width": 1000,
            "height": 1000,
        }
        headers = {"Authorization": f"Bearer {GRAFANA_API_KEY}"}

        try:
            # Fetch the PNG from Grafana
            response = requests.get(render_url, headers=headers, params=params)
            response.raise_for_status()  # Raise an error for HTTP issues

            # Save the PNG to a temporary file
            file_path = f"./graphs/{graph_name}.png"
            os.makedirs("./graphs", exist_ok=True)  # Ensure the directory exists
            with open(file_path, "wb") as file:
                file.write(response.content)

            # Upload the PNG to Slack using files_upload_v2
            app.client.files_upload_v2(
                file=file_path,  # Pass the file path here
                channel=command["channel_id"],
                title=f"{graph_name.capitalize()} Graph",
            )
            say(f"Uploaded the graph for *{graph_name}*.")

        except requests.RequestException as e:
            say(f"Failed to fetch the graph for *{graph_name}*. Error: {e}")

    else:
        say(f"Sorry, I don't have a graph for *{graph_name}*. Try `/list_graphs`.")


# --- Feature 6: Welcome Message ---
@app.event("team_join")
def welcome_new_user(body, say):
    user = body["event"]["user"]["id"]
    say(f"Welcome to the team, <@{user}>! 🎉 Let me know how I can help you!")


if __name__ == "__main__":
    # Start the Socket Mode handler
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
