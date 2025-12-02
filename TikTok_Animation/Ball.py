import pygame


class Ball:
    def __init__(self, pos, speed, color, radius, surface):
        self.x, self.y = pos
        self.sx, self.sy = speed
        self.color = color
        self.radius = radius
        self.surface = surface

    def move(self, width, height):
        """Déplace la balle et gère les rebonds sur les bords."""
        self.x += self.sx
        self.y += self.sy

        # Rebond sur les bords horizontaux
        if self.x - self.radius <= 0 or self.x + self.radius >= width:
            self.sx = -self.sx
            self.x = max(self.radius, min(width - self.radius, self.x))

        # Rebond sur les bords verticaux
        if self.y - self.radius <= 0 or self.y + self.radius >= height:
            self.sy = -self.sy
            self.y = max(self.radius, min(height - self.radius, self.y))

    def draw(self):
        """Dessine la balle."""
        pygame.draw.circle(self.surface, self.color, (int(self.x), int(self.y)), self.radius)
