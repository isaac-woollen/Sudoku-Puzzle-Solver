# GUI.py
import pygame
from solver import solve, valid
import time
from Board import generateValidBoard
pygame.font.init()
theme = 0

themes =    {
                0:{"text": (0,0,0), "line": (0,0,0), "background": (255,255,255), "button": (0,0,0), "name":"Light"},
                1:{"text": (255,255,255), "line": (255,255,255), "background": (0,0,0), "button": (255,255,255), "name":"Dark"},
                2:{"text": (76,201,240), "line": (181,23,158), "background": (72,12,163), "button": (76,201,240), "name":"Retro"},
                3:{"text": (246, 216, 96), "line": (234, 92, 43), "background": (255,127,63), "button": (246, 216, 96), "name":"Fall"},
                4:{"text": (82,94,117), "line": (120,147,138), "background": (241,221,191), "button": (82,94,117), "name":"Calm"}
            }

modes =     {
                0:"Easy",
                1:"Medium",
                2:"Hard"
            }

class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.mode = 1
        self.board = generateValidBoard(self.mode)
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def change_mode(self):
        self.mode = (self.mode + 1) % 3
        self.board = generateValidBoard(self.mode)
        self.cubes = [[Cube(self.board[i][j], i, j, 540, 540) for j in range(9)] for i in range(9)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row,col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        pygame.draw.line(win, themes[theme]["line"], (10, 0), (10 + self.width, 0), 4)
        pygame.draw.line(win, themes[theme]["line"], (10, 0), (10, self.height), 4)
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, themes[theme]["line"], (10, i*gap), (10 + self.width, i*gap), thick)
            pygame.draw.line(win, themes[theme]["line"], (10+ i * gap, 0), (10 + i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("arial", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+27, y))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, themes[theme]["text"])
            win.blit(text, (10 + x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, themes[theme]["line"], (10 + x, y, gap ,gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(win, board, time, strikes):
    win.fill(themes[theme]["background"])
    # Draw time
    fnt = pygame.font.SysFont("arial", 40)
    text = fnt.render("Time: " + format_time(time), 1, themes[theme]["text"])
    win.blit(text, (500 - 160, 570))
    pygame.draw.rect(win, themes[theme]["button"], (40, 570, 120, 45))
    pygame.draw.rect(win, themes[theme]["button"], (180, 570, 120, 45))
    fnt = pygame.font.SysFont("arial", 30)
    text = fnt.render(themes[theme]["name"] , 1, themes[theme]["background"])
    win.blit(text, (53, 575))
    if board.mode == 1:
        fnt = pygame.font.SysFont("arial", 29)
        text = fnt.render(modes[board.mode] , 1, themes[theme]["background"])
        win.blit(text, (188, 575))
    else:
        text = fnt.render(modes[board.mode] , 1, themes[theme]["background"])
        win.blit(text, (205, 575))
    # Draw Strikes
    # text = fnt.render("X " * strikes, 1, (255, 0, 0))
    #win.blit(text, (20, 560))
    # Draw grid and board
    board.draw(win)


def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60
    if sec < 10:
        sec = "0" + str(sec)

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def main():
    win = pygame.display.set_mode((562,650))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540)
    key = None
    run = True
    start = time.time()
    strikes = 0
    global theme
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")
                            run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
                if 570 <= pos[1] <= 570 + 45:
                    if 40 <= pos[0] <= 40 + 120:
                        theme = (theme + 1) % 5
                    if 180 <= pos[0] <= 180 + 120:
                        board.change_mode()


        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()

main()
pygame.quit()
