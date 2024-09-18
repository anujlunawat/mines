import pygame
import settings
import pygame.freetype
from cells import CellsMain

addl_padding = 15

bet_amount_text = None
bet_amount_text_rect = None

mines_text = None
mines_text_rect = None

bet_input_rect = None

numofmines_dd_head_rect = None

menu_items = [n for n in range(1, settings.CELLS_IN_ROW**2)]
item_height = 20
menu_rect = None

profit_amount_rect = None
total_profit_text_rect = None

bet_btn_rect = None


def config():
    global bet_amount_text, bet_amount_text_rect
    global mines_text, mines_text_rect
    global numofmines_dd_head_rect
    global menu_rect

    # -----------------------------TEXT: BET AMOUNT-------------------------------------------
    bet_amount_text = settings.FONT.render("Bet Amount", settings.FONT_COLOUR, settings.LEFT_PART_COLOUR, style=settings.FONT_STYLE)[0].convert_alpha()
    bet_amount_text_rect = bet_amount_text.get_rect(topleft=(settings.LEFT_PART_x, settings.LEFT_PART_y))

    settings.LEFT_PART_y += bet_amount_text.get_height() + addl_padding

    # ----------------------------------TEXT: MINES---------------------------------------------
    mines_text = settings.FONT.render("Mines", settings.FONT_COLOUR, settings.LEFT_PART_COLOUR, style=settings.FONT_STYLE)[0].convert_alpha()
    mines_text_rect = mines_text.get_rect(topleft=
                                          (settings.LEFT_PART_x,
                                           settings.LEFT_PART_y + settings.LEFT_WIN_HEIGHT + addl_padding)
                                          )

    # -----------------------------------CHANGE NUMBER OF MINES-----------------------------------
    numofmines_dd_head_rect = pygame.Rect(
        settings.LEFT_PART_x,
        mines_text_rect.bottom + addl_padding,
        settings.LEFT_WIN_WIDTH,
        settings.LEFT_WIN_HEIGHT
    )

    # ------------------------------DROPDOWN MENU FOR SELECTING NUMBER OF MINES----------------------
    menu_rect = pygame.Rect(
        settings.LEFT_PART_x,
        numofmines_dd_head_rect.bottom,
        settings.LEFT_WIN_WIDTH,
        item_height * len(menu_items)
    )


def display_text(surface):
    # Text: Bet Amount
    surface.blit(bet_amount_text, bet_amount_text_rect)
    # Text: Mines
    surface.blit(mines_text, mines_text_rect)


def bet_input(surface, clr, text):
    global bet_input_rect

    bet_amount = settings.FONT.render(text, settings.WHITE, style=settings.FONT_STYLE)[0].convert_alpha()

    bet_input_btn_rect = pygame.Rect(
        settings.LEFT_PART_x,
        settings.LEFT_PART_y,
        max(settings.LEFT_WIN_WIDTH, bet_amount.get_width() + 24),
        settings.LEFT_WIN_HEIGHT
    )

    if bet_input_btn_rect.collidepoint(mouse_pos) and CellsMain.game_over: clr = settings.BLACK
    bet_input_rect = pygame.draw.rect(surface, clr, bet_input_btn_rect, border_radius=settings.rect_border_rad)

    bet_amount_rect = bet_amount.get_rect(centery=bet_input_rect.centery, left=bet_input_rect.x + 13)
    surface.blit(bet_amount, bet_amount_rect)


def num_of_mines_dd(surface, dropdown_open):
    global numofmines_dd_head_rect, menu_rect

    # set the color of the numofmines_dd_head accordingly
    clr = settings.BLACK if numofmines_dd_head_rect.collidepoint(mouse_pos) and CellsMain.game_over else settings.BLUE_GRAY
    pygame.draw.rect(surface, clr, numofmines_dd_head_rect, border_radius=settings.rect_border_rad)

    # display the current number of mines
    # this is determined by the settings.NUMBER_OF_MINES variable, which can be changed by clicking on any option of the drop-down menu
    numofmines_text = settings.FONT.render(f"{settings.NUMBER_OF_MINES}", settings.FONT_COLOUR, style=settings.FONT_STYLE)[0].convert_alpha()
    numofmines_text_rect = numofmines_text.get_rect(center=numofmines_dd_head_rect.center)
    surface.blit(numofmines_text, numofmines_text_rect)

    # draw the drop-down menu
    if dropdown_open:
        for i, item in enumerate(menu_items):
            top = numofmines_text_rect.bottom + ((i + .5) * item_height)
            r = pygame.Rect(menu_rect.left, top, menu_rect.width, item_height)

            txt = settings.FONT_SMALL.render(f"{item}", settings.FONT_COLOUR, style=settings.FONT_STYLE)[0].convert_alpha()
            txt_rect = txt.get_rect(center=r.center)

            is_hovered = r.collidepoint(mouse_pos)
            if is_hovered:
                settings.NUMBER_OF_MINES = i + 1
            pygame.draw.rect(surface, settings.BLACK if is_hovered else settings.BLUE_GRAY, r)
            surface.blit(txt, txt_rect)


def total_profit_(surface, game_over, text):
    global total_profit_text_rect, profit_amount_rect
    # Text: Total Profit (multiplier)

    # total_p = settings.MULTIPLIER[settings.GEMS_CLICKED][settings.NUMBER_OF_MINES] if settings.GEMS_CLICKED else '1.00x'
    try:
        total_p = settings.MULTIPLIER[settings.GEMS_CLICKED][settings.NUMBER_OF_MINES]
    except Exception:
        total_p = '1.00x'

    total_profit = settings.FONT.render(
        f"Total Profit ({total_p})",
        settings.FONT_COLOUR,
        settings.LEFT_PART_COLOUR,
        style=settings.FONT_STYLE
    )[0]

    total_profit_text_rect = total_profit.get_rect(topleft=(
        settings.LEFT_PART_x,
        numofmines_dd_head_rect.bottom + addl_padding)
    )

    if not game_over:
        # rect to display the total profit in numbers
        profit_amount_rect = pygame.draw.rect(
            surface,
            settings.BLUE_GRAY,
            pygame.Rect(settings.LEFT_PART_x, total_profit_text_rect.bottom + addl_padding, settings.LEFT_WIN_WIDTH, settings.LEFT_WIN_HEIGHT),
            border_radius=settings.rect_border_rad
        )
        # the amount to be displayed in the rect
        profit_amount_text = settings.FONT.render(
            f"{float(text) * float(total_p.strip('x')) : .2f}",
            settings.FONT_COLOUR,
            # settings.LEFT_PART_COLOUR,
            style=settings.FONT_STYLE
        )[0].convert_alpha()
        profit_amount_rect = profit_amount_text.get_rect(center=profit_amount_rect.center)

        surface.blit(total_profit, total_profit_text_rect)
        surface.blit(profit_amount_text, profit_amount_rect)


def bet_button(surface, game_over):
    global total_profit_text_rect, profit_amount_rect
    global bet_btn_rect

    if not game_over:
        y = profit_amount_rect.bottom + addl_padding
        txt = 'Cashout'
    else:
        y = total_profit_text_rect.top
        txt = 'Bet'

    btn_pos_rect = pygame.Rect(
        settings.LEFT_PART_x,
        y + addl_padding,
        settings.LEFT_WIN_WIDTH,
        settings.LEFT_WIN_HEIGHT + 7  # added 7 to its height just to make it look bigger
    )

    clr = settings.GREEN_FOCUS if btn_pos_rect.collidepoint(mouse_pos) else settings.GREEN
    bet_btn_rect = pygame.draw.rect(
        surface,
        clr,
        btn_pos_rect,
        border_radius=settings.rect_border_rad
    )
    bet_btn_text = settings.FONT.render(
        txt,
        settings.FONT_COLOUR,
        # settings.LEFT_PART_COLOUR,
        style=settings.FONT_STYLE
    )[0].convert_alpha()

    btn_pos_rect = bet_btn_text.get_rect(center=bet_btn_rect.center)
    surface.blit(bet_btn_text, btn_pos_rect)


def blit_in_seq(surface, clr, game_over, text, dd_open):
    global mouse_pos
    mouse_pos = pygame.mouse.get_pos()

    display_text(surface)
    bet_input(surface, clr, text)
    total_profit_(surface, game_over, text)
    bet_button(surface, game_over)
    num_of_mines_dd(surface, dd_open)
