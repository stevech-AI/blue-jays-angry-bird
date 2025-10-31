import os
import sys
import math
import time
import pygame
# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
resources_path = os.path.join(project_root, "resources", "images")
current_path = os.getcwd()
import pymunk as pm
from characters import Bird
from level import Level

# Blue Jays players list - 2024-2025 active roster
BLUE_JAYS_PLAYERS = [
    "Vladimir Guerrero Jr.",
    "Bo Bichette",
    "George Springer",
    "Kevin Gausman",
    "Alejandro Kirk",
    "Danny Jansen",
    "Daulton Varsho",
    "Davis Schneider",
    "Ernie Clement",
    "Spencer Horwitz",
    "Isiah Kiner-Falefa",
    "Justin Turner",
    "Yusei Kikuchi",
    "José Berríos",
    "Chris Bassitt"
]

# Track bird player index
bird_player_index = 0
# Track used player names for current level to ensure uniqueness
used_player_names = []

pygame.init()
screen = pygame.display.set_mode((1200, 650))

def colorize_red_to_blue(image):
    """Convert red bird to blue by swapping red and blue color channels"""
    image = image.copy()
    width, height = image.get_size()
    # Create a new surface for the result
    result = pygame.Surface((width, height), pygame.SRCALPHA)
    
    for x in range(width):
        for y in range(height):
            r, g, b, a = image.get_at((x, y))
            # Swap red and blue channels to convert red to blue
            # This preserves green and alpha
            result.set_at((x, y), (b, g, r, a))
    
    return result

# Load original red bird and change color to blue
redbird = pygame.image.load(os.path.join(resources_path, "red-bird.png")).convert_alpha()
redbird = colorize_red_to_blue(redbird)
background2 = pygame.image.load(
    os.path.join(resources_path, "background3.png")).convert_alpha()
sling_image = pygame.image.load(
    os.path.join(resources_path, "sling-3.png")).convert_alpha()
# Load Dodgers logo for pigs
dodgers_logo_path = os.path.join(resources_path, "dodgers_logo.png")
if os.path.exists(dodgers_logo_path):
    try:
        dodgers_logo_original = pygame.image.load(dodgers_logo_path).convert_alpha()
        # Scale to match pig size (30x30)
        original_width, original_height = dodgers_logo_original.get_size()
        scale_factor = min(30 / original_width, 30 / original_height)
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        dodgers_pig_image = pygame.transform.scale(dodgers_logo_original, (new_width, new_height))
        print(f"✓ Loaded Dodgers logo for pigs ({new_width}x{new_height})")
    except Exception as e:
        print(f"✗ Error loading Dodgers logo: {e}")
        # Fallback to default pig image
        full_sprite = pygame.image.load(os.path.join(resources_path, "full-sprite.png")).convert_alpha()
        rect = pygame.Rect(181, 1050, 50, 50)
        cropped = full_sprite.subsurface(rect).copy()
        dodgers_pig_image = pygame.transform.scale(cropped, (30, 30))
        print("   Using default pig image as fallback")
else:
    # Fallback to default pig image
    full_sprite = pygame.image.load("../resources/images/full-sprite.png").convert_alpha()
    rect = pygame.Rect(181, 1050, 50, 50)
    cropped = full_sprite.subsurface(rect).copy()
    dodgers_pig_image = pygame.transform.scale(cropped, (30, 30))
    print(f"⚠️  Dodgers logo not found at {dodgers_logo_path}")
    print("   Using default pig image as fallback")
buttons = pygame.image.load(
    os.path.join(resources_path, "selected-buttons.png")).convert_alpha()
# Load Ohtani image for failed screen
ohtani_image_path = os.path.join(resources_path, "ohtani.png")
if os.path.exists(ohtani_image_path):
    try:
        pig_happy = pygame.image.load(ohtani_image_path).convert_alpha()
        # Scale to appropriate size for failed screen
        ohtani_width, ohtani_height = pig_happy.get_size()
        scale_factor = min(300 / ohtani_width, 300 / ohtani_height)
        new_width = int(ohtani_width * scale_factor)
        new_height = int(ohtani_height * scale_factor)
        pig_happy = pygame.transform.smoothscale(pig_happy, (new_width, new_height))
        print(f"✓ Loaded Ohtani image for failed screen ({new_width}x{new_height})")
    except Exception as e:
        print(f"✗ Error loading Ohtani image: {e}")
        pig_happy = pygame.image.load(os.path.join(resources_path, "pig_failed.png")).convert_alpha()
        print("   Using default pig_failed image as fallback")
else:
    pig_happy = pygame.image.load(os.path.join(resources_path, "pig_failed.png")).convert_alpha()
    print(f"⚠️  Ohtani image not found at {ohtani_image_path}")
    print("   Using default pig_failed image - please add ohtani.png")
stars = pygame.image.load(
    os.path.join(resources_path, "stars-edited.png")).convert_alpha()
rect = pygame.Rect(0, 0, 200, 200)
star1 = stars.subsurface(rect).copy()
rect = pygame.Rect(204, 0, 200, 200)
star2 = stars.subsurface(rect).copy()
rect = pygame.Rect(426, 0, 200, 200)
star3 = stars.subsurface(rect).copy()
rect = pygame.Rect(164, 10, 60, 60)
pause_button = buttons.subsurface(rect).copy()
rect = pygame.Rect(24, 4, 100, 100)
replay_button = buttons.subsurface(rect).copy()
rect = pygame.Rect(142, 365, 130, 100)
next_button = buttons.subsurface(rect).copy()
clock = pygame.time.Clock()
rect = pygame.Rect(18, 212, 100, 100)
play_button = buttons.subsurface(rect).copy()
clock = pygame.time.Clock()
running = True
# the base of the physics
space = pm.Space()
space.gravity = (0.0, -700.0)
pigs = []
birds = []
balls = []
polys = []
beams = []
columns = []
poly_points = []
ball_number = 0
polys_dict = {}
mouse_distance = 0
rope_lenght = 90
angle = 0
x_mouse = 0
y_mouse = 0
count = 0
mouse_pressed = False
t1 = 0
tick_to_next_circle = 10
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
sling_x, sling_y = 135, 450
sling2_x, sling2_y = 160, 450
score = 0
game_state = 0
bird_path = []
counter = 0
restart_counter = False
bonus_score_once = True
bold_font = pygame.font.SysFont("arial", 30, bold=True)
bold_font2 = pygame.font.SysFont("arial", 40, bold=True)
bold_font3 = pygame.font.SysFont("arial", 50, bold=True)
name_font = pygame.font.SysFont("arial", 14, bold=True)
wall = False

# Static floor
static_body = pm.Body(body_type=pm.Body.STATIC)
static_lines = [pm.Segment(static_body, (0.0, 060.0), (1200.0, 060.0), 0.0)]
static_lines1 = [pm.Segment(static_body, (1200.0, 060.0), (1200.0, 800.0), 0.0)]
for line in static_lines:
    line.elasticity = 0.95
    line.friction = 1
    line.collision_type = 3
for line in static_lines1:
    line.elasticity = 0.95
    line.friction = 1
    line.collision_type = 3
space.add(static_body)
for line in static_lines:
    space.add(line)


def to_pygame(p):
    """Convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)


def vector(p0, p1):
    """Return the vector of the points
    p0 = (xo,yo), p1 = (x1,y1)"""
    a = p1[0] - p0[0]
    b = p1[1] - p0[1]
    return (a, b)


def unit_vector(v):
    """Return the unit vector of the points
    v = (a,b)"""
    h = ((v[0]**2)+(v[1]**2))**0.5
    if h == 0:
        h = 0.000000000000001
    ua = v[0] / h
    ub = v[1] / h
    return (ua, ub)


def distance(xo, yo, x, y):
    """distance between points"""
    dx = x - xo
    dy = y - yo
    d = ((dx ** 2) + (dy ** 2)) ** 0.5
    return d


def load_music():
    """Load the music"""
    sounds_path = os.path.join(project_root, "resources", "sounds")
    song1 = os.path.join(sounds_path, "angry-birds.ogg")
    pygame.mixer.music.load(song1)
    pygame.mixer.music.play(-1)


def sling_action():
    """Set up sling behavior"""
    global mouse_distance
    global rope_lenght
    global angle
    global x_mouse
    global y_mouse
    global used_player_names
    # Fixing bird to the sling rope
    v = vector((sling_x, sling_y), (x_mouse, y_mouse))
    uv = unit_vector(v)
    uv1 = uv[0]
    uv2 = uv[1]
    mouse_distance = distance(sling_x, sling_y, x_mouse, y_mouse)
    pu = (uv1*rope_lenght+sling_x, uv2*rope_lenght+sling_y)
    bigger_rope = 102
    x_redbird = x_mouse - 20
    y_redbird = y_mouse - 20
    if mouse_distance > rope_lenght:
        pux, puy = pu
        # Center the logo properly
        pux -= redbird.get_width() // 2
        puy -= redbird.get_height() // 2
        pul = pux, puy
        screen.blit(redbird, pul)
        pu2 = (uv1*bigger_rope+sling_x, uv2*bigger_rope+sling_y)
        pygame.draw.line(screen, (0, 0, 0), (sling2_x, sling2_y), pu2, 5)
        screen.blit(redbird, pul)
        pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y), pu2, 5)
        # Display player name when dragging (rope extended)
        available_players = [p for p in BLUE_JAYS_PLAYERS if p not in used_player_names]
        if available_players:
            player_name = available_players[0]  # Next bird to be launched
        else:
            player_name = BLUE_JAYS_PLAYERS[bird_player_index % len(BLUE_JAYS_PLAYERS)]
        if player_name:
            display_name = player_name
            name_text = name_font.render(display_name, True, WHITE)
            name_rect = name_text.get_rect(center=(pux + 22, puy - 18))
            bg_rect = pygame.Rect(name_rect.x - 3, name_rect.y - 2, 
                                 name_rect.width + 6, name_rect.height + 4)
            pygame.draw.rect(screen, BLACK, bg_rect)
            screen.blit(name_text, name_rect)
    else:
        mouse_distance += 10
        pu3 = (uv1*mouse_distance+sling_x, uv2*mouse_distance+sling_y)
        pygame.draw.line(screen, (0, 0, 0), (sling2_x, sling2_y), pu3, 5)
        # Center the logo properly when dragging
        x_redbird_centered = x_mouse - redbird.get_width() // 2
        y_redbird_centered = y_mouse - redbird.get_height() // 2
        screen.blit(redbird, (x_redbird_centered, y_redbird_centered))
        pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y), pu3, 5)
        # Display player name when dragging (rope not extended)
        available_players = [p for p in BLUE_JAYS_PLAYERS if p not in used_player_names]
        if available_players:
            player_name = available_players[0]  # Next bird to be launched
        else:
            player_name = BLUE_JAYS_PLAYERS[bird_player_index % len(BLUE_JAYS_PLAYERS)]
        if player_name:
            display_name = player_name
            name_text = name_font.render(display_name, True, WHITE)
            name_rect = name_text.get_rect(center=(x_mouse, y_redbird - 18))
            bg_rect = pygame.Rect(name_rect.x - 3, name_rect.y - 2, 
                                 name_rect.width + 6, name_rect.height + 4)
            pygame.draw.rect(screen, BLACK, bg_rect)
            screen.blit(name_text, name_rect)
    # Angle of impulse
    dy = y_mouse - sling_y
    dx = x_mouse - sling_x
    if dx == 0:
        dx = 0.00000000000001
    angle = math.atan((float(dy))/dx)


def draw_level_cleared():
    """Draw level cleared"""
    global game_state
    global bonus_score_once
    global score
    level_cleared = bold_font3.render("Level Cleared!", 1, WHITE)
    score_level_cleared = bold_font2.render(str(score), 1, WHITE)
    if level.number_of_birds >= 0 and len(pigs) == 0:
        if bonus_score_once:
            score += (level.number_of_birds-1) * 10000
        bonus_score_once = False
        game_state = 4
        rect = pygame.Rect(300, 0, 600, 800)
        pygame.draw.rect(screen, BLACK, rect)
        screen.blit(level_cleared, (450, 90))
        if score >= level.one_star and score <= level.two_star:
            screen.blit(star1, (310, 190))
        if score >= level.two_star and score <= level.three_star:
            screen.blit(star1, (310, 190))
            screen.blit(star2, (500, 170))
        if score >= level.three_star:
            screen.blit(star1, (310, 190))
            screen.blit(star2, (500, 170))
            screen.blit(star3, (700, 200))
        screen.blit(score_level_cleared, (550, 400))
        screen.blit(replay_button, (510, 480))
        screen.blit(next_button, (620, 480))


def draw_level_failed():
    """Draw level failed"""
    global game_state
    failed = bold_font3.render("Level Failed", 1, WHITE)
    if level.number_of_birds <= 0 and time.time() - t2 > 5 and len(pigs) > 0:
        game_state = 3
        rect = pygame.Rect(300, 0, 600, 800)
        pygame.draw.rect(screen, BLACK, rect)
        screen.blit(failed, (450, 90))
        # Center the Ohtani image on the failed screen
        ohtani_x = (1200 - pig_happy.get_width()) // 2
        ohtani_y = 120
        screen.blit(pig_happy, (ohtani_x, ohtani_y))
        screen.blit(replay_button, (520, 460))


def restart():
    """Delete all objects of the level"""
    global bird_player_index
    global used_player_names
    pigs_to_remove = []
    birds_to_remove = []
    columns_to_remove = []
    beams_to_remove = []
    for pig in pigs:
        pigs_to_remove.append(pig)
    for pig in pigs_to_remove:
        space.remove(pig.shape, pig.shape.body)
        pigs.remove(pig)
    bird_player_index = 0  # Reset bird player index on restart
    used_player_names = []  # Reset used player names on restart
    for bird in birds:
        birds_to_remove.append(bird)
    for bird in birds_to_remove:
        space.remove(bird.shape, bird.shape.body)
        birds.remove(bird)
    for column in columns:
        columns_to_remove.append(column)
    for column in columns_to_remove:
        space.remove(column.shape, column.shape.body)
        columns.remove(column)
    for beam in beams:
        beams_to_remove.append(beam)
    for beam in beams_to_remove:
        space.remove(beam.shape, beam.shape.body)
        beams.remove(beam)


def post_solve_bird_pig(arbiter, space, _):
    """Collision between bird and pig"""
    surface=screen
    a, b = arbiter.shapes
    bird_body = a.body
    pig_body = b.body
    p = to_pygame(bird_body.position)
    p2 = to_pygame(pig_body.position)
    r = 30
    pygame.draw.circle(surface, BLACK, p, r, 4)
    pygame.draw.circle(surface, RED, p2, r, 4)
    pigs_to_remove = []
    for pig in pigs:
        if pig_body == pig.body:
            pig.life -= 20
            pigs_to_remove.append(pig)
            global score
            score += 10000
    for pig in pigs_to_remove:
        space.remove(pig.shape, pig.shape.body)
        pigs.remove(pig)


def post_solve_bird_wood(arbiter, space, _):
    """Collision between bird and wood"""
    poly_to_remove = []
    if arbiter.total_impulse.length > 1100:
        a, b = arbiter.shapes
        for column in columns:
            if b == column.shape:
                poly_to_remove.append(column)
        for beam in beams:
            if b == beam.shape:
                poly_to_remove.append(beam)
        for poly in poly_to_remove:
            if poly in columns:
                columns.remove(poly)
            if poly in beams:
                beams.remove(poly)
        space.remove(b, b.body)
        global score
        score += 5000


def post_solve_pig_wood(arbiter, space, _):
    """Collision between pig and wood"""
    pigs_to_remove = []
    if arbiter.total_impulse.length > 700:
        pig_shape, wood_shape = arbiter.shapes
        for pig in pigs:
            if pig_shape == pig.shape:
                pig.life -= 20
                global score
                score += 10000
                if pig.life <= 0:
                    pigs_to_remove.append(pig)
    for pig in pigs_to_remove:
        space.remove(pig.shape, pig.shape.body)
        pigs.remove(pig)


# bird and pigs
space.add_collision_handler(0, 1).post_solve=post_solve_bird_pig
# bird and wood
space.add_collision_handler(0, 2).post_solve=post_solve_bird_wood
# pig and wood
space.add_collision_handler(1, 2).post_solve=post_solve_pig_wood
load_music()
level = Level(pigs, columns, beams, space)
level.number = 0
level.load_level()

while running:
    # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            # Toggle wall
            if wall:
                for line in static_lines1:
                    space.remove(line)
                wall = False
            else:
                for line in static_lines1:
                    space.add(line)
                wall = True

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            space.gravity = (0.0, -10.0)
            level.bool_space = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
            space.gravity = (0.0, -700.0)
            level.bool_space = False
        if (pygame.mouse.get_pressed()[0] and x_mouse > 100 and
                x_mouse < 250 and y_mouse > 370 and y_mouse < 550):
            mouse_pressed = True
        if (event.type == pygame.MOUSEBUTTONUP and
                event.button == 1 and mouse_pressed):
            # Release new bird
            mouse_pressed = False
            if level.number_of_birds > 0:
                level.number_of_birds -= 1
                t1 = time.time()*1000
                xo = 154
                yo = 156
                if mouse_distance > rope_lenght:
                    mouse_distance = rope_lenght
                # Assign unique player names - find next unused player
                global used_player_names
                available_players = [p for p in BLUE_JAYS_PLAYERS if p not in used_player_names]
                
                if available_players:
                    # Use first available unique player
                    player_name = available_players[0]
                else:
                    # All players used, reset and start over (shouldn't happen in normal gameplay)
                    used_player_names = []
                    player_name = BLUE_JAYS_PLAYERS[0]
                
                used_player_names.append(player_name)
                bird_player_index += 1
                # Reset index if we've used all players
                if bird_player_index >= len(BLUE_JAYS_PLAYERS):
                    bird_player_index = 0
                if x_mouse < sling_x+5:
                    bird = Bird(mouse_distance, angle, xo, yo, space, player_name)
                    birds.append(bird)
                else:
                    bird = Bird(-mouse_distance, angle, xo, yo, space, player_name)
                    birds.append(bird)
                if level.number_of_birds == 0:
                    t2 = time.time()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if (x_mouse < 60 and y_mouse < 155 and y_mouse > 90):
                game_state = 1
            if game_state == 1:
                if x_mouse > 500 and y_mouse > 200 and y_mouse < 300:
                    # Resume in the paused screen
                    game_state = 0
                if x_mouse > 500 and y_mouse > 300:
                    # Restart in the paused screen
                    restart()
                    level.load_level()
                    game_state = 0
                    bird_path = []
            if game_state == 3:
                # Restart in the failed level screen
                if x_mouse > 500 and x_mouse < 620 and y_mouse > 450:
                    restart()
                    level.load_level()
                    game_state = 0
                    bird_path = []
                    score = 0
            if game_state == 4:
                # Build next level
                if x_mouse > 610 and y_mouse > 450:
                    restart()
                    level.number += 1
                    game_state = 0
                    level.load_level()
                    score = 0
                    bird_path = []
                    bonus_score_once = True
                if x_mouse < 610 and x_mouse > 500 and y_mouse > 450:
                    # Restart in the level cleared screen
                    restart()
                    level.load_level()
                    game_state = 0
                    bird_path = []
                    score = 0
    x_mouse, y_mouse = pygame.mouse.get_pos()
    # Draw background
    screen.fill((130, 200, 100))
    screen.blit(background2, (0, -50))
    # Draw first part of the sling
    rect = pygame.Rect(50, 0, 70, 220)
    screen.blit(sling_image, (138, 420), rect)
    # Draw the trail left behind
    for point in bird_path:
        pygame.draw.circle(screen, WHITE, point, 5, 0)
    # Draw the birds in the wait line
    if level.number_of_birds > 0:
        for i in range(level.number_of_birds-1):
            x = 100 - (i*35)
            # Center the logo properly in the wait line
            bird_x = x
            bird_y = 508
            screen.blit(redbird, (bird_x, bird_y))
            # Display player name above waiting bird - show next unique names in sequence
            available_players = [p for p in BLUE_JAYS_PLAYERS if p not in used_player_names]
            if available_players:
                # Show next available unique player (i+1 because current bird is at index 0)
                queue_position = (i + 1) % len(available_players) if available_players else 0
                player_name = available_players[queue_position] if available_players else BLUE_JAYS_PLAYERS[0]
            else:
                # All used, cycle through original list (shouldn't happen in normal gameplay)
                player_name = BLUE_JAYS_PLAYERS[(bird_player_index + i) % len(BLUE_JAYS_PLAYERS)]
            if player_name:
                display_name = player_name
                name_text = name_font.render(display_name, True, WHITE)
                name_rect = name_text.get_rect(center=(x + 22, 508 - 18))
                bg_rect = pygame.Rect(name_rect.x - 3, name_rect.y - 2, 
                                     name_rect.width + 6, name_rect.height + 4)
                pygame.draw.rect(screen, BLACK, bg_rect)
                screen.blit(name_text, name_rect)
    # Draw sling behavior
    if mouse_pressed and level.number_of_birds > 0:
        sling_action()
    else:
        if time.time()*1000 - t1 > 300 and level.number_of_birds > 0:
            # Center the logo in the sling
            sling_x_pos = 130
            sling_y_pos = 426
            screen.blit(redbird, (sling_x_pos, sling_y_pos))
            # Display player name above bird in sling - show next unique name
            available_players = [p for p in BLUE_JAYS_PLAYERS if p not in used_player_names]
            if available_players:
                player_name = available_players[0]  # Next bird to be launched gets first available
            else:
                # All used, cycle through original list (shouldn't happen in normal gameplay)
                player_name = BLUE_JAYS_PLAYERS[bird_player_index % len(BLUE_JAYS_PLAYERS)]
            if player_name:
                display_name = player_name
                name_text = name_font.render(display_name, True, WHITE)
                name_rect = name_text.get_rect(center=(152, 404))
                bg_rect = pygame.Rect(name_rect.x - 3, name_rect.y - 2, 
                                     name_rect.width + 6, name_rect.height + 4)
                pygame.draw.rect(screen, BLACK, bg_rect)
                screen.blit(name_text, name_rect)
        else:
            pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y-8),
                             (sling2_x, sling2_y-7), 5)
    birds_to_remove = []
    pigs_to_remove = []
    counter += 1
    # Draw birds
    for bird in birds:
        if bird.shape.body.position.y < 0:
            birds_to_remove.append(bird)
        p = to_pygame(bird.shape.body.position)
        x, y = p
        # Center the logo properly based on its actual size
        x -= redbird.get_width() // 2
        y -= redbird.get_height() // 2
        screen.blit(redbird, (x, y))
        pygame.draw.circle(screen, BLUE,
                           p, int(bird.shape.radius), 2)
        # Display player name above bird (flying)
        if bird.player_name:
            # Use full name for display
            display_name = bird.player_name
            name_text = name_font.render(display_name, True, WHITE)
            name_rect = name_text.get_rect(center=(p[0], p[1] - 35))
            # Draw semi-transparent background for better readability
            bg_rect = pygame.Rect(name_rect.x - 3, name_rect.y - 2, 
                                 name_rect.width + 6, name_rect.height + 4)
            pygame.draw.rect(screen, BLACK, bg_rect)
            screen.blit(name_text, name_rect)
        if counter >= 3 and time.time() - t1 < 5:
            bird_path.append(p)
            restart_counter = True
    if restart_counter:
        counter = 0
        restart_counter = False
    # Remove birds and pigs
    for bird in birds_to_remove:
        space.remove(bird.shape, bird.shape.body)
        birds.remove(bird)
    for pig in pigs_to_remove:
        space.remove(pig.shape, pig.shape.body)
        pigs.remove(pig)
    # Draw static lines
    for line in static_lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1)
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, (150, 150, 150), False, [p1, p2])
    i = 0
    # Draw pigs
    for pig_obj in pigs:
        i += 1
        # print (i,pig_obj.life)
        pig_shape = pig_obj.shape
        if pig_shape.body.position.y < 0:
            pigs_to_remove.append(pig_obj)

        p = to_pygame(pig_shape.body.position)
        x, y = p

        # Use Dodgers logo for all pigs
        img_to_use = dodgers_pig_image
        
        angle_degrees = math.degrees(pig_shape.body.angle)
        img = pygame.transform.rotate(img_to_use, angle_degrees)
        w,h = img.get_size()
        x -= w*0.5
        y -= h*0.5
        screen.blit(img, (x, y))
        pygame.draw.circle(screen, BLUE, p, int(pig_shape.radius), 2)
        # Display player name above pig
        if pig_obj.player_name:
            name_text = name_font.render(pig_obj.player_name, True, WHITE)
            name_rect = name_text.get_rect(center=(p[0], p[1] - 30))
            # Draw background for text
            pygame.draw.rect(screen, BLACK, (name_rect.x - 2, name_rect.y - 2, 
                                           name_rect.width + 4, name_rect.height + 4))
            screen.blit(name_text, name_rect)
    # Draw columns and Beams
    for column in columns:
        column.draw_poly('columns', screen)
    for beam in beams:
        beam.draw_poly('beams', screen)
    # Update physics
    dt = 1.0/50.0/2.
    for x in range(2):
        space.step(dt) # make two updates per frame for better stability
    # Drawing second part of the sling
    rect = pygame.Rect(0, 0, 60, 200)
    screen.blit(sling_image, (120, 420), rect)
    # Draw score
    score_font = bold_font.render("SCORE", 1, WHITE)
    number_font = bold_font.render(str(score), 1, WHITE)
    screen.blit(score_font, (1060, 90))
    if score == 0:
        screen.blit(number_font, (1100, 130))
    else:
        screen.blit(number_font, (1060, 130))
    screen.blit(pause_button, (10, 90))
    # Pause option
    if game_state == 1:
        screen.blit(play_button, (500, 200))
        screen.blit(replay_button, (500, 300))
    draw_level_cleared()
    draw_level_failed()
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
