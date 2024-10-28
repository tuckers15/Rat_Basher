"""
Better Move Sprite With Keyboard

Simple program to show moving a sprite with the keyboard.
This is slightly better than sprite_move_keyboard.py example
in how it works, but also slightly more complex.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_move_keyboard_better
"""
import arcade
import constants
from windows import GameView


def main():
    """ Main function """
    window = GameView(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants. SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()