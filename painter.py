#coding:utf-8
import pygame
from pygame.locals import *
import math
import os
import os.path

img_path = "./img"
SCREEN_SITE = (1100,670)
class tool(object):
    def __init__(self,screen):
        self.last_pos = (0,0)
        self.color = (0,0,0)
        self.screen = screen
        self.size = 1
        self.drawing = False

    def start_draw(self,pos):
        self.drawing = True
        self.last_pos = pos

    def end_draw(self):
        self.drawing = False

    def set_size(self,size):
        if size < 1: size = 1
        elif size > 30: size = 30
        self.size = size

    def get_size(self):
        return self.size

    def set_color(self,color):
        self.color = color

    def get_color(self):
        return self.color

    def draw(self, pos):
        if self.drawing:
            for p in self._get_points(pos):
                # draw eveypoint between them
                subsurface = self.screen.subsurface((74,0),(SCREEN_SITE[0]-74,SCREEN_SITE[1]))
                pygame.draw.circle(subsurface, self.color, (p[0]-74,p[1]), self.size)
            self.last_pos = pos

    def _get_points(self, pos):
        """ Get all points between last_point ~ now_point. """
        points = [ (self.last_pos[0], self.last_pos[1]) ]
        len_x = pos[0] - self.last_pos[0]
        len_y = pos[1] - self.last_pos[1]
        length = math.sqrt(len_x ** 2 + len_y ** 2)
        step_x = len_x / length
        step_y = len_y / length
        for i in xrange(int(length)):
            points.append(
                    (points[-1][0] + step_x, points[-1][1] + step_y))
        points = map(lambda x:(int(0.5+x[0]), int(0.5+x[1])), points)
        # return light-weight, uniq list
        return list(set(points))

class Eraser(tool):
    def __init__(self,screen):
        super(Eraser,self).__init__(screen)
        self.color = (255,255,255)
        self.eraser_img = pygame.image.load(os.path.join(img_path,"eraser.png")).convert_alpha()

    def get_eraser_img(self):
        return self.eraser_img

class Paint(tool):
    def __init__(self,screen):
        super(Paint,self).__init__(screen)
        self.paint_img = pygame.image.load(os.path.join(img_path,"paint.png")).convert_alpha()

    def get_paint_img(self):
        return self.paint_img

    def start_draw(self,pos):
        subsurface = self.screen.subsurface((74,0),(SCREEN_SITE[0]-74,SCREEN_SITE[1]))
        subsurface.fill(self.color)
    def draw(self, pos):
        pass
    def end_draw(self):
        pass

class Brush(tool):
    def __init__(self,screen):
        super(Brush,self).__init__(screen)
        self.style = False
        #style为False即为普通画笔，为True就是刷子
        self.brush = pygame.image.load(os.path.join(img_path,"brush.png")).convert_alpha()
        self.brush_now = self.brush.subsurface((0,0),(1,1))

    def set_size(self,size):
        super(Brush,self).set_size(size)
        self.brush_now = self.brush.subsurface((0,0),(self.size*2,self.size*2))

    def get_current_brush(self):
        return self.brush_now

    def set_color(self,color):
        super(Brush,self).set_color(color)
        for x in xrange(self.brush.get_width()):
            for y in xrange(self.brush.get_height()):
                self.brush.set_at((x, y),color + (self.brush.get_at((x, y)).a,))

    def set_brush_style(self,style):
        self.style = style

    def get_brush_style(self):
        return self.style

    def draw(self, pos):
        if self.drawing:
            subsurface = self.screen.subsurface((74,0),(SCREEN_SITE[0]-74,SCREEN_SITE[1]))
            for p in self._get_points(pos):
                # draw eveypoint between them
                if self.style == False:
                    pygame.draw.circle(subsurface,
                            self.color, (p[0]-74,p[1]), self.size)
                else:
                    subsurface.blit(self.brush_now, (p[0]-74,p[1]))
            self.last_pos = pos

class Menu():
    def __init__(self,screen,brush,eraser,paint):
        self.screen = screen
        self.brush = brush
        self.eraser = eraser
        self.paint = paint
        self.activity = brush
        self.colors = [
                (0xff, 0x00, 0xff), (0x80, 0x00, 0x80),
                (0x00, 0x00, 0xff), (0x00, 0x00, 0x80),
                (0x00, 0xff, 0xff), (0x00, 0x80, 0x80),
                (0x00, 0xff, 0x00), (0x00, 0x80, 0x00),
                (0xff, 0xff, 0x00), (0x80, 0x80, 0x00),
                (0xff, 0x00, 0x00), (0x80, 0x00, 0x00),
                (0xc0, 0xc0, 0xc0), (0xff, 0xff, 0xff),
                (0x00, 0x00, 0x00), (0x80, 0x80, 0x80),
        ]
        self.colors_rect = []
        for (i,rgb) in enumerate(self.colors):
            rect = pygame.Rect(10+i%2*32,254+i/2*32,32,32)
            self.colors_rect.append(rect)

        self.pens =[
                pygame.image.load(os.path.join(img_path,"pen1.png")).convert_alpha(),
                pygame.image.load(os.path.join(img_path,"pen2.png")).convert_alpha()
        ]
        self.pens_rect = []
        for (i,pen) in enumerate(self.pens):
            rect = pygame.Rect(10,10+i*64,64,64)
            self.pens_rect.append(rect)

        self.sizes = [
                pygame.image.load(os.path.join(img_path,"big.png")).convert_alpha(),
                pygame.image.load(os.path.join(img_path,"small.png")).convert_alpha()
            ]
        self.sizes_rect = []
        for (i,size) in enumerate(self.sizes):
            rect = pygame.Rect(10+i*32,138,32,32)
            self.sizes_rect.append(rect)
        #eraser
        self.eraser_rect = pygame.Rect(10,520,64,64)
        self.paint_rect = pygame.Rect(10,590,64,64)

    def get_activity(self):
        return self.activity

    def render(self):
        #draw pens
        for (i,img) in enumerate(self.pens):
            self.screen.blit(img,self.pens_rect[i].topleft)
        #draw sizes
        for (i,img) in enumerate(self.sizes):
            self.screen.blit(img,self.sizes_rect[i].topleft)

        self.screen.fill((255,255,255),(10,180,64,64))
        pygame.draw.rect(self.screen,(0,0,0),(10,180,64,64),1)
        size = self.brush.get_size()
        x = 10 + 32
        y = 180 + 32
        if self.brush.get_brush_style():
            x = x - size
            y = y - size
            self.screen.blit(self.brush.get_current_brush(),(x, y))
        else:
             pygame.draw.circle(self.screen,
                    self.brush.get_color(), (x, y), size)

        for (i, rgb) in enumerate(self.colors):
            pygame.draw.rect(self.screen, rgb, self.colors_rect[i])

        self.screen.blit(self.eraser.get_eraser_img(), self.eraser_rect.topleft)
        self.screen.blit(self.paint.get_paint_img(), self.paint_rect.topleft)

    def click_button(self,pos):
        #pen buttons
        for (i,rect) in enumerate(self.pens_rect):
            if rect.collidepoint(pos):
                self.brush.set_brush_style(bool(i))
                self.activity = self.brush
                return True

        #size buttons
        for (i,rect) in enumerate(self.sizes_rect):
            if rect.collidepoint(pos):
                if i == 0:
                    self.brush.set_size(self.brush.get_size()+1)
                    self.eraser.set_size(self.eraser.get_size()+1)
                    return "+"
                else:
                    self.brush.set_size(self.brush.get_size()-1)
                    self.eraser.set_size(self.eraser.get_size()-1)
                    return "-"

        # color buttons
        for (i,rect) in enumerate(self.colors_rect):
            if rect.collidepoint(pos):
                self.brush.set_color(self.colors[i])
                self.paint.set_color(self.colors[i])
                return True

        #eraser buttons
        if self.eraser_rect.collidepoint(pos):
            self.activity = self.eraser
            return True

        #paint buttons
        if self.paint_rect.collidepoint(pos):
            self.activity = self.paint
            return True
        return False
class Painter():
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SITE)
        pygame.display.set_caption("painter")
        self.clock = pygame.time.Clock()
        self.brush = Brush(self.screen)
        self.eraser = Eraser(self.screen)
        self.paint = Paint(self.screen)
        self.menu = Menu(self.screen,self.brush,self.eraser,self.paint)

    def run(self):
        self.screen.fill((255,255,255))
        speed = 0
        #size speed
        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        speed = 1
                    elif event.key == K_DOWN:
                        speed = -1
                elif event.type == KEYUP:
                    speed = 0
                elif event.type == MOUSEBUTTONDOWN:
                    if ((event.pos)[0] <= 74):
                        flag = self.menu.click_button(event.pos)
                        if flag == "+":
                            speed = 1
                        elif flag == "-":
                            speed = -1
                        if flag != False: pass
                    else:
                        self.menu.activity.start_draw(event.pos)
                elif event.type == MOUSEMOTION:
                    self.menu.activity.draw(event.pos)
                elif event.type == MOUSEBUTTONUP:
                    self.menu.activity.end_draw()
                    speed = 0
            self.menu.brush.set_size(self.brush.get_size()+speed)
            self.menu.eraser.set_size(self.eraser.get_size()+speed)
            self.menu.render()
            pygame.display.update()

if __name__ == "__main__":
    app = Painter()
    app.run()
