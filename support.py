from os import walk, path
import pygame

def import_folder(image_path, debug=False):
    surface_list = []
    for folder__, subfolder__, image_files in walk(image_path):
        for image in image_files:
            full_path = image_path + '/' + image
            if debug:
                print(full_path)
            surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(surface)
                

    return surface_list
    
def group_toggle(boolean_tuple:tuple[bool]) -> tuple[bool]:
    for attribute in boolean_tuple:
        if attribute == True:
            attribute= False
        if attribute == False:
            attribute = True
    return boolean_tuple