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

    def __init__(self, text, x, y, w, h, bg_c, text_c, parent=None):
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


class M5Title:
    def __init__(self, text='', text_c=0xFFFFFF, bg_c=0x000000):
        self.text_c = text_c
        self.line = M5Line(x1=0, y1=12, x2=320, y2=12, color=bg_c, width=26, parent=None)
        self.left_label = M5Label(text, x=6, y=5, color=text_c, font=FONT_MONT_14, parent=None)
        self.battery_label = None
        self.icon1 = None
        self.icon2 = None

    def clear_title(self):
        self.icon1.delete()
        self.icon1 = None
        self.icon2.delete()
        self.icon2 = None
        self.battery_label.delete()
        self.battery_label = None

    def set_text(self, text):
        self.left_label.set_text(text)

    def show_battery(self):
        per = str(int((power.getBatVoltage() - 3.2) * 100)) + str('%')
        self.battery_label = M5Label(per, x=287, y=5, color=self.text_c, font=FONT_MONT_14, parent=None)

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
