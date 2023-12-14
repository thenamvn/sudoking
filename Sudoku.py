import pygame
import sys
import copy
import random
class Sudoku:
    def __init__(self,difficulty):
        self.difficulty = difficulty
        self.WIDTH = 9
        self.HEIGHT = 9
        self.CELL_SIZE = 50
        self.BOARD_SIZE = self.WIDTH * self.CELL_SIZE
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)

        self.board_to_solve = self.generate_sudoku()
        self.original_board = copy.deepcopy(self.board_to_solve)
        self.solving_board = copy.deepcopy(self.board_to_solve)
        self.solve(self.solving_board)
        self.print_board(self.solving_board)

        self.count_mistake = 0
        self.cell_colors = [[(128, 128, 128) for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        self.player_input = [[0 for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        self.selected_cell = None
        self.game_over = False
        self.display_lose = False
        self.game_reset = False

        pygame.init()
        self.screen = pygame.display.set_mode((self.BOARD_SIZE, self.BOARD_SIZE + 100))
        pygame.display.set_caption("Sudoking")
        self.clock = pygame.time.Clock()

    def generate_sudoku(self):
        board = [[0 for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        for _ in range(10):
            i, j, num = random.randint(0, 8), random.randint(0, 8), random.randint(1, 9)
            if self.validate(board, num, (i, j)):
                board[i][j] = num

        self.solve(board)
#trừ đi ngẫu nhiên các  số để người dùng tự hoàn thành bảng vì self.solve(board) sẽ tạo ra 1 board đầy đủ
        for _ in range(self.difficulty):
            i, j = random.randint(0, 8), random.randint(0, 8)
            board[i][j] = 0

        return board

    def solve(self, board):
        find = self.empty_search(board)
        if not find:
            return True
        else:
            y, x = find

        for i in range(1, 10):
            if self.validate(board, i, (y, x)):
                board[y][x] = i

                if self.solve(board):
                    return True

                board[y][x] = 0
        return False

    def validate(self, board, num, pos):
        for i in range(self.WIDTH):
            if board[pos[0]][i] == num and pos[1] != i:
                return False
        for i in range(self.HEIGHT):
            if board[i][pos[1]] == num and pos[0] != i:
                return False
        box_pos_x = pos[1] // 3
        box_pos_y = pos[0] // 3
        for i in range(box_pos_y * 3, box_pos_y * 3 + 3):
            for j in range(box_pos_x * 3, box_pos_x * 3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False
        return True

    def empty_search(self, board):
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def print_board(self, board):
        for i in range(self.HEIGHT):
            if i % 3 == 0 and i != 0:
                print("-----------------------")
            for j in range(self.WIDTH):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")
                if j == 8:
                    print(board[i][j])
                else:
                    print(str(board[i][j]) + " ", end="")

    def draw_board(self, board):
        pygame.draw.rect(self.screen, self.BLACK, (0, 0, self.BOARD_SIZE, self.BOARD_SIZE), 2)
        for i in range(self.WIDTH):
            pygame.draw.line(self.screen, self.BLACK, (0, i * self.CELL_SIZE), (self.BOARD_SIZE, i * self.CELL_SIZE), 2)
            pygame.draw.line(self.screen, self.BLACK, (i * self.CELL_SIZE, 0), (i * self.CELL_SIZE, self.BOARD_SIZE), 2)
            if i % 3 == 0 and i != 0:
                pygame.draw.line(self.screen, self.BLACK, (0, i * self.CELL_SIZE - 1), (self.BOARD_SIZE, i * self.CELL_SIZE - 1), 6)
                pygame.draw.line(self.screen, self.BLACK, (i * self.CELL_SIZE - 1, 0), (i * self.CELL_SIZE - 1, self.BOARD_SIZE), 6)
            for j in range(self.WIDTH):
                if board[i][j] != 0:
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(board[i][j]), True, self.BLACK)
                    self.screen.blit(text, (j * self.CELL_SIZE + 15, i * self.CELL_SIZE + 15))

    def boards_are_equal(self, board1, board2):
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if board1[i][j] != board2[i][j]:
                    return False
        return True

    def update_board(self, original_board, player_input):
        updated_board = [row[:] for row in original_board]
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if player_input[i][j] != 0:
                    updated_board[i][j] = player_input[i][j]
        return updated_board

    def new_game(self):
        self.count_mistake = 0
        self.cell_colors = [[(128, 128, 128) for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        self.player_input = [[0 for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        self.selected_cell = None
        self.game_over = False
        self.display_lose = False
        self.game_reset = False

        self.board_to_solve = self.generate_sudoku()
        self.original_board = copy.deepcopy(self.board_to_solve)
        self.solving_board = copy.deepcopy(self.board_to_solve)
        self.solve(self.solving_board)
        self.print_board(self.solving_board)

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    self.selected_cell = (y // self.CELL_SIZE, x // self.CELL_SIZE)
                    if self.solve_button_rect.collidepoint(event.pos):
                        if self.display_lose:
                            self.display_lose = False
                        for i in range(self.HEIGHT):
                            for j in range(self.WIDTH):
                                self.player_input[i][j] = 0
                                self.cell_colors[i][j] = (128, 128, 128)
                        for i in range(self.HEIGHT):
                            for j in range(self.WIDTH):
                                self.original_board[i][j] = self.solving_board[i][j]
                    elif self.quit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    elif self.newgame_button_rect.collidepoint(event.pos):
                        self.game_reset = True
                elif event.type == pygame.KEYDOWN and not self.game_over:
                    if self.selected_cell is not None and self.original_board[self.selected_cell[0]][self.selected_cell[1]] == 0:
                        try:
                            self.player_input[self.selected_cell[0]][self.selected_cell[1]] = int(event.unicode)
                        except ValueError:
                            pass
                        if self.player_input[self.selected_cell[0]][self.selected_cell[1]] != self.solving_board[self.selected_cell[0]][self.selected_cell[1]]:
                            self.cell_colors[self.selected_cell[0]][self.selected_cell[1]] = self.RED
                            self.count_mistake += 1
                            if self.count_mistake > 5:
                                self.game_over = True
                                self.display_lose = True
                        else:
                            self.cell_colors[self.selected_cell[0]][self.selected_cell[1]] = self.GREEN

            self.screen.fill(self.WHITE)
            self.draw_board(self.original_board)
            updated_board = self.update_board(self.original_board, self.player_input)
            if self.boards_are_equal(updated_board, self.solving_board):
                font = pygame.font.Font(None, 100)
                text_surface = font.render("You Win!", True, (255, 255, 0))
                text_rect = text_surface.get_rect()
                text_rect.center = (self.BOARD_SIZE // 2, self.BOARD_SIZE // 2)
                self.screen.blit(text_surface, text_rect)

            for i in range(self.HEIGHT):
                for j in range(self.WIDTH):
                    if self.player_input[i][j] != 0:
                        font = pygame.font.Font(None, 36)
                        text = font.render(str(self.player_input[i][j]), True, self.BLACK)
                        self.screen.blit(text, (j * self.CELL_SIZE + 15, i * self.CELL_SIZE + 15))

            if self.selected_cell is not None:
                if 0 <= self.selected_cell[0] < self.HEIGHT and 0 <= self.selected_cell[1] < self.WIDTH:
                    pygame.draw.rect(self.screen, self.cell_colors[self.selected_cell[0]][self.selected_cell[1]],(self.selected_cell[1] * self.CELL_SIZE, self.selected_cell[0] * self.CELL_SIZE,self.CELL_SIZE, self.CELL_SIZE), 2)

            button_width = 100
            button_height = 50
            button_color = (150, 150, 150)

            self.quit_button_rect = pygame.Rect(10, self.BOARD_SIZE + 20, button_width, button_height)
            pygame.draw.rect(self.screen, button_color, self.quit_button_rect)
            font = pygame.font.Font(None, 36)
            text = font.render("Quit", True, self.BLACK)
            self.screen.blit(text, (15, self.BOARD_SIZE + 30))

            self.solve_button_rect = pygame.Rect(self.BOARD_SIZE - button_width - 10, self.BOARD_SIZE + 20, button_width,button_height)
            pygame.draw.rect(self.screen, button_color, self.solve_button_rect)
            text = font.render("Solve", True, self.BLACK)
            self.screen.blit(text, (self.BOARD_SIZE - button_width + 5, self.BOARD_SIZE + 30))

            self.newgame_button_rect = pygame.Rect(self.BOARD_SIZE - button_width - 180 - 25, self.BOARD_SIZE + 60,button_width + 50, button_height)
            pygame.draw.rect(self.screen, button_color, self.newgame_button_rect)
            text = font.render("New game", True, self.BLACK)
            self.screen.blit(text, ((self.BOARD_SIZE - button_width - 50) // 2, self.BOARD_SIZE + 60))

            text = font.render(f"Fail : {self.count_mistake} < 6", True, self.BLACK)
            self.screen.blit(text, (self.BOARD_SIZE // 2 - 60, self.BOARD_SIZE + 10))

            if self.game_over and self.display_lose and not self.solve_button_rect.collidepoint(pygame.mouse.get_pos()):
                font = pygame.font.Font(None, 100)
                text_lose = font.render("You Lose!", True, self.BLACK)
                text_rect = text_lose.get_rect()
                text_rect.center = (self.BOARD_SIZE // 2, self.BOARD_SIZE // 2)
                self.screen.blit(text_lose, text_rect)

            if self.game_reset:
                self.new_game()

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Sudoku(40)
    game.main()