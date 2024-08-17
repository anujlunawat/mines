import random
import tkinter as tk
import customtkinter as ctk
import tkinter.font as tkfont
import warnings
import settings
import utils
import cells
import leftFrame

warnings.filterwarnings("ignore", message="CTkButton Warning: Given image is not CTkImage")


class Win:
    def __init__(self):
        self.root = root
        self.root.geometry(f"{settings.WIDTH}x{settings.HEIGHT}+0+0")
        self.root.configure(fg_color="black")
        self.root.resizable(False, False)
        # loading custom font
        self.font = tkfont.Font(
            self.root,
            font=settings.FONT_LOC,
            name="proximanova-black"
        )

        # -----------------variables----------------------
        self.bet_amount = tk.DoubleVar(value=0.00)
        self.num_of_mines = tk.IntVar(value=3)
        self.num_of_mines.trace_add("write", lambda *args: leftFrame.change_num_of_mines(self.num_of_mines))
        self.bet_on = tk.BooleanVar()
        # --------------------------------------------------

        self.left_frame = ctk.CTkFrame(
            master=self.root,
            height=utils.height_prct(100),
            width=utils.width_prct(25),
            fg_color=settings.LEFT_FRAME_CLR,
            bg_color=settings.LEFT_FRAME_CLR,
            corner_radius=0
        )

        self.left_frame.place(
            x=utils.width_prct(0),
            y=utils.height_prct(0)
        )
        self.left_frame.grid_propagate(False)  # Prevent frame from resizing based on content

        # creates the left frame, as desired, before placing a bet
        leftFrame.left_frame_before_bet(self)

        self.right_frame = ctk.CTkFrame(
            master=self.root,
            height=utils.height_prct(100),
            width=utils.width_prct(75),
            fg_color=settings.RIGHT_FRAME_CLR,
            corner_radius=0,
        )

        self.right_frame.place(
            x=utils.width_prct(25),
            y=utils.height_prct(0)
        )

        right_frame_height = self.right_frame.cget("height")
        right_frame_width = self.right_frame.cget("width")
        self.cells_frame = ctk.CTkFrame(
            master=self.right_frame,
            height=utils.any_prct(right_frame_height, 75),
            width=utils.any_prct(right_frame_width, 75),
            fg_color=settings.CELLS_FRAME_CLR
        )

        cells_frame_height = self.cells_frame.cget("height")
        cells_frame_width = self.cells_frame.cget("width")
        x_coord = right_frame_width - cells_frame_width
        y_coord = right_frame_height - cells_frame_height

        self.cells_frame.place(
            x=utils.any_prct(x_coord, 80),
            y=utils.any_prct(y_coord, 20)
        )

        self.cells(state=True)  # state=True means we need the cells to be of tk.DISABLED

    def cells(self, state=False):
        for x in range(settings.CELLS_IN_ROW):
            for y in range(settings.CELLS_IN_ROW):
                cell = cells.Cells(x, y, self.BET_BUTTON)
                cell.create_btn_object(self.cells_frame)
                cell.cell_btn_object.grid(
                    row=x,
                    column=y,
                    padx=5,
                    pady=5
                )

                if state:
                    cell.cell_btn_object.configure(state=tk.DISABLED)

        cells.Cells.randomize_mines()

    def bet_click(self):
        self.bet_on.set(not self.bet_on.get())

        # betting the first time
        if settings.FIRST_CLICK:
            settings.FIRST_CLICK = False
            settings.GAME_OVER = False
            leftFrame.placing_left_frame_elements_after_placing_bet(self)
            self.new_bet()

        # when cashout
        elif not self.bet_on.get():
            settings.GAME_OVER = True
            # if you cashout, that means you have won
            # settings.WINS += 1
            cells.Cells.probability_change()
            cells.Cells.show_cells_and_disable()
            leftFrame.reset_left_frame(self)

        # when betting for >1 times
        else:
            settings.GAME_OVER = False
            cells.Cells.show_cells_and_disable()
            # cells.Cells.probability_change()
            leftFrame.placing_left_frame_elements_after_placing_bet(self)

            self.new_bet()

    def new_bet(self) -> None:
        """
        When you click on Bet button
        it destroys all the cells and creates new cells
        the probabilities of the cells do no change though

        :return: None
        """

        # destroys all the existing cells
        for cell in cells.Cells.all:
            cell.cell_btn_object.destroy()
            # self.root.update()

        # for p in cells.Cells.probabilities:
        #     print(p, end=" ")
        # print()

        # resets the clicked cell list
        cells.Cells.clicked_cells = []
        # resets the all cells list
        cells.Cells.all = []
        # creates new cells
        self.cells()
        print(f"{settings.WINS = }")
        print(f"{settings.LOSSES = }")

    def pick_random_tile_(self):

        if not settings.GAME_OVER:
            while True:
                chosen_cell = random.choice(cells.Cells.all)
                if chosen_cell not in cells.Cells.clicked_cells:
                    cells.Cells.cell_click(chosen_cell)
                    break


if __name__ == "__main__":
    root = ctk.CTk()
    obj = Win()
    root.mainloop()