from . import animations

from . import health_bar as hb
from . import helper_func as hf
from .game_object import GameObject


class EntityState:
    IDLE = "IDLE"
    WALK = "WALK"
    ATTACK = "ATTACK"
    KNOCKBACK = "KNOCKBACK"
    COOLDOWN = "COOLDOWN"
    DIE = "DIE"

class Entity(GameObject):
    def __init__(self,
                 health, speed, position, power, strength,
                 idle_left, idle_right,
                 walk_left, walk_right,
                 attack_left, attack_right,
                 die):

        self.anim = animations.EntityAnimations()
        self.anim.load_animations("idle left", idle_left, 8)
        self.anim.load_animations("idle right", idle_right, 8)
        self.anim.load_animations("walk left", walk_left, 8)
        self.anim.load_animations("walk right", walk_right, 8)
        self.anim.load_animations("attack left", attack_left, 5)
        self.anim.load_animations("attack right", attack_right, 5)
        self.anim.load_animations("die", die, 8, False)

        # set state for the first time
        self.anim.set_state("idle right")

        super().__init__(self.anim.animations_db[self.anim.state][0], position)

        self.speed = speed
        self.power = power
        self.strength = strength
        self.state = EntityState.IDLE
        self.health_bar = hb.HealthBar(health, (self.rect.x, self.rect.y))
    
    def collision(self, rects):
        for x in range(len(rects)):
            if self.rect.colliderect(rects[x]):
                if self.movement[0] > 0 and self.rect.x < rects[x].x:
                    self.rect.right = rects[x].left
                elif self.movement[0] < 0 and self.rect.x > rects[x].x:
                    self.rect.left = rects[x].right
                elif self.movement[1] > 0 and self.rect.y < rects[x].y:
                    self.rect.bottom = rects[x].top
                elif self.movement[1] < 0 and self.rect.y > rects[x].y:
                    self.rect.top = rects[x].bottom
        
    def idle(self):
        self.anim.idle_change_state()

        self.set_state(EntityState.IDLE)

    def is_currently(self, state):
        return self.state == state

    def set_state(self, state):
        if (self.state != state):
            self.state = state

    # TODO: Create Move Method

    # TODO: Create Attack Method
                
    def death(self):
        if self.health_bar.get_health() <= 0:
            self.anim.die_change_state()
            self.set_state(EntityState.DIE)
            self.speed = 0

            if self.anim.end_frame():
                return True

        return False
    
    def update(self):
        self.position = (self.rect.x - self.scroll[0], self.rect.y - self.scroll[1])

        self.health_bar.update(self.position)

    def draw(self, screen):
        self.health_bar.draw(screen)

        self.anim.play(screen, self.position)


class Human(Entity):
    def __init__(self, position):
        super().__init__(100, 2, position, 2, 15,
                        "assets/human/idle/left",
                        "assets/human/idle/right",
                        "assets/human/walk/left",
                        "assets/human/walk/right",
                        "assets/human/attack/left",
                        "assets/human/attack/right",
                        "assets/human/die")
        self.inventory = []

    # (1) refactor
    def increase_health(self, hearth):
        # so that the addition of health does not exceed the bar limit
        if self.health_bar.get_health() >= (self.health_bar.get_bar_width() - hearth.health):
            health = self.health_bar.red_bar.width - self.health_bar.get_health()
        else:
            health = hearth.health

        self.health_bar.increase(health)
    
    def pick_hearth(self, hearth):
        limit = 50
        
        if hf.get_distance(self.rect, hearth.rect) <= limit:
            if self.health_bar.get_health() != self.health_bar.get_bar_width():
                self.increase_health(hearth)
                
                return True
            else:
                return False
    
    def pick_puzzle(self, puzzle):
        limit = 13

        if hf.get_distance(self.rect, puzzle.rect) <= limit:
            if puzzle.collected():
                self.inventory.append(puzzle)
                return True
        
        return False
    
    def open_portal(self, limit):
        if len(self.get_inventory()) == limit:
            return True
        
    def move(self, up=False, down=False, right=False, left=False):
        self.movement = [0, 0]

        if up:
            self.anim.walk_change_state()
            self.set_state(EntityState.WALK)
            self.movement[1] = -self.speed
        elif down:
            self.anim.walk_change_state()
            self.set_state(EntityState.WALK)
            self.movement[1] = self.speed
        elif right:
            self.anim.set_state("walk right")
            self.set_state(EntityState.WALK)
            self.movement[0] = self.speed
        elif left:
            self.anim.set_state("walk left")
            self.set_state(EntityState.WALK)
            self.movement[0] = -self.speed
        
        self.rect.x += self.movement[0]
        self.rect.y += self.movement[1]

    def attack(self, orc):
        limit = 30
        self.anim.attack_change_state()
        self.set_state(EntityState.ATTACK)

        if hf.get_distance(self.rect, orc.rect) <= limit:
            orc.health_bar.decrease(self.power)
            orc.knockback(self, self.strength)
    
    def get_inventory(self):
        return self.inventory

    def get_position(self):
        return (self.rect.x, self.rect.y)

    
class Orc(Entity):
    def __init__(self, position):
        super().__init__(50, 1, position, 1, 7,
                        "assets/orc/idle/left",
                        "assets/orc/idle/right",
                        "assets/orc/walk/left",
                        "assets/orc/walk/right",
                        "assets/orc/attack/left",
                        "assets/orc/attack/right",
                        "assets/orc/die")
        
        self.cooldown = 100
        self.cooldown_timer = 0
        self.is_knockback = False
    
    def move(self, human):
        self.movement = [0, 0]

        limit = 130

        if hf.get_distance(self.rect, human.rect) < limit and not self.is_cooldown():
            if self.rect.y > human.rect.y:
                self.anim.walk_change_state()
                self.set_state(EntityState.WALK)
                self.movement[1] = -self.speed
            if self.rect.y < human.rect.y:
                self.anim.walk_change_state()
                self.set_state(EntityState.WALK)
                self.movement[1] = self.speed
            if self.rect.x > human.rect.x:
                self.anim.set_state("walk left")
                self.set_state(EntityState.WALK)
                self.movement[0] = -self.speed
            if self.rect.x < human.rect.x:
                self.anim.set_state("walk right")
                self.set_state(EntityState.WALK)
                self.movement[0] = self.speed
        else:
            self.idle()
        
        self.rect.x += self.movement[0]
        self.rect.y += self.movement[1]
    
    def attack(self, player):
        limit = 25

        if (hf.get_distance(self.rect, player.rect) <= limit) and self.is_currently(EntityState.WALK):
            if (not player.is_currently(EntityState.DIE)):
                self.anim.attack_change_state()
                self.set_state(EntityState.ATTACK)

                player.health_bar.decrease(self.power)
            else:
                self.anim.idle_change_state()
            
            self.speed = 0
        else:
            self.speed = 1

    def knockback(self, source, strength):
        dx = self.rect.x - source.rect.x
        dy = self.rect.y - source.rect.y
        distance = max((dx ** 2 + dy ** 2) ** 0.5, 1)

        self.rect.x += int(strength * dx / distance)
        self.rect.y += int(strength * dy / distance)

        self.cooldown_timer = self.cooldown
        self.set_state(EntityState.KNOCKBACK)

    def is_cooldown(self):
        if ((self.is_currently(EntityState.KNOCKBACK) or self.is_currently(EntityState.COOLDOWN)) and self.cooldown_timer > 0):
            return True 
        
        return False
    
    def update_cooldown(self):
        if (self.cooldown_timer > 0):
            self.cooldown_timer -= 1

            self.set_state(EntityState.COOLDOWN)
        else:
            if (self.is_currently(EntityState.KNOCKBACK)):
                self.set_state(EntityState.IDLE)

    def spawn_area(self):
        return self.rect.x == 50

    def lost_area(self):
        return (self.rect.x <= -50 or self.rect.x > 1000)
    
    def update(self):
        self.update_cooldown()

        super().update()


