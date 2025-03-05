import pygame
import random
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 550, 630 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drone Dash")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Carrega imagens
background = pygame.image.load("assets/img/fundo.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

tela_inicial = pygame.image.load("assets/img/tela_inicial.png")
tela_inicial = pygame.transform.scale(tela_inicial, (WIDTH, HEIGHT))

drone_img = pygame.image.load("assets/img/drone.png")
drone_img = pygame.transform.scale(drone_img, (45, 32))

building_img = pygame.image.load("assets/img/building.png")
building_img = pygame.transform.scale(building_img, (70, 400))

bird_img = pygame.image.load("assets/img/bird.png")
bird_img = pygame.transform.scale(bird_img, (50, 50))

# Carrega sons
flap_sound = pygame.mixer.Sound("assets/audio/flap.wav")
shoot_sound = pygame.mixer.Sound("assets/audio/shoot.wav")
collision_sound = pygame.mixer.Sound("assets/audio/collision.wav")

# Variáveis do drone
drone_x, drone_y = 50, HEIGHT // 2
drone_velocity = 0
gravity = 0.5
jump_strength = -8

# Obstáculos
buildings = []
building_gap = 150
building_speed = 3

# Pássaros
birds = []
bird_speed = 3

# Tiros
tiros = []
tiro_speed = 7

# Contador de pássaros abatidos
bird_count = 0

# Dificuldade progressiva
time_elapsed = 0

def add_building():
    height = random.randint(100, 300)
    buildings.append(pygame.Rect(WIDTH, HEIGHT - height, 70, height))

def add_bird():
    birds.append(pygame.Rect(random.randint(WIDTH, WIDTH + 300), random.randint(50, HEIGHT - 100), 50, 50))

def restart_game():
    global drone_y, drone_velocity, buildings, birds, tiros, bird_count, time_elapsed
    drone_y = HEIGHT // 2
    drone_velocity = 0
    buildings.clear()
    birds.clear()
    tiros.clear()
    bird_count = 0
    time_elapsed = 0
    main()

def main():
    global drone_y, drone_velocity, time_elapsed, bird_count
    clock = pygame.time.Clock()
    game_started = False
    running = True
    
    while running:
        screen.blit(tela_inicial if not game_started else background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    drone_velocity = jump_strength
                    flap_sound.play()
                    game_started = True
                if event.key == pygame.K_x and game_started:
                    tiros.append(pygame.Rect(drone_x + 45, drone_y + 16, 10, 5))
                    shoot_sound.play()

        if game_started:
            drone_velocity += gravity
            drone_y += drone_velocity
            time_elapsed += 1

            if time_elapsed % 120 == 0:  # A cada 2 segundos
                add_building()
                add_bird()

            for building in buildings[:]:
                building.x -= building_speed
                if building.x + building.width < 0:
                    buildings.remove(building)
                if building.colliderect(pygame.Rect(drone_x, drone_y, 45, 32)):
                    collision_sound.play()
                    restart_game()
                screen.blit(building_img, (building.x, building.y))

            for bird in birds[:]:
                bird.x -= bird_speed
                if bird.x + bird.width < 0:
                    birds.remove(bird)
                if bird.colliderect(pygame.Rect(drone_x, drone_y, 45, 32)):
                    collision_sound.play()
                    restart_game()
                screen.blit(bird_img, (bird.x, bird.y))

            for tiro in tiros[:]:
                tiro.x += tiro_speed
                if tiro.x > WIDTH:
                    tiros.remove(tiro)
                for bird in birds[:]:
                    if tiro.colliderect(bird):
                        birds.remove(bird)
                        tiros.remove(tiro)
                        bird_count += 1
                        break
                pygame.draw.rect(screen, WHITE, tiro)

            if drone_y > HEIGHT or drone_y < 0:
                collision_sound.play()
                restart_game()

            screen.blit(drone_img, (drone_x, drone_y))
            score_text = pygame.font.SysFont("Arial", 30).render(f"Pássaros: {bird_count}", True, WHITE)
            screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)

main()
