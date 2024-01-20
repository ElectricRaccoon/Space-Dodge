import pygame
import time
import random
import pygame.mixer
import math
pygame.font.init()

pygame.init()
pygame.mixer.init()  # Intialize mixer module
pygame.mixer.music.load("./Sound/gameplay.mp3") # Load Music

WIDTH, HEIGHT = 400, 500 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
y = -3140

PLAYER_WIDTH = 40
PLAYER_HEIGHT = PLAYER_WIDTH * 2.046 # keep correct aspect ratio of image
PLAYER_VEL = 5

STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 5
FONT = pygame.font.SysFont("comicsans", 30)

BG = pygame.transform.scale(pygame.image.load("./Images/bg.jpeg"), (WIDTH, HEIGHT))
Background = pygame.image.load("./Images/Gamebg.png")
PLAYER_IMG = pygame.transform.scale(pygame.image.load("./Images/rocket.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))

pygame.display.set_caption("Space Dodge")

def start_screen():
    title_font = pygame.font.SysFont("arial", 60)
    title_text = title_font.render("Space Dodge", 1, "white")

    description_font = pygame.font.SysFont("arial", 30)
    description_text = description_font.render("Go into Hyperdrive!", 1, "white")

    start_font = pygame.font.SysFont("arial", 40)
    start_text = start_font.render("Start Game", 1, "white")
    start_text_rect = start_text.get_rect(center=(WIDTH/2, HEIGHT/2))

    bg_image = pygame.transform.scale(pygame.image.load("./Images/Start.jpg"), (WIDTH, HEIGHT))

    while True:
        WIN.blit(bg_image, (0, 0))
        WIN.blit(title_text, (WIDTH/2 - title_text.get_width()/2, 80))
        WIN.blit(description_text, (WIDTH/2 - description_text.get_width()/2, 150))
        WIN.blit(start_text, start_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.update()

def draw(player,elapsed_time,stars):
    global y
    y += 1
    if y == 0:
        y = -3140

    WIN.blit(Background,(0,y))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text,(10, 10))

    WIN.blit(PLAYER_IMG, (player.x, player.y))
    
    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()


def main():
    pygame.mixer.music.play(-1)
    start_screen()
    
    run = True

    player = pygame.Rect(200, HEIGHT-PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    star_lower_increment = 50
    star_higher_increment = 5000
    star_count = 0

    stars = []
    hit =False
    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        global STAR_VEL

        if star_count > random.randrange(star_lower_increment, star_higher_increment, 1):
            if(star_higher_increment >= star_lower_increment):
                star_higher_increment -= 10
            for _ in range(1):
                star_x = random.randint(0,WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_count = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        Keys = pygame.key.get_pressed()
        if Keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if Keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL  

        for star in stars[:]:
           star.y += STAR_VEL
           if star.y > HEIGHT:
            stars.remove(star)
           elif star.y >= player.y and star.colliderect(player):
               stars.remove(star)
               hit =True
               break 

        if hit:
            lost_text = FONT.render("GAME OVER", 1, "white")
            WIN.blit(lost_text,(WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(400)
            pygame.mixer.music.stop()
            break

        draw(player,elapsed_time,stars)

    pygame.quit()        


if __name__ == "__main__":
    main()
