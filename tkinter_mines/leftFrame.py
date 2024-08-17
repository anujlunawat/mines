import customtkinter as ctk

import cells
import settings
import utils


def left_frame_before_bet(self):
    self.bet_amount_label = ctk.CTkLabel(
        master=self.left_frame,
        text="Bet Amount",
        font=(self.font, settings.FONT_SIZE)
    )

    self.bet_amount_label.grid(
        row=0,
        column=0,
        padx=settings.PAD_X_LEFT_FRAME,
        pady=settings.PAD_Y_LEFT_FRAME,
        ipady=5,
        sticky=ctk.SW
    )

    self.bet_amount_frame = ctk.CTkFrame(
        self.left_frame,
        height=settings.BET_AMOUNT_FRAME_HEIGHT,
        width=utils.any_prct(utils.width_prct(25), 80),
        # bg_color=settings.BET_INPUT_BTN_CLR,
        # border_color=settings.BET_INPUT_BTN_CLR,
        fg_color=settings.BET_INPUT_BTN_CLR,
        corner_radius=5
        # border_width=10
    )
    self.bet_amount_frame.grid(
        row=1,
        column=0,
        padx=settings.PAD_X_LEFT_FRAME,
        ipadx=1.5,
        pady=settings.PAD_Y_LEFT_FRAME
    )

    self.bet_amount_entry = ctk.CTkEntry(
        master=self.bet_amount_frame,
        height=utils.any_prct(settings.BET_AMOUNT_FRAME_HEIGHT, 65),
        width=utils.any_prct(utils.any_prct(utils.width_prct(25), 80), 60),
        fg_color=settings.CELL_CLICK_CLR,
        # bg_color=settings.CELL_CLICK_CLR,
        font=(self.font, settings.FONT_SIZE),
        placeholder_text="0.00",
        border_width=0,
        corner_radius=0,
        textvariable=self.bet_amount
    )
    self.bet_amount_entry.grid(
        row=0,
        column=0,
        padx=2
    )

    self.half_amount_btn = ctk.CTkButton(
        self.bet_amount_frame,
        height=utils.any_prct(settings.BET_AMOUNT_FRAME_HEIGHT, 75),
        width=utils.any_prct(utils.any_prct(utils.width_prct(25), 80), 20),
        text="½",
        font=(self.font, settings.FONT_SIZE),
        fg_color=settings.BET_INPUT_BTN_CLR,
        border_width=0,
        corner_radius=0,
        hover_color=settings.HALF_DOUBLE_BTN_HOVER_CLR,
        command=lambda: half_amount(self)
    )
    self.half_amount_btn.grid(
        row=0,
        column=1,
    )

    self.double_amount_btn = ctk.CTkButton(
        self.bet_amount_frame,
        height=utils.any_prct(settings.BET_AMOUNT_FRAME_HEIGHT, 75),
        width=utils.any_prct(utils.any_prct(utils.width_prct(25), 80), 20),
        text="2x",
        font=(self.font, settings.FONT_SIZE),
        fg_color=settings.BET_INPUT_BTN_CLR,
        border_width=0,
        corner_radius=0,
        hover_color=settings.HALF_DOUBLE_BTN_HOVER_CLR,
        command=lambda: double_amount(self)
    )
    self.double_amount_btn.grid(
        row=0,
        column=2,
    )

    self.mines_amount_label = ctk.CTkLabel(
        master=self.left_frame,
        text="Mines",
        font=(self.font, settings.FONT_SIZE)
    )

    self.mines_amount_label.grid(
        row=3,
        column=0,
        padx=settings.PAD_X_LEFT_FRAME,
        sticky='W',
        pady=settings.PAD_Y_LEFT_FRAME,
    )

    self.mines_amount_dd_menu = ctk.CTkOptionMenu(
        self.left_frame,
        values=[str(i) for i in range(1, settings.CELLS_IN_ROW ** 2)],
        height=settings.BET_AMOUNT_FRAME_HEIGHT - 15,
        width=utils.any_prct(utils.width_prct(25), 80),
        font=(self.font, settings.FONT_SIZE),
        fg_color=settings.CELL_CLICK_CLR,
        dropdown_fg_color=settings.CELL_CLICK_CLR,
        button_color=settings.CELL_CLICK_CLR,
        hover=False,
        variable=self.num_of_mines_dd,
        # dropdown_font=(self.font, settings.FONT_SIZE)
    )

    self.mines_amount_dd_menu.grid(
        row=4,
        column=0,
        pady=settings.PAD_Y_LEFT_FRAME,
    )

    self.BET_BUTTON = ctk.CTkButton(
        self.left_frame,
        height=settings.BET_AMOUNT_FRAME_HEIGHT,
        width=utils.any_prct(utils.width_prct(25), 80),
        font=(self.font, settings.FONT_SIZE, "bold"),
        fg_color=settings.BET_BUTTON_CLR,
        text="Bet",
        text_color="black",
        hover_color=settings.BET_BUTTON_HOVER_CLR,
        command=self.bet_click,
    )
    self.BET_BUTTON.grid(
        row=8,
        column=0,
        pady=settings.PAD_Y_LEFT_FRAME,
    )

    # -------------------Total Profit Label----------------------------
    self.total_profit_label = ctk.CTkLabel(
        master=self.left_frame,
        text="Total profit (1.00x)",
        font=(self.font, settings.FONT_SIZE)
    )

    # ---------------------Total Profit Entry--------------------------
    self.total_profit_entry = ctk.CTkEntry(
        self.left_frame,
        height=utils.any_prct(settings.BET_AMOUNT_FRAME_HEIGHT, 75),
        width=utils.any_prct(utils.width_prct(25), 80),
        placeholder_text="0.00",
        font=(self.font, settings.FONT_SIZE),
        fg_color=settings.BET_PLACED_LEFT_FRAME_CLR,
        border_width=0,
        corner_radius=5,
        placeholder_text_color='white',
        # hover_color=settings.HALF_DOUBLE_BTN_CLICK_CLR,
        # state=ctk.DISABLED
    )

    # -----------------Pick random tile--------------------------------
    self.pick_random_tile = ctk.CTkButton(
        self.left_frame,
        height=utils.any_prct(settings.BET_AMOUNT_FRAME_HEIGHT, 75),
        width=utils.any_prct(utils.width_prct(25), 80),
        text="Pick random tile",
        font=(self.font, settings.FONT_SIZE),
        fg_color=settings.BET_PLACED_LEFT_FRAME_CLR,
        border_width=0,
        corner_radius=5,
        hover_color=settings.HALF_DOUBLE_BTN_HOVER_CLR,
        command=self.pick_random_tile_,
    )


def half_amount(self):
    self.bet_amount.set(self.bet_amount.get() * 0.5)


def double_amount(self):
    self.bet_amount.set(self.bet_amount.get() * 2)


def change_num_of_mines(n):
    settings.NUMBER_OF_MINES = int(n.get())


def placing_left_frame_elements_after_placing_bet(self):
    self.BET_BUTTON.configure(text="Cashout")

    # --------------Total Profit Label---------------------------
    self.total_profit_label.grid(
        row=5,
        column=0,
        padx=settings.PAD_X_LEFT_FRAME,
        pady=settings.PAD_Y_LEFT_FRAME,
        sticky='W'
    )

    self.root.update()

    # --------------------Total Profit Entry------------------------
    self.total_profit_entry.grid(
        row=6,
        column=0,
        pady=settings.PAD_Y_LEFT_FRAME,
    )
    # disable the user to make changes to the entry
    self.total_profit_entry.configure(state=ctk.DISABLED)

    self.root.update()

#   -----------------Pick random tile-------------------------------
    self.pick_random_tile.grid(
        row=7,
        column=0,
        pady=settings.PAD_Y_LEFT_FRAME,
    )
    self.root.update()

#   -----------------changing the colours of widgets---------------------
    self.mines_amount_dd_menu.configure(fg_color=settings.BET_PLACED_LEFT_FRAME_CLR)
    self.mines_amount_dd_menu.configure(button_color=settings.BET_PLACED_LEFT_FRAME_CLR)

#   ------------------disable the widgets--------------------------------
    self.bet_amount_entry.configure(state=ctk.DISABLED)
    self.half_amount_btn.configure(state=ctk.DISABLED)
    self.double_amount_btn.configure(state=ctk.DISABLED)
    self.mines_amount_dd_menu.configure(state=ctk.DISABLED)
    self.BET_BUTTON.configure(state=ctk.DISABLED)


def reset_left_frame(self):
    """
    Resets the left frame as it was before placing the bet
    :param self:
    """
    # change the test from "Cashout" to "Bet"
    self.BET_BUTTON.configure(text="Bet")

    # de-grid the widgets that are not needed
    self.total_profit_label.grid_forget()
    self.total_profit_entry.grid_forget()
    self.pick_random_tile.grid_forget()
    # self.root.update()

    # activate the required elements
    self.bet_amount_entry.configure(state=ctk.NORMAL)
    self.half_amount_btn.configure(state=ctk.NORMAL)
    self.double_amount_btn.configure(state=ctk.NORMAL)
    self.mines_amount_dd_menu.configure(state=ctk.NORMAL)
    self.BET_BUTTON.configure(state=ctk.NORMAL)

