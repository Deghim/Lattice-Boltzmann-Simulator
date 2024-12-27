import pygame
import sys
from Droplet import Circle
import random

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Wave Interference Simulation")
clock = pygame.time.Clock()

def create_random_wave_properties(): # Randomized wave properties for variety
    return {
        'amplitude': random.uniform(4, 6),
        'frequency': random.uniform(1.8, 2.2),
        'speed': random.uniform(90, 110)
    }

def main():
    running = True
    circles = []
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Create new circle with random wave properties
                    props = create_random_wave_properties()
                    circles.append(Circle(
                        pygame.mouse.get_pos(),
                        amplitude=props['amplitude'],
                        frequency=props['frequency'],
                        speed=props['speed']
                    ))

        screen.fill("black")
        
        for circle in circles:
            circle.update(circles)  # Pass all circles for interference calculation
        
        circles = [circle for circle in circles 
                  if not (circle.is_offscreen(screen.get_width(), screen.get_height()) 
                         or circle.should_remove)]
        
        for circle in circles:
            circle.draw(screen)

        font = pygame.font.Font(None, 36)
        wave_count = font.render(f'Active Waves: {len(circles)}', True, (255, 255, 255))
        screen.blit(wave_count, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()