import pygame
import sys
import random
import copy
import tkinter as tk


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

    def copy(self):
        gamecopy = DotsAndBoxes(self.n, self.screen)
        gamecopy.horizontal_lines = copy.deepcopy(self.horizontal_lines)
        gamecopy.vertical_lines = copy.deepcopy(self.vertical_lines)
        gamecopy.square_completed = copy.deepcopy(self.square_completed)
        gamecopy.total_squares = self.total_squares
        gamecopy.turn = self.turn
        return gamecopy

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
        self.screen.fill((229, 229, 229))

        for row in range(self.n):  # Squares
            for col in range(self.n):
                if self.square_completed[row][col] == 1:
                    color = (236, 112, 99)  # Red
                    pygame.draw.rect(self.screen, color,
                                     (self.gap * (col + 1), self.gap * (row + 1), self.gap, self.gap))
                elif self.square_completed[row][col] == 2:
                    color = (88, 214, 141)  # Green
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
        players = dict()
        players[0] = "Red"
        players[1] = "Green"

        text_surface = font.render(
            f"Red: {red_squares},  Green: {blue_squares}, Turn: {players[self.turn]}",
            True,
            (0, 0, 0))
        self.screen.blit(text_surface, (10, 10))

    def process_click(self, pos):  # Falla si le damos a la derecha / abajo de la línea
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

    def process_move(self, tuple):
        if tuple[0] == 0:
            self.draw_horizontal_line(tuple[1], tuple[2])
        elif tuple[0] == 1:
            self.draw_vertical_line(tuple[1], tuple[2])

    def eval_green(self, lista): # Función de eval que se usa para el verde
        red_squares = sum(row.count(1) for row in lista)
        blue_squares = sum(row.count(2) for row in lista)
        return (red_squares - blue_squares) * (-1)

    def eval_red(self, lista): # Función de eval que se usa para el rojo
        red_squares = sum(row.count(1) for row in lista)
        blue_squares = sum(row.count(2) for row in lista)
        return red_squares - blue_squares

    def eval2(self, turn):  # Difference in completed squares, but own squares are 2x value
        red_squares = sum(row.count(1) for row in self.square_completed)
        blue_squares = sum(row.count(2) for row in self.square_completed)
        if turn == 0:
            red_squares = red_squares * 2
        else:
            blue_squares = blue_squares * 2
        return (red_squares - blue_squares) * ((-1) ** (turn))

    def eval1(self, turn):  # Cuadrados del contrario
        squares = sum(row.count(turn + 1) for row in self.square_completed)
        return squares

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

    def Minimax(self, n, alfa, beta, turn, func_eval, back=None):
        if back is None:
            back = []
        moves = self.pos_moves()
        random.shuffle(moves)

        # print("Depth:", n, "Turn:", turn)
        if n == 0 or not moves:
            return func_eval(self.square_completed), back[0] if back else None

        best_move = None

        if turn == 0:  # Player's turn
            for move in moves:
                new = self.copy()
                new.process_move(move)

                lista = copy.deepcopy(back)
                lista.append(move)
                # print("Move:", move, "List:", lista)

                val, inicial = new.Minimax(n - 1, alfa, beta, new.turn, func_eval, lista)
                # print(val)
                if val > alfa:
                    alfa = val
                    best_move = inicial

                if beta <= alfa:
                    break

            # print("Best Move (Max):", best_move, "alfa:", alfa)
            return alfa, best_move

        else:  # Opponent's turn
            for move in moves:
                new = self.copy()
                new.process_move(move)

                lista = copy.deepcopy(back)
                lista.append(move)

                # print("Move:", move, "List:", lista)

                val, inicial = new.Minimax(n - 1, alfa, beta, new.turn, func_eval, lista)
                # print(val)

                if val < beta:
                    beta = val
                    best_move = inicial

                if beta <= alfa:
                    break

            # print("Best Move (Min):", best_move, "beta:", beta)
            return beta, best_move


class GameSetupWindow_PvsIA:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Configuración del juego")

        # Etiqueta y botones para el tamaño del tablero
        self.board_size_label = tk.Label(self.window, text="Tamaño del tablero:")
        self.board_size_label.grid(row=0, column=0, padx=5, pady=5)

        self.board_size_buttons_frame = tk.Frame(self.window)
        self.board_size_buttons_frame.grid(row=0, column=1)
        self.board_size_buttons = []
        for size in [2, 3, 4]:
            button = tk.Button(self.board_size_buttons_frame, text=str(size),
                               command=lambda s=size: self.set_board_size(s))
            button.pack(side=tk.LEFT, padx=5, pady=5)
            self.board_size_buttons.append(button)

        # Etiqueta y botones para la profundidad del tablero
        self.depth_label = tk.Label(self.window, text="Profundidad de la IA:")
        self.depth_label.grid(row=1, column=0, padx=5, pady=5)

        self.depth_buttons_frame = tk.Frame(self.window)
        self.depth_buttons_frame.grid(row=1, column=1)
        self.depth_buttons = []
        for size in [1, 2, 3, 4, 5]:
            button = tk.Button(self.depth_buttons_frame, text=str(size),
                               command=lambda s=size: self.set_depth(s))
            button.pack(side=tk.LEFT, padx=5, pady=5)
            self.depth_buttons.append(button)

        # Botón para comenzar el juego
        self.start_button = tk.Button(self.window, text="Comenzar juego", command=self.start_game)
        self.start_button.grid(row=2, columnspan=2, padx=5, pady=5)

        self.board_size = None
        self.depth = None

        self.center_window()

    def set_board_size(self, size):
        self.board_size = size

    def set_depth(self, size):
        self.depth = size

    def start_game(self):
        self.window.destroy()  # Cerrar la ventana de configuración

    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


class GameSetupWindow_IAvsIA:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Configuración del juego")

        # Etiqueta y botones para el tamaño del tablero
        self.board_size_label = tk.Label(self.window, text="Tamaño del tablero:")
        self.board_size_label.grid(row=0, column=0, padx=5, pady=5)

        self.board_size_buttons_frame = tk.Frame(self.window)
        self.board_size_buttons_frame.grid(row=0, column=1)
        self.board_size_buttons = []
        for size in [2, 3, 4]:
            button = tk.Button(self.board_size_buttons_frame, text=str(size),
                               command=lambda s=size: self.set_board_size(s))
            button.pack(side=tk.LEFT, padx=5, pady=5)
            self.board_size_buttons.append(button)

        # Etiqueta y botones para la profundidad del tablero
        self.depth_label = tk.Label(self.window, text="Profundidad IA Roja:")
        self.depth_label.grid(row=1, column=0, padx=5, pady=5)

        self.depth_buttons_frame = tk.Frame(self.window)
        self.depth_buttons_frame.grid(row=1, column=1)
        self.depth_buttons = []
        for size in [1, 2, 3, 4, 5]:
            button = tk.Button(self.depth_buttons_frame, text=str(size),
                               command=lambda s=size: self.set_depth(s))
            button.pack(side=tk.LEFT, padx=5, pady=5)
            self.depth_buttons.append(button)

        # Etiqueta y botones para la profundidad 2
        self.depth2_label = tk.Label(self.window, text="Profundidad IA Verde:")
        self.depth2_label.grid(row=2, column=0, padx=5, pady=5)

        self.depth2_buttons_frame = tk.Frame(self.window)
        self.depth2_buttons_frame.grid(row=2, column=1)
        self.depth2_buttons = []
        for size in [1, 2, 3, 4, 5]:
            button = tk.Button(self.depth2_buttons_frame, text=str(size),
                               command=lambda s=size: self.set_depth2(s))
            button.pack(side=tk.LEFT, padx=5, pady=5)
            self.depth2_buttons.append(button)

        # Botón para comenzar el juego
        self.start_button = tk.Button(self.window, text="Comenzar juego", command=self.start_game)
        self.start_button.grid(row=3, columnspan=2, padx=5, pady=5)

        self.board_size = None
        self.depth = None
        self.depth2 = None

        self.center_window()

    def set_board_size(self, size):
        self.board_size = size

    def set_depth(self, depth):
        self.depth = depth

    def set_depth2(self, depth):
        self.depth2 = depth

    def start_game(self):
        self.window.destroy()

    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


# Función para crear la ventana de selección de modo de juego

def ventana_modo_juego():
    ventana = tk.Tk()
    ventana.title("Seleccionar Modo de Juego")

    # Obtener las dimensiones de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    altura_pantalla = ventana.winfo_screenheight()

    # Dimensiones de la ventana
    ancho_ventana = 300
    altura_ventana = 200

    # Calcular la posición para centrar la ventana
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (altura_pantalla // 2) - (altura_ventana // 2)

    # Establecer las dimensiones y posición de la ventana
    ventana.geometry(f"{ancho_ventana}x{altura_ventana}+{x}+{y}")

    modo_seleccionado = tk.IntVar()  # Variable para almacenar el modo seleccionado

    # Función para manejar la selección de modo de juego
    def on_click(modo):
        modo_seleccionado.set(modo)
        ventana.destroy()

    # Crear cajas clicables para los modos de juego
    modos = [("IA vs IA", 0), ("Jugador vs IA", 1), ("Jugador 1 vs Jugador 2", 2)]
    for modo, valor in modos:
        boton = tk.Button(ventana, text=modo, command=lambda valor=valor: on_click(valor))
        boton.pack(pady=5)

    ventana.mainloop()

    return modo_seleccionado.get() # # Elegir modo de juego



##################### DIFERENTES MODOS DE JUEGO #####################


def main():  # Main function for AI vs AI
    setup_window = GameSetupWindow_IAvsIA()
    setup_window.window.mainloop()
    pygame.init()

    size = (1000, 1000)  # Window size
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Dots and Boxes")  # Window title

    n = setup_window.board_size  # Board size (squares)
    profundidad1 = setup_window.depth # profundidad del player 1 RED
    profundidad2 = setup_window.depth2 # profundidad del player 2 GREEN

    game = DotsAndBoxes(n, screen)

    running = True
    while running:
        for event in pygame.event.get():  # Event handling loop
            if event.type == pygame.QUIT:
                running = False  # Exit the main loop if the user quits the game
                pygame.quit()
                sys.exit()
        game.draw_board()  # Draw the board
        pygame.display.flip()  # Update the display

        while running:

            # Player 1 (red)
            new = game.copy()  # Copiamos el juego para que no fastidie nuestras variables de la clase
            new.turn = 0
            minimax_val, best_move = game.Minimax(profundidad1, -99999, 99999, new.turn,
                                                  new.eval_red)  # Calculate AI's move
            game.process_move(best_move)  # Process AI's move
            game.draw_board()  # Draw the updated board
            pygame.display.flip()  # Update the display

            if game.total_squares == n * n:  # if game is finished then close the window
                pygame.time.wait(2000)
                running = False

            # Player 2 (green)
            pygame.time.wait(1)  # Wait a bit before the next move

            new = game.copy()  # Copiamos el juego para que no fastidie nuestras variables de la clase
            new.turn = 0
            minimax_val, best_move = game.Minimax(profundidad2, -99999, 99999, new.turn,
                                                  new.eval_green)  # Calculate AI's move
            game.process_move(best_move)  # Process AI's move
            game.draw_board()  # Draw the updated board
            pygame.display.flip()  # Update the display

            pygame.time.wait(1)

            if game.total_squares == n * n:  # if game is finished then close the window
                m = game.square_completed
                contr=0
                contg=0
                for fila in m:
                    for cas in fila:
                        if cas == 1:
                            contr += 1
                        elif cas == 2:
                            contg += 1
                if contg < contr:
                    winner = 1
                elif contg > contr:
                    winner = 2
                elif contg == contr:
                    winner = 0
                pygame.time.wait(2000)
                return winner
                running = False

    #pygame.quit()  # Quit Pygame


def main2():  # Player vs Player
    pygame.init()
    size = (1000, 1000)  # Window size
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Dots and Boxes")  # Window title
    n = 2  # Board size (squares)
    game = DotsAndBoxes(n, screen)
    running = True

    while running:
        valid_click = False
        game.draw_board()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                valid_click = game.process_click(pygame.mouse.get_pos())  # Process mouse click for player 1

        if valid_click:  # If a valid click was made, then draw the board and update the screen
            game.draw_board()
            pygame.display.flip()
            if game.total_squares == n * n:
                m = game.square_completed
                contr=0
                contg=0
                for fila in m:
                    for cas in fila:
                        if cas == 1:
                            contr += 1
                        elif cas == 2:
                            contg += 1
                if contg < contr:
                    winner = 1
                elif contg > contr:
                    winner = 2
                elif contg == contr:
                    winner = 0
                pygame.time.wait(2000)
                return winner
                running = False


def main3():  # Player vs AI
    setup_window = GameSetupWindow_PvsIA()
    setup_window.window.mainloop()
    pygame.init()

    size = (1000, 1000)  # Window size
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Dots and Boxes")  # Window title

    n = setup_window.board_size  # Board size (squares)
    profundidad = setup_window.depth

    # Si no le doy click bien a la ventanita pues pongo 2 por la cara

    if n is None:
        n = 2
    if profundidad is None:
        profundidad = 2
        
    game = DotsAndBoxes(n, screen)
    running = True

    while running:
        valid_click = False
        game.draw_board()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Click izquierdo
                valid_click = game.process_click(pygame.mouse.get_pos())  # Procesa el click

        if valid_click:  # Aquí hay un bug, porque si hago click se cambia de turno y no pone línea
            game.draw_board()
            pygame.display.flip()
            new = game.copy()  # Copiamos el juego para que no fastidie nuestras variables de la clase
            new.turn = 0  # Establezco el turno 0 porque queremos que juegue al MAX
            minimax_val, best_move = new.Minimax(profundidad, -99999, 99999, new.turn,
                                                 game.eval_red)  # Calculamos el movimiento
            if game.total_squares != n * n:  # Comprueba a ver si se ha terminado
                game.process_move(best_move)
                game.draw_board()
                pygame.display.flip()
            else:
                m = game.square_completed
                contr=0
                contg=0
                for fila in m:
                    for cas in fila:
                        if cas == 1:
                            contr += 1
                        elif cas == 2:
                            contg += 1
                if contg < contr:
                    winner = 1
                elif contg > contr:
                    winner = 2
                elif contg == contr:
                    winner = 0
                pygame.time.wait(1)
                return winner
                running = False



def mostrar_ganador(color):
    pantalla = pygame.display.set_mode((800, 400))
    pygame.display.set_caption("Ganador")

    if color == 1:
        color_texto = (236,112,99)  # Rojo
        mensaje = "Ganador es Rojo"
    elif color == 2:
        color_texto = (88,214,141)  # Verde
        mensaje = "Ganador es Verde"
    elif color == 0:
        color_texto = (0,0,0)
        mensaje = "Empate"
    else:
        pygame.quit()
        raise ValueError("Error en ganador")

    fuente = pygame.font.SysFont(None, 80)
    texto = fuente.render(mensaje, True, color_texto)

    pantalla.fill((229,229,229))
    pantalla.blit(texto, (170,160))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Ejemplo de uso:
# mostrar_ganador(0)  # Muestra "Ganador es Rojo" en rojo
# mostrar_ganador(1)  # Muestra "Ganador es Verde" en verde


#####################################################################

if __name__ == "__main__":
    gamemode = ventana_modo_juego()
    # gamemode = int(input("0 si AI vs AI, 1 si Player vs AI, 2 si Player vs Player: "))
    if gamemode == 0:
        winner = main()
        mostrar_ganador(winner)
    elif gamemode == 1:
        winner = main3()
        mostrar_ganador(winner)
    elif gamemode == 2:
        winner = main2()
        mostrar_ganador(winner)

