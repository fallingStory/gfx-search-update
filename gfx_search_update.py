from env import DESTINATION, SOURCES
import subprocess


def main():
    # FOR ONLY GOALS
    # Create an empty JSON file
    # Scan through all National Focus .gfx files and add entry for them in JSON, using filename as entry name and containing
        # gfx_name
        # filepath
    # Create directory "safe_images" in destination folder
    # Create a new empty JSON file NEW_J, to use filename as entry and contain
        # gfx_name (blank)
        # filepath (in destination)
    # For every entry in old JSON, compare date_modified of entry to date_modified in destination
        # If entry file does not exist, continue
        # Else if destination file does not exist, convert file if needed, move to safe_images, and add to NEW_J
        # Else if entry_file is modified more recently than destination_file, convert if needed, move to safe_images, and add to NEW_J
        # Else, move destination_file to safe_images and add to NEW_J
    # Delete all files in destination not in safe_images
    # Move all files from safe_images to destination
    # Delete safe_images
    # Delete old JSON file

    # This will update the destination folder while purging unused images, and create a JSON file that associates each image with its gfx_name

    pass


def convert_to_png(image: str):
    image_png: str = image.split(".")[0] + ".png"
    command: str = f"magick {image} {image_png}"


if __name__ == "__main__":
    pass
    # main()
