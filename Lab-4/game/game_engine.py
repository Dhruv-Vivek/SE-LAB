import pygame
import random
from game.ship import Ship
from game.meteor import Meteor
from game.laser import Laser
from game.powerup import ShieldOrb

WIDTH,HEIGHT=700,520
FPS=60
BG=(8,5,20)

LASER_COOLDOWN=12          # frames between shots
LASER_HIT_POINTS=10        # base points per meteor hit
MULTIPLIER_STEP=10*FPS     # frames of hit-free survival per +1 multiplier
ORB_MIN_DELAY,ORB_MAX_DELAY=8*FPS,14*FPS

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Meteor Dodge")
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont("monospace",26,bold=True)
        self.small_font=pygame.font.SysFont("monospace",20,bold=True)
        self.big_font=pygame.font.SysFont("monospace",46,bold=True)
        self.stars=[(random.randint(0,WIDTH),random.randint(0,HEIGHT),random.randint(1,3)) for _ in range(80)]
        self.reset()

    def reset(self):
        self.ship=Ship(WIDTH//2,HEIGHT-80)
        self.meteors=[]
        self.lasers=[]
        self.orbs=[]
        self.timer=0
        self.spawn_interval=60
        self.frames=0              # survival time in frames
        self.score=0               # points (affected by multiplier)
        self.streak=0              # frames survived since last hit
        self.laser_cd=0
        self.orb_timer=random.randint(ORB_MIN_DELAY,ORB_MAX_DELAY)
        self.game_over=False
        self.started=False

    @property
    def multiplier(self):
        return 1+self.streak//MULTIPLIER_STEP

    def fire_laser(self):
        if self.laser_cd>0: return
        self.lasers.append(Laser(self.ship.rect.centerx,self.ship.rect.top))
        self.laser_cd=LASER_COOLDOWN

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: return False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if self.game_over: self.reset()
                    elif not self.started: self.started=True
                    else: self.fire_laser()          # SPACE during flight = shoot
        return True

    def update(self):
        if self.game_over or not self.started: return
        keys=pygame.key.get_pressed()
        self.ship.move(keys,WIDTH,HEIGHT)
        if self.laser_cd>0: self.laser_cd-=1
        if keys[pygame.K_SPACE]: self.fire_laser()   # holding SPACE auto-fires (respects cooldown)

        # spawn meteors
        self.timer+=1
        if self.timer>=self.spawn_interval:
            self.meteors.append(Meteor(WIDTH))
            self.timer=0
            self.spawn_interval=max(20,self.spawn_interval-0.3)

        # spawn shield orb (only when ship has none and none is on screen)
        self.orb_timer-=1
        if self.orb_timer<=0:
            if not self.ship.shield and not self.orbs:
                self.orbs.append(ShieldOrb(WIDTH))
            self.orb_timer=random.randint(ORB_MIN_DELAY,ORB_MAX_DELAY)

        # lasers vs meteors (with splitting)
        new_meteors=[]
        for l in self.lasers:
            l.update()
            for m in self.meteors:
                if l.alive and m.alive_flag and l.hits(m):
                    l.alive=False
                    m.alive_flag=False
                    new_meteors.extend(m.split())
                    self.score+=LASER_HIT_POINTS*self.multiplier
        self.meteors=[m for m in self.meteors if m.alive_flag]+new_meteors
        self.lasers=[l for l in self.lasers if l.alive]

        # meteors vs ship (shield absorbs one hit)
        for m in self.meteors:
            m.update()
            if m.collides(self.ship.rect):
                if self.ship.shield:
                    self.ship.shield=False
                    self.ship.shield_flash=10
                    m.alive_flag=False               # meteor shatters on the barrier
                    self.streak=0                    # a hit, even absorbed, resets the multiplier
                else:
                    self.game_over=True
        self.meteors=[m for m in self.meteors if m.alive_flag and not m.off_screen(HEIGHT)]

        # orbs
        for o in self.orbs:
            o.update(HEIGHT)
            if o.alive and o.collected_by(self.ship.rect):
                self.ship.shield=True
                o.alive=False
        self.orbs=[o for o in self.orbs if o.alive]

        # time + multiplier-based scoring
        self.frames+=1
        self.streak+=1
        self.score+=self.multiplier

    def draw(self):
        self.screen.fill(BG)
        for sx,sy,sr in self.stars:
            pygame.draw.circle(self.screen,(200,200,220),(sx,sy),sr)
        for o in self.orbs: o.draw(self.screen)
        for m in self.meteors: m.draw(self.screen)
        for l in self.lasers: l.draw(self.screen)
        self.ship.draw(self.screen)

        # HUD
        sc=self.font.render(f"Time: {self.frames//60}s",True,(200,200,240))
        self.screen.blit(sc,(10,10))
        pts=self.small_font.render(f"Score: {self.score}",True,(200,200,240))
        self.screen.blit(pts,(10,40))
        mult=self.multiplier
        col=(255,220,90) if mult>1 else (160,160,200)
        mx=self.small_font.render(f"x{mult}",True,col)
        self.screen.blit(mx,(10,66))
        if self.started and not self.game_over:
            # progress bar toward next multiplier level
            frac=(self.streak%MULTIPLIER_STEP)/MULTIPLIER_STEP
            pygame.draw.rect(self.screen,(60,60,90),(50,72,90,10),border_radius=4)
            pygame.draw.rect(self.screen,col,(50,72,int(90*frac),10),border_radius=4)
        if self.ship.shield:
            sh=self.small_font.render("SHIELD",True,(140,240,255))
            self.screen.blit(sh,(WIDTH-sh.get_width()-10,10))

        if not self.started:
            msg=self.font.render("Press SPACE to launch",True,(180,180,240))
            self.screen.blit(msg,(WIDTH//2-msg.get_width()//2,HEIGHT//2))
            hint=self.small_font.render("WASD/Arrows: move   SPACE: fire laser",True,(140,140,200))
            self.screen.blit(hint,(WIDTH//2-hint.get_width()//2,HEIGHT//2+40))
        if self.game_over:
            ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
            ov.fill((0,0,0,150))
            self.screen.blit(ov,(0,0))
            m=self.big_font.render("DESTROYED!",True,(220,80,60))
            s=self.font.render(f"Survived {self.frames//60}s | Score {self.score}",True,(200,200,200))
            r=self.font.render("SPACE to Restart",True,(200,200,200))
            self.screen.blit(m,(WIDTH//2-m.get_width()//2,HEIGHT//2-60))
            self.screen.blit(s,(WIDTH//2-s.get_width()//2,HEIGHT//2))
            self.screen.blit(r,(WIDTH//2-r.get_width()//2,HEIGHT//2+40))
        pygame.display.flip()

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
