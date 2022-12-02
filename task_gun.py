import math
from random import choice, randint

import pygame


FPS = 120

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (125, 125, 125)
GAME_COLORS = [BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1200
HEIGHT = 700
G_CONST = 0.3


class Ball:
    def __init__(self, screen: pygame.Surface, color, x, y):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = color
        self.live = 200
        self.burst = False
        self.h = self.r

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.live -= 1
        self.x += self.vx
        self.y += self.vy
        if self.y > HEIGHT - self.r:
            self.vy = -self.vy
        else:
            self.vy += G_CONST

    def draw(self):
        if not self.burst:
            pygame.draw.circle(self.screen, self.color, (self.x, self.y), min(self.r, self.live))
        else:
            pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r, self.live)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        s = math.sqrt((self.x-obj.x)**2 + (self.y-obj.y) **2)
        return s <= self.r + obj.r


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.x = 50
        self.vx = 0
        self.y = HEIGHT - 50
        self.an = 1
        self.color = WHITE
        self.color_now = WHITE

    def fire2_start(self, event):
        self.f2_on = 1
        self.color = choice(GAME_COLORS)

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls
        new_ball = Ball(self.screen, self.color_now, self.x, self.y)
        new_ball.r += 5
        if event:
            self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.vx + self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.add(new_ball)
        self.f2_on = 0
        self.f2_power = 1
        self.color = WHITE
        self.color_now = WHITE

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2((event.pos[1]-self.y), (event.pos[0]-self.x))

    def move_left(self):
        if self.x > 50:
            self.vx = -5
        else:
            self.vx = 0
        self.x += self.vx
	
    def move_right(self):
        if self.x < WIDTH-50:
            self.vx = 5
        else:
            self.vx = 0
        self.x += self.vx

    def draw(self):
        self.color_now = (255 - (self.f2_power-1)/24*(255-self.color[0]), 255 - (self.f2_power-1)/24*(255-self.color[1]), 255 - (self.f2_power-1)/24*(255-self.color[2]))
        pygame.draw.polygon(self.screen, self.color_now, ((self.x+20*math.cos(self.an)-10*math.sin(self.an), self.y+20*math.sin(self.an)+10*math.cos(self.an)),
                                                      (self.x+20*math.cos(self.an)+10*math.sin(self.an), self.y+20*math.sin(self.an)-10*math.cos(self.an)),
                                                      (self.x-20*math.cos(self.an)+10*math.sin(self.an), self.y-20*math.sin(self.an)-10*math.cos(self.an)),
                                                      (self.x-20*math.cos(self.an)-10*math.sin(self.an), self.y-20*math.sin(self.an)+10*math.cos(self.an))))
        pygame.draw.polygon(self.screen, (102, 102, 0), ((self.x-40, self.y), (self.x+40, self.y), (self.x+40, self.y+25), (self.x-40, self.y+25)))
        pygame.draw.circle(self.screen, GREY, (self.x-25, self.y+35), 10)
        pygame.draw.circle(self.screen, GREY, (self.x, self.y+35), 10)
        pygame.draw.circle(self.screen, GREY, (self.x+25, self.y+35), 10)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 25:
                self.f2_power += 0.3


class Target:
    def __init__(self, screen, target_type):
        """ Инициализация новой цели. """
        self.type = target_type
        self.screen = screen
        self.x = randint(50, WIDTH - 50)
        self.y = randint(50, 300)
        self.vx = randint(-3, 3)
        self.up = True
        self.r = randint(5, 25)
        self.color = RED
        self.live = randint(800, 2000)
        self.burst = False
        self.h = self.r
    
    def move(self):
        self.x += self.vx
        if self.x < 50 or self.x > WIDTH - 50:
            self.vx = - self.vx
        if self.type == 2:
            if self.up:
                self.y += randint(-3, 0)
            else:
                self.y += randint(0, 3)
            if self.y < 50 or self.y > 300:
                self.up = not self.up

    def draw(self):
        self.live -= 1
        if not self.burst:
            pygame.draw.circle(self.screen, self.color, (self.x, self.y), min(self.r, self.live))
        else:
            pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r, self.live)
        pygame.draw.circle(self.screen, WHITE, (self.x, self.y), min(self.r, self.live), 1)


class Plus_Scores():
    '''
    Содержит итерируемый объект, элементами которого являются объекты класса Plus_Score
    '''
    def __init__(self):
        self.plus_scores = set()

    def print_scores(self):  # вывод сообщения о количестве очков за пойманные шарики в местах щелчков
        for plus_score in self.plus_scores:
            plus_score.print_score()
	
    def remove_old(self):  # удаление старых сообщений
        self.plus_scores = set(filter(lambda x: x.t > 0, self.plus_scores))


class Plus_Score():
    '''
    x, y - координаты сообщения о количестве начисленных очков
    score - количество начисленных очков
    t - время жизни сообщения
    '''
    def __init__(self, x, y, score):
        self.x = x + randint(-40, 0)
        self.y = y + randint(-40, 0)
        self.score = score
        self.t = FPS // 2
	
    def print_score(self):  # вывод сообщения о количестве очков за пойманный шарик в месте щелчка
        screen.blit(font_plus_score.render('+' + str(self.score), True, WHITE), (self.x, self.y))
        self.t -= 1
        if self.t <= 0:
            del self


def print_points():
    '''
    Вывод сообщения о текущем количестве очков в левый верхний угол экрана
    '''
    global points, font_score
    screen.blit(font_score.render('Score: ' + str(points), True, WHITE), (0, 0))


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font_score = pygame.font.SysFont('Comic Sans MS', 50, True)
font_plus_score = pygame.font.SysFont('Comic Sans MS', 30, True)
points = 0
delta_points = 0
balls = set()
plus_scores = Plus_Scores()

clock = pygame.time.Clock()
gun = Gun(screen)
targets = [Target(screen, 1), Target(screen, 2)]
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
    if pygame.key.get_pressed()[pygame.K_a]:
        gun.move_left()
    elif pygame.key.get_pressed()[pygame.K_d]:
        gun.move_right()
    else:
        gun.vx = 0

    screen.fill(BLACK)
    for b in balls:
        b.draw()
    for i in range(len(targets)):
        targets[i].draw()
    gun.draw()
    pygame.draw.line(screen, WHITE, (0, HEIGHT), (WIDTH, HEIGHT), 5)
    print_points()
    plus_scores.print_scores()
    pygame.display.update()

    for ball in balls:
        ball.move()
        for i in range(len(targets)):
            if ball.hittest(targets[i]) and not ball.burst and not targets[i].burst:
                delta_points = 35 // targets[i].r
                points += delta_points
                plus_scores.plus_scores.add(Plus_Score(targets[i].x, targets[i].y, delta_points))
                ball.r = min(ball.live, ball.r)
                targets[i].r = min(targets[i].live, targets[i].r)
                ball.live = ball.r
                targets[i].live = targets[i].r
                ball.burst = True
                targets[i].burst = True
    for i in range(len(targets)):
        targets[i].move()
        if targets[i].live == 0:
            targets[i] = Target(screen, i+1)
    balls = set(filter(lambda ball: ball.live != 0, balls))
    plus_scores.remove_old()
    gun.power_up()

pygame.quit()
