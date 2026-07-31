import math
import random

import pygame

#Initialize pygame
pygame.init()

#screen dimensions
WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH,HEIGHT))

#tittle and icon
pygame.display.set_caption("SPACE INVADERS")
icon = pygame.image.load("images/Space-Invaders-Ship.png")
pygame.display.set_icon(icon)

#player
player_img = pygame.transform.scale(pygame.image.load("images/ship.png"), (50, 50))
player_x = WIDTH // 2 - 25
player_y = HEIGHT - 120
player_x_change = 0
player_speed = 0.5

#Enemy
enemy_img = pygame.transform.scale(pygame.image.load("images/enemy.png"), (50,50))
enemy_rows = 3
enemy_cols = 6
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = 50
enemy_speed = 0.05

#Bullet
bullet_img = pygame.transform.scale(pygame.image.load("images/bullet.png"), (50,50))
bullet_x = 0
bullet_y = HEIGHT - 120
bullet_y_change = - 10
bullet_state = "ready"

#score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

#Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)

#inicilize enemies
for i in range (enemy_rows):
    row_x = []
    row_y = []
    for j in range(enemy_cols):
        row_x.append(random.randint(0,WIDTH - 50))
        row_y.append(random.randint(50, 150))
    enemy_x.append(row_x)
    enemy_y.append(row_y)
    enemy_x_change.append([enemy_speed] * enemy_cols)

def show_score():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10,10))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,0,0))
    screen.blit(over_text, (WIDTH // 2 - 50))

def player(x, y):
    screen.blit(player_img, (x,y))

def enemy(x,y):
    screen.blit(enemy_img, (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 15, y))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + 
                         (math.pow(enemy_y - bullet_y, 2)))
    return distance < 27

def tittle_screen():
    tittle_font = pygame.font.Font('freesansbold.ttf', 64)
    start_text = tittle_font.render("SPACE INVADERS", True, (255, 255, 255))
    screen.blit(start_text, (WIDTH // 2 - 250, HEIGHT // 4))

    instruction_text = font.render("Press SPACE to Star", True, (255, 255, 255))
    screen.blit(instruction_text, (WIDTH // 2 - 150, HEIGHT // 2))

    pygame.display.update()

def game_loop():
    global player_x, player_x_change, player_speed, bullet_state, bullet_x, bullet_y, score
    running = True

    while running: 
        screen.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -player_speed
                if event.key == pygame.K_RIGHT:
                    player_x_change = player_speed
                if event.key == pygame.K_SPACE and bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_change = 0

        player_x += player_x_change
        if player_x <= 0:
            player_x = 0
        elif player_x >= WIDTH - 50:
            player_x =  WIDTH -50

        #enemy movement 
        for row in range(enemy_rows):
            for col in range(enemy_cols):
                enemy_x[row][col] += enemy_x_change[row][col]
                if enemy_x[row][col] <= 0 or enemy_x[row][col] >= WIDTH -50:
                    enemy_x_change [row][col] *= -1
                    enemy_y[row][col] += enemy_y_change

        #bullet movement
        if bullet_state == "fire":
            fire_bullet(bullet_x, bullet_y)
            bullet_y += bullet_y_change

        if bullet_y <= 0:
            bullet_y = HEIGHT - 120
            bullet_state = "ready"

        #collision detection for each enemy 
        for row in range(enemy_rows):
            for col in range(enemy_cols):
                collision = is_collision(enemy_x[row][col], enemy_y[row][col], bullet_x, bullet_y)
                if collision:
                    score += 1
                    bullet_y = HEIGHT - 120
                    bullet_state = "ready"
                    enemy_x[row][col] = random.randint(0, WIDTH -50)
                    enemy_y[row][col] = random.randint(50, 150)

        #check for game over 
        for row in range(enemy_rows):
            for col in range(enemy_cols):
                if enemy_y[row][col] > player_y:
                    game_over_text()
                    pygame.display.update()
                    pygame.time.wait(2000)
                    running = False

        #draw player, enemies, and score
        player(player_x, player_y)
        for row in range(enemy_rows):
            for col in range(enemy_cols):
                enemy(enemy_x[row][col], enemy_y[row][col])
        show_score()

        pygame.display.update()

#main program flow
def main():
    tittle_screen()
    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting_for_start = False
                    game_loop()

if __name__ == "__main__":
    main()

pygame.quit()












