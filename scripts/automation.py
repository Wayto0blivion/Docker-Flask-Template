"""
@author :   Zuicie
@date   :   November 22, 2024

Handles automated processed performed before git commit/push.
Includes migrations and unit testing.
"""

import subprocess
import sys
import os


def run_command(command, cwd=None):
    """Run a shell command to handle errors."""
    result = subprocess.run(command, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Command failed {command}")
        sys.exit(result.returncode)


def main():
    # Set cwd to the root of the project. Since this is inside the scripts folder, which is at the root,
    # we have to call dirname twice to get up to that level.
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Start Docker containers
    print("Starting Docker containers...")
    run_command("docker-compose up -d", cwd=cwd)

    # Run pytest unit tests
    print("Running unit tests....")
    run_command("pytest", cwd=cwd)

    # Run flask db migrate inside the Docker container. Ran inside the docker container so that file names
    # and structure remain consistent across containers.
    print("Running Database Migrations...")
    # Name of service from docker-compose.yml
    service_name = "web"
    # Set the FLASK_APP environment variable if needed.



