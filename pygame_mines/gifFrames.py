import glob
import pygame
import re


def load_images_from_directory(directory, prefix):
    images = []
    pattern = fr"{directory}\{prefix}*.png"  # Adjust the pattern for your file types

    # Get a list of all matching files
    file_list = glob.glob(pattern)

    # Extract the number and sort the files
    def extract_number(filename):
        match = re.search(rf"{prefix}(\d+)", filename)
        return int(match.group(1)) if match else float('inf')

    # Sort files based on the extracted number
    file_list.sort(key=extract_number)

    # Load images in the sorted order
    for filepath in file_list:
        image = pygame.image.load(filepath)
        images.append(image)

    return images
