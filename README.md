# todo-fixme-reporter
A Python tool to consolidate TODO/FIXME comments and notes from code projects into a single report

While this is a normal python program and can thus be run on any machine that has python3 installed, it also comes packaged in nix, meaning that it can always be run on any machine that has the nix package manager installed. 

How to run:

Non-nix users: Requires python3. Move reporter.py into the directory in question and run it with 'python reporter.py'. Alternatively, specify a filepath as an argument to target a specific directory, e.g. 'python reporter.py /home/user/repos/foo/'.

Nix users: 
-Install the nix package manager (if you haven't yet): 
https://nixos.org/download/#nix-install-linux

-Move into directory, use 'nix run .' + optional argument for the targeted directory, e.g.: nix run . ~/your/directory/here. 
-Alternatively, use 'nix run github:AndariiDev/todo-fixme-reporter /path/to/project_to_scan/'. This does not require you to download the file.
-Or, use 'nix profile install github:AndariiDev/todo-fixme-reporter' (or 'nix profile install .' from inside the repo after cloning it). This will add it to your PATH, allowing you to run 'todo-reporter-cli /path/to/project_to_scan' from anywhere on your system.

The program generates a file named 'todo_report.txt' by default (this name can be changed, see below) in the directory the program is currently located in.

## Customizing Ignored Directories

By default, the script skips common development directories like `.git` and `__pycache__` to keep the output clean and relevant. You can easily customize which directories are ignored:

1.  **Locate the `directories_to_ignore` list:** Open the `reporter.py` file in your text editor.
2.  **Edit the list:** Find the line that defines `directories_to_ignore` (line 8, after the `import` statements).
3.  **Add or remove names:** Add any directory names you wish to ignore (e.g., `'my_temp_folder'`) or remove any you want the script to search. Ensure each name is a string (enclosed in single or double quotes) and separated by commas.
4.  **Add or remove file extensions:** Add any file extensions that are relevant to your project (e.g., `'.nix', '.py', '.rs'`) or remove any you don't need. As with the directories, ensure each name is a string and separated by commas.
Example:
```python
# Customize this list to ignore specific directories during the search
directories_to_ignore = ['.git', '__pycache__', 'node_modules', 'build']
