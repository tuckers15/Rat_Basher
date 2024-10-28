import arcade
import constants
from player import Player
from pathlib import Path

class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Variables that will hold sprite lists
        self.player_list = None

        # Set up the player info
        self.player_sprite = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        #Adding moving camera
        self.camera = None

        #Tile mapping
        self.map = None

        

    def setup(self):
        """ Set up the game and initialize the variables. """

        #adding camera setup
        self.camera = arcade.Camera(self.width, self.height)

        # Get the path to the current script and navigate to map file location
        map_path = Path(__file__).resolve().parent.parent / "tiled_map" / "map.tmj"

        # Ensure the path is string-formatted for arcade to load
        map_name = str(map_path)

        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            "baseLayer": {
               
            },
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, constants.TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        

        # Sprite lists
        self.player_list = arcade.SpriteList()

        #Load a sprite sheet
        sprite_sheet = arcade.load_spritesheet("/Users/tucker/Documents/Rat_Basher/srcs/megaman-spritesheet.png", 
                                                sprite_width=32, 
                                                sprite_height=32,
                                                columns=4,
                                                count=4)

        # Create a sprite using one of the frames
        self.player_sprite = arcade.Sprite()
        self.player_sprite.texture = sprite_sheet[1]  

        self.player_sprite.center_x = constants.SCREEN_WIDTH/2
        self.player_sprite.center_y = constants.SCREEN_HEIGHT/2
        self.player_list.append(self.player_sprite)

        # --- Other stuff
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

    

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen
        self.clear()

        #camera 
        self.camera.use()

        self.scene.draw()

        # Draw all the sprites.
        self.player_list.draw()

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def update_player_speed(self):

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = constants.MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -constants.MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -constants.MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = constants.MOVEMENT_SPEED

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update to move the sprite
        # If using a physics engine, call update player to rely on physics engine
        # for movement, and call physics engine here.
        self.player_list.update()
        self.center_camera_to_player()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.W:
            self.up_pressed = True
            self.update_player_speed()
        elif key == arcade.key.S:
            self.down_pressed = True
            self.update_player_speed()
        elif key == arcade.key.A:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.D:
            self.right_pressed = True
            self.update_player_speed()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.W:
            self.up_pressed = False
            self.update_player_speed()
        elif key == arcade.key.S:
            self.down_pressed = False
            self.update_player_speed()
        elif key == arcade.key.A:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.D:
            self.right_pressed = False
            self.update_player_speed()
