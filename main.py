import pygame
import sys
import time
import random
from pygame import mixer
import numpy as np


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


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREEN = (200, 255, 200)
DARK_GREEN = (100, 180, 100)
HIGHLIGHT_COLOR = (255, 255, 200)
GRASS_GREEN = (120, 200, 80)
DIRT_BROWN = (139, 69, 19)
TOOLBAR_BG = (242, 240, 230)
BUTTON_COLOR = (80, 200, 120)
BUTTON_HOVER_COLOR = (100, 220, 140)
TEXT_COLOR = (60, 60, 60)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Plants vs. Zombies Sudoku")


title_font = pygame.font.Font(None, 60)
button_font = pygame.font.Font(None, 30)
cell_font = pygame.font.Font(None, 40)


plant_names = [
    "Sunflower", "Peashooter", "Wall-nut", "Cherry Bomb", 
    "Snow Pea", "Chomper", "Repeater", "Puff-shroom", "Potato Mine"
]


plant_animations = []
for i in range(1, 10):
    frames = []
    base_color = (
        random.randint(100, 255),
        random.randint(100, 255),
        random.randint(100, 255)
    )
    
    
    for j in range(8):
        
        plant_surf = pygame.Surface((CELL_SIZE - 10, CELL_SIZE - 10), pygame.SRCALPHA)
        
        
        color_variation = (
            max(0, min(255, base_color[0] + random.randint(-15, 15))),
            max(0, min(255, base_color[1] + random.randint(-15, 15))),
            max(0, min(255, base_color[2] + random.randint(-15, 15)))
        )
        
        
        pygame.draw.circle(plant_surf, color_variation, (CELL_SIZE // 2 - 5, CELL_SIZE // 2 - 5), CELL_SIZE // 2 - 10)
        
        
        eye_pos_y = CELL_SIZE // 2 - 5 + random.randint(-1, 1)  # Slight movement for animation
        pygame.draw.circle(plant_surf, WHITE, (CELL_SIZE // 3 - 5, eye_pos_y), 5)
        pygame.draw.circle(plant_surf, WHITE, (2 * CELL_SIZE // 3 - 5, eye_pos_y), 5)
        pygame.draw.circle(plant_surf, BLACK, (CELL_SIZE // 3 - 5, eye_pos_y), 2)
        pygame.draw.circle(plant_surf, BLACK, (2 * CELL_SIZE // 3 - 5, eye_pos_y), 2)
        
        frames.append(plant_surf)
    
    plant_animations.append(frames)


try:
    place_sound = mixer.Sound("place_sound.wav")  
    complete_sound = mixer.Sound("complete_sound.wav")  
    background_music = "background_music.mp3"  
    
    
    
    place_sound = mixer.Sound(pygame.mixer.Sound(buffer=bytes([random.randint(0, 255) for _ in range(1000)])))
    complete_sound = mixer.Sound(pygame.mixer.Sound(buffer=bytes([random.randint(0, 255) for _ in range(1000)])))
    
    # Set volume
    place_sound.set_volume(0.3)
    complete_sound.set_volume(0.5)
    
    # Play background music
    # mixer.music.load(background_music)
    # mixer.music.set_volume(0.2)
    # mixer.music.play(-1)  # Loop indefinitely
except:
    print("Sound files not found. Continuing without sound.")

# Sudoku board generation and solving
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
        if board[row][x] == num:
            return False
    
    
    for x in range(9):
        if board[x][col] == num:
            return False
    
    
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
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


board, solution = generate_sudoku(0.5)
player_board = board.copy()
selected_cell = None
selected_plant = None
animation_frames = 0
solving = False
solve_steps = []
current_step = 0
animation_speed = 5  


frame_counter = 0
animation_timer = 0
placed_cells = set()  

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
            if rect[2] > rect[3]:  # Horizontal border
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
                cell_color = (210, 240, 210)  #
            
            
            if selected_cell == (row, col):
                cell_color = HIGHLIGHT_COLOR
            
            
            pygame.draw.rect(screen, cell_color, (x, y, CELL_SIZE, CELL_SIZE))
            
            
            if player_board[row][col] != 0:
                plant_idx = player_board[row][col] - 1
                
                
                if (row, col) in placed_cells:
                    frame_idx = (frame_counter // 5) % len(plant_animations[plant_idx])
                    plant_img = plant_animations[plant_idx][frame_idx]
                else:
                    plant_img = plant_animations[plant_idx][0]
                
                screen.blit(plant_img, (x + 5, y + 5))
                
                
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
    
    
    for i in range(9):
        x = BOARD_X + i * (CELL_SIZE + 5)
        y = TOOLBAR_Y + 10
        
        
        if selected_plant == i + 1:
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, 
                            (x - 2, y - 2, CELL_SIZE + 4, CELL_SIZE + 4))
        
        
        pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
        
        
        plant_img = plant_animations[i][0]
        screen.blit(plant_img, (x + 5, y + 5))
        
        
        num_text = button_font.render(str(i + 1), True, TEXT_COLOR)
        screen.blit(num_text, (x + CELL_SIZE // 2 - num_text.get_width() // 2, 
                              y + CELL_SIZE + 5))

def draw_solve_button():
    """Draw the solve button"""
    button_color = BUTTON_COLOR
    
    
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(SOLVE_BUTTON_X, SOLVE_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    
    if button_rect.collidepoint(mouse_pos):
        button_color = BUTTON_HOVER_COLOR
    
    
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, button_rect, 2, border_radius=10)
    
    
    text = button_font.render("Solve", True, BLACK)
    screen.blit(text, (SOLVE_BUTTON_X + BUTTON_WIDTH // 2 - text.get_width() // 2,
                      SOLVE_BUTTON_Y + BUTTON_HEIGHT // 2 - text.get_height() // 2))

def draw_title():
    """Draw the game title"""
    title_text = title_font.render("Plants vs. Zombies Sudoku", True, DARK_GREEN)
    
    
    shadow_text = title_font.render("Plants vs. Zombies Sudoku", True, (0, 0, 0, 128))
    screen.blit(shadow_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2 + 2, 
                             BOARD_Y - 70 + 2))
    
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 
                            BOARD_Y - 70))

def check_completion():
    """Check if the Sudoku puzzle is completed correctly"""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if player_board[row][col] == 0 or not is_valid(player_board, row, col, player_board[row][col]):
                return False
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
    global current_step, solving, placed_cells
    
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
        
       
        try:
            complete_sound.play()
        except:
            pass


clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if not solving:  
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
                                player_board[row][col] = selected_plant
                                placed_cells.add((row, col))
                                
                                
                                try:
                                    place_sound.play()
                                except:
                                    pass
                                
                                
                                if check_completion():
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
    
    
    frame_counter += 1
    
    
    if solving and frame_counter % animation_speed == 0:
        animate_solve_step()
    
    
    draw_garden_background()
    draw_board()
    draw_toolbar()
    draw_solve_button()
    draw_title()
    
    
    pygame.display.flip()
    
    
    clock.tick(60)


pygame.quit()
sys.exit()