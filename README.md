# UDT Optimizer

**UDT Optimizer** is a portable Flask-based application designed to optimize and clean Allen-Bradley `.l5x` User-Defined Type (UDT) files. The app provides a simple web interface where users can upload `.l5x` files, process them to improve structure or remove redundancies, and download the optimized version with an appropriate filename.

## Features

- Upload `.l5x` files via drag-and-drop or file browser.
- Supports all case variations of the `.l5x` file extension.
- Extracts and optimizes UDT definitions inside the `.l5x` file.
- Generates a clean, optimized `.l5x` file for download.
- Returns the optimized file with a filename prefixed by `Optimized_` and includes the UDT name.
- Runs as a portable executable for easy distribution without requiring a Python environment.

## How It Works

1. User uploads a `.l5x` file through the web interface.
2. The Flask backend extracts the UDT definition using `extract_udt_definition`.
3. The UDT is optimized and regenerated with `optimize_and_regenerate_udt`.
4. The optimized `.l5x` content is returned to the user as a downloadable file.

## Note

This code is one part of the bigger project called **LLM4ICS & LLM4L5X** that is still a work in progress.

## Todo
- Option to upload entire Program for optimization. (L5X_TagOptimizer - this will cover UDT tags, global tags, Local tags optimization)
- Enhance UDT optimization algorithms.
- Integrate with other LLM4ICS modules.
