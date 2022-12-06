{\rtf1\ansi\ansicpg1252\cocoartf2706
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 class _Widget():\
  def __init__(self, board, height, width, row, col, color, place_holder):\
    assert row >= 0 and col >= 0 and row < board.rows_num and col < board.cols_num\
    assert row + height <= board.rows_num and col + width <= board.cols_num\
\
    self._board = board\
    self.height = height\
    self.width = width\
    self.row = row\
    self.col = col\
    self.color = color\
    self.place_holder = place_holder\
    self.reserved_blocks = list()\
\
    height_in_pixels = board.block_size * height + (height - 1) * board.split_size\
    height_cords = board.top_margin + row * (board.block_size + board.split_size)\
    left_cords = board.block_size * col + board.split_size * (1 + col)\
\
    rectangle = lv.cont(lv.scr_act(), None)\
    rectangle.set_auto_realign(False)  # Disable auto realign when the size changes\
    rectangle.set_fit(lv.FIT.NONE)  # Do not change the size automatically around the children\
    rectangle.set_layout(lv.LAYOUT.OFF)  # Do not align the children\
    rectangle.set_size(board.block_size * width + (width - 1) * board.split_size, height_in_pixels)\
    rectangle.set_pos(left_cords, height_cords)\
\
    rec_style = lv.style_t()\
    rec_style.init()\
    darker_color = lv.color_t.color_darken(lv.color_hex(color), 30)\
    rec_style.set_border_color(lv.STATE.DEFAULT, darker_color)\
    rec_style.set_border_color(lv.STATE.FOCUSED, darker_color)\
    rec_style.set_border_width(lv.STATE.DEFAULT, 2)\
    rec_style.set_radius(lv.STATE.DEFAULT, 12)\
    rec_style.set_bg_color(lv.STATE.DEFAULT, lv.color_hex(color))\
    rectangle.add_style(rectangle.PART.MAIN, rec_style)\
\
    def event_handler(source, event):\
      global popup_list\
      if event == lv.EVENT.LONG_PRESSED and not self.place_holder:\
        self._board.delete_widget(self)\
\
    rectangle.set_event_cb(event_handler)\
\
    self.rectangle = rectangle\
\
    for i in range(height):\
      for j in range(width):\
        self.reserved_blocks.append([row + i, col + j])\
\
  def set_hidden(self, hide):\
    self.rectangle.set_hidden(hide)\
\
  def delete(self):\
    self.rectangle.delete()\
\
\
class Board():\
  def _init_board(self):\
    for row in range(self.rows_num):\
      for col in range(self.cols_num):\
        empty_block = _Widget(self, 1, 1, row, col, self.default_color, True)\
        self._background_blocks.append(empty_block)\
\
  def reset_board(self):\
    for background_block in self._background_blocks:\
      background_block.set_hidden(False)\
    for colored_block in self._colored_blocks:\
      colored_block.delete()\
    self._colored_blocks = list()\
\
  def __init__(self, top_margin, block_size, split_size, rows_num, cols_num, default_color=0xf2f2f2):\
    self.default_color = default_color\
    self.top_margin = top_margin\
    self.block_size = block_size\
    self.split_size = split_size\
    self.rows_num = rows_num\
    self.cols_num = cols_num\
    self._background_blocks = list()\
    self._colored_blocks = list()\
    self._init_board()\
\
  def draw_widget(self, height, width, row, col, color):\
    widget = _Widget(self, height, width, row, col, color, False)\
    self._colored_blocks.append(widget)\
    for i, j in widget.reserved_blocks:\
      self._background_blocks[i * self.cols_num + j].set_hidden(True)\
    return widget\
\
  def delete_widget(self, widget):\
    widget.delete()\
    for i, j in widget.reserved_blocks:\
      self._background_blocks[i * self.cols_num + j].set_hidden(False)\
\
  def delete(self):\
    for background_block in self._background_blocks:\
      background_block.delete()\
    for colored_block in self._colored_blocks:\
      colored_block.delete()\
    self._background_blocks = list()\
    self._colored_blocks = list()\
\
\'91\'92\'92\
tmp_board = Board(51, 58, 5, 3, 5)\
w1 = tmp_board.draw_widget(2, 2, 0, 0, 0xFF6347)\
w2 = tmp_board.draw_widget(2, 3, 1, 2, 0x9ACD32)\
w3 = tmp_board.draw_widget(1, 1, 0, 4, 0x4682B4)\
tmp_board.delete_widget(w1)\
tmp_board.delete_widget(w3)\
'''\
}