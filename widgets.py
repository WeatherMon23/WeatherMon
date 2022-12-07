from m5stack import *
from m5stack_ui import *
from uiflow import *
import lvgl as lv

# We encapsulated the M5Btn class since it doesn't have getters for its internal variables
class M5Fadingbtn():
  def _btn_pressed(self): 
    self.btn.set_pos(10, 70)
    self.btn.set_size(300, 100)
    self.btn.set_btn_text(self.text)
    self.btn.set_bg_color(self.bg_c)
    self.btn.set_btn_text_color(self.text_c)
    self.btn.set_btn_text_font(FONT_MONT_34)
  pass

  def _btn_released(self):
    self.btn.set_pos(self.x, self.y)
    self.btn.set_size(self.w, self.h)
    self.btn.set_btn_text(self.text)
    self.btn.set_bg_color(self.bg_c)
    self.btn.set_btn_text_color(self.text_c)
    self.btn.set_btn_text_font(FONT_MONT_14)
  pass

  def __init__(self, text, x=0, y=0, w=70, h=30, bg_c=0xFFFFFF, text_c=0x000000, parent = None):
    self.w = w
    self.h = h
    self.x = x
    self.y = y
    self.bg_c = bg_c
    self.text_c = text_c
    self.text = text
    self.btn = M5Btn(text, x, y, w, h, bg_c, text_c, FONT_MONT_14, parent)
    self.btn.pressed(self._btn_pressed)
    self.btn.released(self._btn_released)
    
  def set_btn_text(self, text):
      self.text = text
      self.btn.set_btn_text(text)
      
    
class Title():
    def __init__(self, text = '', text_c = 0xFFFFFF, bg_c=0x000000):
        self.text_c = text_c
        self.line = M5Line(x1=0, y1=12, x2=320, y2=12, color=bg_c, width=26, parent=None)
        self.left_label = M5Label(text, x=6, y=5, color=text_c, font=FONT_MONT_14, parent=None)
        self.battery_label = None
        self.icon1 = None
        self.icon2 = None
        
    def clear_title(self):
        if self.icon1:
            self.icon1.delete()
            self.icon1 = None
        if self.icon2:
            self.icon2.delete()
            self.icon2 = None
        if self.battery_label:
            self.battery_label.delete()
            self.battery_label = None
    
    def delete(self):
        if self.icon1: 
            self.icon1.delete()
        if self.icon2:
            self.icon2.delete()
        if self.battery_label:
            self.battery_label.delete()
        if self.line:
            self.line.delete()
        if self.left_label:
            self.left_label.delete()
        
    def set_text(self, text):
        self.left_label.set_text(text)
        
    def show_battery(self):
        per = int((power.getBatVoltage() - 3.2)*100)
        if 80 <= per <= 100:
            bat_sym = lv.SYMBOL.BATTERY_FULL
        elif 50 <= per < 80:
            bat_sym = lv.SYMBOL.BATTERY_3
        elif 20 <= per < 50:
            bat_sym = lv.SYMBOL.BATTERY_2
        elif 5 <= per < 20:
            bat_sym = lv.SYMBOL.BATTERY_1
        else:
            bat_sym = lv.SYMBOL.BATTERY_EMPTY
            
        per_str = str(per) + str('% ') + bat_sym
        self.battery_label = M5Label(per_str, x=265, y=5, color=self.text_c, font=FONT_MONT_14, parent=None)
        
    def remove_battery(self):
        self.battery_label.delete()
        self.battery_label = None
        
    def show_green_wifi(self):
        if self.icon1 is None:
            self.icon1 = M5Img("img/wifi_green.png", x=255, y=0, parent=None)
        else:
            self.icon1.set_img_src("img/wifi_green.png")
            
    def show_red_wifi(self):
        if self.icon1 is None:
            self.icon1 = M5Img("img/wifi_red.png", x=255, y=0, parent=None)
        else:
            self.icon1.set_img_src("img/wifi_red.png")
            
    def remove_wifi(self):
        self.icon1.delete()
        self.icon1 = None

    def show_green_cloud(self):
        if self.icon2 is None:
            self.icon2 = M5Img("img/cloud_green.png", x=225, y=0, parent=None)
        else:
            self.icon2.set_img_src("img/cloud_green.png")
            
    def show_red_cloud(self):
        if self.icon2 is None:
            self.icon2 = M5Img("img/cloud_red.png", x=225, y=0, parent=None)
        else:
            self.icon2.set_img_src("img/cloud_red.png")
            
    def remove_cloud(self):
        self.icon2.delete()
        self.icon2 = None
        






