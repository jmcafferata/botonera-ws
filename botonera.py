import os
import pygame
from pygame.locals import *
import random
from pathlib import Path
from collections import deque

pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 1920,1080
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Color de fondo verde para chroma keying
BACKGROUND_COLOR = (0, 255, 0)
win.fill(BACKGROUND_COLOR)  # Llena el fondo de la ventana con el color de fondo

# Cargar sonidos e imágenes
sounds_images = {}

assets_folder = 'assets/'  # Cambia esto a la ruta de tu carpeta de activos

for filename in os.listdir(assets_folder):
    filepath = os.path.join(assets_folder, filename)
    base, ext = os.path.splitext(filename)
    if ext in ['.png', '.jpg', '.jpeg','.gif']:
        sounds_images[base] = [pygame.image.load(filepath).convert_alpha()]
    elif ext in ['.wav', '.mp3']:
        sounds_images.setdefault(base, []).append(pygame.mixer.Sound(filepath))

# Variables para rastrear el estado actual
current_image = None
current_sound = None
current_pos = None
start_ticks = None

# Número inicial máximo de sonidos que se pueden reproducir simultáneamente
MAX_SOUNDS = 5

# Cola para rastrear los sonidos que se están reproduciendo
playing_sounds = deque()

def main():
    global current_image, current_sound, current_pos, start_ticks, MAX_SOUNDS
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False

            if event.type == KEYDOWN:
                key_name = pygame.key.name(event.key)
                if key_name.isdigit():
                    MAX_SOUNDS = int(key_name)
                elif key_name in sounds_images and len(sounds_images[key_name]) == 2:
                    current_image, current_sound = sounds_images[key_name]
                    image_width, image_height = current_image.get_size()
                    current_pos = random.randrange(WIDTH - image_width), random.randrange(HEIGHT - image_height)
                    start_ticks = pygame.time.get_ticks()

                    # Si ya se están reproduciendo el máximo de sonidos permitidos, detén el sonido más antiguo
                    if len(playing_sounds) == MAX_SOUNDS:
                        playing_sounds.popleft().stop()

                    # Reproduce el sonido nuevo y añádelo a la cola de sonidos en reproducción
                    current_sound.play()
                    playing_sounds.append(current_sound)
                    
                    win.blit(current_image, current_pos)
                    pygame.display.update()

        # Borrar la imagen después de que el sonido se haya reproducido
        if current_sound is not None and start_ticks is not None and pygame.time.get_ticks() - start_ticks > current_sound.get_length() * 1000:
            win.fill(BACKGROUND_COLOR)
            pygame.display.update()
            current_sound = None
            start_ticks = None

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()