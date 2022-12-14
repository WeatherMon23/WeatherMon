from m5stack import *
from m5stack_ui import *
from uiflow import *

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)


class LLabel(lv.label):
    def __init__(self, text, width, color=0x000000, long_mode=lv.label.LONG.EXPAND, alignment=lv.label.ALIGN.CENTER):
        super().__init__(lv.scr_act())
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
        style_main.set_text_color(lv.STATE.DEFAULT, lv.color_hex(color))
        self.add_style(self.PART.MAIN, style_main)

    def d_refresh(self, func=None, *args):
        if not func:
            return
        new_data = func(*args)
        self.set_text(new_data)


class LCheckbox(lv.checkbox):
    def __init__(self, text, color=0x228B22):
        super().__init__(lv.scr_act())
        self.set_text(text)

        style_bullet = lv.style_t()
        style_bullet.init()
        style_bullet.set_border_color(lv.STATE.DEFAULT, lv.color_hex(color))
        style_bullet.set_bg_color(lv.STATE.CHECKED, lv.color_hex(color))
        style_bullet.set_border_color(lv.STATE.DEFAULT, lv.color_hex(color))
        self.add_style(self.PART.BULLET, style_bullet)

        style_bg = lv.style_t()
        style_bg.init()
        style_bg.set_outline_width(lv.STATE.DEFAULT, 0)
        self.add_style(self.PART.BG, style_bg)

    def d_refresh(self, func=None, *args):
        if not func:
            return
        new_data = func(*args)
        self.set_checked(new_data)


class LLine(lv.line):
    def __init__(self, length, is_vertical=False, width=1, color=0x000000):
        super().__init__(lv.scr_act())
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


class LTable(lv.table):
    def __init__(self, data, num_of_cols, width):
        super().__init__(lv.scr_act())
        self._num_of_cols = num_of_cols
        self.set_col_cnt(num_of_cols)
        for i in range(len(data) / num_of_cols):
            for j in range(num_of_cols):
                if i == 0:
                    self.set_col_width(j, int(width / num_of_cols))
                    self.set_cell_type(i, j, 1)
                else:
                    self.set_cell_type(i, j, 2)
                self.set_cell_align(i, j, lv.label.ALIGN.CENTER)
                self.set_cell_value(i, j, data[i * num_of_cols + j])

        style_bg = lv.style_t()
        style_bg.init()
        style_bg.set_border_width(lv.STATE.DEFAULT, 0)
        self.add_style(self.PART.BG, style_bg)

    def d_refresh(self, func=None, *args):
        if not func:
            return
        new_data = func(*args)
        for i in range(len(new_data) / self._num_of_cols):
            for j in range(self._num_of_cols):
                self.set_cell_value(i, j, new_data[i * self._num_of_cols + j])


class LSwitch(lv.switch):
    def __init__(self, color=0x228B22):
        super().__init__(lv.scr_act())
        self.set_anim_time(100)

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

    def d_refresh(self, func=None, *args):
        if not func:
            return
        switch_state = self.get_state()
        new_data = func(*args)
        if new_data != switch_state:
            self.toggle(lv.ANIM.ON)


class LCpicker(lv.cpicker):
    def __init__(self, height):
        super().__init__(lv.scr_act())
        self.set_size(height, height)  # Changing Type crashes the device  # self.set_type(lv.cpicker.TYPE.RECT)

    def d_refresh(self, func=None, *args):
        if not func:
            return
        new_data = lv.color_hex(func(*args))
        self.set_color(new_data)


class LDropdown(lv.dropdown):
    def __init__(self, options, color=0x228B22):
        super().__init__(lv.scr_act())
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

    def d_refresh(self, func=None, *args):
        if not func:
            return
        new_data = func(*args)
        self.clear_options()
        self.set_options("\n".join(new_data))


class LRoller(lv.roller):
    def __init__(self, options, mode=lv.roller.MODE.INFINITE, color=0x228B22):
        super().__init__(lv.scr_act())
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

    def d_refresh(self, func=None, *args):
        if not func:
            return
        new_data = func(*args)
        self.set_options("\n".join(new_data), self._mode)


class LSlider(lv.slider):
    def __init__(self, width, min_value=0, max_value=100, color=0x228B22):
        super().__init__(lv.scr_act())
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

    def d_refresh(self, func=None, *args):
        if not func:
            return
        new_data = func(*args)
        self.set_value(new_data, lv.ANIM.ON)


class Lbtn(lv.btn):
    def __init__(self, text, width, is_toggled=False, color=0x228B22, radius=8):
        super().__init__(lv.scr_act())
        label_button = LLabel(text, 200)
        label_button.set_parent(self)
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

    def d_refresh(self, func=None, *args):
        return


class LChart(lv.chart):
    def __init__(self, height, width, min_val, max_val, input_vector, chart_type=lv.chart.TYPE.COLUMN, is_faded=True):
        super().__init__(lv.scr_act())
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


class LCont(lv.cont):
    def __init__(self, height, width, color, radius = 8):
        super().__init__(lv.scr_act())
        self.set_auto_realign(False)  # Disable auto realign when the size changes
        self.set_fit(lv.FIT.NONE)  # Do not change the size automatically around the children
        self.set_layout(lv.LAYOUT.OFF)  # Do not align the children
        self.set_size(height, width)
        
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
        

class _Widget(LCont):
    def __init__(self, board, height, width, row, col, color, is_place_holder):
        height_in_pixels = board.block_size * height + (height - 1) * board.split_size
        super().__init__(board.block_size * width + (width - 1) * board.split_size, height_in_pixels, color)
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
        
        def event_handler(source, event):
            if event == lv.EVENT.LONG_PRESSED and not self.is_place_holder:
                # Delete widget from main board
                self._board.delete_widget(self)

        self.set_event_cb(event_handler)
        
        for i in range(height):
            for j in range(width):
                self.reserved_blocks.append([row + i, col + j])


class Board:
    def _init_board(self):
        for row in range(self.rows_num):
            for col in range(self.cols_num):
                # Filling the board with place-holders
                empty_block = _Widget(self, 1, 1, row, col, self._default_color, True)
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

    def __init__(self, top_margin, block_size, split_size, rows_num, cols_num, show_place_holders=True,
                 default_color=0xf2f2f2):
        self.top_margin = top_margin
        self.block_size = block_size
        self.split_size = split_size
        self.rows_num = rows_num
        self.cols_num = cols_num
        self._show_place_holders = show_place_holders
        self._default_color = default_color
        self._background_blocks = list()
        self._colored_blocks = list()
        self._init_board()

    def draw_widget(self, height, width, row, col, color):
        # Checking for collision
        for i, j in [(i, j) for i in range(height) for j in range(width)]:
            if any([row + i, col + j] in colored_block.reserved_blocks for colored_block in self._colored_blocks):
                return None

        widget = _Widget(self, height, width, row, col, color, False)
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
            child.d_refresh()
            child = self.get_child(child)
