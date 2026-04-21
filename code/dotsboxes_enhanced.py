import pygame
import sys
import random
import copy


class DotsAndBoxes:

    def __init__(self, n, screen):
        self.n = n
        self.horizontal_lines = [[False] * n for _ in range(n + 1)]
        self.vertical_lines = [[False] * (n + 1) for _ in range(n)]
        self.square_completed = [[0] * self.n for _ in range(self.n)]
        self.screen = screen
        self.width = self.screen.get_width() * 0.8
        self.height = self.screen.get_height() * 0.8
        self.gap = self.width // (n + 1)
        self.total_squares = 0
        self.turn = 0

    def draw_horizontal_line(self, row, col):
        if 0 <= row <= self.n and 0 <= col <= self.n - 1:
            if not self.horizontal_lines[row][col]:
                self.horizontal_lines[row][col] = True
                # Check adjacent squares to the horizontal line
                if 0 < row <= self.n:
                    if (self.horizontal_lines[row - 1][col], self.vertical_lines[row - 1][col],
                        self.vertical_lines[row - 1][col + 1]) == (True, True, True):
                        self.square_completed[row - 1][col] = self.turn + 1
                        self.total_squares += 1
                if 0 <= row < self.n:
                    if (self.horizontal_lines[row + 1][col], self.vertical_lines[row][col],
                        self.vertical_lines[row][col + 1]) == (True, True, True):
                        self.square_completed[row][col] = self.turn + 1
                        self.total_squares += 1
                self.turn = (self.turn + 1) % 2
                return True
        self.turn = (self.turn + 1) % 2
        return False

    def draw_vertical_line(self, row, col):
        if 0 <= row <= self.n - 1 and 0 <= col <= self.n:
            if not self.vertical_lines[row][col]:
                self.vertical_lines[row][col] = True
                # Check adjacent squares to the vertical line
                if 0 < col <= self.n:
                    if (self.vertical_lines[row][col - 1], self.horizontal_lines[row][col - 1],
                        self.horizontal_lines[row + 1][col - 1]) == (True, True, True):
                        self.square_completed[row][col - 1] = self.turn + 1
                        self.total_squares += 1
                if 0 <= col < self.n:
                    if (self.vertical_lines[row][col + 1], self.horizontal_lines[row][col],
                        self.horizontal_lines[row + 1][col]) == (True, True, True):
                        self.square_completed[row][col] = self.turn + 1
                        self.total_squares += 1
                self.turn = (self.turn + 1) % 2
                return True
        self.turn = (self.turn + 1) % 2
        return False

    def draw_board(self):
        # Clear the screen
        self.screen.fill((255, 255, 255))

        for row in range(self.n):  # Squares
            for col in range(self.n):
                if self.square_completed[row][col] == 1:
                    color = (255, 0, 0)  # Red
                    pygame.draw.rect(self.screen, color,
                                     (self.gap * (col + 1), self.gap * (row + 1), self.gap, self.gap))
                elif self.square_completed[row][col] == 2:
                    color = (0, 0, 255)  # Blue
                    pygame.draw.rect(self.screen, color,
                                     (self.gap * (col + 1), self.gap * (row + 1), self.gap, self.gap))

        for row in range(self.n + 1):
            for col in range(self.n):
                if self.horizontal_lines[row][col]:
                    pygame.draw.line(self.screen, (0, 0, 0), (self.gap * (col + 1), self.gap * (row + 1)),
                                     (self.gap * (col + 2), self.gap * (row + 1)), 2)
        for row in range(self.n):
            for col in range(self.n + 1):
                if self.vertical_lines[row][col]:
                    pygame.draw.line(self.screen, (0, 0, 0), (self.gap * (col + 1), self.gap * (row + 1)),
                                     (self.gap * (col + 1), self.gap * (row + 2)), 2)

        for row in range(self.n + 1):  # Circles
            for col in range(self.n + 1):
                pygame.draw.circle(self.screen, (0, 0, 0), (self.gap * (col + 1), self.gap * (row + 1)), 5)

        red_squares = sum(row.count(1) for row in self.square_completed)
        blue_squares = sum(row.count(2) for row in self.square_completed)
        font = pygame.font.SysFont(None, 24)

        text_surface = font.render(
            f"Total: {self.total_squares},  Red: {red_squares},  Blue: {blue_squares}, Turn: {self.turn}",
            True,
            (0, 0, 0, 0))
        self.screen.blit(text_surface, (10, 10))

    def process_click(self, pos):
        x, y = pos
        row = round(y / self.gap) - 1
        col = round(x / self.gap) - 1
        if min(abs(y % self.gap), self.gap - abs(y % self.gap)) < 5:
            self.draw_horizontal_line(row, col)
            return True
        elif min(abs(x % self.gap), self.gap - abs(x % self.gap)) < 5:
            self.draw_vertical_line(row, col)
            return True
        return False
    
    def process_move(self, orient, row, col):
        print(self.turn)
        if orient == 0:
            self.draw_horizontal_line(row, col)
        elif orient == 1:
            self.draw_vertical_line(row, col)

    def eval1(self, turn):  # Difference in completed squares
        red_squares = sum(row.count(1) for row in self.square_completed)
        blue_squares = sum(row.count(2) for row in self.square_completed)
        if turn == 0:
            return (red_squares - blue_squares)*(-1)**(turn)
        else:
            return red_squares*(1)**(turn)
    
    def pos_moves(self):  # Return list of possible moves
        moves = []
        for i in range(self.n + 1):
            for j in range(self.n):
                if not self.horizontal_lines[i][j]:
                    moves.append((0, i, j))
        for i in range(self.n):
            for j in range(self.n + 1):
                if not self.vertical_lines[i][j]:
                    moves.append((1, i, j))
        return moves

    def Minimax(self, n, alfa, beta, turn):
        moves = self.pos_moves()
        if n == 0 or moves == []:
            return self.eval1(turn), None
        else:
            best_move = None
            if turn == 0:  # My turn
                for move in moves:
                    new = DotsAndBoxes(self.n, self.screen)
                    new.horizontal_lines = copy.deepcopy(self.horizontal_lines)
                    new.vertical_lines = copy.deepcopy(self.vertical_lines)
                    new.square_completed = copy.deepcopy(self.square_completed)
                    new.total_squares = self.total_squares
                    if move[0] == 0:  # Horizontal line
                        new.draw_horizontal_line(move[1], move[2])
                    elif move[0] == 1:  # Vertical line
                        new.draw_vertical_line(move[1], move[2])
                    val, _ = new.Minimax(n - 1, alfa, beta, 1)
                    if val > alfa:
                        alfa = val
                        best_move = move
                    if beta <= alfa:
                        break
                return alfa, best_move
            
            else:  # Opponent's turn
                for move in moves:
                    new = DotsAndBoxes(self.n, self.screen)
                    new.horizontal_lines = copy.deepcopy(self.horizontal_lines)
                    new.vertical_lines = copy.deepcopy(self.vertical_lines)
                    new.square_completed = copy.deepcopy(self.square_completed)
                    new.total_squares = self.total_squares
                    if move[0] == 0:  # Horizontal line
                        new.draw_horizontal_line(move[1], move[2])
                    elif move[0] == 1:  # Vertical line
                        new.draw_vertical_line(move[1], move[2])
                    val, _ = new.Minimax(n - 1, alfa, beta, 0)
                    if val < beta:
                        beta = val
                        best_move = move
                    if beta <= alfa:
                        break
                return beta, best_move


# Main function
def main():
    pygame.init()
    size = (600, 600)  # Window size
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Dots and Boxes")  # Window title
    n = 4  # Board size (squares)
    game = DotsAndBoxes(n, screen)

    running = True
    while running:
        for event in pygame.event.get():  # Event handling loop
            if event.type == pygame.QUIT:
                running = False  # Exit the main loop if the user quits the game

        game.draw_board()  # Draw the board
        pygame.display.flip()  # Update the display

        while running:
            minimax_val, best_move = game.Minimax(4, -99999, 99999, game.turn)  # Calculate AI's move
            print("Minimax value:", minimax_val)
            print("Best move :", best_move)
            if best_move:  # If there's a valid move
                game.process_move(best_move[0], best_move[1], best_move[2])  # Process AI's move
                pygame.time.wait(500)  # Wait for 2 seconds before the next move
                game.draw_board()  # Draw the updated board
                pygame.display.flip()  # Update the display
                if game.total_squares == n * n:
                    pygame.time.wait(2000)
                    running = False
            

    pygame.quit()  # Quit Pygame
    
    """
    running = True
    while running:
        valid_click = False
        game.draw_board()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                valid_click = game.process_click(pygame.mouse.get_pos())  # Process mouse click for player 1
                if valid_click:
                    game.turn = (game.turn + 1) % 2  # Alternating player turns if the click was valid

        if valid_click:  # If a valid click was made, then draw the board and update the screen
            minimax_val, best_move = game.Minimax(4, -99999, 99999, 0)  # Depth 2
            print(f"Minimax value: {minimax_val}, Best Move: {best_move}")
            game.draw_board()
    """


if __name__ == "__main__":
    main()
