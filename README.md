GFX Search & Update Script
This Python script is a utility designed to automate the process of finding, converting, and organizing graphics files referenced in .gfx files for the 'gfx_search repo'.

The script scans specified source directories for .gfx files, parses them to identify the actual image assets (like .dds files), and then processes them into a destination folder inside gfx_search.

How It Works
Scan Sources: The script reads a predefined list of .gfx files and builds a dictionary of all the graphics assets they contain.

Update Destination: For each asset, it checks the destination folder.

It uses a temporary safe_images directory to hold all the necessary files for the current run (both new and existing).

It converts new files or updated files into this safe_images directory.

Existing, unchanged files are moved from the destination into safe_images.

Purge and Finalize: Once all assets are safely in the safe_images directory, the script deletes everything left in the main destination folder (the old, unreferenced files). It then moves the contents of safe_images back into the destination folder and generates the final images.json report.
