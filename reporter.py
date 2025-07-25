# reporter.py
import sys
import os

# Define a list of directory names to ignore during traversal
# # Add or remove directories here to customize which folders are skipped
directories_to_ignore = [".git", "__pycache__", "node_modules", "target", "build", "venv", ".vscode",]
# # Add or remove extensions for files that will be checked
target_extensions = [
    ".py", ".md", ".txt", ".js", ".c", ".cpp", ".java", ".rs", ".nix", ".toml", ".sh", ".json", "yaml", "yml", ".go", ".php", ".rb", ".css", ".html", ".xml"
]
# Define a list of full path segments to ignore
# This will cause the script to ignore any directory whose full path contains any of these stings
paths_to_ignore = [ "/dotfiles/hyprland/themes/assets/" ] # Add more as needed

# fundamental python idioms
# __name__ (Dunder Name) is a special, built-in variable in Python
# It's automatically set to __main__ when script is run directly
# "__main__" (Dunder Main String) is a specific string literal to identify entry point of script
if __name__ == "__main__": # "if" block only runs if script is executed directly; prevents functions from script to be run by other scripts
    # Initialize project_path to None (default value here, 0)
    project_path = None

    if len(sys.argv) == 1: # if there is exactly one argument, do:
        project_path = os.getcwd()
    elif len(sys.argv) == 2: # elif there are exactly two arguments, do:
        project_path = sys.argv[1]
    else: # else there are more than two arguments, do:
        print ("ERROR: only one optional argument accepted, use project directory")
        print (f"Usage: python {sys.argv[0]} [directory_path]")
        sys.exit(1)

    print(f"Searching in: {project_path}")
           
    for (root,dirs,files) in os.walk(project_path, topdown=True):
        should_skip_root = False # flag variable
        for bad_pattern in paths_to_ignore:
            if bad_pattern in root:
                should_skip_root = True # Set flag
                break # exit inner loop early

        if should_skip_root: # check flag AFTER inner loop
            continue
        
        dirs[:] = [d for d in dirs if d not in directories_to_ignore]
        files[:] = [f for f in files if os.path.splitext(f)[1].lower() in target_extensions]
        for f in files:
            # "tuple unpacking" = "function of os submodule to split file path"
            # _, ext = os.path.splitext(f) # "_" = commonly used convention (not rule) to mark variable as "intentionally ignored" or "don't care"
            # if ext.lower() in target_extensions: # .lower for case-insensitive matching
            full_file_path = os.path.join(root,f)
            print(f"Processing file: {full_file_path}") # Temp print, replace with actual TODO logic later
                
        # print (".............")
