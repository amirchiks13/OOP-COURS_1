import sys
import random
import pygame
import datetime
import os


class CarPlayer(pygame.sprite.Sprite):

    def __init__(
        self, x, y, all_sprites=None, engine_sound=None, nitro_sound=None, crash_sound=None
    ):
        super().__init__()

        self.image = pygame.image.load("car.png").convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (150, 150))

        self.rect = self.image.get_rect(center=(x, y))
        self.base_speed = 5
        self.speed = self.base_speed
        self.all_sprites = all_sprites

        self.engine_sound = engine_sound
        self.nitro_sound = nitro_sound
        self.crash_sound = crash_sound
        self.is_nitro = False

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.speed = self.base_speed * 2
            if not self.is_nitro:
                self.is_nitro = True
                if self.engine_sound:
                    self.engine_sound.stop()
                if self.nitro_sound:
                    self.nitro_sound.play(-1)
        else:
            self.speed = self.base_speed
            if self.is_nitro:
                self.is_nitro = False
                if self.nitro_sound:
                    self.nitro_sound.stop()
                if self.engine_sound:
                    self.engine_sound.play(-1)

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

    def car_accident(self):
        if self.engine_sound:
            self.engine_sound.stop()
        if self.nitro_sound:
            self.nitro_sound.stop()
        if self.crash_sound:
            self.crash_sound.play()


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 90))
        self.image.fill((220, 50, 50))
        self.rect = self.image.get_rect()
        self.passed = False
        self.reset_pos()

    def reset_pos(self):
        self.rect.x = random.randint(110, 640)
        self.rect.y = random.randint(-300, -100)
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.reset_pos()
            self.passed = True


class Game:

    def __init__(self, enemy_count=6, difficulty_name="Средняя"):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Машинка")
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.enemy_count = enemy_count
        self.difficulty_name = difficulty_name
        self.is_running = True
        self.font = pygame.font.SysFont("arial", 36, bold=True)
        self.big_font = pygame.font.SysFont("arial", 52, bold=True)

        self.crash_sound = self._load_sound("crash.mp3", volume=0.7)
        self.engine_sound = self._load_sound("drive.mp3", volume=0.3)
        self.nitro_sound = self._load_sound("nitro.mp3", volume=0.6)

        self._reset_game()

    def _load_sound(self, filename, volume=0.5):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, filename)
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            return sound
        except Exception as e:
            print(f"Не удалось загрузить звук '{filename}': {e}")
            return None

    def _reset_game(self):
        self.game_over = False
        self.score = 0
        self.start_ticks = pygame.time.get_ticks()
        self.time_survived = 0.0

        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.car = CarPlayer(
            400, 480, self.all_sprites, self.engine_sound, self.nitro_sound, self.crash_sound
        )
        self.all_sprites.add(self.car)

        for _ in range(self.enemy_count):
            enemy = Enemy()
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

        if self.engine_sound:
            self.engine_sound.stop()
            self.engine_sound.play(-1)

    def run(self):
        while self.is_running:
            self._check_events()
            if not self.game_over:
                self._update()
            self._draw()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False
                elif event.key == pygame.K_r and self.game_over:
                    self._reset_game()

    def _update(self):
        self.time_survived = (pygame.time.get_ticks() - self.start_ticks) / 1000
        self.all_sprites.update()

        for enemy in self.enemies:
            if enemy.passed:
                self.score += 10
                enemy.passed = False

        if pygame.sprite.spritecollide(
            self.car, self.enemies, False, pygame.sprite.collide_rect_ratio(0.65)
        ):
            self.car.car_accident()
            self.game_over = True
            self._save_results()

    def _save_results(self):
        now = datetime.datetime.now()
        line = f"{now} | Сложность: {self.difficulty_name} | Время: {self.time_survived:.1f}сек | Очки: {self.score}\n"
        with open("result.txt", "a", encoding="utf-8") as file:
            file.write(line)

    def _draw(self):
        self.screen.fill((34, 139, 34))
        pygame.draw.rect(self.screen, (60, 60, 60), (100, 0, 600, 600))

        self.all_sprites.draw(self.screen)

        score_text = self.font.render(f"Счет: {self.score}", True, (255, 255, 255))
        time_text = self.font.render(f"Время: {self.time_survived:.1f}с", True, (255, 215, 0))

        self.screen.blit(score_text, (15, 15))
        self.screen.blit(time_text, time_text.get_rect(topright=(self.screen_width - 15, 15)))

        if self.game_over:
            overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, (0, 0))

            over_text = self.big_font.render("GAME OVER — Авария!", True, (224, 100, 117))
            final_score = self.font.render(f"Итоговый счет: {self.score}", True, (255, 255, 255))
            restart_text = self.font.render("Нажми R, чтобы начать заново", True, (200, 200, 200))

            self.screen.blit(
                over_text,
                over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 45)),
            )
            self.screen.blit(
                final_score,
                final_score.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 10)),
            )
            self.screen.blit(
                restart_text,
                restart_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 65)),
            )

        pygame.display.flip()

if __name__ == "__main__":
    difficulties = {
        "легкая": ("Легкая", 4),
        "лёгкая": ("Легкая", 4),
        "1": ("Легкая", 4),
        "средняя": ("Средняя", 6),
        "2": ("Средняя", 6),
        "сложная": ("Сложная", 8),
        "3": ("Сложная", 8),
    }

    user_input = input("Какую сложность вы хотите? (легкая / средняя / сложная): ").strip().lower()
    diff_name, enemy_count = difficulties.get(user_input, ("Средняя", 6))

    game = Game(enemy_count, diff_name)
    game.run()