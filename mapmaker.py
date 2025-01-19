import pygame


class Board:
    # создание поля
    def __init__(self, width, height, file):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.f = open(file, mode="w", encoding="utf-8")

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, s):
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 1:  #wall
                    pygame.draw.rect(s,
                                     pygame.Color("yellow"),
                                     (j * self.cell_size + self.left, i * self.cell_size + self.top,
                                      self.cell_size, self.cell_size), 0)
                elif self.board[i][j] == -1:  # player
                    pygame.draw.rect(s,
                                     pygame.Color("red"),
                                     (j * self.cell_size + self.left, i * self.cell_size + self.top,
                                      self.cell_size, self.cell_size), 0)
                pygame.draw.rect(s,
                                 pygame.Color("white"),
                                 (j * self.cell_size + self.left, i * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        x -= self.left
        y -= self.top
        if x < 0 or y < 0:
            return -1, 0
        result_x, result_y = x // self.cell_size, y // self.cell_size
        if result_x >= self.width or result_y >= self.height:
            return -1, 0
        return result_x, result_y

    def on_click(self, cell_coords):
        x, y = cell_coords
        if x == -1:
            return
        if self.board[y][x] != 0:
            self.board[y][x] = 0
            return
        self.board[y][x] = 1

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def save(self):
        for y in range(self.height):
            for x in range(self.width):
                pass

if __name__ == '__main__':
    pygame.init()
    size = width, height = 620, 620
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("mapmaker")
    board = Board(30, 30, input())
    board.set_view(10, 10, 20)
    running = True
    max_render_cd = 0.5
    clock = pygame.time.Clock()
    deltatime = clock.tick(60) / 1000

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.get_click(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    board.save()
            if event.type == pygame.MOUSEWHEEL:
                pass
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()

    pygame.quit()
