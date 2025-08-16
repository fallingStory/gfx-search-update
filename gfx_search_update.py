# Custom imports
from env import TNO_FOLDER, SOURCES, DESTINATION

# Imports
import os
import shutil
import subprocess
import json


GFX_NAME = "gfx_name"
FILEPATH = "filepath"

updated_images = 0
unchanged_images = 0
created_images = 0
purged_images = 0

###
### Main Functions
###


def main():
    print("Script launched.\n")

    # Create an empty dictionary based on the .gfx files
    dict_gfx: dict = {}

    # Scan through all National Focus .gfx files and add entry for them in dictionary, using filename as entry name and containing gfx_name and filepath
    for category_key in SOURCES:
        category = SOURCES[category_key]
        dict_gfx[category_key] = {}
        print(f"Scanning through .gfx files for '{category_key}'")
        for filename in category:
            fill_dict_gfx(dict_gfx[category_key], filename)
        print(f"Scan complete for '{category_key}'. {len(dict_gfx[category_key])} images found.\n")

    dict_dest: dict = {}
    for category_key in SOURCES:
        sub_dest = os.path.join(DESTINATION, category_key)
        if not os.path.exists(sub_dest):
            try:
                os.mkdir(sub_dest)
            except FileNotFoundError:
                print(f"Error: Destination folder '${DESTINATION}' does not exist.")
                return

        # Create directory "safe_images" in destination folder
        os.mkdir(os.path.join(sub_dest, "safe_images"))

        # Update the destination folder
        print(f"Beginning update proccess for '{category_key}'.")
        dict_dest[category_key] = update_destination(dict_gfx[category_key], sub_dest)
        print(f"Update proccess for '{category_key}' finished.\n")

    # Write dictionary as JSON file
    with open("images.json", "w") as json_file:
        json.dump(dict_dest, json_file, indent=4)
    print("Created JSON file of images in destination folder.\n")

    # Log output
    print("Script complete.")
    print(f" - {updated_images} images updated.")
    print(f" - {created_images} new images added.")
    print(f" - {unchanged_images} images unchanged.")
    print(f" - {purged_images} images purged.")


def fill_dict_gfx(dict_gfx: dict, filename):
    filepath = os.path.join(TNO_FOLDER, filename)
    # Proccess all the entries in a gfx file
    try:
        with open(filepath, "r") as file:
            open_bracket: bool = True
            entry_filename: str = ""
            entry_gfx_name: str = ""
            entry_filepath: str = ""
            for preprocessed_line in file:
                # Figure out what to do with line in file
                line = preprocessed_line.strip()
                if line == "":
                    continue
                elif line[0] == "#":
                    continue
                elif line[-1] == "{":
                    open_bracket = True
                elif line[-1] == "}":
                    if open_bracket:
                        open_bracket = False
                        dict_gfx[entry_filename] = {
                            GFX_NAME: entry_gfx_name,
                            FILEPATH: entry_filepath,
                        }
                        entry_filename, entry_gfx_name, entry_filepath = "", "", ""
                elif open_bracket:
                    split_line = preprocessed_line.split()
                    if split_line[0] == "name":
                        entry_gfx_name = split_line[2].strip('"')
                    elif split_line[0] == "texturefile":
                        entry_filepath = split_line[2].strip('"')
                        entry_filename = entry_filepath.split("/")[-1]

    except FileNotFoundError:
        print(f"Error: Cannot find '{filename}'.")


def update_destination(dict_gfx: dict, sub_dest: str):
    # Create an empty dictionary based on the destination folder
    dict_dest: dict = {}

    global purged_images

    # Update the destination folder to have up-to-date images, move them to safe_images
    for entry in dict_gfx:
        entry_filepath: str = os.path.join(TNO_FOLDER, dict_gfx[entry][FILEPATH])
        if os.path.exists(entry_filepath):
            update_dest_image(dict_dest, dict_gfx, entry_filepath, entry, sub_dest)

    # Delete all files in destination not in safe_images
    for damned_file in os.listdir(sub_dest):
        damned_filepath = os.path.join(sub_dest, damned_file)
        if os.path.isfile(damned_filepath):
            os.remove(damned_filepath)

    # Move all files from safe_images to destination
    for saved_filename in os.listdir(os.path.join(sub_dest, "safe_images")):
        saved_filepath = os.path.join(sub_dest, "safe_images", saved_filename)
        shutil.move(saved_filepath, dict_dest[saved_filename][FILEPATH])

    # Delete safe_images
    os.rmdir(os.path.join(sub_dest, "safe_images"))

    return dict_dest


def update_dest_image(dict_dest, dict_gfx, entry_filepath, entry, sub_dest):
    # Declare variables
    global created_images
    global updated_images
    global unchanged_images

    dest_filename: str = get_png_name(entry)
    dest_filepath: str = os.path.join(sub_dest, dest_filename)
    dest_safe_filepath: str = os.path.join(sub_dest, "safe_images", dest_filename)

    # Handle the image
    if not os.path.exists(dest_filepath):
        exit_code = magick(entry_filepath, dest_safe_filepath)
        action = 0
    elif os.path.getmtime(entry_filepath) > os.path.getmtime(dest_filepath):
        exit_code = magick(entry_filepath, dest_safe_filepath)
        action = 1
    else:
        shutil.move(dest_filepath, dest_safe_filepath)
        exit_code = 0
        action = 2

    # Update dictionary and log if handling successful
    if exit_code == 0:
        dict_dest[dest_filename] = {
            GFX_NAME: dict_gfx[entry][GFX_NAME],
            FILEPATH: dest_filepath,
        }

        if action == 0:
            created_images += 1
        elif action == 1:
            updated_images += 1
        elif action == 2:
            unchanged_images += 1


###
### Helper Functions
###
def get_png_name(filename: str):
    if filename[-4:] == ".png":
        return filename
    else:
        return filename.split(".")[0] + ".png"


def magick(source_image: str, dest_image: str):
    result = subprocess.run(["magick", source_image, dest_image])
    return result.returncode


if __name__ == "__main__":
    main()
