from os import walk
import pygame

def import_folder(path):
    surface_list = []
    for folder__, subfolder__, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(surface)

    return surface_list
    