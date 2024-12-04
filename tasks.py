import os
from invoke import task
import signal
import subprocess

# Define the path to the `development/` directory
DOCKER_COMPOSE_DIR = os.path.join(os.getcwd(), "development")


@task
def up(ctx):
    """Start and run the Docker Compose services in the development directory."""
    with ctx.cd(DOCKER_COMPOSE_DIR):
        ctx.run("docker-compose up -d")


@task
def detach(ctx, target="all"):
    """Stop and detach the Docker Compose services in the development directory."""
    with ctx.cd(DOCKER_COMPOSE_DIR):
        ctx.run(f"docker-compose stop {target} && docker-compose detach {target}")


@task
def stop(ctx, target="all"):
    """Stop the Docker Compose services in the development directory."""
    with ctx.cd(DOCKER_COMPOSE_DIR):
        ctx.run(f"docker-compose stop {target}")


@task
def destroy(ctx):
    """Destroy and remove all Docker Compose services in the development directory."""
    with ctx.cd(DOCKER_COMPOSE_DIR):
        ctx.run("docker-compose down -v")


# Store the bot process globally to manage it
bot_process = None


@task
def chat_start(ctx):
    """
    Start the Slack bot.
    """
    global bot_process

    # Define the path to the bot script
    bot_script = os.path.join(os.getcwd(), "bot.py")  # Adjust the path if needed

    # Start the bot using subprocess.Popen
    bot_process = subprocess.Popen(
        ["python", bot_script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print(f"Slack bot started with PID {bot_process.pid}")


@task
def chat_stop(ctx):
    """
    Stop the Slack bot if it's running.
    """
    global bot_process

    if bot_process is not None:
        print(f"Stopping Slack bot with PID {bot_process.pid}...")
        # Send the SIGTERM signal to the process
        bot_process.send_signal(signal.SIGTERM)
        bot_process.wait()  # Wait for the process to terminate
        print("Slack bot stopped.")
        bot_process = None
    else:
        print("Slack bot is not running.")


@task(help={"fix": "Apply fixes to linting and formatting issues (default: False)"})
def auto_format(ctx, fix=False):
    """
    Run ruff and black for linting and formatting.
    """
    # Determine the mode based on the --fix argument
    ruff_command = "ruff check . --fix" if fix else "ruff check ."
    black_command = "black ." if fix else "black --check ."

    # Run ruff
    print("Running ruff...")
    ctx.run(ruff_command, echo=True)

    # Run black
    print("Running black...")
    ctx.run(black_command, echo=True)
