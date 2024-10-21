import arcade, time, colorama
from pyglet.image import load as pyglet_load
from colorama import Fore, Back, Style
from mazelib import Maze
from mazelib.solve.BacktrackingSolver import BacktrackingSolver
from mazelib.generate.HuntAndKill import HuntAndKill

colorama.init(autoreset=True)
print(Fore.YELLOW + "STARTING...")
# --- Constants ---
SPRITE_SCALING_WALL = 2
SPRITE_SCALING_PLAYER = 1.2
SPRITE_SIZE = 16
SCALED_SPRITE_SIZE_WALL = SPRITE_SIZE * SPRITE_SCALING_WALL
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 608
SCREEN_TITLE = "maze speedrun"

MOVEMENT_SPEED = 5
FADE_RATE = 5

total_time = 0.0
fastest_possible_time = 0.0
time_score = 0.0

# enable fps getting
arcade.enable_timings(max_history=100)

class FadingView(arcade.View):
    def __init__(self):
        super().__init__()
        self.fade_out = None
        self.fade_in = 255

    def update_fade(self, next_view=None):
        if self.fade_out is not None:
            self.fade_out += FADE_RATE
            if self.fade_out is not None and self.fade_out > 255 and next_view is not None:
                game_view = next_view()
                try:
                    game_view.setup()
                except:
                    AttributeError
                self.window.show_view(game_view)

        if self.fade_in is not None:
            self.fade_in -= FADE_RATE
            if self.fade_in <= 0:
                self.fade_in = None

    def draw_fading(self):
        if self.fade_out is not None:
            arcade.draw_rectangle_filled(self.window.width / 2, self.window.height / 2,
                                         self.window.width, self.window.height,
                                         (0, 0, 0, self.fade_out))

        if self.fade_in is not None:
            arcade.draw_rectangle_filled(self.window.width / 2, self.window.height / 2,
                                         self.window.width, self.window.height,
                                         (0, 0, 0, self.fade_in))
            

class InstructionView(FadingView):
    def on_update(self, dt):
        self.update_fade(next_view=GameView)
        
        
    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color((15, 23, 38))
        self.text_effect = 0
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        print(Fore.GREEN + "LOADED Instruction View ✅")
    def on_draw(self):
        """ Draw this view """
        self.clear()

        arcade.draw_text("INSTRUCTIONS", 
                         self.window.width / 2, self.window.height * (3 / 4),
                         width=self.window.width * 0.9,
                         color=(255, 160, 122), font_size=32, anchor_x="center",
                         multiline=False,
                         font_name="Kenney Blocks")
        arcade.draw_text("1.  You will spawn in a maze.  Your goal is to navigate the maze and get to the orange tile in the fastest time", 
                         self.window.width / 2, self.window.height * (65 / 100),
                         color=(245, 249, 239),
                         font_name="Kenney Pixel",
                         width=self.window.width * 0.8,
                         multiline=True,
                         font_size=24, anchor_x="center",
                         )
        arcade.draw_text("2.  Move around the maze using WASD", 
                         self.window.width / 2, self.window.height * (53 / 100),
                         color=(245, 249, 239),
                         font_name="Kenney Pixel",
                         width=self.window.width * 0.8,
                         multiline=True,
                         font_size=24, anchor_x="center",
                         )
        arcade.draw_text("3.  Sometimes the corners of the walls will be a little 'sticky'.  Make your movement precise to avoid getting stuck.", 
                         self.window.width / 2, self.window.height * (45 / 100),
                         color=(245, 249, 239),
                         font_name="Kenney Pixel",
                         width=self.window.width * 0.8,
                         multiline=True,
                         font_size=24, anchor_x="center",
                         )
        arcade.draw_text("4.  During the game, you can press 'L' to restart.", 
                         self.window.width / 2, self.window.height * (35 / 100),
                         color=(245, 249, 239),
                         font_name="Kenney Pixel",
                         width=self.window.width * 0.8,
                         multiline=True,
                         font_size=24, anchor_x="center",
                         )
        arcade.draw_text("Press the Enter key to continue.", 
                         self.window.width / 2, self.window.height * (20 / 100),
                         color=(245, 249, 239),
                         font_name="Kenney Pixel",
                         width=self.window.width * 0.8,
                         multiline=True,
                         font_size=24, anchor_x="center",
                         )
        self.draw_fading()

    def on_key_press(self, key, modifiers):
        if self.fade_out is None and key == arcade.key.ENTER:
            self.fade_out = 0
    
class GameOverView(FadingView):
    """ View to show when game is over """

    def on_update(self, dt):
        self.update_fade(next_view=InstructionView)

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color((15, 23, 38))
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
        print(Fore.GREEN + "LOADED Game Over View ✅")

    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("END SCREEN", 
                         self.window.width / 2, self.window.height * (3 / 4),
                         width=self.window.width * 0.9,
                         color=(255, 160, 122), font_size=32, anchor_x="center",
                         multiline=False,
                         font_name="Kenney Blocks")
        arcade.draw_text(f"Your time is: {total_time}", 
                         self.window.width / 2, self.window.height * (66 / 100),
                         color=(245, 249, 239),
                         font_name="Kenney Pixel",
                         width=self.window.width * 0.8,
                         multiline=True,
                         font_size=24, anchor_x="center",
                         )
        arcade.draw_text(f"Fastest possible time is: {fastest_possible_time}", 
                         self.window.width / 2, self.window.height * (60 / 100),
                         color=(245, 249, 239),
                         font_name="Kenney Pixel",
                         width=self.window.width * 0.8,
                         multiline=True,
                         font_size=24, anchor_x="center",
                         )
        arcade.draw_text(f"Time Score: {time_score}%", 
                         self.window.width / 2, self.window.height * (53 / 100),
                         color=(245, 249, 239),
                         font_name="Kenney Pixel",
                         width=self.window.width * 0.8,
                         multiline=True,
                         font_size=24, anchor_x="center",
                         )
        arcade.draw_text(f"Press R to restart, press I to go to Instructions", 
                         self.window.width / 2, self.window.height * (45 / 100),
                         color=(245, 249, 239),
                         font_name="Kenney Pixel",
                         width=self.window.width * 0.8,
                         multiline=True,
                         font_size=24, anchor_x="center",
                         )
        self.draw_fading()
        
    def on_key_press(self, key, modifiers): 
        if key == arcade.key.I:
            self.fade_out = 0
        if key == arcade.key.R:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

class GameView(FadingView):
    """ This class represents the main window of the game. """
    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()

        # Sprite lists
        self.player_list = None
        self.wall_list = None
        self.start_sprite_list = None
        self.end_sprite_list = None

        # Set up the player
        self.player_sprite = None
        self.start_sprite = None
        self.end_sprite = None

        # Physics engine
        self.physics_engine = None

        # Time variables
        self.start_time = None
        self.end_time = None
        
        # Restart variable
        self.restart = False

        # Maze variables
        self.maze_col = 12
        self.maze_row = 9
        print(Fore.BLUE + f"Generating maze with {self.maze_col} columns and {self.maze_row} rows...")

        m = Maze()
        m.generator = HuntAndKill(self.maze_row, self.maze_col)
        m.solver = BacktrackingSolver()
        
        m.generate_monte_carlo(100, 30, 1.0)
        m.generate_entrances(start_outer=False, end_outer=False)
        m.solve()
        maze_sol = str(m.solve)
        self.len_maze_sol = maze_sol.count('+')

        print(Fore.BLUE + f"Maze Generation Complete. Solution Length: {Fore.YELLOW} {self.len_maze_sol}")    
        px_count_maze_sol = self.len_maze_sol * (SPRITE_SIZE * SPRITE_SCALING_WALL)
        self.frames_needed = px_count_maze_sol / MOVEMENT_SPEED
        
        self.m = m
        self.started = True


    def on_show_view(self):
        # Set the background color
        arcade.set_background_color((30, 20, 10))
        print(Fore.GREEN + "LOADED Game View ✅")
        
    def setup(self):
        # Timer
        self.total_time = 0.0
        
        # Precise timer started variables
        self.timer_started = False
        self.timer_ended = False

        
        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.start_sprite_list = arcade.SpriteList()
        self.end_sprite_list = arcade.SpriteList()
        
        # Add sprites in accordance to maze layout and scaled for screen
        maze_list = list(self.m.grid.tolist())
        for y in range(0, len(maze_list)):
            for x in range(0, len(maze_list[y])):
                if maze_list[y][x] == 1:
                    wall = arcade.Sprite("assets/textures/walltexture.png", SPRITE_SCALING_WALL)
                    wall.center_y = y * SCALED_SPRITE_SIZE_WALL + (SCALED_SPRITE_SIZE_WALL // 2)
                    wall.center_x = x * SCALED_SPRITE_SIZE_WALL + (SCALED_SPRITE_SIZE_WALL // 2)
                    self.wall_list.append(wall)

        # Create starting tile sprite
        start_coords = self.m.start
        self.start_sprite = arcade.Sprite("assets/textures/start.png", SPRITE_SCALING_WALL)
        self.start_sprite.center_y = start_coords[0] * SCALED_SPRITE_SIZE_WALL + (SCALED_SPRITE_SIZE_WALL // 2)
        self.start_sprite.center_x = start_coords[1] * SCALED_SPRITE_SIZE_WALL + (SCALED_SPRITE_SIZE_WALL // 2)
        self.start_sprite_list.append(self.start_sprite)

        # Create ending tile sprite
        end_coords = self.m.end
        self.end_sprite = arcade.Sprite("assets/textures/end.png", SPRITE_SCALING_WALL)
        self.end_sprite.center_y = end_coords[0] * SCALED_SPRITE_SIZE_WALL + (SCALED_SPRITE_SIZE_WALL // 2)
        self.end_sprite.center_x = end_coords[1] * SCALED_SPRITE_SIZE_WALL + (SCALED_SPRITE_SIZE_WALL // 2)
        self.end_sprite_list.append(self.end_sprite)

        # Create the player
        self.player_sprite = arcade.Sprite("assets/textures/playerdesign.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_y = self.start_sprite.center_y
        self.player_sprite.center_x = self.start_sprite.center_x
        self.player_list.append(self.player_sprite)

        # Create the physics engine. Give it a reference to the player, and
        # the walls we can't run into.
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)


    def on_draw(self):
        self.clear()
        arcade.start_render()
        self.wall_list.draw()
        self.start_sprite_list.draw()
        self.end_sprite_list.draw()
        self.player_list.draw()
        
        
        # Draw the timer text. 
        output = self.total_time
        arcade.draw_text(output, SCREEN_WIDTH * 0.05, SCREEN_HEIGHT * 0.91, arcade.color.WHITE, 32, font_name="Kenney Mini Square")
        self.draw_fading()
        

    def on_update(self, delta_time):
        global total_time
        global fastest_possible_time
        global time_score
        self.update_fade(next_view=GameOverView)
        if self.restart == True:
            self.update_fade(next_view=GameView)

        # goofy ahh code
        if self.timer_started and not self.timer_ended:
            self.total_time = round(time.time() - self.start_time, 3)
            for player in self.player_list:
                if len(arcade.check_for_collision_with_list(self.player_sprite, self.end_sprite_list)) > 0:
                    print(Fore.YELLOW + "Run Complete.")
                    self.end_time = time.time()
                    
                    print(f"---- {Back.BLUE}{Fore.WHITE}STATS{Style.RESET_ALL} ----")
                    print(f"{Fore.CYAN} Your time is: {Fore.YELLOW}{self.total_time}")
                    total_time = self.total_time
                    fps = arcade.get_fps(100)

                    # Fuck over potato pcs and lucky people
                    if self.len_maze_sol < 5 or fps < 40:
                        self.fastest_possible_time = round(self.frames_needed / 60, 3)
                    else:
                        self.fastest_possible_time = round(self.frames_needed / fps, 3)
                    print(f"{Fore.CYAN} Fastest possible time: {Fore.GREEN}{self.fastest_possible_time}")
                    fastest_possible_time = self.fastest_possible_time
                    self.time_score = round(fastest_possible_time / total_time * 100, 1)
                    time_score = self.time_score
                    self.timer_ended = True
                    
        if self.timer_started and self.timer_ended:
            if self.fade_out is None:
                time.sleep(0.2)
                self.fade_out = 0
            # game_over_view = GameOverView()
            # # game_over_view.setup()
            # self.window.show_view(game_over_view)     
        self.physics_engine.update()
        
        

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key in [arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D]:
            if not self.timer_started:
                self.timer_started = True
                self.start_time = time.time()
                print(Fore.YELLOW + f"Timer Started! ⏱️")
        if key == arcade.key.L:
            self.restart = True
            self.fade_out = 0
        
        if key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED 
        elif key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED 
        elif key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED 
        elif key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED
        
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0


def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.set_icon(pyglet_load("assets/images/game_icon.png"))
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()
    print(Fore.RED + "EXITING...")


if __name__ == "__main__":
    main()
