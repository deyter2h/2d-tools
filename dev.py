import pygame as py


def rotate(image, angle, pos, display):
    rot = 0
    rot_speed = angle
    image_r = image.copy()
    rect = image_r.get_rect()
    rect.center = pos
    old_center = rect.center
    rot = (rot + rot_speed) % 360
    new_image = py.transform.rotate(image_r, rot)
    rect = new_image.get_rect()
    rect.center = old_center
    display.blit(new_image, rect)


def trail(length, display, list_of_cords, image): #cursor afterimage like in osu
    pos = [py.mouse.get_pos()[0] - image.get_rect()[2] // 2, py.mouse.get_pos()[1] - image.get_rect()[3] // 2]

    list_of_cords.append(pos)

    for i in range(len(list_of_cords)):
        display.blit(image, (list_of_cords[i]))

    if len(list_of_cords) > length:
        del list_of_cords[0]


COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

FONT = pg.font.Font(None, 62)


class Menu:
    def __init__(self, pos, size, image, trans_limit):
        self.pos = pos
        self.size = size
        self.image = image
        self.menu_rect = pygame.Rect(self.pos, self.size)
        self.transparency_level = 255
        self.limit = trans_limit
        self.c = 0
        self.m = pygame.mouse.get_pos()
        self.m_rect = pygame.Rect(self.m, (3, 3))

    def blit_alpha(self, target, source, location, opacity):

        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)

        if self.transparency_level < self.limit:
            self.transparency_level = self.limit
        if self.transparency_level > 255:
            self.transparency_level = 255

    def add_menu(self, display):
        self.p1, self.p2, self.p3 = pygame.mouse.get_pressed()
        self.m_rect = pygame.Rect(pygame.mouse.get_pos(), (3, 3))

        self.blit_alpha(display, pygame.transform.scale(self.image, self.size), self.pos, self.transparency_level)

        if self.m_rect.colliderect(self.menu_rect):
            self.transparency_level -= 5
            self.c = 0
        else:
            self.transparency_level += 5
            self.c += 1

    def fade_out(self, time):

        if self.c > time:

            self.limit = 0
            self.transparency_level -= 10
            if self.transparency_level < 1:
                self.transparency_level = 0

    def is_menu_clicked(self):
        self.p1, self.p2, self.p3 = pygame.mouse.get_pressed()
        if self.m_rect.colliderect(self.menu_rect):
            if self.p1:
                return True
            else:
                return False


class InputBox:
    def __init__(self, x, y, w, h, is_showing_rect, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

        self.input_text = ''
        self.is_showing_rect = is_showing_rect

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                self.text = ''
            else:
                self.active = False

            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.input_text = self.text
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        if self.is_showing_rect:
            self.active = True
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        self.input_text = self.text

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        if self.active:

            pg.draw.rect(screen, self.color, self.rect, 2)
