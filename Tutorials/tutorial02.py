'''
Tutorial 1 example -- creating a board and drawing widgets inside it 
'''
from ALTwidgets import *

## Creating the screen we want to display our content at ##
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xB6D0E2)

## Creating a Board and Widgets on it ##
board = Board(top_margin=51, block_size=58, split_size=5, rows_num=3, cols_num=5, show_place_holders=True)

## Drawing empty widgets on the board - each with a different color
widget1 = board.draw_widget(2, 2, 0, 0, 0x0818A8)
widget2 = board.draw_widget(2, 1, 0, 2, 0x4682B4)
widget3 = board.draw_widget(1, 3, 2, 0, 0x191970)
widget4 = board.draw_widget(2, 2, 0, 3, 0x0F52BA)
widget5 = board.draw_widget(1, 2, 2, 3, 0x088F8F)
