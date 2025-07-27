#!/usr/bin/env python3
import tomllib
# import sys
import os
import argparse
from datetime import datetime

# Define a list of directory names to ignore during traversal
# Add or remove directories here to customize which folders are skipped
DEFAULT_DIRECTORIES_TO_IGNORE = [".git", "__pycache__", "node_modules", "target", "build", "venv", ".vscode",]

# Define a list of full path segments to ignore
# This will cause the script to ignore any directory whose full path contains any of these stings
DEFAULT_PATHS_TO_IGNORE = ["/dotfiles/hyprland/themes/assets/"]  # Add more as needed

# report_file = "todo_report.txt"  # change to desired filename of report

# Add or remove extensions for files that will be checked
DEFAULT_TARGET_EXTENSIONS = [
    ".py", ".md", ".txt", ".js", ".ts", ".c", ".h", ".cpp", ".cs", ".java", ".rs", ".nix", ".toml", ".sh", ".yaml", ".yml", ".go", ".php", ".rb", ".css", ".html", ".xml"
]

found_todos = []

# fundamental python idioms
if __name__ == "__main__":

    # project_path = None

    # # sys.argv always contains script name as index 0
    # if len(sys.argv) == 1:  # exactly one argument
    #     project_path = os.getcwd()
    # elif len(sys.argv) == 2:  # exactly two arguments
    #     project_path = sys.argv[1]
    #     if not os.path.isdir:
    #         print(f"ERROR: invalid path: {sys.argv[1]}")
    #         sys.exit(1)
    # else:  # more than two arguments
    #     print("ERROR: only one optional argument accepted, use project directory")
    #     print(f"Usage: python {sys.argv[0]} [directory_path]")
    #     sys.exit(1)

    parser = argparse.ArgumentParser(
        description="A tool to find TODO/FIXME comments and generate a report."
    )
    parser.add_argument(
        "project_path",
        nargs="?",  # This makes it optional. If not provided, it will be None.
        default=os.getcwd(),  # Set default to CWD if not provided.
        help="The root directory of the project to scan. Defaults to the current working directory."
    )
    parser.add_argument(
        "--output",
        "-o",  # Short option for --output
        default="todo_report.txt",  # Default output filename
        help="The path and filename for the generated TODO/FIXME report. Defaults to 'todo_report.txt' in the current directory."
    )
    parser.add_argument(
        "--config",
        "-c",  # Short option for --config
        default="todo_reporter_config.toml",  # Default config file name
        help="Path to a TOML configuration file. Defaults to 'todo_reporter_config.toml' in the current directory."
    )
    args = parser.parse_args()

    # Initialize the lists with default values first
    directories_to_ignore = list(DEFAULT_DIRECTORIES_TO_IGNORE)  # Use list() to make them mutable copies
    target_extensions = list(DEFAULT_TARGET_EXTENSIONS)
    paths_to_ignore = list(DEFAULT_PATHS_TO_IGNORE)

    config_file_path = args.config

    try:
        with open(config_file_path, 'rb') as f:  # Open in binary mode ('rb') for tomllib
            config_data = tomllib.load(f)  # Load the TOML data

        # Now, try to get values from config_data and override defaults
        # For 'ignore.directories' in TOML -> directories_to_ignore in Python
        if 'ignore' in config_data:
            if 'directories' in config_data['ignore']:
                directories_to_ignore = config_data['ignore']['directories']
            if 'paths' in config_data['ignore']:
                paths_to_ignore = config_data['ignore']['paths']

        if 'target' in config_data:
            if 'extensions' in config_data['target']:
                target_extensions = config_data['target']['extensions']

        print(f"Loaded configuration from: {config_file_path}")  # Optional feedback

    except FileNotFoundError:
        print(f"Configuration file '{config_file_path}' not found. Using default settings.")
    except tomllib.TOMLDecodeError as e:  # Catch specific TOML parsing errors
        print(f"Error parsing configuration file '{config_file_path}': {e}. Using default settings.")
    except Exception as e:  # Catch any other unexpected errors
        print(f"An unexpected error occurred while reading config file: {e}. Using default settings.")

    print(f"Searching in: {args.project_path}")

    for (root, dirs, files) in os.walk(args.project_path, topdown=True):
        should_skip_root = False  # flag variable
        for bad_pattern in paths_to_ignore:
            if bad_pattern in root:
                should_skip_root = True  # Set flag
                break  # exit inner loop early

        if should_skip_root:  # check flag AFTER inner loop
            continue

        dirs[:] = [d for d in dirs if d not in directories_to_ignore]
        files[:] = [f for f in files if os.path.splitext(f)[1].lower() in target_extensions]
        for f in files:
            full_file_path = os.path.join(root, f)
            print(f"Processing file: {full_file_path}")  # User feedback: informs about current file being processed

            with open(full_file_path, 'r', encoding="utf-8") as file_handle:
                for line_number, current_line in enumerate(file_handle):
                    if "todo" in current_line.lower() or "fixme" in current_line.lower():
                        todo_entry = {
                            "filepath": full_file_path,
                            "line_number": line_number + 1,
                            "content": current_line.strip(),
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        found_todos.append(todo_entry)

    found_todos.sort(key=lambda item: item["filepath"])
    with open(args.output, 'w', encoding='utf-8') as report_file_handle:
        report_file_handle.write("--- ALL Collected TODOs/FIXMEs ---\n\n")
        for todo_entry in found_todos:
            report_file_handle.write(f"File: {todo_entry['filepath']}\n")
            report_file_handle.write(f"  Line: {todo_entry['line_number']}: {todo_entry['content']}\n")
            report_file_handle.write(f"  (Found: {todo_entry['timestamp']})\n")
            report_file_handle.write("-" * 40 + "\n")

    print(f"\nReport generated successfully in {args.output}")
