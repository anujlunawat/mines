from PIL import Image, ImageEnhance
import os
import pygame.image, pygame.freetype
import utils
import multipliers
import gifFrames

info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h
CELLS_IN_ROW = 5
NUMBER_OF_MINES = 3
GEMS_CLICKED = 0
WINS = 0
LOSSES = 0
BET_AMOUNT = 0

# User events
GAME_OVER_EVENT = pygame.USEREVENT + 1

# cell settings
CELL_WIDTH = 120
CELL_HEIGHT = 120
CELL_BORDER_RAD = 7
CELL_PAD_X = 10
CELL_PAD_Y = 15
# the width that the entire group of cells requires is 640
# the width of the right_part_surf (surface) is 1080 (75% of 1440)
# so (1080 - 640) / 2 is the width you require on either side
LEFT_SPACE_FOR_CELLS = 220 + 360
# since the cells are square shaped, they require the same amount of height, as they require width(640)
# since height = 720, required height on both sided = (720 - 640) / 2 = 40
# should have been 40, but I increased CELL_PAD_Y by 5. so TOP_SPACE_FOR_CELLS becomes 30
TOP_SPACE_FOR_CELLS = 30

# left part widgets settings
rect_border_rad = 7

# probabilities
PROBABILITY_INC_OF_FIRST_CLICKED_CELL = 0.02
PROBABILITY_INC_OF_CLICKED_CELL = 0.01
LEAST_PROBABILITY = 0.0000001

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE_GRAY = "#5885AF"  # bfd7ed
GREEN = "#00e701"
GREEN_FOCUS = "#1fff20"
LEFT_PART_COLOUR = (33, 55, 67)
BG_COLOUR = (15, 33, 46)
CELL_FG_COLOUR = (47, 69, 83)
CELLS_HOVER_CLR = "#557086"
CELL_CLICK_CLR = "#071824"
CELL_SHADOW_CLR = "#1b303c"
BET_2X_FRAME_CLR = "#2f4553"
BET_INPUT_BTN_CLR = "#0f212e"

# --------------loading images-------------
IMAGE_SIZE = (80, 80)
IMAGE_SIZE_SMALL = (60, 60)

gem_image = Image.open(os.path.join("assets", "images", "gem1.png"))
mine_image = Image.open(os.path.join("assets", "images", "mine1.png"))

# loading normal gem image
mode = gem_image.mode
size = gem_image.size
data = gem_image.tobytes()
GEM_IMAGE = pygame.image.fromstring(data, size, mode)

# loading normal mine image
mode = mine_image.mode
size = mine_image.size
data = mine_image.tobytes()
MINE_IMAGE = pygame.image.fromstring(data, size, mode)

gem_image_small = Image.open(os.path.join("assets", "images", "gem_small.png"))
mine_image_small = Image.open(os.path.join("assets", "images", "mine_small.png"))
gem_enhancer = ImageEnhance.Brightness(gem_image_small)
mine_enhancer = ImageEnhance.Brightness(mine_image_small)
defocused_gem_image = gem_enhancer.enhance(factor=0.5)
defocused_mine_image = mine_enhancer.enhance(factor=0.5)

# loading defocused, small gem image
mode = defocused_gem_image.mode
size = defocused_gem_image.size
data = defocused_gem_image.tobytes()
GEM_IMAGE_SMALL = pygame.image.fromstring(data, size, mode)

# loading defocused, small mine image
mode = defocused_mine_image.mode
size = defocused_mine_image.size
data = defocused_mine_image.tobytes()
MINE_IMAGE_SMALL = pygame.image.fromstring(data, size, mode)

# font
FONT_STYLE = pygame.freetype.STYLE_STRONG
FONT_SIZE = 2
FONT_PATH = os.path.join("assets", "Font", "DejaVuSansMono.ttf")
FONT = pygame.freetype.Font(FONT_PATH, FONT_SIZE, resolution=800)
FONT_SMALL = pygame.freetype.Font(FONT_PATH, 12)
FONT_COLOUR = (255, 255, 255)

# left part surfaces/rects settings
LEFT_PART_x = 10
LEFT_PART_y = 15
LEFT_FRAME_PADDING = 10
LEFT_WIN_HEIGHT = 50
LEFT_WIN_WIDTH = int(utils.any_prct(utils.any_prct(WIDTH, 25), 90))

# load music
maxtime = 0  # the maxtime the sound will play (in ms) (0 for playing the full sound)
RISKY_DIAMOND_N = 7
start_bet_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "Start bet button.mp3"))
checkout_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "Checkout.mp3"))
diamond_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "Diamond.mp3"))
mine_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "Mine.mp3"))
risky_diamond_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "Risky Diamond.mp3"))

# multiplier file
MULTIPLIER = multipliers.f()

# load the frames of mine gif
gif_frames = gifFrames.load_images_from_directory(os.path.join("assets", "images", "frames"), "frame_")
