from PIL import Image, ImageEnhance
import pygame
pygame.mixer.init()

FIRST_CLICK = True
GAME_OVER = False
WINS = 0
LOSSES = 0

HEIGHT = 720
WIDTH = 1440
CELLS_IN_ROW = 5
NUMBER_OF_MINES = 3
CELL_WIDTH = 120
CELL_HEIGHT = 120

BET_AMOUNT_FRAME_HEIGHT = 50
PAD_Y_LEFT_FRAME = 5
PAD_X_LEFT_FRAME = 10

# colours
LEFT_FRAME_CLR = "#213743"
RIGHT_FRAME_CLR = "#0f212e"
CELLS_FRAME_CLR = RIGHT_FRAME_CLR
CELLS_FG_CLR = "#2f4553"
CELLS_HOVER_CLR = "#557086"
CELL_CLICK_CLR = "#071824"

BET_INPUT_BTN_CLR = "#2f4553"
HALF_DOUBLE_BTN_HOVER_CLR = "#557086"
BET_BUTTON_CLR = "#00e701"
BET_BUTTON_HOVER_CLR = "#1fff20"
BET_PLACED_LEFT_FRAME_CLR = "#2f4553"

# file loc of images
GEM_IMAGE = Image.open(r"C:\Users\Mohit\OneDrive\Desktop\AIES Mini Project\mines\assets\gem.png")
MINE_IMAGE = Image.open(r"C:\Users\Mohit\OneDrive\Desktop\AIES Mini Project\mines\assets\mine.png")

gem_enhancer = ImageEnhance.Brightness(GEM_IMAGE)
mine_enhancer = ImageEnhance.Brightness(MINE_IMAGE)
DEFOCUSED_GEM_IMAGE = gem_enhancer.enhance(factor=0.5)
DEFOCUSED_MINE_IMAGE = mine_enhancer.enhance(factor=0.5)
IMAGE_SIZE = (80, 80)
IMAGE_SIZE_SMALL = (60, 60)

CELL_MOTION_STEPS = 10
DELAY = 10
# probability of each cell * total num of cells
# PROBABILITIES = [1 / (CELLS_IN_ROW ** 2)] * (CELLS_IN_ROW**2)
# increase in probability of first cell you click
PROBABILITY_INC_OF_FIRST_CLICKED_CELL = 0.02
PROBABILITY_INC_OF_CLICKED_CELL = 0.01

FONT_LOC = fr"\assets\Fontspring-DEMO-proximanova-black.otf"
FONT_SIZE = 20

LEAST_PROBABILITY = 0.0000001

GEM_MUSIC = r"C:\Users\Mohit\OneDrive\Desktop\AIES Mini Project\mines\assets\Sounds\gem.wav"
MINE_MUSIC = r"C:\Users\Mohit\OneDrive\Desktop\AIES Mini Project\mines\assets\Sounds\mine1.mp3"
# Load the music
gem_sound = pygame.mixer.Sound(GEM_MUSIC)
mine_sound = pygame.mixer.Sound(MINE_MUSIC)
