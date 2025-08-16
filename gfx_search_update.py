from env import TNO_FOLDER, SOURCES, DESTINATION
import subprocess
import os
import shutil

GFX_NAME = "gfx_name"
FILEPATH = "filepath"

def main():
    # FOR ONLY GOALS
    # Create an empty dictionary
    json_from_gfx: dict = {}

    # Scan through all National Focus .gfx files and add entry for them in dictionary, using filename as entry name and containing gfx_name and filepath
    for filename in SOURCES:
        fill_json_from_gfx(json_from_gfx, filename)

    # Create directory "safe_images" in destination folder
    try:
        os.mkdir(f"{DESTINATION}/safe_images")
    except FileNotFoundError:
        print(f"Error: Destination folder '${DESTINATION}' does not exist.")
        return
    except FileExistsError:
        pass

    # Update the destination folder
    json_from_destination: dict = update_destination(json_from_gfx)

    # Write dictionary as JSON file

    # This will update the destination folder while purging unused images, and create a JSON file that associates each image with its gfx_name


def fill_json_from_gfx(json_from_gfx: dict, filename):
    # Proccess all the entries in a gfx file
    try:
        with open(filename, "r") as file:
            open_bracket: bool = True
            entry_filename: str = ""
            entry_gfx_name: str = ""
            entry_filepath: str = ""
            for preprocessed_line in file:
                # Figure out what to do with line in file
                line = preprocessed_line.strip()
                if line[-1] == "{":
                    open_bracket = True
                elif line[-1] == "}":
                    if open_bracket:
                        open_bracket = False
                        json_from_gfx[entry_filename] = {
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

def get_png_name(filename: str):
    if filename[-4:] == ".png":
        return filename
    else:
        return filename.split(".")[0] + ".png"
    
def update_destination(json_from_gfx: dict):
    # Create a new empty dictionary for destination
    json_from_destination: dict = {}

    # For every entry in dictionary, compare date_modified of entry to date_modified in destination
    for entry in json_from_gfx:
        entry_filepath: str = os.path.join(TNO_FOLDER, json_from_gfx[entry][FILEPATH])
        destination_filename: str = get_png_name(entry)
        destination_filepath: str = os.path.join(DESTINATION, destination_filename)
        dest_safe_filepath: str = os.path.join(DESTINATION, "safe_images", destination_filename)
        #   If entry file does not exist, delete item from dictionary and continue
        if not os.path.exists(entry_filepath):
            print(f"'{entry_filepath}' does not exist, continuing.")
            continue
        #   Else if destination file does not exist, convert file if needed, move to safe_images, and update filepath and filename (if needed)
        elif not os.path.exists(destination_filepath):
            magick(entry_filepath, dest_safe_filepath)
            json_from_destination[destination_filename] = {
                GFX_NAME: json_from_gfx[entry][GFX_NAME],
                FILEPATH: destination_filepath
            }
        #   Else if entry_file is modified more recently than destination_file, convert if needed, move to safe_images, and update filepath and filename (if needed)
        elif os.path.getmtime(entry_filepath) > os.path.getmtime(destination_filepath):
            magick(entry_filepath, dest_safe_filepath)
            json_from_destination[destination_filename] = {
                GFX_NAME: json_from_destination[entry][GFX_NAME],
                FILEPATH: destination_filepath
            }
        #   Else, move destination_file to safe_images and update filepath and filename (if needed)
        else:
            shutil.move(destination_filepath, dest_safe_filepath)
    
    # Delete all files in destination not in safe_images
    for damned_file in os.listdir(DESTINATION):
        damned_filepath = os.path.join(DESTINATION, damned_file)
        if os.path.isfile(damned_filepath):
            os.remove(damned_filepath)

    # Move all files from safe_images to destination
    for saved_filename in os.listdir(os.path.join(DESTINATION, "safe_images")):
        saved_filepath = os.path.join(DESTINATION, "safe_images", saved_filename)
        shutil.move(saved_filepath, json_from_destination[saved_filename][FILEPATH])
    
    # Delete safe_images
    os.rmdir(os.path.join(DESTINATION, "safe_images"))

    return json_from_destination

def magick(source_image: str, destination_image: str):
    command: str = f"magick {source_image} {destination_image}"
    print(command)


if __name__ == "__main__":
    main()
