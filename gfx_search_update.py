from env import TNO_FOLDER, SOURCES, DESTINATION
import subprocess
import os


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

    # For every entry in dictionary, compare date_modified of entry to date_modified in destination
    for entry in json_from_gfx:
        # Continue if entry file doesn't exist
        full_filepath: str = TNO_FOLDER + "/" + json_from_gfx[entry]["filepath"]
        if not os.path.exists(full_filepath):
            del json_from_gfx[entry]
            continue

    #   If entry file does not exist, delete item from dictionary
    #   Else if destination file does not exist, convert file if needed, move to safe_images, and update filepath and filename (if needed)
    #   Else if entry_file is modified more recently than destination_file, convert if needed, move to safe_images, and update filepath and filename (if needed)
    #   Else, move destination_file to safe_images and update filepath and filename (if needed)
    # Delete all files in destination not in safe_images
    # Move all files from safe_images to destination
    # Delete safe_images
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
                            "gfx_name": entry_gfx_name,
                            "filepath": entry_filepath,
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


def convert_to_png(image: str):
    image_png: str = image.split(".")[0] + ".png"
    command: str = f"magick {image} {image_png}"


if __name__ == "__main__":
    main()
