import sys

import pygame

import entity
import camera
import gui
import map

import helper_func as hf
import game_object as go

from colors import Colors


pygame.init()

clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode((500, 500))

FPS = 60


def exit():
    pygame.quit()
    sys.exit()


class GameOver:
    def __init__(self):
        self.game_text = gui.Text("Game", 32, (220, 120))
        self.over_text = gui.Text("Over", 32, (220, 150))
        self.menu_button = gui.Button("Exit", (225, 210))
        self.square = pygame.Rect(150, 100, 200, 200)
        self.click = False

    def _input_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.click = True

    def _logic(self):
        mx, my = pygame.mouse.get_pos()
        if self.menu_button.rect.collidepoint(mx, my):
            if self.click:
                exit()

    def _draw(self, window):
        pygame.draw.rect(window, Colors.BLACK, self.square)
        self.game_text.draw(window)
        self.over_text.draw(window)
        self.menu_button.draw(window)

    def run(self):
        while True:
            clock.tick(FPS)

            self._input_handle()

            self._logic()

            self._draw(WINDOW)
            
            pygame.display.update()


class Game:
    def __init__(self):
        self.level = 1
        self.game = self._reload_level()

    def _reload_level(self):
        level_path = f"../level/level{self.level}.json"
        load = hf.load_json(level_path)
        border = [-400, 400]

        map_images_path = "../assets/tiles"
        map_parse = load["tilemap"]
        collide_parse = load["collide"]
        self.map = map.Map(map_parse, map_images_path, collide_parse, [border[0], -border[1]])

        self.camera = camera.Camera(border)

        puzzles_parse = load["puzzles"]
        self.puzzles = [go.Puzzles(puzzles_parse[puzzle]) for puzzle in puzzles_parse.keys()]

        hearths_parse = load["hearth"]
        self.hearths = [go.Hearth(hearths_parse[h]) for h in hearths_parse.keys()]

        portal_parse = load["portal"]
        self.portal = go.Portal(portal_parse)

        player_parse = load["player"]
        self.human = entity.Human(player_parse)

        orcs_parse = load["orcs"]
        self.orcs = [entity.Orc(orcs_parse[orc]) for orc in orcs_parse.keys()]
        
        self.collection = gui.Score(str(len(self.human.get_inventory())), len(puzzles_parse.keys()), 60, (10, 10))
        
        self.entitys = [self.human, *self.orcs]
        
        self.game_objects = [*self.hearths, *self.entitys, *self.puzzles]

    def _input_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYUP:
                self.human.idle()

        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_UP]:
            self.human.move(up=True)
        elif key_pressed[pygame.K_DOWN]:
            self.human.move(down=True)
        elif key_pressed[pygame.K_LEFT]:
            self.human.move(left=True)
        elif key_pressed[pygame.K_RIGHT]:
            self.human.move(right=True)
        elif key_pressed[pygame.K_SPACE]:
            for orc in self.orcs[:]:
                self.human.attack(orc)

        if key_pressed[pygame.K_z]:
            for h in self.hearths[:]:
                if self.human.pick_hearth(h):
                    self.hearths.remove(h)
                    self.game_objects.remove(h)
        
        if key_pressed[pygame.K_x]:
            for p in self.puzzles[:]:
                if self.human.pick_puzzle(p):
                    self.collection.set_score(str(len(self.human.get_inventory())))
                    self.puzzles.remove(p)
                    self.game_objects.remove(p)

    def _logic(self):
        if self.portal.entered(self.human):
            self.level += 1
            self._reload_level()

        if self.human.open_portal(self.collection.get_limit()):
            # so it will not appending multiple times
            if self.portal not in self.game_objects:
                self.game_objects.append(self.portal)

        for orc in self.orcs[:]:
            orc.move(self.human)
            orc.attack(self.human)

        for object in self.entitys[:]:
            object.collision(self.map.rects)
            if object.death():
                self.entitys.remove(object)
                self.game_objects.remove(object)

                if isinstance(object, entity.Human):
                    game_over = GameOver()
                    game_over.run()

                if isinstance(object, entity.Orc):
                    self.orcs.remove(object)

    def _update(self):
        self.camera.focus(self.human.get_position())

        # to get camera scrolling effect
        self.map.set_scroll(self.camera.get_scroll())

        for game_object in self.game_objects:
            game_object.set_scroll(self.camera.get_scroll())
            game_object.update()

    def _draw(self):
        WINDOW.fill(Colors.BLACK)

        self.map.draw(WINDOW)

        for game_object in self.game_objects:
            game_object.draw(WINDOW)
        
        self.collection.draw(WINDOW)

    def play(self):
        while True:
            clock.tick(FPS)

            self._input_handle()

            self._logic()

            self._update()

            self._draw()
                                    
            pygame.display.update()