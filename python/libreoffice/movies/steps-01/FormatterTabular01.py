class FormatterBase:
  def __init__(self) -> None:
    self.controller = self.document.getCurrentController()

  def formatOneSheet(self) -> None:
    self.reset_pos_columns()

  def processOne(self) -> None:
    self.sheet = self.controller.getActiveSheet()
    self.formatOneSheet()

  def processAll(self) -> None:
    for sheet in self.document.Sheets:
      print(sheet.Name)
      self.sheet = sheet
      self.formatOneSheet()

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class TabularFormatterCommon(FormatterBase):
  def __init__(self) -> None:
    self.document = XSCRIPTCONTEXT.getDocument()
    super().__init__()

  def reset_pos_columns(self) -> None:
    columns = self.sheet.Columns
    column_width_div = 0.5 * 1000  # Width of 0.5 cm

    # Insert one column at the specified indexes
    columns.insertByIndex( 0, 1) # Column A
    columns.insertByIndex( 7, 1) # Column H
    columns.insertByIndex(11, 1) # Column L

    # Set widths for columns A, H
    columns.getByIndex( 0).Width = column_width_div
    columns.getByIndex( 7).Width = column_width_div
    columns.getByIndex(11).Width = column_width_div

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

def processOne() -> None:
  sample = TabularFormatterCommon()
  sample.processOne()

def processAll() -> None:
  sample = TabularFormatterCommon()
  sample.processAll()