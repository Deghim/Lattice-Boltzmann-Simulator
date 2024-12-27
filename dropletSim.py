import pygame
import sys
from Droplet import Circle

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Droplet Simulation")

clock = pygame.time.Clock()
        

def main():
    running = True
    circles = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    circles.append(Circle(pygame.mouse.get_pos()))
        
        screen.fill("black")
        
        circles = [
            circle for circle in circles 
                if not (circle.is_offscreen(screen.get_width(), screen.get_height()) 
                        or circle.should_remove)]
        
        for circle in circles:
            circle.update()
            circle.draw(screen)


        # flip() the display to put your work on screen
        pygame.display.flip()
        dt = clock.tick(60) / 1000

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()