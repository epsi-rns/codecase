from com.sun.star.\
  table import BorderLine2, BorderLineStyle, TableBorder2

class BorderFormatManager:
  def create_line_format_none(self):
    lineFormatNone = BorderLine2()
    lineFormatNone.LineStyle = BorderLineStyle.NONE
    return lineFormatNone

  def create_line_format_black(self):
    lineFormatBlack = BorderLine2()
    lineFormatBlack.LineStyle = BorderLineStyle.SOLID
    lineFormatBlack.LineWidth = 20
    lineFormatBlack.Color = 0x000000 #black
    return lineFormatBlack

  def create_line_format_gray(self):
    lineFormatGray = BorderLine2()
    lineFormatGray.LineStyle = BorderLineStyle.SOLID
    lineFormatGray.LineWidth = 20
    lineFormatGray.Color = 0xE0E0E0 #gray300
    return lineFormatGray

# table border
bfm = BorderFormatManager()
lfNone  = bfm.create_line_format_none()
lfBlack = bfm.create_line_format_black()
lfGray  = bfm.create_line_format_gray()