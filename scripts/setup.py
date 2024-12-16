"""
@author :   Zuicie
@date   :   December 16, 2024

Ran when the template is ready to be used.
For initializing the template.
"""

import shutil
import os


def create_env_copy(filename):
    """
    Create a copy of example.env named .env for editing environment variables in a safer way.
    """
    # Determine the absolute path to the folder containing this script.
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    # The project root is one level up from scripts_dir.
    project_root = os.path.dirname(scripts_dir)

    source_file = os.path.join(project_root, f'example{filename}')
    dest_file = os.path.join(project_root, filename)

    # Check if example.env exists
    if not os.path.isfile(source_file):
        print(f"Error: {source_file} does not exist or could not be found.")
        return
    # If .env already exists, optionally warn or overwrite
    if os.path.isfile(dest_file):
        print(f"Error: {dest_file} already exists. It will be overwritten.")

    # Copy the file
    shutil.copyfile(source_file, dest_file)
    print(f"Copied {source_file} to {dest_file} successfully.")


if __name__ == "__main__":
    create_env_copy('.env')
    create_env_copy('.env.db')


