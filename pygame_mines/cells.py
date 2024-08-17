import random
import pygame
import settings
import utils


class CellsMain:
    probabilities = [1 / (settings.CELLS_IN_ROW ** 2)] * (settings.CELLS_IN_ROW ** 2)  # probability of individual cell to have a mine
    clicked_cells = []
    cells_sprites = pygame.sprite.Group()
    cell_animation_on = False
    game_over = True

    def __init__(self, surf):
        self.surf = surf
        self.create_cell()
        self.assign_probability()
        self.randomize_mines()

    def create_cell(self):
        self.cells_sprites.empty()

        for x in range(5):
            left = settings.LEFT_SPACE_FOR_CELLS
            top = settings.TOP_SPACE_FOR_CELLS + x * settings.CELL_PAD_Y + (x * settings.CELL_HEIGHT)
            for y in range(5):
                cell = Cells(left, top, self.surf)
                self.cells_sprites.add(cell)
                left += settings.CELL_PAD_X + settings.CELL_WIDTH

    def probability_change(self):
        # clear the probabilities list
        if not len(self.clicked_cells):
            return
        self.probabilities.clear()

        # the total probability increase for clicked cells
        total_probability_inc = 0

        # increase the probability of the first cell clicked
        self.clicked_cells[0].probability += settings.PROBABILITY_INC_OF_FIRST_CLICKED_CELL
        total_probability_inc += settings.PROBABILITY_INC_OF_FIRST_CLICKED_CELL

        # increase the probability of rest of the clicked cells
        if len(self.clicked_cells) > 0:
            for cell in self.clicked_cells[1:]:
                cell.probability += settings.PROBABILITY_INC_OF_CLICKED_CELL
                total_probability_inc += settings.PROBABILITY_INC_OF_CLICKED_CELL

        # probability decrease per cell
        probability_dec_per_cell = total_probability_inc / ((settings.CELLS_IN_ROW ** 2) - len(self.clicked_cells))

        for cell in self.cells_sprites:
            # skip when a clicked cell appears
            if cell not in self.clicked_cells and (cell.probability-probability_dec_per_cell) > settings.LEAST_PROBABILITY:
                cell.probability -= probability_dec_per_cell
            self.probabilities.append(cell.probability)

    @staticmethod
    def assign_probability():
        for i, cell in enumerate(CellsMain.cells_sprites.sprites()):
            cell.probability = CellsMain.probabilities[i]

    def randomize_mines(self):
        mines = []
        all_cpy = self.cells_sprites.sprites().copy()
        p_cpy = self.probabilities.copy()

        for i in range(settings.NUMBER_OF_MINES):
            while True:
                m = random.choices(
                    population=all_cpy,
                    weights=p_cpy,
                    k=1
                )

                if m not in mines:
                    mines.extend(m)
                    index = all_cpy.index(m[0])
                    all_cpy.remove(m[0])
                    p_cpy.pop(index)
                    break

        for mine in mines:
            mine.isMine = True

    @staticmethod
    def clicked_cells_():
        CellsMain.clicked_cells = [cell for cell in CellsMain.cells_sprites.sprites() if cell.clicked]

    def update(self):
        self.probability_change()
        self.create_cell()
        self.assign_probability()
        self.randomize_mines()

        self.clicked_cells.clear()
        settings.GEMS_CLICKED = 0


class Cells(pygame.sprite.Sprite):
    def __init__(self, x, y, surf):
        super().__init__()
        self.surface = surf
        self.x = x
        self.y = y
        self.isMine = False
        self.probability = 0
        self.animation_on = 0
        self.speed = 0
        self.active = True
        self.clicked = False
        self.cell_colour = settings.CELL_FG_COLOUR
        self.img = None

        # Surface for the image (either the mine or the gem)
        self.image = pygame.Surface((settings.CELL_WIDTH, settings.CELL_HEIGHT)).convert_alpha()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.display_cell()

    def display_cell(self):
        self.cell = pygame.draw.rect(self.surface, self.cell_colour, self.rect, border_radius=settings.CELL_BORDER_RAD)

    def cell_shadow(self):
        if self.active:
            pygame.draw.rect(
                self.surface,
                settings.CELL_SHADOW_CLR,
                pygame.Rect(self.rect.x, self.rect.y + 5, self.rect.width, self.rect.height),
                border_radius=settings.CELL_BORDER_RAD)

    def animate(self):
        # got the animation. yay!
        if self.animation_on and self.active:
            CellsMain.cell_animation_on = True
            if self.animation_on == 1:
                if self.speed < 2:
                    self.rect.x -= 1
                    self.rect.y -= 1
                    self.rect.width += 2
                    self.rect.height += 2
                    self.speed += 0.25
                else:
                    self.animation_on = 2
            elif self.animation_on == 2:

                if 0 < self.speed:
                    self.rect.x += 1
                    self.rect.y += 1
                    self.rect.width -= 2
                    self.rect.height -= 2
                    self.speed -= 0.25
                else:
                    self.speed = 0
                    self.animation_on = 0
                    CellsMain.cell_animation_on = False
                    # call cell_click to disable the cell
                    self.cell_click()
                    self.get_img()

    def cell_click(self):
        self.rect.x += 1
        self.rect.y += 1
        self.rect.width -= 2
        self.rect.height -= 2
        self.active = False
        # append the cell to the clicked cells list
        CellsMain.clicked_cells.append(self)
        # uncomment the line below for a cool look
        # self.cell_colour = settings.CELL_CLICK_CLR
        self.play_sound()

    def play_sound(self):
        if self.isMine:
            settings.mine_sound.play(maxtime=settings.maxtime)
            utils.is_sound_playing()
        elif settings.GEMS_CLICKED > settings.RISKY_DIAMOND_N:
            settings.risky_diamond_sound.play(maxtime=settings.maxtime)
            utils.is_sound_playing()
        else:
            settings.diamond_sound.play(maxtime=settings.maxtime)
            utils.is_sound_playing()

    def show_cell_contents(self):
        if not self.active:
            # comment the line below for a cool look
            self.cell_colour = settings.CELL_CLICK_CLR

            if self.isMine:
                self.mine()
            else:
                self.gem()

    def mine(self):
        if self.img is None:
            self.img = settings.MINE_IMAGE_SMALL if CellsMain.game_over else settings.MINE_IMAGE
        self.image_rect = self.img.get_rect(center=self.rect.center)
        self.surface.blit(self.img, self.image_rect)

        CellsMain.game_over = True
        # pygame.event.post(pygame.event.Event(settings.GAME_OVER_EVENT))
        self.display_and_disable_cells()

    def gem(self):
        if self.img is None:
            self.img = settings.GEM_IMAGE_SMALL if CellsMain.game_over else settings.GEM_IMAGE
        self.image_rect = self.img.get_rect(center=self.rect.center)
        self.surface.blit(self.img, self.image_rect)

    def display_and_disable_cells(self):
        """
        display and set the self.active to False after a mine is hit
        """
        # CellsMain.clicked_cells_()
        for cell in CellsMain.cells_sprites.sprites():
            # if cell in CellsMain.clicked_cells:
            #     continue
            cell.active = False

    def get_img(self):
        if self.isMine:
            self.img = settings.MINE_IMAGE
        else:
            self.img = settings.GEM_IMAGE

    def update(self):
        self.cell_shadow()
        self.display_cell()
        self.animate()
        self.show_cell_contents()



