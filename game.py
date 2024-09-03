import pgzrun
from utils import *


WIDTH = 800
HEIGHT = 600
TILE_SIZE = 18
ROWS = 30
COLS = 20
TITLE = "Platformer"
WIDTH = TILE_SIZE * ROWS
HEIGHT = TILE_SIZE * COLS

menu_options = ["Continue", "Restart", "Toggle Sound", "Quit"]
game_state = 'menu'
current_selection = 0
sound_on = True
enemy_left = True

sounds.background_music.play(-1)  
sounds.background_music.set_volume(0.5)

platforms = build("platformer_platforms.csv", TILE_SIZE)
cakes = build("platformer_cakes.csv", TILE_SIZE)
obstacles = build("platformer_obstacles.csv", TILE_SIZE)

color_key = (0, 0, 0)
fox_stand = Sprite("fox.png", (0, 32, 32, 32), 14, color_key, 30)
fox_walk = Sprite("fox.png", (0, 64, 32, 32), 8, color_key, 5)
enemy_walk = Sprite("enemy.png", (0, 0, 64, 64), 8, color_key, 5)

player = SpriteActor(fox_stand)
enemy = SpriteActor(enemy_walk)

gravity = 1
jump_velocity = -10

def reset_game():
    global cakes, player, over, win
    cakes = build("platformer_cakes.csv", TILE_SIZE)
    player.bottomleft = (0, HEIGHT - TILE_SIZE)
    enemy.bottomleft = (140, 130)
    player.velocity_x = 3
    player.velocity_y = 0
    player.jumping = False
    player.alive = True
    over = False
    win = False

reset_game()

def draw():
    screen.clear()
    screen.fill("black")
    if game_state == 'menu':
        draw_menu()
    elif game_state == 'game':
        draw_game()


def draw_menu():
    y = HEIGHT / 2 - 100
    for index, option in enumerate(menu_options):
        color = "red" if index == current_selection else "white"
        if option == "Toggle Sound":
            option += f" ({'On' if sound_on else 'Off'})"
        screen.draw.text(option, center=(WIDTH / 2, y), fontsize=50, color=color)
        y += 70

def draw_game():
    global cakes, player, enemy_left
    screen.fill("skyblue")
    for platform in platforms:
        platform.draw()
    for obstacle in obstacles:
        obstacle.draw()
    for cake in cakes:
        cake.draw()
    
    enemy.draw()
    if player.alive:
        player.draw()

    if over:
        screen.draw.text("Game over!", center=(WIDTH / 2, HEIGHT / 2))
    if win:
        screen.draw.text("You win!", center=(WIDTH / 2, HEIGHT / 2))

def update():
    global over, win, cakes, player, enemy, enemy_left
    
    if enemy.midleft[0] < 120:
        enemy.x += 1
        enemy_left = True
    elif enemy.midleft[0] > 160:
        enemy.x -= 1
        enemy_left = False
    else:
        if enemy_left:
            enemy.x += 1
        else:
            enemy.x -= 1
    if keyboard.LEFT and player.midleft[0] > 0:
        player.x -= player.velocity_x
        player.sprite = fox_walk
        player.flip_x = True
        if (index := player.collidelist(platforms)) != -1:
            obj = platforms[index]
            player.x = obj.x + (obj.width / 2 + player.width / 2)
    if keyboard.RIGHT and player.midright[0] < WIDTH:
        player.x += player.velocity_x
        player.sprite = fox_walk
        player.flip_x = False
        if (index := player.collidelist(platforms)) != -1:
            obj = platforms[index]
            player.x = obj.x - (obj.width / 2 + player.width / 2)

    player.y += player.velocity_y
    player.velocity_y += gravity

    if (index := player.collidelist(platforms)) != -1:
        obj = platforms[index]

        if player.velocity_y >= 0:
            player.y = obj.y - (obj.height / 2 + player.height / 2)
            player.jumping = False
        else:
            player.y = obj.y + (obj.height / 2 + player.height / 2)

        player.y = obj.y - (obj.height / 2 + player.height / 2)
        player.velocity_y = 0

    if player.collidelist(obstacles) != -1:
        player.alive = False
        over = True

    for cake in cakes:
        if player.colliderect(cake):
            cakes.remove(cake)

    if player.colliderect(enemy):
        player.alive = False
        over = True

    if len(cakes) == 0:
        win = True
        


def on_key_down(key):
    global current_selection, sound_on, game_state, over, win, cakes, player

    if key == keys.UP and game_state == 'menu':
        current_selection -= 1
        if current_selection < 0:
            current_selection = len(menu_options) - 1
    elif key == keys.UP and game_state == 'game' and not player.jumping:
        player.velocity_y = jump_velocity
        player.jumping = True
        if sound_on:
            sounds.jump.play()
    elif key == keys.DOWN and game_state == 'menu':
        current_selection += 1
        if current_selection >= len(menu_options):
            current_selection = 0
    elif key == keys.RETURN and game_state == 'menu':
        if menu_options[current_selection] == "Continue":
            print("Continue")
            game_state = 'game'
        elif menu_options[current_selection] == "Restart":
            print("Restart")
            game_state = 'game'
            reset_game()
        elif menu_options[current_selection] == "Toggle Sound":
            sound_on = not sound_on
            print(f"Sound {'On' if sound_on else 'Off'}")
            if sound_on:
                sounds.background_music.play(-1)
                print("Music On")
            else:
                sounds.background_music.stop()
                print("Music Off")
        elif menu_options[current_selection] == "Quit":
            print("Quit Selected")
            quit()
    elif key == keys.ESCAPE:
        game_state = 'menu' if game_state != 'menu' else 'game'

def on_key_up(key):
    if key == keys.LEFT or key == keys.RIGHT and game_state == 'game':
        player.sprite = fox_stand


pgzrun.go()