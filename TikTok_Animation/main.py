import sys

import pygame

from Ball import Ball


class Screen:
    def __init__(self):
        # Initialisation de Pygame
        pygame.init()

        # Fenêtre
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tiktok Screen")

        # Couleurs
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        # Horloge
        self.clock = pygame.time.Clock()

        # Liste de balles
        self.balls = [
            Ball((400, 300), (50, 100), self.WHITE, 20, self.screen)
        ]

    def update(self):
        """Met à jour la logique des objets."""
        for ball in self.balls:
            ball.move(self.width, self.height)

    def draw(self):
        """Dessine tout à l'écran."""
        self.screen.fill(self.BLACK)
        for ball in self.balls:
            ball.draw()
        pygame.display.flip()

    def run(self):
        """Boucle principale."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Mise à jour logique
            self.update()

            # Rendu graphique
            self.draw()

            self.clock.tick(60)

        pygame.quit()
        sys.exit()


def main():
    screen = Screen()
    screen.run()


if __name__ == "__main__":
    main()
