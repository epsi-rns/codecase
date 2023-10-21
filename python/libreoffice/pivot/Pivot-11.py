class PivotSample:
  def __init__(self) -> None:
    document = XSCRIPTCONTEXT.getDocument()
    self.sheet_src = document.Sheets['Table']

  def get_last_used_row(self):
    cursor = self.sheet_src.createCursor()
    cursor.gotoEndOfUsedArea(False)
    cursor.gotoStartOfUsedArea(True)
    rows = cursor.getRows()
    
    return len(rows)

  def process(self):
    # range to be proceed
    # omit header and plus one for the last
    max_row = self.get_last_used_row()
    range_rows = range(2, max_row+1)

    print(f'Range  : {range_rows}')


def main():
  sample = PivotSample()
  sample.process()
