import sys
import pygame


class CarPlayer(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
      
        self.image = pygame.image.load("car.png").convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (150, 150))

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5 

    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed


class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Машинка")
        self.clock = pygame.time.Clock()

        self.car = CarPlayer(400, 300)
        self.all_sprites = pygame.sprite.Group(self.car)
        self.is_running = True

    def run(self):
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    self.is_running = False

            self.all_sprites.update()

            self.screen.fill((80, 85, 90))
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()