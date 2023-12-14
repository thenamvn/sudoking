import pygame
import sys
import os
from Sudoku import Sudoku

class SudokuMenu:
    def __init__(self):
        pygame.init()
        self.difficulty = 0
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("SudoKing - Menu")

        self.clock = pygame.time.Clock()
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.background_image_path = os.path.join(self.current_dir, 'assets/menu.jpg')
        self.background_image = pygame.image.load(self.background_image_path)
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))

        self.play_button_rect = pygame.Rect(350, 250, 100, 50)
        self.play_clicked = False
        self.quit_button_rect = pygame.Rect(350, 350, 100, 50)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def draw_button(self, surface, color, x, y, width, height, text):
        pygame.draw.rect(surface, color, (x, y, width, height))
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
        surface.blit(text_surface, text_rect)

    def draw_difficulty_buttons(self):
        # Draw difficulty buttons
        font = pygame.font.Font(None, 36)
        easy_button_rect = pygame.Rect(50, 150, 200, 50)
        medium_button_rect = pygame.Rect(50, 250, 200, 50)
        hard_button_rect = pygame.Rect(50, 350, 200, 50)

        pygame.draw.rect(self.screen, (0, 128, 255), easy_button_rect)
        pygame.draw.rect(self.screen, (0, 128, 0), medium_button_rect)
        pygame.draw.rect(self.screen, (255, 0, 0), hard_button_rect)

        text_easy = font.render("Easy", True, (255, 255, 255))
        text_medium = font.render("Medium", True, (255, 255, 255))
        text_hard = font.render("Hard", True, (255, 255, 255))

        self.screen.blit(text_easy, (easy_button_rect.x + 10, easy_button_rect.y + 10))
        self.screen.blit(text_medium, (medium_button_rect.x + 10, medium_button_rect.y + 10))
        self.screen.blit(text_hard, (hard_button_rect.x + 10, hard_button_rect.y + 10))

        return easy_button_rect, medium_button_rect, hard_button_rect
    
    def run(self):
        game = None  # Initialize the Sudoku instance outside the loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button_rect.collidepoint(event.pos):
                        self.play_clicked = True
                    elif self.quit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            self.screen.blit(self.background_image, (0, 0))
            self.draw_button(self.screen, (0, 128, 255), 350, 250, 100, 50, "Play")
            self.draw_button(self.screen, (255, 0, 0), 350, 350, 100, 50, "Quit")

            if self.play_clicked:
                while True:
                    easy_button_rect, medium_button_rect, hard_button_rect = self.draw_difficulty_buttons()
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if easy_button_rect.collidepoint(pygame.mouse.get_pos()):
                                self.set_difficulty(40)
                            elif medium_button_rect.collidepoint(pygame.mouse.get_pos()):
                                self.set_difficulty(50)
                            elif hard_button_rect.collidepoint(pygame.mouse.get_pos()):
                                self.set_difficulty(60)
                            # Create Sudoku instance here
                            game = Sudoku(self.difficulty)
                            game.main()  # Start the Sudoku game
                    pygame.display.flip()

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    menu = SudokuMenu()
    menu.run()

if __name__ == "__main__":
    menu = SudokuMenu()
    menu.run()
