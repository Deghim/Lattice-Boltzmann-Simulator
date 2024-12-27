import pygame
import math
from typing import List, Tuple

class Circle:
    def __init__(self, pos, radius=10, amplitude=5, frequency=2, speed=100):
        self.pos = pos
        self.radius = radius
        self.initial_radius = radius
        
        self.amplitude = amplitude  # Wave height
        self.frequency = frequency  # Wave frequency
        self.speed = speed         # Wave propagation speed
        self.creation_time = pygame.time.get_ticks() / 1000.0  # Time in seconds
        self.should_remove = False
        self.wave_points: List[Tuple[float, float]] = []
        self.max_radius = 2000

    def calculate_wave(self, time: float, distance: float) -> float:
        """
        Calculate wave amplitude at a given point using the wave equation
        A(x,t) = A₀ * sin(kx - ωt) * e^(-αx)
        where:
        - A₀ is initial amplitude
        - k is wave number (2π/wavelength)
        - ω is angular frequency
        - α is damping coefficient
        """
        wavelength = 50.0  # pixels
        k = 2 * math.pi / wavelength
        w = 2 * math.pi * self.frequency
        damping = 0.005  # Damping coefficient or could be used as viscosity
        
        wave = self.amplitude * math.sin(k * distance - w * time) * math.exp(-damping * distance)
        return wave

    def update(self, other_circles: List['Circle']) -> None:
        print(self.radius)
        current_time = pygame.time.get_ticks() / 1000.0
        elapsed_time = current_time - self.creation_time
        
        self.radius = self.initial_radius + self.speed * elapsed_time
        
        if self.radius > self.max_radius:
            self.should_remove = True
            return

        
        num_points = 314 #Quantity of lines in the circle: hexagon, octagon, pentagon, etc

        self.wave_points = []
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            base_x = self.pos[0] + math.cos(angle) * self.radius
            base_y = self.pos[1] + math.sin(angle) * self.radius
            
            total_displacement = self.calculate_wave(elapsed_time, self.radius)
            
            
            for other in other_circles: # Interference from other circles
                if other != self:
                    dx = base_x - other.pos[0]
                    dy = base_y - other.pos[1]
                    distance = math.sqrt(dx * dx + dy * dy)
                    other_time = current_time - other.creation_time
                    
                    if distance <= other.radius:
                        total_displacement += other.calculate_wave(other_time, distance)

            displacement_x = math.cos(angle) * total_displacement
            displacement_y = math.sin(angle) * total_displacement
            
            self.wave_points.append((
                base_x + displacement_x,
                base_y + displacement_y
            ))

    def draw(self, screen: pygame.Surface) -> None:
        if len(self.wave_points) < 2:
            return

        pygame.draw.lines(screen, "white", True, self.wave_points, width=2)

    def is_offscreen(self, screen_width: int, screen_height: int) -> bool:
        if not self.wave_points:
            return True
            
        for x, y in self.wave_points:
            if (0 <= x <= screen_width and 0 <= y <= screen_height):
                return False
        return True