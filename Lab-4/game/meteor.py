import pygame
import random
import math

class Meteor:
    SPLIT_MIN_RADIUS = 20   # meteors at least this big fracture when destroyed
    FRAGMENT_COUNT = 2

    def __init__(self, width, x=None, y=None, radius=None, vx=None, vy=None):
        self.x = random.randint(0, width) if x is None else x
        self.y = -30 if y is None else y
        self.radius = random.randint(12, 28) if radius is None else radius
        angle = random.uniform(70,110)
        speed = random.uniform(2,5)
        self.vx = math.cos(math.radians(angle))*speed if vx is None else vx
        self.vy = math.sin(math.radians(angle))*speed if vy is None else vy
        self.color = (
            random.randint(160,220),
            random.randint(80,120),
            random.randint(40,80)
        )
        self.rot = 0
        self.alive_flag = True
        self.rot_speed = random.uniform(-3,3)

    @property
    def is_large(self):
        return self.radius >= self.SPLIT_MIN_RADIUS

    def split(self):
        """Return child fragments if large; small meteors dissolve (empty list)."""
        if not self.is_large:
            return []
        kids = []
        child_radius = max(8, int(self.radius * 0.55))
        for direction in (-1, 1):
            kid = Meteor(
                0, x=self.x + direction * child_radius, y=self.y,
                radius=child_radius,
                vx=self.vx + direction * random.uniform(1.2, 2.2),  # diverge outwards
                vy=max(1.5, self.vy * random.uniform(0.8, 1.1)),
            )
            kid.color = self.color
            kid.rot_speed = random.uniform(-5, 5)
            kids.append(kid)
        return kids

    def update(self):
        self.x+=self.vx; self.y+=self.vy
        self.rot=(self.rot+self.rot_speed)%360

    def off_screen(self, height):
        return self.y > height + 60

    def collides(self, rect):
        cx,cy=rect.centerx,rect.centery
        dx,dy=self.x-cx,self.y-cy
        return (dx**2+dy**2)**0.5 < self.radius + 16

    def draw(self, screen):
        import math
        pts=[]
        for i in range(7):
            angle=math.radians(self.rot+i*(360/7))
            r=self.radius*(0.8+0.2*(i%2))
            pts.append((int(self.x+r*math.cos(angle)),int(self.y+r*math.sin(angle))))
        pygame.draw.polygon(screen,self.color,pts)
        inner=[(int(self.x+(r*0.5)*math.cos(math.radians(self.rot+i*(360/7)))),
                int(self.y+(r*0.5)*math.sin(math.radians(self.rot+i*(360/7)))))
               for i,(cx,cy) in enumerate(pts)]
        pygame.draw.polygon(screen,tuple(max(0,c-40) for c in self.color),inner)
