from customtkinter import CTkButton
import customtkinter as ctk
# import numpy.random
import random
import settings
import asyncio
import sounddevice as sd
import soundfile as sf
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor()

# loading the images of gem and mine
gem_image = ctk.CTkImage(
    light_image=settings.GEM_IMAGE,
    dark_image=settings.GEM_IMAGE,
    size=settings.IMAGE_SIZE
)

gem_image_small = ctk.CTkImage(
    light_image=settings.DEFOCUSED_GEM_IMAGE,
    dark_image=settings.DEFOCUSED_GEM_IMAGE,
    size=settings.IMAGE_SIZE_SMALL
)

mine_image = ctk.CTkImage(
    light_image=settings.MINE_IMAGE,
    dark_image=settings.MINE_IMAGE,
    size=settings.IMAGE_SIZE
)

mine_image_small = ctk.CTkImage(
    light_image=settings.DEFOCUSED_MINE_IMAGE,
    dark_image=settings.DEFOCUSED_MINE_IMAGE,
    size=settings.IMAGE_SIZE_SMALL
)


class Cells:
    all = []
    # probabilities = settings.PROBABILITIES.copy()
    probabilities = [1 / (settings.CELLS_IN_ROW ** 2)] * (settings.CELLS_IN_ROW**2)  # probability of individual cell to have a mine
    clicked_cells = []  # clicked cells

    def __init__(self, x, y, bet_btn):
        self.x = x
        self.y = y
        self.isMine = False
        self.cell_btn_object = None
        self.probability = None

        self.bet_btn = bet_btn
        # self.mine_hit = ctk.BooleanVar(value=False)

        self.assign_probability(self.x, self.y)

        Cells.all.append(self)

    def create_btn_object(self, frame):
        self.cell_btn_object = CTkButton(
            master=frame,
            width=settings.CELL_WIDTH,
            height=settings.CELL_HEIGHT,
            fg_color=settings.CELLS_FG_CLR,
            bg_color='transparent',
            hover_color=settings.CELLS_HOVER_CLR,
            text="",
            command=self.cell_click,
            image=""
        )

    def assign_probability(self, x, y):
        self.probability = Cells.probabilities[x*settings.CELLS_IN_ROW + y]

    def cell_click(self):
        Cells.clicked_cells.append(self)
        self.cell_btn_object.configure(hover=False)
        self.cell_btn_object.configure(fg_color=settings.CELL_CLICK_CLR)
        self.bet_btn.configure(state=ctk.ACTIVE)
        # self.cell_btn_object.update()

        if self.isMine:
            self.mine_click()
            settings.GAME_OVER = True
        else:
            # self.mine_hit.set(True)
            self.gem_click()

    def mine_click(self):
        self.cell_btn_object.configure(bg_color="red")
        self.cell_btn_object.configure(image=mine_image)

        Cells.play_music(is_gem=False)
        Cells.show_cells_and_disable()
        Cells.probability_change()

    def gem_click(self, img=gem_image):
        self.cell_btn_object.configure(image=img)
        Cells.play_music(is_gem=True)
        # self.cell_btn_object.update()

    @staticmethod
    def show_cells_and_disable():
        for cell in Cells.all:
            if cell in Cells.clicked_cells:
                continue

            if cell.isMine:
                cell.cell_btn_object.configure(bg_color="red")
                cell.cell_btn_object.configure(image=mine_image_small)
                # self.cell_btn_object.update()
            else:
                Cells.gem_click(cell, gem_image_small)

            cell.cell_btn_object.configure(fg_color=settings.CELL_CLICK_CLR)
            cell.cell_btn_object.configure(state=ctk.DISABLED)

    @staticmethod
    def probability_change():
        # clear the probabilities list
        Cells.probabilities.clear()

        # the total probability increase for clicked cells
        total_probability_inc = 0

        # increase the probability of the first cell clicked
        Cells.clicked_cells[0].probability += settings.PROBABILITY_INC_OF_FIRST_CLICKED_CELL
        total_probability_inc += settings.PROBABILITY_INC_OF_FIRST_CLICKED_CELL

        # increase the probability of rest of the clicked cells
        if len(Cells.clicked_cells) > 0:
            for cell in Cells.clicked_cells[1:]:
                cell.probability += settings.PROBABILITY_INC_OF_CLICKED_CELL
                total_probability_inc += settings.PROBABILITY_INC_OF_CLICKED_CELL

        # probability decrease per cell
        probability_dec_per_cell = total_probability_inc / ((settings.CELLS_IN_ROW ** 2) - len(Cells.clicked_cells))

        for cell in Cells.all:
            # skip when a clicked cell appears
            if cell not in Cells.clicked_cells and (cell.probability-probability_dec_per_cell) > settings.LEAST_PROBABILITY:
                cell.probability -= probability_dec_per_cell
            Cells.probabilities.append(cell.probability)

    @staticmethod
    def randomize_mines():
        # mines = numpy.random.choice(
        #     Cells.all,
        #     size=settings.NUMBER_OF_MINES,
        #     replace=False,
        #     p=Cells.probabilities
        # )
        # mines = random.choices(
        #     Cells.all,
        #     weights=Cells.probabilities,
        #     k=settings.NUMBER_OF_MINES
        # )
        mines = []
        all_cpy = Cells.all.copy()
        p_cpy = Cells.probabilities.copy()

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

        # # checking if all values are unique
        # # if not, making them unique
        # for i, mine in enumerate(mines):
        #     if mine in mines[:i]:
        #         while True:
        #             m = random.choices(
        #                 Cells.all,
        #                 weights=Cells.probabilities,
        #                 k=1
        #             )
        #
        #             if m != mine:
        #                 mines[i] = m[0]
        #                 break

        print(f"{mines = }")
        for mine in mines:
            mine.isMine = True

    @staticmethod
    async def play_music(is_gem):
        if is_gem:
            await Cells.play_sound_async(settings.GEM_MUSIC)
        else:
            await Cells.play_sound_async(settings.MINE_MUSIC)

        # pygame.mixer.music.play()
    @staticmethod
    async def play_sound_async(file_path):
        loop = asyncio.get_event_loop()
        data, fs = sf.read(file_path, dtype='float32')
        await loop.run_in_executor(executor, sd.play, data, fs)
        await loop.run_in_executor(executor, sd.wait)


    def __repr__(self):
        return f"Cell({self.x}, {self.y})"


