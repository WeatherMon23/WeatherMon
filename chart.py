class ChartType():
  # enum Is Not Available
  NONE = 0
  LINE = 1
  COLUMN = 2
  
  
class Chart():
  def __init__(self, height, width, min_val, max_val, input_vector):
    self.height = height
    self.width = width
    self._min_val = min_val
    self._max_val = max_val
    self._input_vector = input_vector
    
  def draw_chart(self, chart_type, title, is_faded=True):
    chart_con = lv.cont(lv.scr_act(), None)
    chart_con.set_auto_realign(True)
    chart_con.set_fit(lv.FIT.TIGHT)
    chart_con.set_layout(lv.LAYOUT.COLUMN_MID)
    
    chart_title = lv.label(chart_con)
    chart_title.set_long_mode(lv.label.LONG.SROLL_CIRC)
    chart_title.set_align(lv.label.ALIGN.CENTER)
    chart_title.set_width(self.width)
    chart_title.set_text(title)
    
    chart = lv.chart(chart_con)
    chart.set_size(self.width, self.height - chart_title.get_height())
    
    chart_style = lv.style_t()
    chart_style.init()
    chart_style.set_border_width(lv.STATE.DEFAULT, 0)
    chart.add_style(chart.PART.BG, chart_style)
    chart.set_y_range(0, self._min_val, self._max_val)
    
    chart_con.add_style(chart.PART.BG, chart_style)
    chart_con.set_pos(0, 0)
    
    if chart_type == ChartType.NONE:
      chart.set_type(lv.chart.TYPE.NONE)
    elif chart_type == ChartType.LINE:
      chart.set_type(lv.chart.TYPE.LINE)
    elif chart_type == ChartType.COLUMN:
      chart.set_type(lv.chart.TYPE.COLUMN)
    
    if is_faded:
      chart.set_style_local_bg_opa(lv.chart.PART.SERIES, lv.STATE.DEFAULT, lv.OPA._50)
      chart.set_style_local_bg_grad_dir(lv.chart.PART.SERIES, lv.STATE.DEFAULT, lv.GRAD_DIR.VER)
      chart.set_style_local_bg_main_stop(lv.chart.PART.SERIES, lv.STATE.DEFAULT, 255)
      chart.set_style_local_bg_grad_stop(lv.chart.PART.SERIES, lv.STATE.DEFAULT, 0)
    
    for color, points in self._input_vector:
      tmp_ser = chart.add_series(lv.color_hex(color))
      chart.set_points(tmp_ser, points)
