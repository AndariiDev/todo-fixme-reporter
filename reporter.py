# reporter.py
import sys
import os

# Define a list of directory names to ignore during traversal
# # Add or remove directories here to customize which folders are skipped
directories_to_ignore = [".git", "__pycache__", "node_modules", "target", "build", "venv", ".vscode"]

# fundamental python idioms
# __name__ (Dunder Name) is a special, built-in variable in Python
# It's automatically set to __main__ when script is run directly
# "__main__" (Dunder Main String) is a specific string literal to identify entry point of script
if __name__ == "__main__": # "if" block only runs if script is executed directly; prevents functions from script to be run by other scripts
    # Initialize project_path to None (default value here)
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
        dirs[:] = [d for d in dirs if d not in directories_to_ignore]
        print (root)
        print (dirs)
        print (files)
        print ('.............')
