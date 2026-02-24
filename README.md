# todo-fixme-reporter

A Python tool to consolidate TODO/FIXME comments and notes from code projects into a single report.

---

### What it Does

Are you tired of TODO/FIXME comments getting lost in the depths of your codebase? `todo-fixme-reporter` recursively scans your project directory for these crucial markers (and more!), aggregating them into a single, organized report file. Gain immediate oversight of all your outstanding tasks and scattered notes, grouped by file for quick navigation.

### Key Features

* **Recursive Project Scanning:** Scans all files and subdirectories within a specified project root.
* **Customizable Filtering:** Easily define which directories and file extensions to ignore or target.
* **TOML Configuration:** Configure ignore lists and target extensions via an external, human-readable TOML file, without editing the script's source code.
* **Dynamic Report Output:** Specify the report filename and path via command-line arguments.
* **Structured Output:** Generates a clean, sorted report with file path, line number, content, and timestamp for each entry.
* **Nix Packaging:** Available as a reproducible Nix app, ensuring consistent execution across any system with the Nix package manager.

---

### How to Run

This tool can be run as a standard Python script or as a seamlessly integrated Nix application.

**Common Usage:**

```bash
# Scan the current directory and generate report.txt
todo-reporter-cli .

# Scan a specific project directory
todo-reporter-cli /path/to/my/project/

# Scan a project and save report to a custom file
todo-reporter-cli /path/to/my/project/ -o my-project-todos.txt

# Scan with a custom configuration file
todo-reporter-cli . --config my_custom_settings.toml
```

---

**Non-Nix Users:**

(Requires Python 3.11+ for built-in TOML support, or Python 3.8+ with pip install toml)

Clone the repository:
```bash
git clone https://github.com/AndariiDev/todo-fixme-reporter.git

cd todo-fixme-reporter
```

Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
# If using Python < 3.11, install 'toml':
# pip install toml
```

Run the script:
```bash
python reporter.py [PROJECT_PATH] [--output <filename>] [--config <config_file>]

[PROJECT_PATH]: (Optional) The root directory to scan. Defaults to the current working directory.

--output <filename>, -o <filename>: (Optional) The path and filename for the generated report. Defaults to todo_report.txt in the current working directory.

--config <config_file>, -c <config_file>: (Optional) Path to a TOML configuration file. Defaults to todo_reporter_config.toml in the current working directory.
```

---

**Nix Users:**
(Requires Nix Flakes enabled: nix-command and flakes experimental features)

Run directly (from anywhere):

- From your cloned repository:
```bash
    cd /path/to/your/cloned/todo-fixme-reporter
    nix run . [PROJECT_PATH] [--output <filename>] [--config <config_file>]
```

- Without cloning (references your GitHub repo):
```bash
nix run github:AndariiDev/todo-fixme-reporter [PROJECT_PATH] [--output <filename>] [--config <config_file>]

Example: nix run github:AndariiDev/todo-fixme-reporter ~/my-dev-project -o ~/my-dev-project/project-todos.txt
```

Install to your PATH (for global access):

```bash
nix profile install github:AndariiDev/todo-fixme-reporter
```

Once installed, you can run the tool from any directory:
```bash
todo-reporter-cli [PROJECT_PATH] [--output <filename>] [--config <config_file>]

Example: todo-reporter-cli . --output my-local-report.txt
```
---

### Configuration (via todo_reporter_config.toml)

The tool's behavior is highly customizable via an external TOML configuration file. By default, it looks for todo_reporter_config.toml in the directory from which you run the command. You can specify a custom path using the --config (or -c) command-line argument.

Example todo_reporter_config.toml:
```TOML
# todo_reporter_config.toml
#
# Customize the behavior of the TODO/FIXME Reporter.

[ignore]
# List of directory names to completely skip during recursive traversal.
# These are matched against the directory's base name (e.g., "node_modules").
directories = [
    ".git",
    "__pycache__",
    "node_modules",
    "target",
    "build",
    "venv",
    ".vscode"
]

# List of full path segments to ignore.
# If a directory's full path contains any of these strings, the entire directory subtree will be skipped.
# Useful for specific problematic subfolders, e.g., "/home/user/myproject/assets/"
paths = [
    "/dotfiles/hyprland/themes/assets/"
]

[target]
# List of file extensions to search for TODO/FIXME comments.
# Only files with these extensions will be scanned. Extensions are matched case-insensitively.
extensions = [
    ".py", ".md", ".txt", ".js", ".c", ".cpp", ".java",
    ".rs", ".nix", ".toml", ".sh", ".json", ".yaml", ".yml",
    ".go", ".php", ".rb", ".css", ".html", ".xml"
]

# You can omit any section or key; the script will fall back to its built-in default values.
```

---

## Future Improvements (Ideas for Growth)

- Context Lines: Capture and include lines immediately preceding and following a TODO/FIXME for better context.

- Interactive Output: Explore creating a Terminal User Interface (TUI) for interactive Browse, filtering, and marking of TODOs.

- Output Formats: Support additional output formats (e.g., Markdown, HTML, JSON) for the report.

- More Advanced Filters: Implement regex-based searching, tag-based filtering (e.g., #TODO[high]), or author-based filtering.

- Integration with IDEs/Git Hooks: Consider integrating with development environments or Git pre-commit hooks.

- Notes Aggregation: Extend functionality to aggregate generic notes.txt files or specific comment blocks.

---

## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This project is licensed under the **GNU General Public License v3.0**.

### Summary of terms:
* **Source sharing:** If you modify this code and distribute it, you must also share your source code under the same license.
* **Liability:** The software is provided "as is" without warranty.
* **Anti-grifter protection:** You cannot take this code, make it proprietary, and sell it without giving the users the same rights to the source code.

See the [LICENSE](LICENSE) file for the full legal text.

---

### Acknowledgements
Built by AndariiDev as part of the Boot.dev Hackathon 2025. https://blog.boot.dev/news/hackathon-2025/
Thank you to the team for hosting this event! I learned a lot and had tons of fun.
