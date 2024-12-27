import pygame

class Circle:
    def __init__(self, pos, radius=10):
        self.pos = pos
        self.radius = radius
        self.should_remove = False

    def update(self):
        self.radius *= 1.02  
        if self.radius> 2000:
            self.should_remove = True
        print(self.radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.pos, int(self.radius), width=2)

    def is_offscreen(self, screen_width, screen_height) -> bool:
        x, y = self.pos
        return (
            x + self.radius < 0 
            or x - self.radius > screen_width 
            or y + self.radius < 0 
            or y - self.radius > screen_height
        )
        
