import lvgl as lv
from imagetools import get_png_info, open_png
import urequests

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
_DEFAULT_IMG = '/flash/Icons/default.png'


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
            raise OSError(__name__ + ': ' + str(e) + '\n default.png is missing from the Icons folder!')

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
    def __init__(self, parent=lv.scr_act(), x=0, y=0, color=_DEFAULT_THEME_COLOR, unchecked_bg=None):
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
        if unchecked_bg != None:
            style_bg.set_bg_color(lv.STATE.DEFAULT, lv.color_hex(unchecked_bg))
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
    def __init__(self, parent=lv.scr_act(), x=0, y=0, width=100, options=[], color=_DEFAULT_THEME_COLOR):
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_width(width)
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

    def __init__(self, parent=lv.scr_act(), x=0, y=0, width=150, min_value=0, max_value=100, color=_DEFAULT_THEME_COLOR,
                 show_label=True):
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

        if show_label:
            self._slider_label.set_hidden(False)
        else:
            self._slider_label.set_hidden(True)

    def set_value(self, value):
        super().set_value(value, lv.ANIM.ON)
        self._slider_label.set_text(str(value))

    def set_label_hidden(self, hide):
        self._slider_label.set_hidden(hide)

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
            super().set_points(tmp_ser, points)
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


class Gauge(lv.gauge):
    def __init__(self, parent=lv.scr_act(), x=0, y=0, gauge_color=_DEFAULT_THEME_COLOR, length=150, initial_value=0,
                 min_value=0, max_value=100):
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_size(length, length)
        self.set_needle_count(1, [lv.color_hex(gauge_color)])
        super().set_value(0, initial_value)
        self.set_range(min_value, max_value)
        super().set_critical_value(max_value - round((max_value - min_value) / 5))

        style_bg = lv.style_t()
        style_bg.init()
        style_bg.set_border_width(lv.STATE.DEFAULT, 1)
        self.add_style(self.PART.MAIN, style_bg)

    def set_value(self, value):
        super().set_value(0, value)

    def set_critical_value(self, value=None):
        if value == None:
            super().set_critical_value(self.get_max_value() - round((self.get_max_value() - self.get_min_value()) / 5))
        else:
            super().set_critical_value(value)

    # func() returns an integer within the gauge's range of value and changes needle's direction accordingly
    def d_refresh(self, func=None, *args):
        if not func:
            return
        new_data = func(*args)
        self.set_value(0, new_data)


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


class Page(lv.page):
    def __init__(self, parent=lv.scr_act(), x=0, y=0, height=150, width=100, color=_DEFAULT_THEME_COLOR,
                 radius=_DEFAULT_RADIUS):
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_size(width, height)

        style_main = lv.style_t()
        style_main.init()
        darker_color = lv.color_t.color_darken(lv.color_hex(color), 30)
        style_main.set_border_color(lv.STATE.DEFAULT, darker_color)
        style_main.set_border_width(lv.STATE.DEFAULT, 0)
        style_main.set_radius(lv.STATE.DEFAULT, radius)
        style_main.set_bg_color(lv.STATE.DEFAULT, lv.color_hex(color))
        style_main.set_pad_all(lv.STATE.DEFAULT, 0)
        style_main.set_pad_bottom(lv.STATE.DEFAULT, 5)
        self.add_style(self.PART.BG, style_main)

        self.set_scrollbar_mode(lv.SCROLLBAR_MODE.DRAG)

    def d_refresh(self, func=None, *args):
        return
