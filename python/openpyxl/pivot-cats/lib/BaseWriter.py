from openpyxl.styles import (Color,
  PatternFill, Font, Border, Side, Alignment)

class BaseWriter:
  def init_sheet_style(self):
    self.blueFills = {}  # Dictionary to store PatternFill objects
    blueScale = {
      0: 0xE3F2FD, 1: 0xBBDEFB, 2: 0x90CAF9,
      3: 0x64B5F6, 4: 0x42A5F5, 5: 0x2196F3,
      6: 0x1E88E5, 7: 0x1976D2, 8: 0x1565C0,
      9: 0x0D47A1
    }

    for key, color_value in blueScale.items():
      # Convert the color value to a hexadecimal string
      hex_color = f'ff{color_value:06x}'
      self.blueFills[key] = PatternFill(
        start_color=hex_color,
        end_color=hex_color,
        fill_type='solid')

    self.headerFont = Font(
      name='Arial', sz='10', bold=True)
    self.normalFont = Font(name='Arial', sz='10')
    self.centerText = Alignment(horizontal='center')
    
    # Define the border style and color
    side = Side(style='thin', color='2196F3')
    self.top_border    = Border(top   = side)
    self.bottom_border = Border(bottom= side)
    self.inner_border  = Border(
      left  = side, right = side)
    self.left_border   = Border(left  = side)
    self.right_border  = Border(right = side)
