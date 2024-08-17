import pygame
pygame.init()
from sys import exit
import settings
import utils
import cells
import leftFrame


class Mines:
    def __init__(self, WIN):
        self.win = WIN
        pygame.display.set_caption("Mines")
        self.clock = pygame.time.Clock()
        self.partition()
        self.cells_sprites = pygame.sprite.Group()
        self.cm = cells.CellsMain(self.win)
        self.cells_sprites = self.cm.cells_sprites
        self.cell_clr = settings.CELL_FG_COLOUR

        clr = settings.BLUE_GRAY
        text = "1.00"
        # leftFrame.bet_amount_text.convert_alpha()
        dropdown_open = False
        leftFrame.config()

        while True:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                #     mouse_pos = pygame.mouse.get_pos()
                #
                #     if leftFrame.bet_btn_rect.collidepoint(mouse_pos):
                #         # Start new game
                #         if cells.CellsMain.game_over:
                #             print("game not over")
                #             cells.CellsMain.game_over = not cells.CellsMain.game_over
                #             self.cm.update()
                #             self.cells_sprites = self.cm.cells_sprites
                #         elif settings.GEMS_CLICKED:
                #             print("game over")
                #             cells.CellsMain.game_over = not cells.CellsMain.game_over
                #             self.cm.cells_sprites.sprites()[0].display_and_disable_cells()

                if not cells.CellsMain.game_over:

                    if event.type == pygame.MOUSEMOTION:
                        mouse_pos = pygame.mouse.get_pos()

                        for cell in self.cells_sprites:
                            if not cell.active:
                                continue
                            if cell.rect.collidepoint(mouse_pos):
                                cell.cell_colour = settings.CELLS_HOVER_CLR
                            else:
                                cell.cell_colour = settings.CELL_FG_COLOUR

                    elif event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                        mouse_pos = pygame.mouse.get_pos()

                        if leftFrame.bet_btn_rect.collidepoint(mouse_pos):
                            if settings.GEMS_CLICKED:
                                print("game over")
                                cells.CellsMain.game_over = not cells.CellsMain.game_over
                                self.cm.cells_sprites.sprites()[0].display_and_disable_cells()

                        else:
                            for cell in self.cells_sprites:
                                if cell.active and cell.rect.collidepoint(mouse_pos) and not self.cm.cell_animation_on:
                                    cell.animation_on = 1
                                    cell.clicked = True
                                    if not cell.isMine: settings.GEMS_CLICKED += 1

                else:

                    if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                        mouse_pos = pygame.mouse.get_pos()
                        # if you click the button to input your bet
                        if leftFrame.bet_input_rect.collidepoint(mouse_pos):
                            clr = settings.BLACK
                        else:
                            clr = settings.BLUE_GRAY

                        if leftFrame.bet_btn_rect.collidepoint(mouse_pos):
                            # Start new game
                            if not dropdown_open:
                                print("game not over")
                                cells.CellsMain.game_over = not cells.CellsMain.game_over
                                self.cm.update()
                                self.cells_sprites = self.cm.cells_sprites

                        # clicking on the button to change the number of mines
                        if leftFrame.numofmines_dd_head_rect.collidepoint(mouse_pos):
                            dropdown_open = True
                            print("dd open")
                        else:
                            dropdown_open = False
                            print("dd close")

                    if event.type == pygame.KEYUP and clr == settings.BLACK:
                        if event.key == pygame.K_RETURN:
                            clr = settings.BLUE_GRAY
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            if event.unicode.isdigit() or (event.unicode == '.' if text.find('.') == -1 else False):
                                text += event.unicode

            # ---------------Blit surfaces on the main surface------------------
            self.win.fill(settings.BG_COLOUR)
            # self.win.blit(self.left_part_surf, self.left_part_rect)
            self.cells_sprites.update()

            leftFrame.blit_in_seq(self.win, clr, cells.CellsMain.game_over, text, dropdown_open)

            pygame.display.update()

    def partition(self):
        # ------------------left part of the main window----------------
        self.left_part_surf = pygame.Surface((
            int(utils.width_prct(25)), int(utils.height_prct(100))
        )).convert_alpha()

        self.left_part_surf.fill(settings.LEFT_PART_COLOUR)
        self.left_part_rect = self.left_part_surf.get_rect(topleft=(0, 0))


if __name__ == "__main__":
    WIN = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    obj = Mines(WIN)
    pygame.quit()
