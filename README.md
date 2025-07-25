### todo-fixme-reporter
A Python tool to consolidate TODO/FIXME comments and notes from code projects into a single report

## Customizing Ignored Directories

By default, the script skips common development directories like `.git` and `__pycache__` to keep the output clean and relevant. You can easily customize which directories are ignored:

1.  **Locate the `directories_to_ignore` list:** Open the `reporter.py` file in your text editor.
2.  **Edit the list:** Find the line that defines `directories_to_ignore` (it's near the top, after the `import` statements).
3.  **Add or remove names:** Add any directory names you wish to ignore (e.g., `'my_temp_folder'`) or remove any you want the script to search. Ensure each name is a string (enclosed in single or double quotes) and separated by commas.

Example:
```python
# Customize this list to ignore specific directories during the search
directories_to_ignore = ['.git', '__pycache__', 'node_modules', 'build']
