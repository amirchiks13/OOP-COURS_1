import sys
import random
import pygame

class CarPlayer(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
      
        self.image = pygame.image.load("car.png").convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (150, 150))

        self.rect = self.image.get_rect(center=(x, y))
        self.base_speed = 5 
        self.speed = self.base_speed

    def update(self):
        keys = pygame.key.get_pressed()
        #Добавил нитро
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.speed = self.base_speed * 2
        else:
            self.speed = self.base_speed
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        # задал такие значения потомучто у изображения границы больше чем у машинки
        if self.rect.top < -20:
            self.rect.top = -20
        if self.rect.bottom > 620:
            self.rect.bottom = 620
        if self.rect.right > 750:
            self.rect.right = 750
        if self.rect.left < 50:
            self.rect.left = 50


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 90))
        self.image.fill((220, 50, 50))
        self.rect = self.image.get_rect()
        self.reset_pos()

    def reset_pos(self):
        
        self.rect.x = random.randint(110, 640)
        self.rect.y = random.randint(-300, -100)
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.reset_pos()


class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Машинка")
        self.clock = pygame.time.Clock()

        self.car = CarPlayer(400, 480)
        self.all_sprites = pygame.sprite.Group(self.car)

        for _ in range(6):
            enemy = Enemy()
            self.all_sprites.add(enemy)

        self.is_running = True
    def run(self):
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                    ):
                    self.is_running = False

            self.all_sprites.update()

            self.screen.fill((34, 139, 34))
            pygame.draw.rect(self.screen, (60, 60, 60), (100, 0, 600, 600))

            self.all_sprites.draw(self.screen)
            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().run()
