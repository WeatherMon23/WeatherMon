import lvgl as lv
from imagetools import get_png_info, open_png
from m5stack import *
from m5stack_ui import *
from uiflow import *
from urequests import *


LV_HOR_RES=320
LV_VER_RES=240

_DEFAULT_TEXT_COLOR = 0x000000
_DEFAULT_THEME_COLOR = 0x228B22
_DEFAULT_DISABLED_COLOR = 0xf2f2f2

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)

_DEFAULT_TEXT_COLOR = 0x000000
_DEFAULT_THEME_COLOR = 0x228B22
_DEFAULT_DISABLED_COLOR = 0xf2f2f2
_DEFAULT_RADIUS = 8
_DEFAULT_ANIME_TIME = 100
_DEFAULT_FONT = lv.font_montserrat_14
'''
Fonts:
- lv.font_montserrat_10
- lv.font_montserrat_14
- lv.font_montserrat_18
- lv.font_montserrat_22
- lv.font_montserrat_26
- lv.font_montserrat_30
- lv.font_montserrat_34
- lv.font_montserrat_38
- lv.font_montserrat_48
- lv.font_PHT_unicode_24
'''
_DEFAULT_IMG = '/flash/icons/default.png'


class Image(lv.img):
    def _set_src_aux(self, src):
        # Register PNG image decoder
        decoder = lv.img.decoder_create()
        decoder.info_cb = get_png_info
        decoder.open_cb = open_png

        with open(src, 'rb') as f:
            png_data = f.read()

        png_img_dsc = lv.img_dsc_t({'data_size': len(png_data), 'data': png_data})

        super().set_src(png_img_dsc)

    def _set_src_url(self, src):
        response = urequests.get(src)
        image_bytes = response.content
        png_img_dsc = lv.img_dsc_t({'data_size': len(image_bytes), 'data': image_bytes})
        super().set_src(png_img_dsc)

    def _set_img_default(self):
        try:
            self._set_src_aux(_DEFAULT_IMG)
        except OSError as e:
            raise OSError(__name__ + ': ' + str(e) + '\n default.png is missing from the icons folder!')

    def __init__(self, parent=lv.scr_act(), x=0, y=0, src=_DEFAULT_IMG):
        super().__init__(parent)
        self.set_pos(x, y)
        if 'http://' in src or 'https://' in src:
            self._set_src_url(src)
        elif src == _DEFAULT_IMG:
            self._set_img_default()
        else:
            self._set_src_aux(src)

    def set_src(self, src):
        if 'http://' in src or 'https://' in src:
            self._set_src_url(src)
        else:
            self._set_src_aux(src)

    # func() returns a string of a src image to be displayed
    def d_refresh(self, func=None, *args):
        if not func:
            return
        new_src = func(*args)
        self.set_src(new_src)


class Label(lv.label):
    def _event_handler(self, source, evt):
        if evt == lv.EVENT.PRESSING:
            super().set_pos(10, 70)
            super().set_size(300,
                             100)  # self.set_style_local_text_font(self.PART.MAIN, lv.STATE.DEFAULT,lv.font_montserrat_34)

        elif evt == lv.EVENT.RELEASED:
            super().set_pos(self._o_x, self._o_y)
            super().set_size(self._o_width,
                             self._o_height)  # self.set_style_local_text_font(self.PART.MAIN, lv.STATE.DEFAULT, self._o_font)

    def __init__(self, parent=lv.scr_act(), x=0, y=0, text='Label', text_color=_DEFAULT_TEXT_COLOR, font=_DEFAULT_FONT,
                 width=0, long_mode=lv.label.LONG.EXPAND, alignment=lv.label.ALIGN.CENTER):
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_text(text)
        self.set_long_mode(long_mode)
        '''
        lv.label.LONG.EXPAND - Expand the object size to the text size
        lv.label.LONG.BREAK - Keep the object width, break (wrap) the too long lines and expand the object height
        lv.label.LONG.DOT - Keep the object size, break the text and write dots in the last line (not supported when using lv_label_set_text_static)
        lv.label.LONG.SROLL - Keep the size and scroll the label back and forth
        lv.label.LONG.SROLL_CIRC - Keep the size and scroll the label circularly
        lv.label.LONG.CROP - Keep the size and crop the text out of it
        '''
        self.set_width(width)
        self.set_align(alignment)
        '''
        lv.label.ALIGN.LEFT
        lv.label.ALIGN.RIGHT
        lv.label.ALIGN.CENTER
        '''
        style_main = lv.style_t()
        style_main.init()
        style_main.set_text_font(lv.STATE.DEFAULT, font)
        style_main.set_text_color(lv.STATE.DEFAULT, lv.color_hex(text_color))
        self.add_style(self.PART.MAIN, style_main)

        self.set_event_cb(self._event_handler)

    # func() returns a string to be displayed inside the label
    def d_refresh(self, func=None, *args):
        if not func:
            return
        new_data = func(*args)
        self.set_text(new_data)


class Checkbox(lv.checkbox):
    def __init__(self, parent=lv.scr_act(), x=0, y=0, text='Checkbox', text_color=_DEFAULT_TEXT_COLOR,
                 color=_DEFAULT_THEME_COLOR, state=lv.btn.STATE.RELEASED):
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_state(state)
        '''
        lv.btn.STATE.RELEASED
        lv.btn.STATE.PRESSED
        lv.btn.STATE.CHECKED_RELEASED
        lv.btn.STATE.CHECKED_PRESSED
        lv.btn.STATE.DISABLED
        lv.btn.STATE.CHECKED_DISABLED
        '''
        self.set_text(text)

        style_bullet = lv.style_t()
        style_bullet.init()
        style_bullet.set_border_color(lv.STATE.DEFAULT, lv.color_hex(color))
        style_bullet.set_bg_color(lv.STATE.CHECKED, lv.color_hex(color))
        style_bullet.set_border_color(lv.STATE.DEFAULT, lv.color_hex(color))
        self.add_style(self.PART.BULLET, style_bullet)

        style_bg = lv.style_t()
        style_bg.init()
        style_bg.set_text_color(lv.STATE.DEFAULT, lv.color_hex(text_color))
        style_bg.set_text_font(lv.STATE.DEFAULT, font)
        style_bg.set_outline_width(lv.STATE.DEFAULT, 0)
        self.add_style(self.PART.BG, style_bg)

    # func() returns a boolean representing the new state of the checkbox
    def d_refresh(self, func=None, *args):
        if not func:
            return
        new_data = func(*args)
        self.set_checked(new_data)


class Line(lv.line):
    def __init__(self, parent=lv.scr_act(), x=0, y=0, length=50, is_vertical=False, width=1,
                 color=_DEFAULT_THEME_COLOR):
        super().__init__(parent)
        self.set_pos(x, y)
        start_point, end_point = {"x": 0, "y": 0}, {"x": 0, "y": length}
        if is_vertical:
            end_point = {"x": length, "y": 0}

        style_line = lv.style_t()
        style_line.init()
        style_line.set_line_width(lv.STATE.DEFAULT, width)
        style_line.set_line_color(lv.STATE.DEFAULT, lv.color_hex(color))
        style_line.set_line_rounded(lv.STATE.DEFAULT, True)
        self.set_points([start_point, end_point], 2)
        self.add_style(lv.line.PART.MAIN, style_line)

    def d_refresh(self, func=None, *args):
        return


class Table(lv.table):
    def __init__(self, parent=lv.scr_act(), x=0, y=0, data=[], text_color=_DEFAULT_TEXT_COLOR, font=_DEFAULT_FONT,
                 alignment=lv.label.ALIGN.CENTER, num_of_cols=0, width=150):
        super().__init__(parent)
        self.set_pos(x, y)
        self._num_of_cols = num_of_cols
        self.set_col_cnt(num_of_cols)
        for i in range(int(len(data) / num_of_cols)):
            for j in range(num_of_cols):
                if i == 0:
                    self.set_col_width(j, int(width / num_of_cols))
                    self.set_cell_type(i, j, 1)
                else:
                    self.set_cell_type(i, j, 2)
                self.set_cell_align(i, j, alignment)
                '''
                lv.label.ALIGN.LEFT
                lv.label.ALIGN.RIGHT
                lv.label.ALIGN.CENTER
                '''
                self.set_cell_value(i, j, data[i * num_of_cols + j])

        style_bg = lv.style_t()
        style_bg.init()
        style_bg.set_text_color(lv.STATE.DEFAULT, lv.color_hex(text_color))
        style_bg.set_text_font(lv.STATE.DEFAULT, font)
        style_bg.set_border_width(lv.STATE.DEFAULT, 0)
        self.add_style(self.PART.BG, style_bg)

    # func() returns a list of strings to be displayed inside the table (including headers)
    def d_refresh(self, func=None, *args):
        if not func:
            return
        new_data = func(*args)
        for i in range(int(len(new_data) / self._num_of_cols)):
            for j in range(self._num_of_cols):
                self.set_cell_value(i, j, new_data[i * self._num_of_cols + j])


class Switch(lv.switch):
    def __init__(self, parent=lv.scr_act(), x=0, y=0, color=_DEFAULT_THEME_COLOR):
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_anim_time(_DEFAULT_ANIME_TIME)

        style_indic = lv.style_t()
        style_indic.init()
        style_indic.set_bg_color(lv.STATE.CHECKED, lv.color_hex(color))
        darker_color = lv.color_t.color_darken(lv.color_hex(color), 30)
        style_indic.set_bg_color(lv.STATE.DEFAULT, darker_color)
        self.add_style(self.PART.INDIC, style_indic)

        style_bg = lv.style_t()
        style_bg.init()
        style_bg.set_outline_width(lv.STATE.DEFAULT, 0)
        self.add_style(self.PART.BG, style_bg)

    # func() returns a boolean representing the new status of the switch
    def d_refresh(self, func=None, *args):
        if not func:
            return
        switch_state = self.get_state()
        new_data = func(*args)
        if new_data != switch_state:
            self.toggle(lv.ANIM.ON)


class Cpicker(lv.cpicker):
    def __init__(self, parent=lv.scr_act(), x=0, y=0, length=150):
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_size(length, length)  # self.set_type(lv.cpicker.TYPE.RECT) - Changing Type crashes the device

    # func() returns a color to be set for the color picker
    def d_refresh(self, func=None, *args):
        if not func:
            return
        new_data = lv.color_hex(func(*args))
        self.set_color(new_data)


class Dropdown(lv.dropdown):
    def __init__(self, parent=lv.scr_act(), x=0, y=0, options=[], color=_DEFAULT_THEME_COLOR):
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_options("\n".join(options))

        style_main = lv.style_t()
        style_main.init()
        style_main.set_border_color(lv.STATE.DEFAULT, lv.color_hex(color))
        darker_color = lv.color_t.color_darken(lv.color_hex(color), 30)
        lighter_color = lv.color_t.color_lighten(lv.color_hex(color), 30)
        style_main.set_border_color(lv.STATE.FOCUSED, darker_color)
        self.add_style(self.PART.MAIN, style_main)

        style_selected = lv.style_t()
        style_selected.init()
        style_selected.set_bg_color(lv.STATE.DEFAULT, lighter_color)
        self.add_style(self.PART.SELECTED, style_selected)

    # func() returns a list of strings to be filled into the drop-down
    def d_refresh(self, func=None, *args):
        if not func:
            return
        new_data = func(*args)
        self.clear_options()
        self.set_options("\n".join(new_data))


class Roller(lv.roller):
    def __init__(self, parent=lv.scr_act(), x=0, y=0, options=[], mode=lv.roller.MODE.INFINITE,
                 color=_DEFAULT_THEME_COLOR):
        super().__init__(parent)
        self.set_pos(x, y)
        self._mode = mode
        self.set_options("\n".join(options), mode)
        '''
        lv.roller.MODE.NORMAL - Roller ends at the end of the options
        lv.roller.MODE.INFINITE - Roller can be scrolled forever
        '''
        self.set_visible_row_count(4)

        style_bg = lv.style_t()
        style_bg.init()
        style_bg.set_border_width(lv.STATE.DEFAULT, 0)
        self.add_style(self.PART.BG, style_bg)

        style_selected = lv.style_t()
        style_selected.init()
        lighter_color = lv.color_t.color_lighten(lv.color_hex(color), 30)
        style_selected.set_bg_color(lv.STATE.DEFAULT, lighter_color)
        self.add_style(self.PART.SELECTED, style_selected)

    # func() returns a list of strings to be filled into the roller
    def d_refresh(self, func=None, *args):
        if not func:
            return
        new_data = func(*args)
        self.set_options("\n".join(new_data), self._mode)


class Slider(lv.slider):
    def _event_handler(self, source, evt):
        if evt == lv.EVENT.VALUE_CHANGED:
            self._slider_label.set_text(str(self.get_value()))

    def __init__(self, parent=lv.scr_act(), x=0, y=0, width=150, min_value=0, max_value=100,
                 color=_DEFAULT_THEME_COLOR):
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_width(width)
        self.set_range(min_value, max_value)

        style_bg = lv.style_t()
        style_bg.init()
        style_bg.set_outline_width(lv.STATE.DEFAULT, 0)
        self.add_style(self.PART.BG, style_bg)

        style_indic = lv.style_t()
        style_indic.init()
        style_indic.set_bg_color(lv.STATE.DEFAULT, lv.color_hex(color))
        self.add_style(self.PART.INDIC, style_indic)

        style_knob = lv.style_t()
        style_knob.init()
        darker_color = lv.color_t.color_darken(lv.color_hex(color), 30)
        style_knob.set_bg_color(lv.STATE.DEFAULT, darker_color)
        self.add_style(self.PART.KNOB, style_knob)

        self._slider_label = Label(parent=parent, text='0')
        self._slider_label.set_auto_realign(True)
        self._slider_label.align(self, lv.ALIGN.OUT_BOTTOM_MID, 0, 10)
        self.set_event_cb(self._event_handler)

    # func() returns an integer between min_value and max_value (including) to be represented in the slider
    def d_refresh(self, func=None, *args):
        if not func:
            return
        new_data = func(*args)
        self.set_value(new_data, lv.ANIM.ON)


class Button(lv.btn):
    def __init__(self, parent=lv.scr_act(), x=0, y=0, text='Button', text_color=_DEFAULT_TEXT_COLOR,
                 color=_DEFAULT_THEME_COLOR, height=50, width=100, is_toggled=False, font=_DEFAULT_FONT,
                 radius=_DEFAULT_RADIUS):
        super().__init__(parent)
        self._o_x = x
        self._o_y = y
        self._o_width = width
        self._o_height = height
        self._o_font = font
        self.set_pos(x, y)
        self.set_size(width, height)
        self._label_button = Label(parent=self, text=text, font=font, text_color=text_color)
        self.set_checkable(is_toggled)

        style_main = lv.style_t()
        style_main.init()
        style_main.set_radius(lv.STATE.DEFAULT, radius)
        style_main.set_outline_width(lv.STATE.DEFAULT, 0)
        darker_color = lv.color_t.color_darken(lv.color_hex(color), 30)
        style_main.set_border_color(lv.STATE.PRESSED, darker_color)
        style_main.set_bg_color(lv.STATE.PRESSED, lv.color_hex(color))
        style_main.set_bg_opa(lv.STATE.PRESSED, 30)
        style_main.set_border_color(lv.STATE.DEFAULT, lv.color_hex(color))
        self.add_style(self.PART.MAIN, style_main)

    # func() returns a string to be displayed inside the button
    def d_refresh(self, func=None, *args):
        if not func:
            return
        new_data = func(*args)
        self._label_button.set_text(new_data)


class FadingButton(Button):
    def _event_handler(self, source, evt):
        if evt == lv.EVENT.PRESSING:
            super().set_pos(10, 70)
            super().set_size(300, 100)
            c = self.get_child(None)
            c.set_style_local_text_font(self.PART.MAIN, lv.STATE.DEFAULT, lv.font_montserrat_34)

        elif evt == lv.EVENT.RELEASED:
            super().set_pos(self.primal_x, self.primal_y)
            super().set_size(self.primal_width, self.primal_height)
            c = self.get_child(None)
            c.set_style_local_text_font(self.PART.MAIN, lv.STATE.DEFAULT, self.primal_font)

    def __init__(self, parent=lv.scr_act(), x=0, y=0, text='Button', text_color=_DEFAULT_TEXT_COLOR,
                 color=_DEFAULT_THEME_COLOR, height=50, width=100, is_toggled=False, font=_DEFAULT_FONT,
                 radius=_DEFAULT_RADIUS):
        super().__init__(parent=parent, x=x, y=y, text=text, text_color=text_color, color=color, height=height,
                         width=width, is_toggled=is_toggled, font=font, radius=radius)
        self.primal_x = x
        self.primal_y = y
        self.primal_height = height
        self.primal_width = width
        self.primal_font = font

        self.set_event_cb(self._event_handler)

    def set_pos(self, x, y):
        super().set_pos(x, y)
        self.primal_x = x
        self.primal_y = y

    def set_x(self, x):
        super().set_x(x)
        self.primal_x = x

    def set_y(self, y):
        super().set_y(y)
        self.primal_y = y

    def set_size(self, width, height):
        super().set_size(width, height)
        self.primal_height = height
        self.primal_width = width

    def set_width(self, width):
        super().set_width(width)
        self.primal_width = width

    def set_height(self, height):
        super().set_height(height)
        self.primal_height = height


class Chart(lv.chart):
    def __init__(self, parent=lv.scr_act(), x=0, y=0, height=150, width=200, min_val=0, max_val=100, input_vector=[],
                 chart_type=lv.chart.TYPE.COLUMN, is_faded=True):
        super().__init__(parent)
        self.set_pos(x, y)
        self._series = list()
        self.set_size(width, height)
        self.set_type(chart_type)
        '''
        lv.chart.TYPE.NONE - Do not display any data. It can be used to hide the series.
        lv.chart.TYPE.LINE - Draw lines between the points.
        lv.chart.TYPE.COLUMN - Draw columns.LV_CHART_TYPE_NONE - Do not display any data. It can be used to hide the series.
        '''
        style_bg = lv.style_t()
        style_bg.init()
        style_bg.set_border_width(lv.STATE.DEFAULT, 0)
        self.add_style(self.PART.BG, style_bg)

        self.set_y_range(0, min_val, max_val)
        if is_faded:
            self.set_style_local_bg_opa(lv.chart.PART.SERIES, lv.STATE.DEFAULT, lv.OPA._50)
            self.set_style_local_bg_grad_dir(lv.chart.PART.SERIES, lv.STATE.DEFAULT, lv.GRAD_DIR.VER)
            self.set_style_local_bg_main_stop(lv.chart.PART.SERIES, lv.STATE.DEFAULT, 255)
            self.set_style_local_bg_grad_stop(lv.chart.PART.SERIES, lv.STATE.DEFAULT, 0)
        for color, points in input_vector:
            tmp_ser = self.add_series(lv.color_hex(color))
            self.set_points(tmp_ser, points)
            self._series.append(tmp_ser)
        self.refresh()

    # func() returns data in the following format: `[(0xff0000, [point1, point2, point3]), (0x00ff00, [point1, point2, point3])]` to draw a new series inside the chart
    def d_refresh(self, func=None, *args):
        if not func:
            return
        new_data = func(*args)
        for series in self._series:
            self.clear_series(series)
        self._series = list()
        for color, points in new_data:
            tmp_ser = self.add_series(lv.color_hex(color))
            self.set_points(tmp_ser, points)
        self.refresh()


class Container(lv.cont):
    def __init__(self, parent=lv.scr_act(), x=0, y=0, height=150, width=100, color=_DEFAULT_THEME_COLOR,
                 layout=lv.LAYOUT.OFF, fit=lv.FIT.NONE, radius=_DEFAULT_RADIUS):
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_auto_realign(False)  # Disable auto realign when the size changes
        self.set_fit(fit)
        '''
        lv.FIT.NONE - Do not change the size automatically.
        lv.FIT.TIGHT - Shrink-wrap the container around all of its children, while keeping pad_top/bottom/left/right space on the edges.
        lv.FIT.PARENT - Set the size to the parent's size minus pad_top/bottom/left/right (from the parent's style) space.
        lv.FIT.MAX - Use lv.FIT.PARENT while smaller than the parent and lv.FIT.TIGHT when larger. It will ensure that the container is, at minimum, the size of its parent.
        '''
        self.set_layout(layout)
        '''
        lv.LAYOUT.OFF - Do not align the children.
        lv.LAYOUT.CENTER - Align children to the center in column and keep pad_inner space between them.
        lv.LAYOUT.COLUMN_LEFT - Align children in a left-justified column. Keep pad_left space on the left, pad_top space on the top and pad_inner space between the children.
        lv.LAYOUT.COLUMN_MID - Align children in centered column. Keep pad_top space on the top and pad_inner space between the children.
        lv.LAYOUT.COLUMN_RIGHT - Align children in a right-justified column. Keep pad_right space on the right, pad_top space on the top and pad_inner space between the children.
        lv.LAYOUT.ROW_TOP - Align children in a top justified row. Keep pad_left space on the left, pad_top space on the top and pad_inner space between the children.
        lv.LAYOUT.ROW_MID - Align children in centered row. Keep pad_left space on the left and pad_inner space between the children.
        lv.LAYOUT.ROW_BOTTOM - Align children in a bottom justified row. Keep pad_left space on the left, pad_bottom space on the bottom and pad_inner space between the children.
        lv.LAYOUT.PRETTY_TOP - Put as many objects as possible in a row (with at least pad_inner space and pad_left/right space on the sides). Divide the space in each line equally between the children. If here are children with different height in a row align their top edge.
        lv.LAYOUT.PRETTY_MID - Same as lv.LAYOUT.PRETTY_TOP but if here are children with different height in a row align their middle line.
        lv.LAYOUT.PRETTY_BOTTOM - Same as lv.LAYOUT.PRETTY_TOP but if here are children with different height in a row align their bottom line.
        lv.LAYOUT.GRID - Similar to lv.LAYOUT.PRETTY but not divide horizontal space equally just let pad_left/right on the edges and pad_inner space between the elements.
        '''
        self.set_size(width, height)

        style_main = lv.style_t()
        style_main.init()
        darker_color = lv.color_t.color_darken(lv.color_hex(color), 30)
        style_main.set_border_color(lv.STATE.DEFAULT, darker_color)
        style_main.set_border_width(lv.STATE.DEFAULT, 0)
        style_main.set_radius(lv.STATE.DEFAULT, radius)
        style_main.set_bg_color(lv.STATE.DEFAULT, lv.color_hex(color))
        self.add_style(self.PART.MAIN, style_main)

    def d_refresh(self, func=None, *args):
        return


class _DialogBase():
    """
    A base class for all possible pop up dialogues.
    Every class that inherits and wants to customize the messsage box's event call back
    should make implement a function and call set_evt_cb_aux(func).
    It's also possible for classes that inherit to customize the buttons that appear.
    ...
    Attributes
    ----------
    mbox : lv.msgbox
        LVGL message box to contain buttons and text.
    
    Methods
    -------
    set_evt_cb_aux(func)
    
    """
    
    def _opa_anim(self,mbox,v):
        bg = lv.obj.__cast__(mbox)
        mbox.get_parent().set_style_local_bg_opa(lv.obj.PART.MAIN, lv.STATE.DEFAULT, v)
        
    def _mbox_event_cb(self, obj, evt):
        """
        A default event callback function.
        The default behavior for every button is to close the dialog.
    
        """
        if evt == lv.EVENT.DELETE:
            # Delete the parent modal background 
            lv.obj.del_async(obj.get_parent())
        elif evt == lv.EVENT.VALUE_CHANGED:
            # a button was clicked
            obj.start_auto_close(0)
    
    def __init__(self, text, text_color, title, title_color, color, btns):
        """
        Parameters
        ----------
        text : str
            The dialog's main message.
        text_color : hex int
            The dialog's main message's color.
        title : str
            The dialog's title text
        title_color : hex int
            The dialog's title text's color.
        color : hex int
            The dialog's background color.
        btns: str list (e.g. ['btn1', 'btn2'])
            A list of button names to appear in the dialog.
        
        """    
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
        mbox_style = lv.style_t()
        mbox_style.init()
        label_style = lv.style_t()
        label_style.init()
        btn_style = lv.style_t()
        btn_style.init()
        btn_style.set_text_font(lv.STATE.DEFAULT, lv.font_montserrat_18)
        mbox_style.set_bg_color(lv.STATE.DEFAULT, lv.color_hex(color))
        
        
        if title:
            mlabel = lv.label(self.mbox, None)
            mlabel.set_text(text)
            mlabel.set_long_mode(mlabel.LONG.BREAK)
            label_style.set_text_font(lv.STATE.DEFAULT, lv.font_montserrat_18)
            label_style.set_text_color(lv.STATE.DEFAULT, lv.color_hex(text_color))
            label_style.set_pad_hor(lv.STATE.DEFAULT, 50)
            mlabel.add_style(mlabel.PART.MAIN, label_style)
            mlabel.set_align(mlabel.ALIGN.CENTER)
            mbox_style.set_text_font(lv.STATE.DEFAULT, lv.font_montserrat_26)
            mbox_style.set_text_color(lv.STATE.DEFAULT, lv.color_hex(title_color))
            self.mbox.set_text(title)
        else:
            mbox_style.set_text_font(lv.STATE.DEFAULT, lv.font_montserrat_18)
            mbox_style.set_text_color(lv.STATE.DEFAULT, lv.color_hex(text_color))
            self.mbox.set_text(text)
        
        self.mbox.add_btns(btns)
        self.mbox.add_style(self.mbox.PART.BG, mbox_style)
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
        

class ALTConfirmation(_DialogBase):
    """
    A class that implements a confirmation widget.
    A pop up dialogue with a message, title (optional) and two buttons:
        close: Closes the dialog.
        confirm: Executes a confirmation function.
    
    """
    
    def _mbox_event_cb(self, obj, evt):
        """
        A cutomized event callback function that exectues confirm_func upon clicking on
        the confirm button.
        
        """
        if evt == lv.EVENT.DELETE:
            # Delete the parent modal background 
            lv.obj.del_async(obj.get_parent())
        elif evt == lv.EVENT.VALUE_CHANGED:
            # a button was clicked
            if obj.get_active_btn_text() == "Confirm":
                self.confirm_func(self.args)
            obj.start_auto_close(0)

    def __init__(self, text, text_color=_DEFAULT_TEXT_COLOR, title = '',
                 title_color=_DEFAULT_TEXT_COLOR, color=0xFFFFFF, confirm_func = None, *args):
        """
        Parameters
        ----------
        text : str
            The dialog's main message.
        text_color : hex int
            The dialog's main message's color (Default is black).
        title : str
            The dialog's title text
        title_color : hex int
            The dialog's title text's color (Default is black).
        color : hex int
            The dialog's background color (Default is white).
        confirm_func : function
            A function to be executed when clicking on the confirm button.
        
        """ 
        btns = ["Confirm", "Cancel", ""]
        super().__init__(text, text_color, title, title_color, color, btns)
        self.confirm_func = confirm_func
        self.args = args
        super().set_evt_cb_aux(self._mbox_event_cb)
        
        
class _Widget(Container):
    def _event_handler(self, source, event):
        if event == lv.EVENT.LONG_PRESSED and not self.is_place_holder:
            # Delete widget from main board
            conf = ALTConfirmation(text = 'Delete Widget', confirm_func = self._board.delete_widget(self))

    def __init__(self, board, height, width, row, col, color, is_place_holder, parent=lv.scr_act()):
        height_in_pixels = board.block_size * height + (height - 1) * board.split_size
        width_in_pixels = board.block_size * width + (width - 1) * board.split_size
        super().__init__(parent=parent, height=height_in_pixels, width=width_in_pixels, color=color)
        if not (0 <= row < board.rows_num) or (not 0 <= col < board.cols_num) or not (
                row + height <= board.rows_num) or (not col + width <= board.cols_num) or height <= 0 or width <= 0:
            raise Exception('Invalid Parameters')

        self._board = board
        self.is_place_holder = is_place_holder
        self.reserved_blocks = list()

        # Drawing the container
        height_cords = board.top_margin + row * (board.block_size + board.split_size)
        left_cords = board.block_size * col + board.split_size * (1 + col)

        self.set_pos(left_cords, height_cords)

        self.set_event_cb(self._event_handler)

        for i in range(height):
            for j in range(width):
                self.reserved_blocks.append([row + i, col + j])


class Board:
    def _init_board(self):
        for row in range(self.rows_num):
            for col in range(self.cols_num):
                # Filling the board with place-holders
                empty_block = _Widget(parent=self.parent, board=self, height=1, width=1, row=row, col=col,
                                      color=self._default_color, is_place_holder=True)
                if not self._show_place_holders:
                    empty_block.set_hidden(True)
                self._background_blocks.append(empty_block)

    def reset_board(self):
        if self._show_place_holders:
            for background_block in self._background_blocks:
                background_block.set_hidden(False)
        for colored_block in self._colored_blocks:
            colored_block.delete()
        self._colored_blocks = list()

    def __init__(self, top_margin=51, block_size=58, split_size=5, rows_num=3, cols_num=5, show_place_holders=True,
                 _default_color=_DEFAULT_DISABLED_COLOR, parent=lv.scr_act()):
        self.parent = parent
        self.top_margin = top_margin
        self.block_size = block_size
        self.split_size = split_size
        self.rows_num = rows_num
        self.cols_num = cols_num
        self._show_place_holders = show_place_holders
        self._default_color = _default_color
        self._background_blocks = list()
        self._colored_blocks = list()
        self._init_board()

    def draw_widget(self, height, width, row, col, color):
        # Checking for collision
        for i, j in [(i, j) for i in range(height) for j in range(width)]:
            if any([row + i, col + j] in colored_block.reserved_blocks for colored_block in self._colored_blocks):
                return None

        widget = _Widget(self, parent=self.parent, height=height, width=width, row=row, col=col, color=color,
                         is_place_holder=False)
        self._colored_blocks.append(widget)
        # Hide background blocks
        for i, j in widget.reserved_blocks:
            self._background_blocks[i * self.cols_num + j].set_hidden(True)
        return widget

    def delete_widget(self, widget):
        if self._show_place_holders:
            for i, j in widget.reserved_blocks:
                self._background_blocks[i * self.cols_num + j].set_hidden(False)
        widget.delete()

    def delete(self):
        for background_block in self._background_blocks:
            background_block.delete()
        for colored_block in self._colored_blocks:
            colored_block.delete()
        self._background_blocks = list()
        self._colored_blocks = list()

    def d_refresh(self):
        child = self.get_child(None)
        while child:
            try:
                child.d_refresh()
            except AttributeError as e:
                print(__name__ + ': ' + str(e))
            child = self.get_child(child)


'''
# Running Examples:
vec = [(0xff0000, [10, 20, 30, 40, 10, 20, 30, 100, 10, 20])]
tmp = Chart(input_vector=vec, chart_type=lv.chart.TYPE.LINE)]]
'''

# TODO:
# confirmation?
tmp1 = Board()
tmp1.draw_widget(2,2,1,1, 0xfff0f0)

