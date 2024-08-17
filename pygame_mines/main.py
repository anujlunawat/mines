import os
import time

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
        self.frame_rect = None

        clr = settings.BLUE_GRAY
        text = "1.00"
        # leftFrame.bet_amount_text.convert_alpha()
        dropdown_open = False
        leftFrame.config()
        frame = None

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
                            # Checkout when at least one cell is opened
                            if settings.GEMS_CLICKED:
                                cells.CellsMain.game_over = not cells.CellsMain.game_over

                                settings.checkout_sound.play(maxtime=settings.maxtime)
                                utils.is_sound_playing()

                                self.cm.cells_sprites.sprites()[0].display_and_disable_cells()

                        else:
                            for cell in self.cells_sprites:
                                if cell.active and cell.rect.collidepoint(mouse_pos) and not self.cm.cell_animation_on:
                                    cell.animation_on = 1
                                    cell.clicked = True
                                    if not cell.isMine: settings.GEMS_CLICKED += 1
                                    else: self.get_frame_rect(cell, frame := 0)

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
                                frame = None
                                cells.CellsMain.game_over = not cells.CellsMain.game_over
                                self.cm.update()

                                settings.start_bet_sound.play(maxtime=settings.maxtime)
                                utils.is_sound_playing()

                                self.cells_sprites = self.cm.cells_sprites

                        # clicking on the button to change the number of mines
                        if leftFrame.numofmines_dd_head_rect.collidepoint(mouse_pos):
                            dropdown_open = True
                        else:
                            dropdown_open = False

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

            if frame is not None:
                if frame >= len(settings.gif_frames):
                    frame = 0
                self.win.blit(settings.gif_frames[frame], self.frame_rect)
                # draw the mine above the gif
                mine_rect = settings.MINE_IMAGE.get_rect(center=self.frame_rect.center)
                self.win.blit(settings.MINE_IMAGE, mine_rect)
                frame += 1

            leftFrame.blit_in_seq(self.win, clr, cells.CellsMain.game_over, text, dropdown_open)

            pygame.display.update()

    def partition(self):
        # ------------------left part of the main window----------------
        self.left_part_surf = pygame.Surface((
            int(utils.width_prct(25)), int(utils.height_prct(100))
        )).convert_alpha()

        self.left_part_surf.fill(settings.LEFT_PART_COLOUR)
        self.left_part_rect = self.left_part_surf.get_rect(topleft=(0, 0))

    def get_frame_rect(self, cell, frame):
        self.frame_rect = settings.gif_frames[frame].get_rect(center=cell.rect.center)


if __name__ == "__main__":
    WIN = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    obj = Mines(WIN)
    pygame.quit()
