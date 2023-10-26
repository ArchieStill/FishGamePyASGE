import pyasge
import random


class Fish:

    # replaced fishArray with fishDictionary
    fishDictionary = {
        1: "/data/images/kenney_fishpack/fishTile_073.png",
        2: "/data/images/kenney_fishpack/fishTile_075.png",
        3: "/data/images/kenney_fishpack/fishTile_077.png",
        4: "/data/images/kenney_fishpack/fishTile_079.png",
        5: "/data/images/kenney_fishpack/fishTile_081.png",
        6: "/data/images/kenney_fishpack/fishTile_100.png",
        7: "/data/images/kenney_fishpack/fishTile_102.png"
    }

    # calling game_res as part of init in Fish class - used for generating values in game
    def __init__(self, game_res):
        self.game_res = game_res
    # defining variables to use for Fish which are then used in main file
        self.score_modifier = 0

        self.current_velocity = 0

        self.sprite = pyasge.Sprite()

        self.eel_clicked = bool

        self.spawn()

    # defining values of fish
    def initFish(self, score, speed, texture, eelClicked):
        if self.sprite.loadTexture(self.fishDictionary[texture]):
            self.score_modifier = score
            self.current_velocity = speed
            self.sprite.z_order = 1
            self.sprite.scale = 1
            self.eel_clicked = eelClicked
        pass

    def spawn(self) -> None:
        # generates a random number between 1 and 100, the value decides the rarity of fish that spawns
        random_fish = random.randint(1, 100)
        if 0 <= random_fish <= 5:
            self.initFish(-5, 500, 6, False)   # Pufferfish: -5
        elif 6 <= random_fish <= 30:
            self.initFish(2, 300, 1, False)    # Green: +2
        elif 31 <= random_fish <= 50:
            self.initFish(3, 450, 3, False)    # Blue: +3
        elif 51 <= random_fish <= 60:
            self.initFish(4, 600, 5, False)    # Yellow: +4
        elif 61 <= random_fish <= 65:
            self.initFish(5, 800, 2, False)    # Pink: +5
        elif 66 <= random_fish <= 67:
            self.initFish(0, 1000, 7, True)    # Eel: +5 seconds
        else:
            self.initFish(1, 200, 4, False)    # Red: +1

        # fish always spawn on left side of screen, makes it more fair
        # generates random y coords but don't let the fish spawn on the edge
        self.sprite.x = 0 - self.sprite.width
        self.sprite.y = random.randint(0, self.game_res[1] - self.sprite.height)
        pass

    def update(self, game_time: pyasge.GameTime) -> None:
        # defining fish speed
        self.sprite.x += self.current_velocity * game_time.fixed_timestep
        if self.sprite.x >= self.game_res[0]:
            self.sprite.x = 0 - self.sprite.width
            return True
        return False


    def render(self, renderer: pyasge.Renderer):
        renderer.render(self.sprite)
