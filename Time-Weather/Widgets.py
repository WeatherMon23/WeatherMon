from m5stack import *
from m5stack_ui import *
from uiflow import *


class M5Fadingbtn(M5Btn):
  def _btn_pressed(self): 
    super().set_pos(10, 70)
    super().set_size(300, 100)
    super().set_btn_text(self.text)
    super().set_bg_color(self.bg_c)
    super().set_btn_text_color(self.text_c)
    super().set_btn_text_font(FONT_MONT_34)
  pass

  def _btn_released(self):
    super().set_pos(self.x, self.y)
    super().set_size(self.w, self.h)
    super().set_btn_text(self.text)
    super().set_bg_color(self.bg_c)
    super().set_btn_text_color(self.text_c)
    super().set_btn_text_font(FONT_MONT_14)
  pass

  def __init__(self, text, x, y, w, h, bg_c, text_c, parent = None):
    self.w = w
    self.h = h
    self.x = x
    self.y = y
    self.bg_c = bg_c
    self.text_c = text_c
    self.text = text
    super().__init__(text, x, y, w, h, bg_c, text_c, FONT_MONT_14, parent)
    super().pressed(self._btn_pressed)
    super().released(self._btn_released)





