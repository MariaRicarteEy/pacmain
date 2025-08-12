import pygame
import random

# Config
TILE = 24
MAP = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "     #.##### ## #####.#     ",
    "     #.##          ##.#     ",
    "     #.## ###--### ##.#     ",
    "######.## #      # ##.######",
    "      .   #      #   .      ",
    "######.## #      # ##.######",
    "     #.## ######## ##.#     ",
    "     #.##          ##.#     ",
    "     #.## ######## ##.#     ",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#...##................##...#",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################",
]

maxw = max(len(row) for row in MAP)
MAP = [row.ljust(maxw) for row in MAP]
WIDTH = len(MAP[0]) * TILE
HEIGHT = len(MAP) * TILE

# Cores usadas
BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
PINK = (255,100,180)
CYAN = (0,255,255)
ORANGE = (255,165,0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-EY com Menu Inicial")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 24)

# Funções utilitárias para o menu inicial
def draw_text(text, pos, color=(255,255,255)):
    img = FONT.render(text, True, color)
    screen.blit(img, pos)

def draw_button(rect, color, text, selected=False):
    pygame.draw.rect(screen, color, rect)
    if selected:
        pygame.draw.rect(screen, (255,255,255), rect, 3)
    txt_surf = FONT.render(text, True, (0,0,0))
    txt_rect = txt_surf.get_rect(center=rect.center)
    screen.blit(txt_surf, txt_rect)

# Tela inicial de configuração
def menu_inicial():
    color_options = {
        "Amarelo": (255, 255, 0),
        "Verde": (0, 255, 0),
        "Azul": (0, 0, 255),
        "Vermelho": (255, 0, 0),
    }
    selected_color_name = None
    selected_color = None
    input_active = False
    score_input = ""
    error_msg = ""

    buttons = []
    running = True
    while running:
        screen.fill((30,30,30))
        draw_text("Escolha a cor do Pac-Man:", (20, 20))

        # Mostrar botões cores
        x = 20
        y = 60
        buttons.clear()
        for name, color in color_options.items():
            rect = pygame.Rect(x, y, 90, 40)
            buttons.append((rect, name, color))
            draw_button(rect, color, name, selected=(name == selected_color_name))
            x += 100

        # Caixa input pontuação
        draw_text("Digite a pontuação para vencer:", (20, 120))
        input_rect = pygame.Rect(20, 150, 120, 40)
        pygame.draw.rect(screen, (255,255,255), input_rect, 2)
        input_text_surf = FONT.render(score_input, True, (255,255,255))
        screen.blit(input_text_surf, (input_rect.x+5, input_rect.y+5))

        # Botão iniciar
        start_rect = pygame.Rect(200, 150, 150, 40)
        can_start = selected_color is not None and score_input.isdigit() and int(score_input) > 0
        start_color = (0, 200, 0) if can_start else (100, 100, 100)
        draw_button(start_rect, start_color, "Iniciar")

        if error_msg:
            draw_text(error_msg, (20, 210), (255, 100, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # clicar cores
                for rect, name, color in buttons:
                    if rect.collidepoint(mx, my):
                        selected_color_name = name
                        selected_color = color
                        error_msg = ""
                # clicar input pontuação
                if input_rect.collidepoint(mx, my):
                    input_active = True
                else:
                    input_active = False
                # clicar iniciar
                if start_rect.collidepoint(mx, my) and can_start:
                    return selected_color, int(score_input)

            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    score_input = score_input[:-1]
                elif event.unicode.isdigit():
                    score_input += event.unicode
                else:
                    error_msg = "Apenas números são permitidos"

        pygame.display.flip()
        clock.tick(30)

def tela_final(mensagem):
    final_font = pygame.font.SysFont(None, 48)
    running = True
    while running:
        screen.fill((0, 0, 0))
        text_surf = final_font.render(mensagem, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text_surf, text_rect)

        sub_surf = FONT.render("Pressione ESC para sair", True, (255, 255, 255))
        sub_rect = sub_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        screen.blit(sub_surf, sub_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        pygame.display.flip()
        clock.tick(30)

# Funções do jogo

def tile_at(px, py):
    col = px // TILE
    row = py // TILE
    if 0 <= row < len(MAP) and 0 <= col < len(MAP[0]):
        return MAP[row][col]
    return '#'

def collides(px, py):
    r = TILE//2 - 2
    pts = [(px - r, py - r), (px + r, py - r), (px - r, py + r), (px + r, py + r)]
    for (sx, sy) in pts:
        if tile_at(int(sx), int(sy)) == '#':
            return True
    return False

class Player:
    def __init__(self, x, y, color):
        self.x = x*TILE + TILE//2
        self.y = y*TILE + TILE//2
        self.dir = (0,0)
        self.next_dir = (0,0)
        self.speed = 2
        self.score = 0
        self.color = color

    def update(self):
        nx = self.x + self.next_dir[0]*self.speed
        ny = self.y + self.next_dir[1]*self.speed
        if not collides(nx, ny):
            self.dir = self.next_dir
        mx = self.x + self.dir[0]*self.speed
        my = self.y + self.dir[1]*self.speed
        if not collides(mx, my):
            self.x = mx
            self.y = my
        else:
            self.dir = (0,0)

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), TILE//2 - 2)

class Ghost:
    def __init__(self, x, y, color=BLUE):
        self.x = x*TILE + TILE//2
        self.y = y*TILE + TILE//2
        self.speed = 1
        self.dir = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        self.color = color

    def update(self):
        mx = self.x + self.dir[0]*self.speed
        my = self.y + self.dir[1]*self.speed
        if collides(mx, my):
            options = [(1,0),(-1,0),(0,1),(0,-1)]
            opos = (-self.dir[0], -self.dir[1])
            choices = [d for d in options if d != opos]
            random.shuffle(choices)
            for d in choices:
                if not collides(self.x + d[0]*self.speed, self.y + d[1]*self.speed):
                    self.dir = d
                    break
        else:
            self.x = mx
            self.y = my

    def draw(self, surf):
        rect = pygame.Rect(0,0, TILE-4, TILE-4)
        rect.center = (int(self.x), int(self.y))
        pygame.draw.rect(surf, self.color, rect, border_radius=6)

def find_tile(ch):
    for r,row in enumerate(MAP):
        for c,ch2 in enumerate(row):
            if ch2 == ch:
                return c, r
    return None

# INÍCIO DO PROGRAMA

pacman_color, pontuacao_para_vencer = menu_inicial()

map_list = [list(row) for row in MAP]

player_pos = find_tile(' ')
if player_pos is None:
    player_pos = (1,1)
player = Player(player_pos[0], player_pos[1], pacman_color)

ghost_colors = [BLUE, PINK, CYAN, ORANGE]
spawn = find_tile('-')
if spawn is None:
    spawn = (len(map_list[0])//2, len(map_list)//2)

ghosts = []
for i, col_offset in enumerate([-1,1,-3,3]):
    g = Ghost(spawn[0] + col_offset, spawn[1], color=random.choice(ghost_colors))
    ghosts.append(g)

running = True
win = False
lose = False

while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_UP:
                player.next_dir = (0,-1)
            elif event.key == pygame.K_DOWN:
                player.next_dir = (0,1)
            elif event.key == pygame.K_LEFT:
                player.next_dir = (-1,0)
            elif event.key == pygame.K_RIGHT:
                player.next_dir = (1,0)

    if not win and not lose:
        player.update()
        for g in ghosts:
            g.update()

        pc = player.x // TILE
        pr = player.y // TILE
        if 0 <= pr < len(map_list) and 0 <= pc < len(map_list[0]):
            if map_list[pr][pc] == '.':
                player.score += 1
                map_list[pr][pc] = ' '

        for g in ghosts:
            dist2 = (g.x - player.x)**2 + (g.y - player.y)**2
            if dist2 < (TILE//2)**2:
                lose = True

        if player.score >= pontuacao_para_vencer:
            win = True

    screen.fill(BLACK)
    for r,row in enumerate(map_list):
        for c,ch in enumerate(row):
            x = c*TILE
            y = r*TILE
            if MAP[r][c] == '#':
                pygame.draw.rect(screen, RED, (x, y, TILE, TILE))
            if ch == '.':
                pygame.draw.circle(screen, WHITE, (x + TILE//2, y + TILE//2), 3)

    player.draw(screen)
    for g in ghosts:
        g.draw(screen)

    score_s = FONT.render(f"Pontos: {player.score}", True, WHITE)
    screen.blit(score_s, (8, 8))
    if win:
        tela_final("Você venceu! Todas as bolinhas coletadas.")
    elif lose:
        tela_final("Você perdeu! Colidiu com um fantasma.")

    pygame.display.flip()

pygame.quit()