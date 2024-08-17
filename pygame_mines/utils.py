import settings
import pygame.mixer
import time


def height_prct(percentage):
    return (settings.HEIGHT / 100) * percentage


def width_prct(percentage):
    return (settings.WIDTH / 100) * percentage


def any_prct(hw, percentage):
    return (hw / 100) * percentage


def is_sound_playing():
    return
    while pygame.mixer.get_busy():
        time.sleep(.01)
