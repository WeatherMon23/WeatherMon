from m5stack import *
from m5stack_ui import *
from uiflow import *
from ALTelements import *
import lvgl as lv

LV_HOR_RES=320
LV_VER_RES=240
      
    
class ALTTitle():
    def _calc_battery_per(self):
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
        return per_str

    def __init__(self, text = '', text_color = 0xFFFFFF, color=0x000000):
        self.line = ALTContainer(x=0, y=0, height=26, width=LV_HOR_RES, color=color, radius=0)
        self.left_label = ALTLabel(self.line, x=6, y=5, text=text, text_color=text_color)
        self.battery_label = ALTLabel(self.line, x=265, y=5, text=self._calc_battery_per(), text_color=text_color)
        self.battery_label.set_hidden(True)

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
            self.battery_label.set_hidden(True)
    
    def delete(self):
        self.line.delete()
        
    def set_text(self, text):
        self.left_label.set_text(text)
        
    def show_battery(self):
        self.battery_label.set_text(self._calc_battery_per())
        self.battery_label.set_hidden(False)
                
    def remove_battery(self):
        self.battery_label.set_hidden(True)
        
    def show_green_wifi(self):
        if self.icon1 is None:
            self.icon1 = ALTImage(self.line, x=241, y=5, src='/flash/icons/wifi_green.png')
        else:
            self.icon1.set_src("/flash/icons/wifi_green.png")
            
    def show_red_wifi(self):
        if self.icon1 is None:
            self.icon1 = ALTImage(self.line, x=241, y=5, src='/flash/icons/wifi_red.png')
        else:
            self.icon1.set_src("/flash/icons/wifi_red.png")
            
    def remove_wifi(self):
        self.icon1.delete()
        self.icon1 = None

    def show_green_cloud(self):
        if self.icon2 is None:
            self.icon2 = ALTImage(self.line, x=215, y=7, src='/flash/icons/cloud_green.png')
        else:
            self.icon2.set_src("/flash/icons/cloud_green.png")
            
    def show_red_cloud(self):
        if self.icon2 is None:
            self.icon2 = ALTImage(self.line, x=215, y=7, src='/flash/icons/cloud_red.png')
        else:
            self.icon2.set_src("/flash/icons/cloud_red.png")
            
    def remove_cloud(self):
        self.icon2.delete()
        self.icon2 = None


# Every class that inherits and wants to customize _mbox_even_cb
# should make sure to implement the most basic functionality and then
# customize the buttons.
# Check ALTConfirmation for an example
class _DialogBase():
    def _opa_anim(self,mbox,v):
        bg = lv.obj.__cast__(mbox)
        mbox.get_parent().set_style_local_bg_opa(lv.obj.PART.MAIN, lv.STATE.DEFAULT, v)
        
    def _mbox_event_cb(self, obj, evt):
        if evt == lv.EVENT.DELETE:
            # Delete the parent modal background 
            lv.obj.del_async(obj.get_parent())
        elif evt == lv.EVENT.VALUE_CHANGED:
            # a button was clicked
            obj.start_auto_close(0)
    
    def __init__(self, text, title, btns):
        obj = lv.obj(lv.scr_act(), None)
        style_modal = lv.style_t()
        style_modal.init()
        style_modal.set_bg_color(lv.STATE.DEFAULT, lv.color_hex(0x000000))
        obj.reset_style_list(lv.obj.PART.MAIN)
        obj.add_style(lv.obj.PART.MAIN, style_modal)
        obj.set_pos(0, 0)
        obj.set_size(LV_HOR_RES, LV_VER_RES)

        # Create the message box as a child of the modal background 
        self.mbox = lv.msgbox(obj, None)
        self.mbox_style = lv.style_t()
        self.mbox_style.init()
        label_style = lv.style_t()
        label_style.init()
        btn_style = lv.style_t()
        btn_style.init()
        btn_style.set_text_font(lv.STATE.DEFAULT, lv.font_montserrat_18)
        
        
        if title:
            mlabel = lv.label(self.mbox, None)
            mlabel.set_text(text)
            mlabel.set_long_mode(mlabel.LONG.BREAK)
            label_style.set_text_font(lv.STATE.DEFAULT, lv.font_montserrat_18)
            label_style.set_pad_hor(lv.STATE.DEFAULT, 50)
            mlabel.add_style(mlabel.PART.MAIN, label_style)
            mlabel.set_align(mlabel.ALIGN.CENTER)
            self.mbox_style.set_text_font(lv.STATE.DEFAULT, lv.font_montserrat_26)
            self.mbox.set_text(title)
        else:
            self.mbox_style.set_text_font(lv.STATE.DEFAULT, lv.font_montserrat_18)
            self.mbox.set_text(text)
        
        self.mbox.add_btns(btns)
        self.mbox.add_style(self.mbox.PART.BG, self.mbox_style)
        self.mbox.add_style(self.mbox.PART.BTN, btn_style)
        self.mbox.set_width(250)
        self.mbox.align(None, lv.ALIGN.CENTER, 0, 0)
        self.mbox.set_event_cb(self._mbox_event_cb)
        self.mbox.set_anim_time(0)
            
        # Fade the message box in with an animation 
        a=lv.anim_t()
        a.init()
        a.set_var(obj)
        a.set_time(100)
        a.set_values(lv.OPA.TRANSP, lv.OPA._70)
        a.set_custom_exec_cb(lambda a, val: self._opa_anim(self.mbox,val))
        lv.anim_t.start(a)
        
    def set_evt_cb_aux(self, func):
        self.mbox.set_event_cb(self._mbox_event_cb)
        
class ALTAlert(_DialogBase):
    def __init__(self, text, title = ''):
        btns = ["Close", ""]
        super().__init__(text, title, btns)


class ALTConfirmation(_DialogBase):
    def _mbox_event_cb(self, obj, evt):
        if evt == lv.EVENT.DELETE:
            # Delete the parent modal background 
            lv.obj.del_async(obj.get_parent())
        elif evt == lv.EVENT.VALUE_CHANGED:
            # a button was clicked
            if obj.get_active_btn_text() == "Confirm":
                self.confirm_func()
            obj.start_auto_close(0)

    def __init__(self, text, title = '', confirm_func = None):
        btns = ["Confirm", "Cancel", ""]
        super().__init__(text, title, btns)
        self.confirm_func = confirm_func
        super().set_evt_cb_aux(self._mbox_event_cb)



