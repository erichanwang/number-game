import pygame
import random
import sys
import time

# ------------------ CONFIG ------------------
GRID   = 3
TILE_W = 100
GAP    = 4
MARGIN = 40
FONT_SIZE = 48
TIMER_FONT = 32
FPS      = 60

BG, EMPTY, TILE, TEXT = (30, 30, 30), (60, 60, 60), (50, 150, 255), (255, 255, 255)

# ------------------ GAME --------------------
class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        win_size   = MARGIN*2 + GRID*TILE_W + (GRID-1)*GAP
        self.screen = pygame.display.set_mode((win_size, win_size))
        pygame.display.set_caption("Slide 1-9  (timer)")
        self.font      = pygame.font.SysFont("Consolas", FONT_SIZE, bold=True)
        self.timerfont = pygame.font.SysFont("Consolas", TIMER_FONT, bold=True)
        self.reset()

    # ---------- state helpers ----------
    def solved(self):
        flat = [num for row in self.board for num in row]
        return flat == list(range(1, GRID*GRID)) + [0]

    def blank_pos(self):
        for r in range(GRID):
            for c in range(GRID):
                if self.board[r][c] == 0:
                    return r, c

    def move_tile(self, dr, dc):
        br, bc = self.blank_pos()
        nr, nc = br + dr, bc + dc
        if 0 <= nr < GRID and 0 <= nc < GRID:
            self.board[br][bc], self.board[nr][nc] = self.board[nr][nc], 0
            return True
        return False

    def scramble(self, moves=200):
        dirs = [(0,1), (0,-1), (1,0), (-1,0)]
        for _ in range(moves):
            self.move_tile(*random.choice(dirs))

    def reset(self):
        self.board = [list(range(1+i*GRID, 1+(i+1)*GRID)) for i in range(GRID)]
        self.board[-1][-1] = 0
        self.scramble()
        self.start_time = time.time()         # reset timer
        self.finished   = False

    # ---------- drawing ----------
    def draw(self):
        self.screen.fill(BG)

        # draw tiles
        for r in range(GRID):
            for c in range(GRID):
                val = self.board[r][c]
                x = MARGIN + c*(TILE_W+GAP)
                y = MARGIN + r*(TILE_W+GAP)
                rect = pygame.Rect(x, y, TILE_W, TILE_W)
                if val == 0:
                    pygame.draw.rect(self.screen, EMPTY, rect, border_radius=8)
                else:
                    pygame.draw.rect(self.screen, TILE, rect, border_radius=8)
                    txt = self.font.render(str(val), True, TEXT)
                    self.screen.blit(txt, txt.get_rect(center=rect.center))

        # draw timer
        elapsed = (self.finished_time if self.finished else time.time()) - self.start_time
        timer_surf = self.timerfont.render(f"{elapsed:.2f} s", True, TEXT)
        self.screen.blit(timer_surf, (MARGIN, 10))

        pygame.display.flip()

    # ---------- main loop ----------
    def run(self):
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_q, pygame.K_ESCAPE):
                        pygame.quit(); sys.exit()
                    elif event.key == pygame.K_r:
                        self.reset()
                    elif not self.finished:
                        if event.key == pygame.K_LEFT:
                            self.move_tile(0, 1)
                        elif event.key == pygame.K_RIGHT:
                            self.move_tile(0, -1)
                        elif event.key == pygame.K_UP:
                            self.move_tile(1, 0)
                        elif event.key == pygame.K_DOWN:
                            self.move_tile(-1, 0)

            # detect win
            if not self.finished and self.solved():
                self.finished = True
                self.finished_time = time.time()

            self.draw()

# ------------------ MAIN --------------------
if __name__ == "__main__":
    Game().run()