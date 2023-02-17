import lvgl as lv
from m5stack import power

import ALTelements as alte

LV_HOR_RES = 320
LV_VER_RES = 240
MAX_BR = 100
MIN_BR = 20
_DEFAULT_TEXT_COLOR = 0x000000
_DEFAULT_THEME_COLOR = 0x228B22
_DEFAULT_DISABLED_COLOR = 0xf2f2f2
_DEFAULT_RADIUS = 8
_DEFAULT_ANIME_TIME = 100
_DEFAULT_FONT = lv.font_montserrat_14


class Title():
    """
    A class that implements a status bar widget

    ...

    Attributes
    ----------
    line : Container
        A container in the shape of line.
    left_label : Label
        A label which is located on the left side of the status bar.
    battery_label : Label
        A battery label which is located in the upper right of the status bar.
    wifi_icon : Image
        A small icon that shows a wifi symbol.
    cloud_icon : Image
        A small icon that shows a cloud symbol.

    Methods
    -------
    get_height()
    set_color()
    set_text_color()
    clear_title()
    delete()
    set_text()
    show_battery()
    remove_battery()
    show_green_wifi()
    show_red_wifi()
    remove_wifi()
    show_green_cloud()
    show_red_cloud()
    remove_cloud()
    """

    def _update_positions(self):
        """
        Changes the positions of battery_label, wifi_icon, cloud_icon accordingly.
        The function takes into consideration if the above exist or not.

        """
        if self.battery_label and not self.battery_label.get_hidden():
            self.battery_label.set_pos(265, 5)
            if self.wifi_icon and self.cloud_icon:
                self.wifi_icon.set_pos(241, 5)
                self.cloud_icon.set_pos(215, 7)
            elif self.wifi_icon:
                self.wifi_icon.set_pos(241, 5)
            elif self.cloud_icon:
                self.cloud_icon.set_pos(241, 7)
        else:
            if self.wifi_icon and self.cloud_icon:
                self.wifi_icon.set_pos(296, 5)
                self.cloud_icon.set_pos(270, 7)
            elif self.wifi_icon:
                self.wifi_icon.set_pos(296, 5)
            elif self.cloud_icon:
                self.cloud_icon.set_pos(296, 7)

    def _calc_battery_per(self):
        """
        A function that calculates the battery precentage with the help of the
        battery voltage.

        Returns
        -------
        per_str : str
            A string that contains the percentage's number with the '%' symbol concatenated to it,
            in addition to the appropriate battery symbol.

        """
        per = int((power.getBatVoltage() - 3.2) * 100)
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

    def __init__(self, text='', text_color=0xFFFFFF, color=0x000000):
        """
        Parameters
        ----------
        text : str (default is '')
            The text to appear in the upper left side.
        text_color : hex int
            The overall text color. (default is 0xFFFFFF (white))
        color : hex int
            The color of the status bar. (default is 0x000000 (black))
        """
        self.height = 26
        self.green_wifi_path = "/flash/Icons/wifi_green.png"
        self.red_wifi_path = "/flash/Icons/wifi_red.png"
        self.green_cloud_path = "/flash/Icons/cloud_green.png"
        self.red_cloud_path = "/flash/Icons/cloud_red.png"
        self.line = alte.Container(x=0, y=0, height=self.height, width=LV_HOR_RES, color=color, radius=0)
        self.left_label = alte.Label(self.line, x=6, y=5, text=text, text_color=text_color)
        self.battery_label = alte.Label(self.line, x=265, y=5, text=self._calc_battery_per(), text_color=text_color)
        self.battery_label.set_hidden(True)

        self.wifi_icon = None
        self.cloud_icon = None

    def get_height(self):
        """
        Returns the height of the title's container.

        """
        return self.height

    def set_color(self, color):
        """
        Sets the title's container's color.

        """
        self.line.set_style_local_bg_color(self.line.PART.MAIN, lv.STATE.DEFAULT, lv.color_hex(color))

    def set_text_color(self, color):
        """
        Sets the title's container's color.

        """
        self.left_label.set_style_local_text_color(self.left_label.PART.MAIN, lv.STATE.DEFAULT, lv.color_hex(color))
        self.battery_label.set_style_local_text_color(self.battery_label.PART.MAIN, lv.STATE.DEFAULT,
                                                      lv.color_hex(color))

    def clear_title(self):
        """
        Returns the status bar to the default state.

        """
        self.set_text('')
        if self.wifi_icon:
            self.wifi_icon.delete()
            self.wifi_icon = None
        if self.cloud_icon:
            self.cloud_icon.delete()
            self.cloud_icon = None
        if self.battery_label:
            self.battery_label.set_hidden(True)

    def delete(self):
        """
        Deletes the status bar.

        """
        self.line.delete()

    def set_text(self, text):
        """
        Changes the text of the upper left label.

        Parameters
        ----------
        text : str
            The new text to be set.

        """
        self.left_label.set_text(text)

    def show_battery(self):
        """
        Makes the battery label visible with updated value.

        """
        self.battery_label.set_text(self._calc_battery_per())
        self.battery_label.set_hidden(False)
        self._update_positions()

    def remove_battery(self):
        """
        Hides the battery label.

        """
        self.battery_label.set_hidden(True)
        self._update_positions()

    def show_green_wifi(self):
        """
        A green wifi icon becomes visible in the upper right side of the status bar.

        Assumes
        --------
        flash/Icons/wifi_green.png exists.

        """
        if self.wifi_icon is None:
            self.wifi_icon = alte.Image(self.line, x=241, y=5, src=self.green_wifi_path)
        else:
            self.wifi_icon.set_src(self.green_wifi_path)
        self._update_positions()

    def show_red_wifi(self):
        """
        A red wifi icon becomes visible in the upper right side of the status bar.

        Assumes
        --------
        flash/Icons/wifi_red.png exists.

        """
        if self.wifi_icon is None:
            self.wifi_icon = alte.Image(self.line, x=241, y=5, src=self.red_wifi_path)
        else:
            self.wifi_icon.set_src(self.red_wifi_path)
        self._update_positions()

    def remove_wifi(self):
        """
        Removes the Wifi icon.

        """
        self.wifi_icon.delete()
        self.wifi_icon = None
        self._update_positions()

    def show_green_cloud(self):
        """
        A green cloud icon becomes visible in the upper right side of the status bar.

        Assumes
        --------
        flash/Icons/wifi_cloud.png exists.

        """
        if self.cloud_icon is None:
            self.cloud_icon = alte.Image(self.line, x=215, y=7, src=self.green_cloud_path)
        else:
            self.cloud_icon.set_src(self.green_cloud_path)
        self._update_positions()

    def show_red_cloud(self):
        """
        A red cloud icon becomes visible in the upper right side of the status bar.

        Assumes
        --------
        flash/Icons/cloud_red.png exists.

        """
        if self.cloud_icon is None:
            self.cloud_icon = alte.Image(self.line, x=215, y=7, src=self.red_cloud_path)
        else:
            self.cloud_icon.set_src(self.red_cloud_path)
        self._update_positions()

    def remove_cloud(self):
        """
        Removes the cloud icon.

        """
        self.cloud_icon.delete()
        self.cloud_icon = None
        self._update_positions()


class FadingButton(alte.Button):
    """
    A class that implements a button, when long pressed, becomes large.
    When the long press is released, it returns to normal size.

    ...

    Attributes
    ----------
    primal_x : int
        The original x coordinate.
    primal_y : int
        The original y coordinate.
    primal_width : int
        The original width.
    primal_height : int
        The original height.
    primal_font : int
        The original font.

    Overrides
    -------
    set_pos()
    set_x()
    set_y()
    set_size()
    set_width()
    set_height()
    """

    def _event_handler(self, source, evt):
        """
        Event callback function.
        When long pressed, the button becomes large.
        When released, the button returns to the normal size.
        """
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
        """
        Parameters
        ----------
        parent : lv.obj
            The button's parent widget.
        x : int
            The button's on screen x-coordinate. 
        y : int
            The button's on screen y-coordinate.
        text : str
        text_color : hex int
        color: hex int
        height: int
        width: int
        is_toggled : bool
        font : lv.font_*
        radius : int
            The button corner's radius.
        """
        super().__init__(parent=parent, x=x, y=y, text=text, text_color=text_color, color=color, height=height,
                         width=width, is_toggled=is_toggled, font=font, radius=radius)
        self.primal_x = x
        self.primal_y = y
        self.primal_height = height
        self.primal_width = width
        self.primal_font = font

        self.set_event_cb(self._event_handler)

    def set_pos(self, x, y):
        """
        Sets the button's position to x,y.

        """
        super().set_pos(x, y)
        self.primal_x = x
        self.primal_y = y

    def set_x(self, x):
        """
        Sets the button's x-coordinate.

        """
        super().set_x(x)
        self.primal_x = x

    def set_y(self, y):
        """
        Sets the button's y-coordinate.

        """
        super().set_y(y)
        self.primal_y = y

    def set_size(self, width, height):
        """
        Sets the button's size.

        """
        super().set_size(width, height)
        self.primal_height = height
        self.primal_width = width

    def set_width(self, width):
        """
        Sets the button's width.

        """
        super().set_width(width)
        self.primal_width = width

    def set_height(self, height):
        """
        Sets the button's height.

        """
        super().set_height(height)
        self.primal_height = height


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

    def _opa_anim(self, mbox, v):
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
        btn_style.set_radius(lv.STATE.DEFAULT, _DEFAULT_RADIUS)
        mbox_style.set_bg_color(lv.STATE.DEFAULT, lv.color_hex(color))

        if title:
            mlabel = alte.Label(parent=self.mbox, text=text, text_color=text_color, font=lv.font_montserrat_18,
                                width=200, long_mode=lv.label.LONG.BREAK, alignment=lv.label.ALIGN.CENTER)
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
        a = lv.anim_t()
        a.init()
        a.set_var(obj)
        a.set_time(100)
        a.set_values(lv.OPA.TRANSP, lv.OPA._70)
        a.set_custom_exec_cb(lambda a, val: self._opa_anim(self.mbox, val))
        lv.anim_t.start(a)

    def set_evt_cb_aux(self, func):
        self.mbox.set_event_cb(func)


class Alert(_DialogBase):
    """
    A class that implements an alert widget.
    A pop up dialogue with a message, title (optional) and a single 'close' button that closes the dialog.

    """

    def _mbox_event_cb_child(self, obj, evt):
        """
        A cutomized event callback function that exectues close_func upon clicking on
        the close button.

        """
        if evt == lv.EVENT.DELETE:
            # Delete the parent modal background
            lv.obj.del_async(obj.get_parent())
        elif evt == lv.EVENT.VALUE_CHANGED:
            # a button was clicked
            if obj.get_active_btn_text() == "Close":
                self.close_func(*self.args)
            obj.start_auto_close(0)

    def __init__(self, text, text_color=_DEFAULT_TEXT_COLOR, title='', title_color=_DEFAULT_TEXT_COLOR, color=0xFFFFFF,
                 close_func=None, *args):
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

        """
        btns = ["Close", ""]
        super().__init__(text, text_color, title, title_color, color, btns)
        self.close_func = close_func
        self.args = args
        if close_func != None:
            super().set_evt_cb_aux(self._mbox_event_cb_child)


class Confirmation(_DialogBase):
    """
    A class that implements a confirmation widget.
    A pop up dialogue with a message, title (optional) and two buttons:
        close: Closes the dialog.
        confirm: Executes a confirmation function.

    """

    def _mbox_event_cb_child(self, obj, evt):
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
                self.confirm_func(*self.args)
            obj.start_auto_close(0)

    def __init__(self, text, text_color=_DEFAULT_TEXT_COLOR, title='', title_color=_DEFAULT_TEXT_COLOR, color=0xFFFFFF,
                 confirm_func=None, *args):
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
        if confirm_func != None:
            super().set_evt_cb_aux(self._mbox_event_cb_child)


class BrightnessSlider(alte.Slider):
    """
    A class that implements a brightness slider.
    A slider with label under, changes the brightness relative to MAX_BR and MIN_BR

    """

    def _compute_relative_br(self, value):
        """
        A function that commputes the relative brightness.
        
        Parameters
        ----------
        value : str
            A value between slider.min_value and slider.max_value.
            
        Returns
        ---------
        : int
            An integer between MIN_BR and MAX_BR.
        """
        relative = self.get_max_value() - self.get_min_value()
        return MIN_BR + int((value * (MAX_BR - MIN_BR)) / relative)

    def _event_handler(self, source, evt):
        """
        A cutomized event callback function that changes the label's text and brightness when there's
        a value change.

        """
        super()._event_handler(source, evt)
        if evt == lv.EVENT.VALUE_CHANGED:
            brightness = self._compute_relative_br(self.get_value())
            power.setLCDBrightness(brightness)

    def set_value(self, value):
        """
        Sets the slider's label value and screen brightness.

        """
        super().set_value(value)
        brightness = self._compute_relative_br(value)
        power.setLCDBrightness(brightness)

    def __init__(self, parent=lv.scr_act(), x=0, y=0, width=200, color=_DEFAULT_THEME_COLOR, show_label=False):
        """
        Parameters
        ----------
        parent : lv.obj
            The parent of the slider (Default is the active screen).
        x : int
            The slider's x-coordinate.
        y : int
            The slider's y-coordinate.
        width : int
            The slider's width (Default is 200)
        color : hex int
            The slider's main color (Default is black).

        """
        super().__init__(parent=parent, x=x, y=y, width=width, min_value=0, max_value=100, color=color,
                         show_label=show_label)
        self.set_event_cb(self._event_handler)
        self.set_value(self.get_max_value())


class _Widget(alte.Container):
    def _gl_delete_widget(self, board, widget):
        """
        Deleted a widget from a given board

        Parameters
        ----------
        board : Board
            Parent board of the widget
        widget : Widget
            Widget to delete
        """
        board.delete_widget(widget)

    def _event_handler(self, source, event):
        if event == lv.EVENT.LONG_PRESSED and not self.is_place_holder:
            # Delete widget from main board
            conf = Confirmation('Remove Widget?', _DEFAULT_TEXT_COLOR, '', _DEFAULT_TEXT_COLOR, 0xFFFFFF,
                                self._gl_delete_widget, self._board, self)

    def __init__(self, board, height, width, row, col, color, is_place_holder, parent=lv.scr_act()):
        """
        Parameters
        ----------
        board : Board
            Parent board to draw the widget inside
        height : int
            Number of rows to be occupied by the widget
        width : int
            Number of columns to be occupied by the widget
        row : int
            Top row from which to draw the widget
        col : int
            Left row from which to draw the widget
        color : int
            Background color of the widget
        is_place_holder : bool
            Bool variable to indicate whether this is a placeholder block or not
        parent : pointer
            Pointer to a screen to contain the drawn element (default is lv.scr_act())
        """
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
        """
        Initializes the board with small blocks
        """
        for row in range(self.rows_num):
            for col in range(self.cols_num):
                # Filling the board with place-holders
                empty_block = _Widget(parent=self.parent, board=self, height=1, width=1, row=row, col=col,
                                      color=self._default_color, is_place_holder=True)
                if not self._show_place_holders:
                    empty_block.set_hidden(True)
                self._background_blocks.append(empty_block)

    def reset_board(self):
        """
        Deletes all colored widgets from current board
        """
        if self._show_place_holders:
            for background_block in self._background_blocks:
                background_block.set_hidden(False)
        for colored_block in self._colored_blocks:
            colored_block.delete()
        self._colored_blocks = list()

    def __init__(self, top_margin=51, block_size=58, split_size=5, rows_num=3, cols_num=5, show_place_holders=True,
                 _default_color=_DEFAULT_DISABLED_COLOR, parent=lv.scr_act()):
        """
        Parameters
        ----------
        top_margin : int
            Space from top of screen in pixels (default is 51)
        block_size : int
            Height and Width of block in pixels (default is 58)
        split_size : int
            Space between blocks in pixels (default is 5)
        rows_num : int
            Number of rows inside the board (default is 3)
        cols_num : int
        Number of columns inside the board (default is 5)
        show_place_holders : bool
            Bool variable to decide whether to hide placeholder or to show them (default is True)
        _default_color : int
            Color of placeholder blocks (default is _DEFAULT_DISABLED_COLOR)
        parent : pointer
            Pointer to a screen to contain the drawn element (default is lv.scr_act())
        """
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
        """
        Draws widget inside current board

        Parameters
        ----------
        height : int
            Number of rows to be occupied by the widget
        width : int
            Number of columns to be occupied by the widget
        row : int
            Top row from which to draw the widget
        col : int
            Left row from which to draw the widget
        color : int
            Background color of the widget

        Returns
        -------
        Widget
            The created widget

        """
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
        """
        Deletes widget from current board

        Parameters
        ----------
        widget : Widget
            The widget to be deleted from current board
        """
        if self._show_place_holders:
            for i, j in widget.reserved_blocks:
                self._background_blocks[i * self.cols_num + j].set_hidden(False)
        widget.delete()

    def delete(self):
        """
        Deletes all widgets from current board (including placeholders)
        """
        for background_block in self._background_blocks:
            background_block.delete()
        for colored_block in self._colored_blocks:
            colored_block.delete()
        self._background_blocks = list()
        self._colored_blocks = list()

    def set_hidden(self, hidden):
        """
        Shows / Hides all blocks inside a widget

        Parameters
        ----------
        hidden : bool
            Bool variable to decide whether to hide the blocks or to show them
        """
        for colored_block in self._colored_blocks:
            colored_block.set_hidden(hidden)

    def d_refresh(self):
        child = self.get_child(None)
        while child:
            try:
                child.d_refresh()
            except AttributeError as e:
                print(__name__ + ': ' + str(e))
            child = self.get_child(child)
