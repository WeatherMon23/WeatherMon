'''
Tutorial 14 example -- communicating with a web server
'''
from m5stack import *
from ALTconnection import *
from ALTwidgets import *
from ALTweb_server import *

## Creating the screen we want to display our content at ##
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xB6D0E2)

connect_wifi("TH", "thomas1234")
l = Label(x=120, y=100, text = 'Empty Label')
user_input = get_user_input(port=8082)

l.set_text(str(user_input))
print(user_input)
