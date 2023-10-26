import random
import pyasge
from gamedata import GameData
from fish import Fish

def isInside(sprite, mouse_x, mouse_y) -> bool:
    # grabs the sprite's bounding box with 4 vertices
    bounds = sprite.getWorldBounds()
    # assigns the bounds of the screen

    # checks to see if the mouse position is within the x and y bounds
    if bounds.v1.x < mouse_x < bounds.v2.x and bounds.v1.y < mouse_y < bounds.v3.y:
        return True
    pass


class MyASGEGame(pyasge.ASGEGame):
    """
    The main game class
    """

    def __init__(self, settings: pyasge.GameSettings):
        """
        Initialises the game and sets up the shared data.

        Args:
            settings (pyasge.GameSettings): The game settings
        """
        pyasge.ASGEGame.__init__(self, settings)

        # create a game data object, we can store all shared game content here

        self.difficulty_level = None
        self.data = GameData()
        self.data.inputs = self.inputs
        self.data.renderer = self.renderer
        self.data.game_res = [settings.window_width, settings.window_height]

        self.renderer.setClearColour(pyasge.COLOURS.MEDIUMAQUAMARINE)
        self.data.fonts["MainFont"] = self.data.renderer.loadFont("/data/fonts/KGHAPPY.ttf", 64)

        # register the key and mouse click handlers for this class
        self.key_id = self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.keyHandler)
        self.mouse_id = self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.clickHandler)

        # set the game to the menu
        self.game_state = 0
        self.play_option = None
        self.exit_option = None
        self.menu_option = 0

        self.data.background = pyasge.Sprite()
        self.initBackground()

        self.menu_text = None
        self.initMenu()

        self.scoreboard = None
        self.initScoreboard()

        self.game_over_text = None
        self.game_over_exit = None
        self.game_over_score = None
        self.initGameOver()

        self.next_level_text = None
        self.next_level_exit = None
        self.initNextLevel()

        self.timer_display = None
        self.timer = 0
        self.time_limit = 21
        self.initTimer()

        self.difficulty_level = 1
        self.goal_score = self.difficulty_level * 10

        # change number of fish on screen (set to 10 at a time)
        self.class_fish_list = [] # square brackets used in lists!!!!!!
        # adds instance of Fish class to class_fish_list
        for i in range(10):
            self.class_fish_list.append(Fish(self.data.game_res))

        self.level_display = None
        self.target_display = None
        self.initGameDisplay()

    def initBackground(self) -> bool:
        if self.data.background.loadTexture("/data/images/background.png"):
            # loaded, so make sure this gets rendered first
            self.data.background.z_order = -100
            return True
        else:
            return False

    # initFish was here

    # spawn was here

    def initMenu(self) -> bool:
        self.menu_text = pyasge.Text(self.data.fonts["MainFont"])
        self.menu_text.string = "Funny Fish Gamma"
        self.menu_text.position = [100, 100]
        self.menu_text.colour = pyasge.COLOURS.RED

        self.play_option = pyasge.Text(self.data.fonts["MainFont"])
        self.play_option.string = ">START"
        self.play_option.position = [100, 400]
        self.play_option.colour = pyasge.COLOURS.HOTPINK

        self.exit_option = pyasge.Text(self.data.fonts["MainFont"])
        self.exit_option.string = "EXIT"
        self.exit_option.position = [500, 400]
        self.exit_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY

        return True

    def initScoreboard(self) -> None:
        self.scoreboard = pyasge.Text(self.data.fonts["MainFont"])
        self.scoreboard.string = str(self.data.score).zfill(3)
        self.scoreboard.scale = 1.25
        self.scoreboard.position = [1350, 100]
        self.scoreboard.colour = pyasge.COLOURS.GREEN

    def initGameOver(self):
        # GOS text
        self.game_over_text = pyasge.Text(self.data.fonts["MainFont"])
        self.game_over_text.string = "GAME OVER!"
        self.game_over_text.scale = 1.5
        self.game_over_text.position = [250, 250]
        self.game_over_text.colour = pyasge.COLOURS.BLACK
        # GOS exit
        self.game_over_exit = pyasge.Text(self.data.fonts["MainFont"])
        self.game_over_exit.string = "Press Enter to return to the main menu"
        self.game_over_exit.scale = 0.75
        self.game_over_exit.position = [350, 700]
        self.game_over_exit.colour = pyasge.COLOURS.LIGHTSLATEGRAY
        # GOS score
        self.game_over_score = pyasge.Text(self.data.fonts["MainFont"])
        self.game_over_score.string = "Final score: " + str(self.data.score)
        self.game_over_score.position = [550, 550]
        self.game_over_score.colour = pyasge.COLOURS.BLACK
        # GOS text and GOS score rendered in render function!!!!!!!!

    def initGameDisplay(self):
        # level number
        self.level_display = pyasge.Text(self.data.fonts["MainFont"])
        self.level_display.string = str("Level " + str(self.difficulty_level))
        self.level_display.scale = 1
        self.level_display.position = [50, 75]
        self.level_display.colour = pyasge.COLOURS.NAVY
        # next level exit
        self.target_display = pyasge.Text(self.data.fonts["MainFont"])
        self.target_display.string = str("Target: " + str(self.goal_score))
        self.target_display.scale = 1
        self.target_display.position = [50, 150]
        self.target_display.colour = pyasge.COLOURS.NAVY

    def initNextLevel(self):
        # next level text
        self.next_level_text = pyasge.Text(self.data.fonts["MainFont"])
        self.next_level_text.string = "You win!"
        self.next_level_text.scale = 1.5
        self.next_level_text.position = [400, 250]
        self.next_level_text.colour = pyasge.COLOURS.BLACK
        # next level exit
        self.next_level_exit = pyasge.Text(self.data.fonts["MainFont"])
        self.next_level_exit.string = "Press Enter to go to the next level!"
        self.next_level_exit.scale = 0.75
        self.next_level_exit.position = [400, 700]
        self.next_level_exit.colour = pyasge.COLOURS.BLACK

    def initTimer(self) -> None:
        self.timer_display = pyasge.Text(self.data.fonts["MainFont"])
        self.timer_display.string = str(self.timer)
        self.timer_display.scale = 1.75
        self.timer_display.position = [700, 200]

    def clickHandler(self, event: pyasge.ClickEvent) -> None:
        # checks if M1 is pressed
        if event.action == pyasge.MOUSE.BUTTON_PRESSED and \
                event.button == pyasge.MOUSE.MOUSE_BTN1:
            # checks if mouse is in bounding box
            for fish in self.class_fish_list:
                if isInside(fish.sprite, event.x, event.y):
                    self.data.score += fish.score_modifier
                    self.scoreboard.string = str(self.data.score).zfill(3)
                    if fish.eel_clicked == True:
                        self.timer -= 5
                    fish.spawn()
        pass

    def keyHandler(self, event: pyasge.KeyEvent) -> None:
        if event.action == pyasge.KEYS.KEY_PRESSED:
            if event.key == pyasge.KEYS.KEY_RIGHT or event.key == pyasge.KEYS.KEY_LEFT:
                self.menu_option = 1 - self.menu_option
                if self.menu_option == 0:
                    self.play_option.string = ">START"
                    self.play_option.colour = pyasge.COLOURS.HOTPINK
                    self.exit_option.string = "EXIT"
                    self.exit_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                else:
                    self.play_option.string = "START"
                    self.play_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                    self.exit_option.string = ">EXIT"
                    self.exit_option.colour = pyasge.COLOURS.HOTPINK

            if event.key == pyasge.KEYS.KEY_0:
                self.spawn(self.fish_list[0])

            if event.key == pyasge.KEYS.KEY_ENTER:
                if self.exit_option.string == ">EXIT":
                    self.signalExit()
                elif self.game_state == 0:
                    self.game_state = 1
                elif self.game_state == 2:
                    self.game_state = 0
                    self.data.score = 0
                    self.scoreboard.string = str(self.data.score).zfill(3)
                    self.timer = 0
                elif self.game_state == 3:
                    self.difficulty_level += 1
                    self.goal_score = self.difficulty_level * 10
                    self.game_state = 1
                    self.data.score = 0
                    self.timer = 0
                    self.level_display.string = str("Level " + str(self.difficulty_level))
                    self.target_display.string = str("Target: " + str(self.goal_score))
                    self.scoreboard.string = str(self.data.score).zfill(3)
                    for fish in self.class_fish_list:
                        fish.spawn()
        pass

    def update(self, game_time: pyasge.GameTime) -> None:

        # update the menu here
        if self.game_state == 0:
            self.difficulty_level = 1
            self.goal_score = self.difficulty_level * 10
            self.level_display.string = str("Level " + str(self.difficulty_level))
            self.target_display.string = str("Target: " + str(self.goal_score))

        elif self.game_state == 1:
            # timer changing colour as it decreases
            if 15 < self.timer <= 99:
                self.timer_display.colour = pyasge.COLOURS.RED
            if 10 < self.timer <= 15:
                self.timer_display.colour = pyasge.COLOURS.ORANGE
            if 5 < self.timer <= 10:
                self.timer_display.colour = pyasge.COLOURS.YELLOW
            if 0 < self.timer <= 5:
                self.timer_display.colour = pyasge.COLOURS.WHITE

            # taking away points equal to fish value by calling Fish
            for fish in self.class_fish_list:
                off_screen = fish.update(game_time)
                if off_screen == True:
                    self.data.score -= fish.score_modifier
                    # can't get negative score
                    if self.data.score < 0:
                        self.data.score = 0
                    self.scoreboard.string = str(self.data.score).zfill(3)

            if self.timer >= self.time_limit:
                self.game_state = 2
            if self.data.score >= self.goal_score:
                self.game_state = 3
            pass
        elif self.game_state == 2:
            self.game_over_score.string = "Final score: " + str(self.data.score)
        else:
            self.time_limit = 21
            pass

    def render(self, game_time: pyasge.GameTime) -> None:
        """
        This is the variable time-step function. Use to update
        animations and to render the gam    e-world. The use of
        ``frame_time`` is essential to ensure consistent performance.
        @param game_time: The tick and frame deltas.
        """

        if self.game_state == 0:
            # render the menu here
            self.data.renderer.render(self.data.background)
            self.data.renderer.render(self.menu_text)
            self.data.renderer.render(self.play_option)
            self.data.renderer.render(self.exit_option)
        elif self.game_state == 1:
            # render the game here
            self.data.renderer.render(self.data.background)
            self.data.renderer.render(self.scoreboard)
            self.data.renderer.render(self.timer_display)
            self.data.renderer.render(self.level_display)
            self.data.renderer.render(self.target_display)
            self.timer_display.string = str(int(self.time_limit - self.timer))
            self.timer += game_time.frame_time

            # console printing timer - used for testing time limit and game over screen:
            #           if self.timer >= self.time_limit:
            #               print("TIME UP")

            for fish in self.class_fish_list:
                fish.render(self.data.renderer)
        elif self.game_state == 2:
            self.data.renderer.render(self.game_over_text)
            self.data.renderer.render(self.game_over_exit)
            self.data.renderer.render(self.game_over_score)
        else:
            self.data.renderer.render(self.next_level_text)
            self.data.renderer.render(self.next_level_exit)

def main():
    """
    Creates the game and runs it
    For ASGE Games to run they need settings. These settings
    allow changes to the way the game is presented, its
    simulation speed and also its dimensions. For this project
    the FPS and fixed updates are capped at 60hz and Vsync is
    set to adaptive.
    """
    settings = pyasge.GameSettings()
    settings.window_width = 1600
    settings.window_height = 900
    settings.fixed_ts = 60
    settings.fps_limit = 60
    settings.window_mode = pyasge.WindowMode.BORDERLESS_WINDOW
    settings.vsync = pyasge.Vsync.ADAPTIVE
    game = MyASGEGame(settings)
    game.run()


if __name__ == "__main__":
    main()
