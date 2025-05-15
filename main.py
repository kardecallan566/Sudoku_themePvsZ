import pygame
import sys
import time
import random
import numpy as np
import math
from pygame import mixer


pygame.init()
mixer.init()


SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
GRID_SIZE = 9
CELL_SIZE = 60
GRID_PADDING = 20
BOARD_SIZE = CELL_SIZE * GRID_SIZE
BOARD_X = (SCREEN_WIDTH - BOARD_SIZE) // 2
BOARD_Y = 100
TOOLBAR_HEIGHT = 80
TOOLBAR_Y = BOARD_Y + BOARD_SIZE + 20
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 50
SOLVE_BUTTON_X = SCREEN_WIDTH - 150
SOLVE_BUTTON_Y = BOARD_Y + BOARD_SIZE + 35
HINT_BUTTON_X = SOLVE_BUTTON_X - BUTTON_WIDTH - 20
HINT_BUTTON_Y = SOLVE_BUTTON_Y
FREE_MODE_X = HINT_BUTTON_X - BUTTON_WIDTH - 20
FREE_MODE_Y = SOLVE_BUTTON_Y


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREEN = (200, 255, 200)
DARK_GREEN = (100, 180, 100)
HIGHLIGHT_COLOR = (255, 255, 200)
ERROR_COLOR = (255, 150, 150)
GRASS_GREEN = (120, 200, 80)
DIRT_BROWN = (139, 69, 19)
TOOLBAR_BG = (242, 240, 230)
BUTTON_COLOR = (80, 200, 120)
BUTTON_HOVER_COLOR = (100, 220, 140)
TEXT_COLOR = (60, 60, 60)
VICTORY_BG = (0, 0, 0, 180)  


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Plants vs. Zombies Sudoku")


title_font = pygame.font.Font(None, 60)
button_font = pygame.font.Font(None, 30)
cell_font = pygame.font.Font(None, 40)
victory_font = pygame.font.Font(None, 80)
timer_font = pygame.font.Font(None, 36)


plant_names = [
    "Sunflower", "Peashooter", "Wall-nut", "Cherry Bomb", 
    "Snow Pea", "Chomper", "Repeater", "Puff-shroom", "Potato Mine"
]


def create_plant_animations():
    animations = []
    for i in range(1, 10):
        
        frames = []
        base_color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
        
        
        for j in range(12):
            
            plant_surf = pygame.Surface((CELL_SIZE - 10, CELL_SIZE - 10), pygame.SRCALPHA)
            
            
            phase = j / 12 * 2 * math.pi
            scale_factor = 1.0 + 0.05 * math.sin(phase)
            
            
            size = int((CELL_SIZE // 2 - 10) * scale_factor)
            
           
            color_variation = (
                max(0, min(255, base_color[0] + int(15 * math.sin(phase)))),
                max(0, min(255, base_color[1] + int(15 * math.cos(phase)))),
                max(0, min(255, base_color[2] + int(15 * math.sin(phase + 1))))
            )
            
            
            pygame.draw.circle(plant_surf, color_variation, 
                              (CELL_SIZE // 2 - 5, CELL_SIZE // 2 - 5), size)
            
            
            eye_open = j % 12 != 0  
            eye_pos_y = CELL_SIZE // 2 - 5 + int(2 * math.sin(phase))  
            
            if eye_open:
                
                pygame.draw.circle(plant_surf, WHITE, 
                                  (CELL_SIZE // 3 - 5, eye_pos_y), 5)
                pygame.draw.circle(plant_surf, WHITE, 
                                  (2 * CELL_SIZE // 3 - 5, eye_pos_y), 5)
                pygame.draw.circle(plant_surf, BLACK, 
                                  (CELL_SIZE // 3 - 5, eye_pos_y), 2)
                pygame.draw.circle(plant_surf, BLACK, 
                                  (2 * CELL_SIZE // 3 - 5, eye_pos_y), 2)
            else:
                
                pygame.draw.line(plant_surf, BLACK, 
                                (CELL_SIZE // 3 - 10, eye_pos_y), 
                                (CELL_SIZE // 3, eye_pos_y), 2)
                pygame.draw.line(plant_surf, BLACK, 
                                (2 * CELL_SIZE // 3 - 10, eye_pos_y), 
                                (2 * CELL_SIZE // 3, eye_pos_y), 2)
            
            
            smile_y = CELL_SIZE // 2 + 5 + int(2 * math.sin(phase))
            pygame.draw.arc(plant_surf, BLACK, 
                           (CELL_SIZE // 4 - 5, smile_y - 5, 
                            CELL_SIZE // 2, 10), 
                           0, math.pi, 2)
            
            frames.append(plant_surf)
        
        animations.append(frames)
    
    return animations


plant_animations = create_plant_animations()


try:
    place_sound = mixer.Sound(pygame.mixer.Sound(buffer=bytes([random.randint(0, 255) for _ in range(1000)])))
    error_sound = mixer.Sound(pygame.mixer.Sound(buffer=bytes([random.randint(0, 255) for _ in range(1000)])))
    complete_sound = mixer.Sound(pygame.mixer.Sound(buffer=bytes([random.randint(0, 255) for _ in range(1000)])))
    hint_sound = mixer.Sound(pygame.mixer.Sound(buffer=bytes([random.randint(0, 255) for _ in range(1000)])))
    
    # Set volume
    place_sound.set_volume(0.3)
    error_sound.set_volume(0.2)
    complete_sound.set_volume(0.5)
    hint_sound.set_volume(0.4)
    
except:
    print("Sound initialization failed. Continuing without sound.")


def generate_sudoku(difficulty=0.5):
    """Generate a Sudoku puzzle with the given difficulty (0.0-1.0)"""
    
    board = np.zeros((9, 9), dtype=int)
    
    
    for i in range(0, 9, 3):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for r in range(3):
            for c in range(3):
                board[i + r][i + c] = nums.pop()
    
    
    solve_sudoku(board)
    
    
    solution = board.copy()
    
    
    cells_to_remove = int(difficulty * 60)
    
    
    while cells_to_remove > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board[row][col] != 0:
            temp = board[row][col]
            board[row][col] = 0
            
            
            test_board = board.copy()
            if count_solutions(test_board) == 1:
                cells_to_remove -= 1
            else:
                board[row][col] = temp
    
    return board, solution

def is_valid(board, row, col, num):
    """Check if placing num at board[row][col] is valid"""
    
    for x in range(9):
        if board[row][x] == num and x != col:
            return False
    
    
    for x in range(9):
        if board[x][col] == num and x != row:
            return False
    
    
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num and (start_row + i != row or start_col + j != col):
                return False
    
    return True

def solve_sudoku(board):
    """Solve the Sudoku board using backtracking"""
    empty = find_empty(board)
    if not empty:
        return True
    
    row, col = empty
    
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            
            if solve_sudoku(board):
                return True
            
            board[row][col] = 0
    
    return False

def find_empty(board):
    """Find an empty cell in the board"""
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def count_solutions(board):
    """Count the number of solutions for the board"""
    solutions = [0]
    
    def backtrack():
        empty = find_empty(board)
        if not empty:
            solutions[0] += 1
            return
        
        row, col = empty
        
        for num in range(1, 10):
            if is_valid(board, row, col, num):
                board[row][col] = num
                backtrack()
                board[row][col] = 0
                
                
                if solutions[0] > 1:
                    return
    
    backtrack()
    return solutions[0]

def get_hint(board, solution):
    """Get a hint for the player (a random empty cell)"""
    empty_cells = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 0:
                empty_cells.append((row, col))
    
    if empty_cells:
        row, col = random.choice(empty_cells)
        return row, col, solution[row][col]
    
    return None


difficulty = 0.5 
board, solution = generate_sudoku(difficulty)
player_board = board.copy()
selected_cell = None
selected_plant = None
animation_frames = 0
solving = False
solve_steps = []
current_step = 0
animation_speed = 5  
free_mode = False  
show_victory = False  
error_cells = set()  
error_timer = 0  
hint_cell = None  
hint_timer = 0  
game_start_time = time.time()  
game_end_time = None  


frame_counter = 0
animation_timer = 0
placed_cells = set()  
victory_animation_timer = 0  

button_hover = None  

def shake_offset(timer):
    """Calculate shake offset based on timer"""
    if timer <= 0:
        return 0, 0
    
    amplitude = min(5, timer / 5)
    x_offset = amplitude * math.sin(timer * 2)
    y_offset = amplitude * math.cos(timer * 3)
    
    return x_offset, y_offset

def draw_garden_background():
    """Draw the garden-themed background"""
    
    screen.fill(LIGHT_GREEN)
    
    
    for i in range(20):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        if not (BOARD_X - 20 <= x <= BOARD_X + BOARD_SIZE + 20 and 
                BOARD_Y - 20 <= y <= BOARD_Y + BOARD_SIZE + 20):
            pygame.draw.ellipse(screen, GRASS_GREEN, 
                               (x, y, random.randint(30, 100), random.randint(10, 30)))
    
    
    for i in range(15):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        if not (BOARD_X - 50 <= x <= BOARD_X + BOARD_SIZE + 50 and 
                BOARD_Y - 50 <= y <= BOARD_Y + BOARD_SIZE + 50):
            
            pygame.draw.line(screen, DARK_GREEN, (x, y + 15), (x, y + 30), 3)
            
            petal_color = (random.randint(200, 255), 
                          random.randint(100, 255), 
                          random.randint(100, 255))
            for angle in range(0, 360, 45):
                rad_angle = angle * 3.14159 / 180
                petal_x = x + 10 * np.cos(rad_angle)
                petal_y = y + 10 * np.sin(rad_angle)
                pygame.draw.circle(screen, petal_color, (int(petal_x), int(petal_y)), 5)
            
            pygame.draw.circle(screen, (255, 255, 0), (x, y), 4)

def draw_board():
    """Draw the Sudoku board with garden styling"""
    
    pygame.draw.rect(screen, DIRT_BROWN, 
                    (BOARD_X - 10, BOARD_Y - 10, 
                     BOARD_SIZE + 20, BOARD_SIZE + 20))
    
    
    border_rects = [
        (BOARD_X - 10, BOARD_Y - 10, BOARD_SIZE + 20, 10),  # Top
        (BOARD_X - 10, BOARD_Y + BOARD_SIZE, BOARD_SIZE + 20, 10),  # Bottom
        (BOARD_X - 10, BOARD_Y, 10, BOARD_SIZE),  # Left
        (BOARD_X + BOARD_SIZE, BOARD_Y, 10, BOARD_SIZE)  # Right
    ]
    
    for rect in border_rects:
        pygame.draw.rect(screen, GRASS_GREEN, rect)
        
        for i in range(rect[2] // 5):
            x = rect[0] + i * 5 + random.randint(-2, 2)
            if rect[2] > rect[3]:  
                y = rect[1] - random.randint(0, 5)
                height = random.randint(5, 10)
                pygame.draw.line(screen, DARK_GREEN, (x, y + height), (x, y), 2)
            else:  
                x = rect[0] - random.randint(0, 5)
                y = rect[1] + i * 5 + random.randint(-2, 2)
                width = random.randint(5, 10)
                pygame.draw.line(screen, DARK_GREEN, (x + width, y), (x, y), 2)
    
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = BOARD_X + col * CELL_SIZE
            y = BOARD_Y + row * CELL_SIZE
            
            
            if (row // 3 + col // 3) % 2 == 0:
                cell_color = (230, 255, 230)  
            else:
                cell_color = (210, 240, 210)  
            
            
            if selected_cell == (row, col):
                cell_color = HIGHLIGHT_COLOR
            
            
            if (row, col) in error_cells:
                
                shake_x, shake_y = shake_offset(error_timer)
                x += shake_x
                y += shake_y
                cell_color = ERROR_COLOR
            
            
            if hint_cell and hint_cell[0] == row and hint_cell[1] == col:
                
                hint_alpha = int(128 + 127 * math.sin(hint_timer * 0.2))
                hint_color = (255, 255, 100, hint_alpha)
                
                
                hint_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                hint_surface.fill(hint_color)
                screen.blit(hint_surface, (x, y))
            
            
            pygame.draw.rect(screen, cell_color, (x, y, CELL_SIZE, CELL_SIZE))
            
            
            if player_board[row][col] != 0:
                plant_idx = player_board[row][col] - 1
                
                
                if (row, col) in placed_cells:
                    frame_idx = (frame_counter // 5) % len(plant_animations[plant_idx])
                    plant_img = plant_animations[plant_idx][frame_idx]
                else:
                    plant_img = plant_animations[plant_idx][0]
                
               
                bounce_offset = 0
                if (row, col) in placed_cells and frame_counter % 60 < 15:
                    bounce_offset = int(3 * math.sin(frame_counter * 0.5))
                
                screen.blit(plant_img, (x + 5, y + 5 - bounce_offset))
                
                
                if board[row][col] != 0:
                    pygame.draw.rect(screen, (0, 0, 0, 50), (x, y, CELL_SIZE, CELL_SIZE), 1)
    
    
    for i in range(GRID_SIZE + 1):
        line_width = 1
        if i % 3 == 0:
            line_width = 3
        
        
        pygame.draw.line(screen, BLACK, 
                        (BOARD_X, BOARD_Y + i * CELL_SIZE),
                        (BOARD_X + BOARD_SIZE, BOARD_Y + i * CELL_SIZE),
                        line_width)
        
        
        pygame.draw.line(screen, BLACK,
                        (BOARD_X + i * CELL_SIZE, BOARD_Y),
                        (BOARD_X + i * CELL_SIZE, BOARD_Y + BOARD_SIZE),
                        line_width)
    
    
    shadow_surface = pygame.Surface((BOARD_SIZE + 20, 20), pygame.SRCALPHA)
    shadow_surface.fill((0, 0, 0, 50))
    screen.blit(shadow_surface, (BOARD_X - 10, BOARD_Y + BOARD_SIZE + 10))

def draw_toolbar():
    """Draw the toolbar with plant selection"""
    
    pygame.draw.rect(screen, TOOLBAR_BG, 
                    (BOARD_X - 10, TOOLBAR_Y, BOARD_SIZE + 20, TOOLBAR_HEIGHT))
    
    
    shadow_surface = pygame.Surface((BOARD_SIZE + 20, 10), pygame.SRCALPHA)
    shadow_surface.fill((0, 0, 0, 30))
    screen.blit(shadow_surface, (BOARD_X - 10, TOOLBAR_Y))
    
    
    mouse_pos = pygame.mouse.get_pos()
    for i in range(9):
        x = BOARD_X + i * (CELL_SIZE + 5)
        y = TOOLBAR_Y + 10
        
        
        plant_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        is_hovering = plant_rect.collidepoint(mouse_pos)
        
        
        if selected_plant == i + 1:
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, 
                            (x - 2, y - 2, CELL_SIZE + 4, CELL_SIZE + 4))
        
       
        if is_hovering:
            hover_surface = pygame.Surface((CELL_SIZE + 4, CELL_SIZE + 4), pygame.SRCALPHA)
            hover_surface.fill((255, 255, 255, 100))
            screen.blit(hover_surface, (x - 2, y - 2))
            
            
            scale_factor = 1.1
            hover_offset = (CELL_SIZE * (1 - scale_factor)) / 2
        else:
            scale_factor = 1.0
            hover_offset = 0
        
        
        pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
        
        
        plant_img = plant_animations[i][0]
        if is_hovering:
            
            plant_img = pygame.transform.scale(
                plant_img, 
                (int(plant_img.get_width() * scale_factor), 
                 int(plant_img.get_height() * scale_factor))
            )
        
        screen.blit(plant_img, (x + 5 - hover_offset, y + 5 - hover_offset))
        
        
        num_text = button_font.render(str(i + 1), True, TEXT_COLOR)
        screen.blit(num_text, (x + CELL_SIZE // 2 - num_text.get_width() // 2, 
                              y + CELL_SIZE + 5))

def draw_button(x, y, width, height, text, is_toggle=False, is_active=False):
    """Draw a button with hover effect"""
    button_rect = pygame.Rect(x, y, width, height)
    mouse_pos = pygame.mouse.get_pos()
    is_hovering = button_rect.collidepoint(mouse_pos)
    
    
    if is_toggle and is_active:
        button_color = (200, 100, 100)  
    elif is_hovering:
        button_color = BUTTON_HOVER_COLOR
        button_hover = text  
    else:
        button_color = BUTTON_COLOR
    
    
    if is_hovering:
        
        glow_surface = pygame.Surface((width + 10, height + 10), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (255, 255, 255, 100), 
                        (0, 0, width + 10, height + 10), border_radius=12)
        screen.blit(glow_surface, (x - 5, y - 5))
    
    
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, button_rect, 2, border_radius=10)
    
    
    text_surf = button_font.render(text, True, BLACK)
    screen.blit(text_surf, (x + width // 2 - text_surf.get_width() // 2,
                          y + height // 2 - text_surf.get_height() // 2))
    
    return is_hovering

def draw_solve_button():
    """Draw the solve button"""
    return draw_button(SOLVE_BUTTON_X, SOLVE_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, "Solve")

def draw_hint_button():
    """Draw the hint button"""
    return draw_button(HINT_BUTTON_X, HINT_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, "Hint")

def draw_free_mode_button():
    """Draw the free mode toggle button"""
    return draw_button(FREE_MODE_X, FREE_MODE_Y, BUTTON_WIDTH, BUTTON_HEIGHT, 
                     "Free Mode", True, free_mode)

def draw_title():
    """Draw the game title"""
    title_text = title_font.render("Plants vs. Zombies Sudoku", True, DARK_GREEN)
    
    
    shadow_text = title_font.render("Plants vs. Zombies Sudoku", True, (0, 0, 0, 128))
    screen.blit(shadow_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2 + 2, 
                             BOARD_Y - 70 + 2))
    
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 
                            BOARD_Y - 70))

def draw_timer():
    """Draw the game timer"""
    if game_end_time:
        elapsed_time = game_end_time - game_start_time
    else:
        elapsed_time = time.time() - game_start_time
    
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    timer_text = timer_font.render(f"Time: {minutes:02d}:{seconds:02d}", True, DARK_GREEN)
    screen.blit(timer_text, (BOARD_X - 10, BOARD_Y - 40))

def draw_victory_screen():
    """Draw the victory screen with animations"""
    if not show_victory:
        return
    
    
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill(VICTORY_BG)
    screen.blit(overlay, (0, 0))
    
    
    victory_scale = 1.0 + 0.1 * math.sin(victory_animation_timer * 0.1)
    victory_text = victory_font.render("Victory!", True, (255, 255, 100))
    victory_text = pygame.transform.scale(
        victory_text, 
        (int(victory_text.get_width() * victory_scale), 
         int(victory_text.get_height() * victory_scale))
    )
    
    screen.blit(victory_text, 
               (SCREEN_WIDTH // 2 - victory_text.get_width() // 2,
                SCREEN_HEIGHT // 3 - victory_text.get_height() // 2))
    
    
    elapsed_time = game_end_time - game_start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    time_text = button_font.render(
        f"Completion Time: {minutes:02d}:{seconds:02d}", 
        True, WHITE
    )
    screen.blit(time_text, 
               (SCREEN_WIDTH // 2 - time_text.get_width() // 2,
                SCREEN_HEIGHT // 2))
    
    
    for i in range(9):
        angle = i * 40 + victory_animation_timer * 2
        radius = 150
        x = SCREEN_WIDTH // 2 + radius * math.cos(math.radians(angle))
        y = SCREEN_HEIGHT * 2 // 3 + 20 * math.sin(victory_animation_timer * 0.2) + radius * math.sin(math.radians(angle))
        
        
        frame_idx = (frame_counter // 5 + i) % len(plant_animations[i])
        plant_img = plant_animations[i][frame_idx]
        
        
        bounce = 10 * math.sin(victory_animation_timer * 0.1 + i)
        
        
        screen.blit(plant_img, (x - plant_img.get_width() // 2, 
                               y - plant_img.get_height() // 2 + bounce))
    
    
    if draw_button(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 
                 SCREEN_HEIGHT * 3 // 4, 
                 BUTTON_WIDTH, BUTTON_HEIGHT, "New Game"):
        return True
    
    return False

def check_completion():
    """Check if the Sudoku puzzle is completed correctly"""
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if player_board[row][col] == 0:
                return False
    
   
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            num = player_board[row][col]
            
            
            player_board[row][col] = 0
            if not is_valid(player_board, row, col, num):
                player_board[row][col] = num
                return False
            player_board[row][col] = num
    
    return True

def prepare_solve_animation():
    """Prepare the steps for the solve animation"""
    global solve_steps, current_step, solving
    
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 0:
                player_board[row][col] = 0
    
    
    solve_steps = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if player_board[row][col] == 0:
                solve_steps.append((row, col, solution[row][col]))
    
    
    random.shuffle(solve_steps)
    
    current_step = 0
    solving = True

def animate_solve_step():
    """Animate one step of the solving process"""
    global current_step, solving, placed_cells, show_victory, game_end_time
    
    if current_step < len(solve_steps):
        row, col, value = solve_steps[current_step]
        player_board[row][col] = value
        placed_cells.add((row, col))
        
       
        try:
            place_sound.play()
        except:
            pass
        
        current_step += 1
    else:
        solving = False
        
        
        if check_completion():
            show_victory = True
            game_end_time = time.time()
            
            
            try:
                complete_sound.play()
            except:
                pass

def show_hint():
    """Show a hint to the player"""
    global hint_cell, hint_timer
    
    hint = get_hint(player_board, solution)
    if hint:
        row, col, value = hint
        hint_cell = (row, col)
        hint_timer = 60  
        
        
        try:
            hint_sound.play()
        except:
            pass

def check_placement_validity(row, col, value):
    """Check if placing a value at (row, col) is valid and handle errors"""
    global error_cells, error_timer
    
    if free_mode:
        return True
    
    if not is_valid(player_board, row, col, value):
        error_cells.add((row, col))
        error_timer = 30  
        
        
        try:
            error_sound.play()
        except:
            pass
        
        return False
    
    return True


clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if show_victory:
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                mouse_pos = pygame.mouse.get_pos()
                new_game_rect = pygame.Rect(
                    SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
                    SCREEN_HEIGHT * 3 // 4,
                    BUTTON_WIDTH, BUTTON_HEIGHT
                )
                
                if new_game_rect.collidepoint(mouse_pos):
                    
                    board, solution = generate_sudoku(difficulty)
                    player_board = board.copy()
                    selected_cell = None
                    selected_plant = None
                    solving = False
                    show_victory = False
                    error_cells.clear()
                    placed_cells.clear()
                    game_start_time = time.time()
                    game_end_time = None
        
        elif not solving:  
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
               
                if (BOARD_X <= mouse_pos[0] <= BOARD_X + BOARD_SIZE and
                    BOARD_Y <= mouse_pos[1] <= BOARD_Y + BOARD_SIZE):
                    
                   
                    col = (mouse_pos[0] - BOARD_X) // CELL_SIZE
                    row = (mouse_pos[1] - BOARD_Y) // CELL_SIZE
                    
                    
                    if board[row][col] == 0:
                        selected_cell = (row, col)
                        
                        
                        if selected_plant is not None:
                            if player_board[row][col] != selected_plant:
                              
                                if check_placement_validity(row, col, selected_plant):
                                    player_board[row][col] = selected_plant
                                    placed_cells.add((row, col))
                                    
                                   
                                    try:
                                        place_sound.play()
                                    except:
                                        pass
                                    
                                    
                                    if check_completion():
                                        show_victory = True
                                        game_end_time = time.time()
                                        

                                        try:
                                            complete_sound.play()
                                        except:
                                            pass
                            else:
                                player_board[row][col] = 0
                                if (row, col) in placed_cells:
                                    placed_cells.remove((row, col))
                

                elif (BOARD_X <= mouse_pos[0] <= BOARD_X + BOARD_SIZE and
                      TOOLBAR_Y <= mouse_pos[1] <= TOOLBAR_Y + TOOLBAR_HEIGHT):
                    

                    plant_idx = (mouse_pos[0] - BOARD_X) // (CELL_SIZE + 5) + 1
                    
                    if 1 <= plant_idx <= 9:
                        if selected_plant == plant_idx:
                            selected_plant = None
                        else:
                            selected_plant = plant_idx
                

                solve_button_rect = pygame.Rect(SOLVE_BUTTON_X, SOLVE_BUTTON_Y, 
                                              BUTTON_WIDTH, BUTTON_HEIGHT)
                if solve_button_rect.collidepoint(mouse_pos):
                    prepare_solve_animation()
                

                hint_button_rect = pygame.Rect(HINT_BUTTON_X, HINT_BUTTON_Y, 
                                             BUTTON_WIDTH, BUTTON_HEIGHT)
                if hint_button_rect.collidepoint(mouse_pos):
                    show_hint()
                

                free_mode_rect = pygame.Rect(FREE_MODE_X, FREE_MODE_Y, 
                                           BUTTON_WIDTH, BUTTON_HEIGHT)
                if free_mode_rect.collidepoint(mouse_pos):
                    free_mode = not free_mode
    

    frame_counter += 1
    

    if error_timer > 0:
        error_timer -= 1
        if error_timer == 0:
            error_cells.clear()
    

    if hint_timer > 0:
        hint_timer -= 1
        if hint_timer == 0:
            hint_cell = None
    

    if show_victory:
        victory_animation_timer += 1
    

    if solving and frame_counter % animation_speed == 0:
        animate_solve_step()

    draw_garden_background()
    draw_board()
    draw_toolbar()
    draw_solve_button()
    draw_hint_button()
    draw_free_mode_button()
    draw_title()
    draw_timer()
    
    if show_victory:
        new_game = draw_victory_screen()
        if new_game:
            board, solution = generate_sudoku(difficulty)
            player_board = board.copy()
            selected_cell = None
            selected_plant = None
            solving = False
            show_victory = False
            error_cells.clear()
            placed_cells.clear()
            game_start_time = time.time()
            game_end_time = None
    
    pygame.display.flip()
    

    clock.tick(60)


pygame.quit()
sys.exit()